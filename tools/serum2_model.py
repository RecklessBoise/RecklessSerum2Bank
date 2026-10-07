"""High-level builder on top of the raw Serum 2 preset state.

Only parameters that differ from Serum's defaults are written ("plainParams"
holds overrides); everything else stays "default", like presets saved by Serum.
"""
import copy
import json
import math
import os
import struct

SERUM2_ROOT = os.environ.get(
    "SERUM2_ROOT", "/Library/Audio/Presets/Xfer Records/Serum 2 Presets"
)
TABLES_DIR = os.path.join(SERUM2_ROOT, "Tables")
NOISES_DIR = os.path.join(SERUM2_ROOT, "Samples", "Factory Non-Tonal", "Noises")
SKELETON = os.path.join(os.path.dirname(__file__), "skeleton.json")

# Modulation source IDs (derived from the factory library, see docs/FORMAT.md)
SRC_ENV = {1: 2, 2: 3, 3: 4, 4: 5}          # Env 1..4
SRC_LFO = {i + 1: 6 + i for i in range(10)}  # LFO 1..10
SRC_VELO = 16
SRC_NOTE = 17
SRC_MACRO = {i + 1: 25 + i for i in range(8)}  # Macro 1..8

# (destModuleTypeString, paramName) -> destModuleParamID
PARAM_IDS = {
    ("Oscillator", "kParamVolume"): 1,
    ("Oscillator", "kParamPan"): 2,
    ("Oscillator", "kParamOctave"): 3,
    ("Oscillator", "kParamPitch"): 4,
    ("Oscillator", "kParamFine"): 5,
    ("Oscillator", "kParamCoarsePit"): 6,
    ("Oscillator", "kParamDetune"): 26,
    ("WTOsc", "kParamWarp"): 0,
    ("WTOsc", "kParamTablePos"): 6,
    ("VoiceFilter", "kParamWet"): 1,
    ("VoiceFilter", "kParamFreq"): 3,
    ("VoiceFilter", "kParamReso"): 4,
    ("VoiceFilter", "kParamDrive"): 5,
    ("LFO", "kParamRate"): 0,
    ("Global", "kParamPortamentoTime"): 3,
    ("FXDistortion", "kParamWet"): 1,
    ("FXDistortion", "kParamDrive"): 2,
    ("FXReverb", "kParamWet"): 1,
    ("FXReverb", "kParamSize"): 2,
    ("FXDelay", "kParamWet"): 1,
    ("FXDelay", "kParamFeedback"): 9,
    ("FXChorus", "kParamWet"): 1,
    ("FXHyperD", "kParamWet"): 1,
    ("FXHyperD", "kParamDetune"): 3,
    ("FXPhaser", "kParamWet"): 1,
    ("FXFlanger", "kParamWet"): 1,
    ("FXComp", "kParamWet"): 1,
    ("FXFilter", "kParamWet"): 1,
    ("FXFilter", "kParamFreq"): 3,
    ("FXUtils", "kParamWidth"): 3,
}

FX_TYPES = {
    "FXDistortion": 0, "FXFlanger": 1, "FXPhaser": 2, "FXChorus": 3,
    "FXDelay": 4, "FXComp": 5, "FXReverb": 6, "FXEQ": 7, "FXFilter": 8,
    "FXHyperD": 9, "FXBode": 10, "FXConv": 11, "FXUtils": 12,
}

OSC_INDEX = {"A": 0, "B": 1, "C": 2, "N": 3, "S": 4}
ROUTING_SLOT = {"A": 0, "B": 1, "C": 2, "N": 3, "S": 4}


def hz_to_cutoff(hz):
    """Map Hz to Serum's normalized filter cutoff (8.18 Hz .. 22.05 kHz, exponential)."""
    hz = min(max(hz, 8.2), 22050.0)
    return math.log(hz / 8.176) / math.log(22050.0 / 8.176)


