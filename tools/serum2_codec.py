"""Read/write Serum 2 .SerumPreset files.

Layout: b"XferJson\\0" | u64 LE json_len | json metadata | u32 LE raw_len | u32 LE 2 | zstd(cbor(state))
metadata["hash"] is the MD5 hex of the zstd block.
"""
import hashlib
import json
import struct

import cbor2
import zstandard

MAGIC = b"XferJson\0"


def read_preset(path):
    with open(path, "rb") as f:
        data = f.read()
    if data[:9] != MAGIC:
        raise ValueError(f"{path}: not a Serum 2 preset")
    n = struct.unpack("<Q", data[9:17])[0]
    meta = json.loads(data[17:17 + n])
    raw_len, ver = struct.unpack("<II", data[17 + n:25 + n])
    blob = data[25 + n:]
    raw = zstandard.ZstdDecompressor().decompress(blob, max_output_size=raw_len)
    return meta, cbor2.loads(raw), ver


def encode_preset(meta, state, ver=2):
    raw = cbor2.dumps(state)
    blob = zstandard.ZstdCompressor(level=3).compress(raw)
    meta = dict(meta, hash=hashlib.md5(blob).hexdigest())
    js = json.dumps(meta, separators=(",", ":"), sort_keys=True).encode()
    return MAGIC + struct.pack("<Q", len(js)) + js + struct.pack("<II", len(raw), ver) + blob


def write_preset(path, meta, state, ver=2):
    with open(path, "wb") as f:
        f.write(encode_preset(meta, state, ver))
