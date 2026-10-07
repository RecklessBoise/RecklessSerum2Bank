"""Run: python -m unittest discover tests"""
import glob
import hashlib
import json
import os
import struct
import sys
import unittest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(ROOT, "tools"))

from serum2_codec import encode_preset, read_preset  # noqa: E402
from serum2_model import NOISES_DIR, TABLES_DIR  # noqa: E402

BANK = os.path.join(ROOT, "RecklessSerum2Bank_1")


def _bytes(path):
    with open(path, "rb") as fh:
        return fh.read()


FILES = sorted(glob.glob(os.path.join(BANK, "**", "*.SerumPreset"), recursive=True))
EXPECTED = {"Bass": 45, "Lead": 40, "Keys": 30, "Pad": 30, "Arp": 25, "Atmos": 25,
            "Pluck": 20, "Synth & Stab": 15, "808 & Sub": 10, "FX": 10}


class TestBank(unittest.TestCase):
    def test_count_and_folders(self):
        self.assertEqual(len(FILES), 250)
        for folder, n in EXPECTED.items():
            self.assertEqual(len(glob.glob(os.path.join(BANK, folder, "*.SerumPreset"))), n, folder)

    def test_unique_names(self):
        names = [os.path.basename(f) for f in FILES]
        self.assertEqual(len(names), len(set(names)))

    def test_files_decode_and_hash(self):
        for f in FILES:
            data = _bytes(f)
            n = struct.unpack("<Q", data[9:17])[0]
            meta = json.loads(data[17:17 + n])
            self.assertEqual(meta["hash"], hashlib.md5(data[25 + n:]).hexdigest(), f)
            m, s, _ = read_preset(f)
            self.assertEqual(m["presetName"], os.path.basename(f)[:-len(".SerumPreset")])
            self.assertEqual(s["presetName"], m["presetName"])

    def test_roundtrip(self):
        for f in FILES[:20]:
            m, s, v = read_preset(f)
            self.assertEqual(encode_preset(m, s, v), _bytes(f))

    def test_mod_slots_valid(self):
        for f in FILES:
            _, s, _ = read_preset(f)
            for k, x in s.items():
                if k.startswith("ModSlot") and "source" in x:
                    amt = x["plainParams"]["kParamAmount"]
                    self.assertTrue(-100 <= amt <= 100, f)
                    self.assertTrue(1 <= x["source"][0] <= 60, f)

    @unittest.skipUnless(os.path.isdir(TABLES_DIR), "Serum 2 factory content not installed")
    def test_factory_content_exists(self):
        for f in FILES:
            _, s, _ = read_preset(f)
            for i in range(3):
                wt = s[f"Oscillator{i}"][f"WTOsc{i}"].get("relativePathToWT")
                if wt:
                    self.assertTrue(os.path.exists(os.path.join(TABLES_DIR, wt)), wt)
            ns = s["Oscillator3"]["NoiseOsc3"].get("relativePathToNoiseSample")
            if ns:
                self.assertTrue(os.path.exists(os.path.join(NOISES_DIR, ns)), ns)


if __name__ == "__main__":
    unittest.main()