def wav_info(path):
    """Return (numFrames, numChannels, sampleRate) of a RIFF wav file."""
    with open(path, "rb") as f:
        data = f.read()
    if data[:4] != b"RIFF":
        raise ValueError(f"{path}: not a RIFF file")
    i, fmt = 12, None
    while i + 8 <= len(data):
        cid = data[i:i + 4]
        n = struct.unpack("<I", data[i + 4:i + 8])[0]
        if cid == b"fmt ":
            fmt = struct.unpack("<HHIIHH", data[i + 8:i + 24])
        elif cid == b"data":
            _tag, ch, sr, _br, align, _bits = fmt
            return n // align, ch, sr
        i += 8 + n + (n & 1)
    raise ValueError(f"{path}: no data chunk")


def _load_skeleton():
    with open(SKELETON) as f:
        return json.load(f)


_SKELETON_CACHE = None


class Preset:
    def __init__(self, name, author, tags, description=""):
        global _SKELETON_CACHE
        if _SKELETON_CACHE is None:
            _SKELETON_CACHE = _load_skeleton()
        sk = copy.deepcopy(_SKELETON_CACHE)
        self.meta = sk["meta"]
        self.s = sk["state"]
        self.name = name
        for target in (self.meta, self.s):
            target["presetName"] = name
            target["presetAuthor"] = author
            target["presetDescription"] = description
            target["tags"] = list(tags)
        self._mod_slot = 0
        self._fx = {0: [], 1: [], 2: []}
        self.tables_used = set()
        self.noises_used = set()

    # -- low level -----------------------------------------------------------
    @staticmethod
    def _pp(block):
        if not isinstance(block.get("plainParams"), dict):
            block["plainParams"] = {}
        return block["plainParams"]

    def _set(self, block, **params):
        pp = self._pp(block)
        for k, v in params.items():
            if v is None:
                continue
            pp["kParam" + k] = float(v) if isinstance(v, (int, float)) and not isinstance(v, bool) else v

    # -- oscillators ---------------------------------------------------------
    def wt(self, slot, table, pos=1.0, vol=0.7, octave=0, semi=0, fine=0,
           unison=1, detune=None, blend=None, stereo=None, pan=None,
           warp=None, warp_amt=None, warp2=None, warp2_amt=None,
           rand_phase=None, enable=True, route_filter=True):
        i = OSC_INDEX[slot]
        osc = self.s[f"Oscillator{i}"]
        path = os.path.join(TABLES_DIR, table)
        frames, ch, sr = wav_info(path)
        self.tables_used.add(table)
        w = osc[f"WTOsc{i}"]
        w.update({"relativePathToWT": table, "numFrames": frames,
                  "numChannels": ch, "sampleRate": sr})
        w.setdefault("flex", {})
        self._set(w, TablePos=pos, WarpMenu=warp, Warp=warp_amt,
                  **{"WarpMenu2": warp2, "Warp2": warp2_amt},
                  RandomPhase=rand_phase)
        self._set(osc, Enable=1.0 if enable else 0.0, Volume=vol,
                  Octave=octave or None, Pitch=semi or None, Fine=fine or None,
                  Unison=unison if unison > 1 else None, Detune=detune,
                  DetuneWid=blend, UnisonStereo=stereo, Pan=pan)
        if route_filter:
            self.route(slot)
        return self

    def sub(self, shape="kSine", octave=-1, vol=0.6, route_filter=False):
        osc = self.s["Oscillator4"]
        if shape != "kSine":
            self._set(osc["SubOsc4"], Shape=shape)
        self._set(osc, Enable=1.0, Volume=vol, Octave=octave)
        if route_filter:
            self.route("S")
        return self

    def noise(self, sample, vol=0.25, one_shot=False, color=None, route_filter=True):
        osc = self.s["Oscillator3"]
        n = osc["NoiseOsc3"]
        frames, ch, sr = wav_info(os.path.join(NOISES_DIR, sample))
        self.noises_used.add(sample)
        n.update({"relativePathToNoiseSample": sample, "numFrames": frames,
                  "numChannels": ch, "sampleRate": sr})
        self._set(n, OneShot=1.0 if one_shot else None, Color=color)
        self._set(osc, Enable=1.0, Volume=vol)
        if route_filter:
            self.route("N")
        return self

    def route(self, slot, dest="kRoutingDestFilter"):
        rs = self.s[f"RoutingSlot{ROUTING_SLOT[slot]}"]
        self._set(rs, RoutingDest=dest)

    # -- filter / envelopes / lfos ------------------------------------------
    def filt(self, ftype="MgL24", hz=2000, reso=10, drive=None, wet=None,
             keytrack=False, var=None, index=0):
        f = self.s[f"VoiceFilter{index}"]
        self._set(f, Enable=1.0, Type=ftype, Freq=hz_to_cutoff(hz), Reso=reso,
                  Drive=drive, Wet=wet, Var=var,
                  KeyTrack=1.0 if keytrack else None)
        return self

    def env(self, n, a=0.001, h=None, d=1.0, s=1.0, r=0.05):
        e = self.s[f"Env{n - 1}"]
        self._set(e, Attack=a, Hold=h, Decay=d, Sustain=s, Release=r)
        return self

    def lfo(self, n, hz=None, shape=None, sync=False, rate=None, mode=None, smooth=None):
        L = self.s[f"LFO{n - 1}"]
        if sync:
            self._set(L, Rate=rate)
        else:
            self._set(L, BeatSync=0.0, Rate=hz)
        self._set(L, Mode=mode, Smooth=smooth)
        if shape:
            xs, ys = shape
            L["curveData"] = {"numPoints": len(xs) - 1, "xVals": list(map(float, xs)),
                              "yVals": list(map(float, ys)),
                              "curveVals": [0.5] * len(xs)}
            L["curveDisplayName"] = "Custom"
        return self

    # -- modulation ----------------------------------------------------------
    def mod(self, source, dest_type, dest_id, param, amount, bipolar=False):
        if self._mod_slot >= 64:
            raise RuntimeError(f"{self.name}: out of mod slots")
        slot = {
            "destModuleID": dest_id,
            "destModuleParamID": PARAM_IDS[(dest_type, param)],
            "destModuleParamName": param,
            "destModuleTypeString": dest_type,
            "plainParams": {"kParamAmount": float(amount)},
            "source": [source, 0],
        }
        if bipolar:
            slot["plainParams"]["kParamBipolar"] = 1.0
        self.s[f"ModSlot{self._mod_slot}"] = slot
        self._mod_slot += 1
        return self

    def macro(self, n, name, value=0.0):
        m = self.s[f"Macro{n - 1}"]
        m["name"] = name
        if value:
            self._set(m, Value=value)
        return self

    # -- fx ------------------------------------------------------------------
    def fx(self, kind, rack=0, **params):
        """Append an FX module to a rack. Returns its module id for modulation."""
        entry = {kind: {"plainParams": "default"}, "type": FX_TYPES[kind]}
        if kind == "FXHyperD":
            entry["kUIParamMixOrGainDimE"] = 0.0
            entry["kUIParamMixOrGainHyper"] = 0.0
        elif kind != "FXEQ":
            entry["kUIParamMixOrGain"] = 0.0
        if kind == "FXDistortion":
            entry["flex"] = [{}, {}]
        self._set(entry[kind], **params)
        rack_list = self.s[f"FXRack{rack}"]["FX"]
        rack_list.append(entry)
        return rack * 100 + len(rack_list) - 1

    # -- global / arp --------------------------------------------------------
    def glob(self, volume=0.5, mono=False, legato=False, porta=None,
             porta_always=None, poly=None, bend=None):
        g = self.s["Global0"]
        self._set(g, MasterVolume=volume,
                  MonoToggle=1.0 if mono else None,
                  Legato=1.0 if legato else None,
                  PortamentoTime=porta,
                  PortaAlways=1.0 if porta_always else None,
                  PolyCount=poly)
        if bend:
            self._set(g, BendRangeUp=bend, BendRangeDn=-bend)
        return self

    def arp(self, shape="Up", octaves=None, gate=None, chance=None, rate=None):
        self._set(self.s["Arp0"], Enabled=1.0)
        clip = self.s["ArpClip0"]
        clip["name"] = "Pattern 1"
        self._set(clip, Shape=shape, TransposeRange=octaves, Gate=gate,
                  Chance=chance, Rate=rate)
        return self

    def build(self):
        return self.meta, self.s
