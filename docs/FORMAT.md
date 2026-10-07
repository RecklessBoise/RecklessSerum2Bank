# Serum 2 `.SerumPreset` format (reverse-engineered)

```
offset  size  content
0       9     b"XferJson\0"
9       8     u64 LE  N = JSON metadata length
17      N     JSON metadata (presetName, presetAuthor, tags, product, productVersion, version, hash, ...)
17+N    4     u32 LE  length of the decompressed state
21+N    4     u32 LE  2 (container version)
25+N    ...   zstd( CBOR(state) )
```

- `metadata.hash` is the **MD5 hex digest of the zstd block**.
- The state is a CBOR map of modules: `Oscillator0..4` (A, B, C, Noise, Sub), `VoiceFilter0..1`, `Env0..3`, `LFO0..9`, `Macro0..7`, `ModSlot0..63`, `FXRack0..2` (Main, Bus 1, Bus 2), `RoutingSlot0..6`, `Global0`, `Arp0`, `ArpClip0..11`, ...
- Every module carries `plainParams`. It is either `"default"` or a dict of overrides `{"kParamXxx": value}` in real units: seconds, Hz, %, or enum strings such as `"MgL24"` or `"kDownsample"`.
- Filter cutoff (`kParamFreq`) is normalized from 0 to 1 on an exponential scale (about 8 Hz to 22 kHz).
- WT position (`kParamTablePos`) runs from 1 to 256 across the whole table.
- Wavetable: `WTOscN.relativePathToWT` is relative to `Tables/`, with `numFrames`, `numChannels` and `sampleRate` taken from the file.
- Noise: `NoiseOsc3.relativePathToNoiseSample` is relative to `Samples/Factory Non-Tonal/Noises/`.
- FX: `{"FXReverb": {"plainParams": ...}, "type": 6}`. The types are Distortion 0, Flanger 1, Phaser 2, Chorus 3, Delay 4, Comp 5, Reverb 6, EQ 7, Filter 8, HyperD 9, Bode 10, Conv 11, Utils 12.
- The mod matrix (`ModSlotN`) has the form `{"source": [src, aux], "destModuleTypeString", "destModuleID", "destModuleParamName", "destModuleParamID", "plainParams": {"kParamAmount": -100..100}}`.
  - Sources: Env1 to Env4 are 2 to 5, LFO1 to LFO10 are 6 to 15, Velocity is 16, Note is 17, Macro1 to Macro8 are 25 to 32.
  - An FX destination has `destModuleID = rack*100 + position`.
- Routing: `RoutingSlot0..4` is A, B, C, Noise, Sub, with `kParamRoutingDest` set to `kRoutingDestFilter`, `...Master`, `...Direct` or `...None`.

The codec was validated with a lossless round trip (decode → encode → decode, identical state) on 1615 local Serum 2 presets. It is not byte-for-byte, because CBOR and zstd encoding can differ, but Serum accepts the files. The generated presets were loaded and played in Serum 2.0.19.
