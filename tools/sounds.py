"""Sound-design archetypes for RecklessSerum2Bank.

Four flavours drive every archetype:
  hollis  - hyperpop / glossy: wide supersaws, hyper-dimension, OTT, bright reverb
  mink    - raw underground rap: distorted 808s, tape grit, dry & mono
  castles - 8-bit witch-house: square/pulse chips, downsample crush, vintage verb
  electro - underground electro: acid, reese, FM, Juno pulse, phasers, ping-pong
"""
from serum2_model import Preset, SRC_ENV, SRC_LFO, SRC_MACRO, SRC_VELO

AUTHOR = "RecklessBoise"

# ---- wavetables (relative to Serum 2 "Tables" folder) -------------------------
DEFAULT = "S2 Tables/Default Shapes.wav"   # pos: 1 saw, 33 sine, 65 tri, 129 square, 160-256 pulses
POS = {"saw": 1.0, "sine": 33.0, "tri": 65.0, "sqr": 129.0, "pulse": 200.0, "thin": 245.0}
T = {
    "polysaw": "S2 Tables/Analog/PolySaw II.wav",
    "synstring": "S2 Tables/Analog/SynStringSaw.wav",
    "sawdrift": "S2 Tables/Analog/Saw Drift.wav",
    "saw303": "S2 Tables/Analog/Saw Drift 303.wav",
    "sq303": "S2 Tables/Analog/Square Drift 303.wav",
    "anothersaw": "S2 Tables/Analog/Yet Another Saw.wav",
    "sawphasey": "S2 Tables/Analog/Saw Phasey.wav",
    "sawsquare": "S2 Tables/Analog/Saw to Square.wav",
    "juno": "S2 Tables/Analog/AT Juno 106.wav",
    "warmsub": "S2 Tables/Analog/Warm Sub.wav",
    "sub808": "S2 Tables/Analog/Perfect 808 Sub Shapes.wav",
    "harms808": "S2 Tables/Analog/808 Harms.wav",
    "mello": "S2 Tables/Analog/Mello.wav",
    "solina": "S2 Tables/Analog/Solina Viola.wav",
    "subroller": "S2 Tables/Analog/Subby Roller.wav",
    "trisub": "S2 Tables/Analog/Triangle Sub Morph.wav",
    "fmsaw": "S2 Tables/Digital/FM Dangerous Saw.wav",
    "fmsquare": "S2 Tables/Digital/FM Dirty Square.wav",
    "fmpiano": "S2 Tables/Digital/FM Piano.wav",
    "dxhard": "S2 Tables/Digital/DX Hard Attack.wav",
    "opl": "S2 Tables/Digital/Basic OPL.wav",
    "tine": "S2 Tables/Digital/RMrK1 Tine.wav",
    "organ": "S2 Tables/Digital/Memory Organ.wav",
    "bellpluck": "S2 Tables/Digital/Braids Bell Pluck.wav",
    "richpluck": "S2 Tables/Digital/Rich Pluck.wav",
    "xylo": "S2 Tables/Digital/Xylo Pluck.wav",
    "talkvox": "S2 Tables/Digital/Talking Vox.wav",
    "vocalhum": "S2 Tables/Digital/Vocal Hum.wav",
    "voxy": "S2 Tables/Digital/Voxy.wav",
    "shep": "S2 Tables/Digital/Shep. Octaves.wav",
    "harmsmooth": "S2 Tables/Digital/Harmonic Series Smooth.wav",
    "generative": "S2 Tables/Digital/Generative Waves.wav",
    "elecnoise": "S2 Tables/Digital/Electric Noise.wav",
    "hypersqueak": "S2 Tables/Digital/HyperSqueak.wav",
    "bitspeek": "S2 Tables/Digital/Bitspeek 2 Seperate.wav",
    "dyingsaw": "S2 Tables/Digital/Dying Saw.wav",
    "dyingsq": "S2 Tables/Digital/Dying Square.wav",
    "dyingsine": "S2 Tables/Digital/Dying Sine.wav",
    "chord": "S2 Tables/Digital/Chord.wav",
    "softgrowl": "S2 Tables/Digital/Softest Growl.wav",
    "harshharm": "S2 Tables/Digital/Harsh Harm.wav",
    "pwmc64": "Analog/PWM C64.wav",
    "matrixc64": "Analog/MATRIXY C64.wav",
    "pwmjuno": "Analog/PWM Juno.wav",
    "acid": "Analog/Acid.wav",
    "mario": "Digital/Mario.wav",
    "fwap8bit": "Digital/Dist 8bit Fwap.wav",
    "dulltoy": "Digital/Dull_toy.wav",
    "crushwub": "Digital/CrushWub.wav",
    "longreece": "Digital/Evol Longreece.wav",
    "fmfm": "Digital/FMFM.wav",
    "fmfreak": "Digital/FM_Freak.wav",
    "gritty": "Digital/Gritty.wav",
    "hypa": "Digital/Hypa.wav",
    "squeal": "Digital/FFT_SQUEAL.wav",
}
NOISE = {
    "white": "Analog/ARP white.wav",
    "pink": "Analog/ARP pink.wav",
    "juno": "Analog/J106.wav",
    "breath": "Organics/H-Breath.wav",
    "aircan": "Organics/Air Can 1.wav",
    "hum": "Organics/AC hum1.wav",
    "atmos": "SOR/Atmos 05.wav",
    "atmos2": "SOR/Atmos 18.wav",
    "flow": "SOR/Analog Flow.wav",
}

# LFO curve shapes (x, y); y=1 is the top of the LFO graph
SHAPE_SAW_DOWN = ([0.0, 1.0], [1.0, 0.0])
SHAPE_SQUARE = ([0.0, 0.5, 0.5, 1.0], [1.0, 1.0, 0.0, 0.0])
SHAPE_TRI = ([0.0, 0.5, 1.0], [0.0, 1.0, 0.0])


class Ctx:
    """Small helper bundling rng + style for an archetype."""

    def __init__(self, rng, style):
        self.rng = rng
        self.style = style

    def u(self, a, b):
        return round(self.rng.uniform(a, b), 4)

    def pick(self, seq):
        return self.rng.choice(seq)

    def chance(self, p):
        return self.rng.random() < p


# ---- shared finishing -----------------------------------------------------------
def standard_macros(p, c, dist_id=None, verb_id=None, delay_id=None, wt_osc=0,
                    tone_amt=None, move="wt"):
    """Every preset exposes the same 4 macros: TONE / DIRT / SPACE / MOVE."""
    p.macro(1, "TONE")
    p.mod(SRC_MACRO[1], "VoiceFilter", 0, "kParamFreq", tone_amt or c.u(30, 45))
    p.macro(2, "DIRT")
    if dist_id is not None:
        p.mod(SRC_MACRO[2], "FXDistortion", dist_id, "kParamDrive", c.u(45, 70))
    p.mod(SRC_MACRO[2], "VoiceFilter", 0, "kParamDrive", c.u(30, 60))
    p.macro(3, "SPACE")
    if verb_id is not None:
        p.mod(SRC_MACRO[3], "FXReverb", verb_id, "kParamWet", c.u(35, 55))
    if delay_id is not None:
        p.mod(SRC_MACRO[3], "FXDelay", delay_id, "kParamWet", c.u(25, 40))
    p.macro(4, "MOVE")
    if move == "wt":
        p.mod(SRC_MACRO[4], "WTOsc", wt_osc, "kParamTablePos", c.u(25, 45))
    elif move == "lfo":
        p.mod(SRC_MACRO[4], "LFO", 0, "kParamRate", c.u(30, 60))
    elif move == "detune":
        p.mod(SRC_MACRO[4], "Oscillator", wt_osc, "kParamDetune", c.u(30, 50))


def style_fx(p, c, role, dist_mode=None, dist_drive=None, verb=None, delay=None):
    """Common FX chain by style. Returns ids (dist, reverb, delay)."""
    st = c.style
    dist = verb_id = delay_id = None
    if st == "hollis":
        dist = p.fx("FXDistortion", Mode=dist_mode or c.pick(["kSoftClip", "kTapeSat", "kSoftSat"]),
                    Drive=dist_drive if dist_drive is not None else c.u(8, 25), Wet=100)
        if role not in ("bass", "808"):
            p.fx("FXHyperD", Wet=c.u(25, 55), Detune=c.u(20, 45), Unison=c.pick([3, 4, 5]),
                 DimESize=c.u(40, 80), DimEWet=c.u(20, 50))
        p.fx("FXComp", Multiband=1.0, Wet=c.u(25, 50))
        if delay or (delay is None and role in ("lead", "arp", "pluck", "key")):
            delay_id = p.fx("FXDelay", Wet=c.u(10, 22), Feedback=c.u(25, 45), Mode=1.0)
        if verb or (verb is None and role != "bass" and role != "808"):
            verb_id = p.fx("FXReverb", Type=c.pick(["kHall", "kSpace"]), Wet=c.u(12, 30),
                           Size=c.u(55, 85), Width=100)
    elif st == "mink":
        dist = p.fx("FXDistortion", Mode=dist_mode or c.pick(["kTapeSat", "kOverdrive", "kDiode1", "kAsym"]),
                    Drive=dist_drive if dist_drive is not None else c.u(20, 50), Wet=100)
        if c.chance(0.45):
            p.fx("FXDistortion", Mode="kDownsample", Drive=c.u(5, 18), Wet=c.u(30, 60))
        p.fx("FXComp", Multiband=1.0, Wet=c.u(15, 35))
        if verb or (verb is None and role in ("pad", "atmos", "key", "lead")):
            verb_id = p.fx("FXReverb", Type=c.pick(["kVintage", "kHall"]), Wet=c.u(10, 25),
                           Size=c.u(35, 70), Width=c.u(60, 100))
    elif st == "castles":
        p.fx("FXDistortion", Mode="kDownsample", Drive=c.u(25, 55), Wet=c.u(55, 100))
        dist = p.fx("FXDistortion", Mode=dist_mode or c.pick(["kHardClip", "kDiode2", "kZeroSquare", "kRectify"]),
                    Drive=dist_drive if dist_drive is not None else c.u(15, 40), Wet=100)
        if role in ("lead", "arp", "pluck", "key", "stab", "fx") or delay:
            delay_id = p.fx("FXDelay", Wet=c.u(12, 28), Feedback=c.u(30, 55), Mode=1.0)
        if verb is not False:
            verb_id = p.fx("FXReverb", Type="kVintage", Wet=c.u(15, 35), Size=c.u(60, 95),
                           Width=100)
    else:  # electro
        dist = p.fx("FXDistortion", Mode=dist_mode or c.pick(["kOverdrive", "kTapeSat", "kDiode1", "kSoftClip"]),
                    Drive=dist_drive if dist_drive is not None else c.u(10, 35), Wet=100)
        mod = c.pick(["FXPhaser", "FXChorus", "FXFlanger", None])
        if mod == "FXPhaser":
            p.fx("FXPhaser", Wet=c.u(25, 55), Rate=c.u(0.1, 0.6), Depth=c.u(40, 80), Feedback=c.u(20, 60))
        elif mod == "FXChorus":
            p.fx("FXChorus", Wet=c.u(25, 50), Rate=c.u(0.2, 0.8), Depth=c.u(6, 15), Feedback=c.u(0, 30))
        elif mod == "FXFlanger":
            p.fx("FXFlanger", Wet=c.u(20, 45), Rate=c.u(0.05, 0.4), Depth=c.u(40, 80), Feedback=c.u(30, 70))
        if role not in ("bass", "808") or delay:
            delay_id = p.fx("FXDelay", Wet=c.u(12, 26), Feedback=c.u(30, 55), Mode=1.0)
        if verb or (verb is None and role in ("pad", "atmos", "key", "lead", "arp")):
            verb_id = p.fx("FXReverb", Type=c.pick(["kHall", "kSpace", "kVintage"]),
                           Wet=c.u(10, 25), Size=c.u(45, 80), Width=100)
    return dist, verb_id, delay_id


def vibrato(p, c, lfo_n=2, osc_ids=(0,), depth=None):
    p.lfo(lfo_n, hz=c.u(4.5, 6.2))
    for o in osc_ids:
        p.mod(SRC_LFO[lfo_n], "Oscillator", o, "kParamFine", depth or c.u(4, 9), bipolar=True)


# ---- archetypes ---------------------------------------------------------------
def bass(p, c):
    st = c.style
    if st == "mink":
        kind = c.pick(["808grit", "subsaw", "tape"])
        if kind == "808grit":
            p.wt("A", T["sub808"], pos=c.u(1, 120), vol=0.8, octave=-1)
            p.env(3, a=0.0, d=c.u(0.05, 0.12), s=0.0, r=0.05)
            p.mod(SRC_ENV[3], "Oscillator", 0, "kParamCoarsePit", c.u(10, 20))
        elif kind == "subsaw":
            p.wt("A", T["warmsub"], pos=c.u(1, 200), vol=0.75, octave=-1)
            p.sub(octave=-2, vol=0.45)
        else:
            p.wt("A", DEFAULT, pos=c.pick([POS["tri"], POS["sine"] + 10]), vol=0.8, octave=-1,
                 warp="kDistTube", warp_amt=c.u(0.3, 0.7))
        p.filt("MgL24", hz=c.u(500, 1600), reso=c.u(5, 25), drive=c.u(20, 50))
        p.env(1, a=0.001, d=c.u(0.6, 2.5), s=c.u(0.6, 1.0), r=c.u(0.05, 0.25))
        p.glob(volume=c.u(0.38, 0.48), mono=True, legato=True, porta=c.u(0.06, 0.2))
        d, v, dl = style_fx(p, c, "bass", dist_drive=c.u(30, 60))
        standard_macros(p, c, d, v, dl)
    elif st == "castles":
        p.wt("A", c.pick([T["pwmc64"], T["matrixc64"], DEFAULT]), pos=c.pick([1, 64, 129, 180]),
             vol=0.75, octave=-1, warp="kQuantize", warp_amt=c.u(0.2, 0.6))
        p.sub(shape=c.pick(["kSquare", "kPulse"]), octave=-2, vol=0.4)
        p.filt(c.pick(["MgL18", "L24", "LadderMg"]), hz=c.u(700, 2500), reso=c.u(10, 35))
        p.env(1, a=0.001, d=c.u(0.2, 0.8), s=c.u(0.3, 0.8), r=0.08)
        p.env(2, a=0.0, d=c.u(0.08, 0.3), s=0.0, r=0.1)
        p.mod(SRC_ENV[2], "VoiceFilter", 0, "kParamFreq", c.u(20, 40))
        p.glob(volume=c.u(0.36, 0.46), mono=True, legato=True, porta=c.u(0.02, 0.08))
        d, v, dl = style_fx(p, c, "bass", verb=False)
        standard_macros(p, c, d, v, dl)
    elif st == "electro":
        kind = c.pick(["acid", "reese", "fm", "pulse"])
        if kind == "acid":
            p.wt("A", c.pick([T["acid"], T["saw303"], T["sq303"]]), pos=c.u(1, 256), vol=0.8, octave=-1)
            p.filt("LadderAcid", hz=c.u(250, 700), reso=c.u(55, 80), drive=c.u(20, 50))
            p.env(2, a=0.0, d=c.u(0.12, 0.35), s=c.u(0.0, 0.15), r=0.1)
            p.mod(SRC_ENV[2], "VoiceFilter", 0, "kParamFreq", c.u(35, 55))
            p.mod(SRC_VELO, "VoiceFilter", 0, "kParamFreq", c.u(10, 20))
            p.env(1, a=0.001, d=0.8, s=0.7, r=0.06)
            p.glob(volume=c.u(0.36, 0.45), mono=True, legato=True, porta=c.u(0.05, 0.12))
        elif kind == "reese":
            p.wt("A", c.pick([T["longreece"], T["sawdrift"], DEFAULT]), pos=1.0, vol=0.65, octave=-1,
                 unison=c.pick([2, 3, 4]), detune=c.u(0.08, 0.18), blend=c.u(60, 85))
            p.wt("B", T["anothersaw"], pos=c.u(1, 100), vol=0.5, octave=-1, fine=c.u(10, 25))
            p.sub(octave=-2, vol=0.45)
            p.filt(c.pick(["MgL24", "L24", "LadderMg"]), hz=c.u(400, 1100), reso=c.u(10, 30), drive=c.u(10, 30))
            p.lfo(1, hz=c.u(0.08, 0.35))
            p.mod(SRC_LFO[1], "VoiceFilter", 0, "kParamFreq", c.u(10, 22), bipolar=True)
            p.env(1, a=0.002, d=1.5, s=1.0, r=0.15)
            p.glob(volume=c.u(0.34, 0.42), mono=True, legato=True, porta=c.u(0.03, 0.1))
        elif kind == "fm":
            p.wt("A", c.pick([T["fmsaw"], T["fmfm"], T["opl"]]), pos=c.u(1, 200), vol=0.75, octave=-1,
                 warp="kFM_SUB", warp_amt=c.u(0.1, 0.4))
            p.sub(octave=-1, vol=0.4)
            p.filt("MgL24", hz=c.u(600, 2000), reso=c.u(5, 20))
            p.env(2, a=0.0, d=c.u(0.1, 0.3), s=0.0, r=0.1)
            p.mod(SRC_ENV[2], "WTOsc", 0, "kParamWarp", c.u(25, 45))
            p.env(1, a=0.001, d=0.6, s=0.6, r=0.08)
            p.glob(volume=c.u(0.36, 0.45), mono=True, legato=True, porta=0.04)
        else:
            p.wt("A", c.pick([T["pwmjuno"], T["juno"]]), pos=c.u(20, 200), vol=0.75, octave=-1)
            p.sub(shape="kSquare", octave=-2, vol=0.35)
            p.filt("LadderMg", hz=c.u(400, 1200), reso=c.u(15, 40))
            p.env(2, a=0.0, d=c.u(0.15, 0.4), s=0.1, r=0.1)
            p.mod(SRC_ENV[2], "VoiceFilter", 0, "kParamFreq", c.u(25, 45))
            p.lfo(1, hz=c.u(0.2, 0.8))
            p.mod(SRC_LFO[1], "WTOsc", 0, "kParamTablePos", c.u(10, 25), bipolar=True)
            p.env(1, a=0.001, d=0.5, s=0.5, r=0.08)
            p.glob(volume=c.u(0.36, 0.45), mono=True, legato=True, porta=0.05)
        d, v, dl = style_fx(p, c, "bass")
        standard_macros(p, c, d, v, dl)
    else:  # hollis
        kind = c.pick(["hyperbass", "growl", "glide"])
        if kind == "hyperbass":
            p.wt("A", c.pick([T["polysaw"], DEFAULT]), pos=1.0, vol=0.6, octave=-1,
                 unison=c.pick([3, 5]), detune=c.u(0.1, 0.2), blend=c.u(50, 75), stereo=c.u(40, 80))
            p.sub(octave=-2, vol=0.5)
        elif kind == "growl":
            p.wt("A", c.pick([T["softgrowl"], T["crushwub"], T["harshharm"]]), pos=c.u(1, 256), vol=0.7, octave=-1)
            p.lfo(1, sync=True)
            p.mod(SRC_LFO[1], "WTOsc", 0, "kParamTablePos", c.u(20, 50))
            p.sub(octave=-2, vol=0.45)
        else:
            p.wt("A", DEFAULT, pos=c.pick([POS["saw"], POS["sqr"]]), vol=0.7, octave=-1,
                 warp="kSync", warp_amt=c.u(0.1, 0.4))
            p.sub(octave=-2, vol=0.5)
        p.filt(c.pick(["MgL24", "L18", "LadderMg"]), hz=c.u(900, 3000), reso=c.u(10, 25))
        p.env(1, a=0.001, d=1.2, s=0.85, r=0.12)
        p.glob(volume=c.u(0.34, 0.42), mono=True, legato=True, porta=c.u(0.08, 0.2), porta_always=True)
        d, v, dl = style_fx(p, c, "bass")
        standard_macros(p, c, d, v, dl)


def sub808(p, c):
    p.wt("A", c.pick([T["sub808"], DEFAULT, T["trisub"], T["subroller"]]),
         pos=c.pick([1.0, POS["sine"], c.u(1, 80)]), vol=0.85, octave=-1)
    if c.chance(0.4):
        p.wt("B", T["harms808"], pos=c.u(1, 200), vol=c.u(0.15, 0.3), octave=-1)
    p.env(1, a=0.0, d=c.u(1.5, 4.0), s=0.0, r=c.u(0.2, 0.6))
    p.env(3, a=0.0, d=c.u(0.04, 0.1), s=0.0, r=0.05)
    p.mod(SRC_ENV[3], "Oscillator", 0, "kParamCoarsePit", c.u(12, 24))
    p.filt("MgL24", hz=c.u(2500, 9000), reso=5)
    p.glob(volume=c.u(0.38, 0.48), mono=True, legato=True, porta=c.u(0.08, 0.25), porta_always=True,
           bend=12)
    d, v, dl = style_fx(p, c, "808", dist_mode=c.pick(["kTapeSat", "kOverdrive", "kSoftClip", "kDiode1"]),
                        dist_drive=c.u(25, 65), verb=False)
    standard_macros(p, c, d, v, dl)


def lead(p, c):
    st = c.style
    if st == "hollis":
        kind = c.pick(["supersaw", "glass", "vocal"])
        if kind == "supersaw":
            p.wt("A", c.pick([T["polysaw"], T["synstring"], DEFAULT]), pos=1.0, vol=0.55,
                 unison=c.pick([7, 9]), detune=c.u(0.18, 0.32), blend=c.u(65, 90), stereo=c.u(70, 100))
            p.wt("B", DEFAULT, pos=POS["sqr"], vol=0.35, octave=1, unison=3, detune=0.1)
        elif kind == "glass":
            p.wt("A", c.pick([T["bellpluck"], T["harmsmooth"], T["tine"]]), pos=c.u(1, 200), vol=0.6,
                 unison=3, detune=c.u(0.05, 0.12))
            p.wt("B", DEFAULT, pos=POS["saw"], vol=0.4, octave=1, unison=5, detune=0.2)
        else:
            p.wt("A", c.pick([T["talkvox"], T["vocalhum"], T["voxy"]]), pos=c.u(1, 200), vol=0.6,
                 unison=5, detune=c.u(0.1, 0.2))
            p.lfo(1, hz=c.u(0.3, 1.2))
            p.mod(SRC_LFO[1], "WTOsc", 0, "kParamTablePos", c.u(15, 35), bipolar=True)
        p.filt(c.pick(["L12", "MgL12", "LH12"]), hz=c.u(5000, 14000), reso=c.u(0, 15))
        p.env(1, a=c.u(0.001, 0.01), d=1.0, s=0.9, r=c.u(0.15, 0.4))
        vibrato(p, c, 2, (0, 1))
        p.glob(volume=c.u(0.32, 0.4), mono=c.chance(0.6), legato=True, porta=c.u(0.05, 0.15))
        d, v, dl = style_fx(p, c, "lead")
        standard_macros(p, c, d, v, dl)
    elif st == "castles":
        p.wt("A", c.pick([DEFAULT, T["pwmc64"], T["matrixc64"], T["mario"], T["bitspeek"]]),
             pos=c.pick([POS["sqr"], POS["pulse"], POS["thin"], c.u(1, 256)]), vol=0.65,
             warp=c.pick(["kQuantize", "kPWM", None]), warp_amt=c.u(0.2, 0.7))
        if c.chance(0.5):
            p.wt("B", DEFAULT, pos=POS["sqr"], vol=0.35, octave=c.pick([1, -1]), fine=c.u(5, 12))
        p.filt(c.pick(["L12", "MgL12", "H12"]), hz=c.u(3000, 12000) if c.chance(0.8) else c.u(150, 400),
               reso=c.u(5, 25))
        p.env(1, a=0.001, d=c.u(0.3, 1.5), s=c.u(0.4, 0.9), r=c.u(0.08, 0.3))
        vibrato(p, c, 2, (0,), depth=c.u(6, 14))
        p.glob(volume=c.u(0.34, 0.42), mono=True, legato=c.chance(0.5), porta=c.u(0.0, 0.06))
        d, v, dl = style_fx(p, c, "lead")
        standard_macros(p, c, d, v, dl)
    elif st == "mink":
        p.wt("A", DEFAULT, pos=c.pick([POS["sine"], POS["tri"], c.u(40, 90)]), vol=0.7,
             warp=c.pick(["kDistTube", "kBendPos", "kFM_SUB"]), warp_amt=c.u(0.2, 0.6))
        if c.chance(0.5):
            p.wt("B", c.pick([T["dyingsine"], T["dyingsq"]]), pos=c.u(1, 256), vol=0.35, octave=1)
        p.filt("MgL18", hz=c.u(2000, 7000), reso=c.u(5, 20), drive=c.u(10, 40))
        p.env(1, a=0.002, d=1.2, s=0.8, r=c.u(0.1, 0.35))
        vibrato(p, c, 2, (0,), depth=c.u(3, 7))
        p.glob(volume=c.u(0.36, 0.44), mono=True, legato=True, porta=c.u(0.06, 0.2), porta_always=True)
        d, v, dl = style_fx(p, c, "lead", dist_mode=c.pick(["kHardClip", "kTapeSat", "kDiode2"]),
                            dist_drive=c.u(25, 55))
        standard_macros(p, c, d, v, dl)
    else:  # electro
        kind = c.pick(["sync", "fmsquelch", "acidlead"])
        if kind == "sync":
            p.wt("A", DEFAULT, pos=POS["saw"], vol=0.6, warp="kSync", warp_amt=c.u(0.2, 0.5), unison=2,
                 detune=0.05)
            p.env(2, a=0.0, d=c.u(0.2, 0.6), s=0.1, r=0.1)
            p.mod(SRC_ENV[2], "WTOsc", 0, "kParamWarp", c.u(25, 45))
        elif kind == "fmsquelch":
            p.wt("A", c.pick([T["fmfreak"], T["fmsquare"], T["squeal"]]), pos=c.u(1, 256), vol=0.6,
                 warp="kFM_OSC", warp_amt=c.u(0.1, 0.35))
            p.wt("B", DEFAULT, pos=POS["sine"], vol=0.0, octave=1, enable=True, route_filter=False)
        else:
            p.wt("A", c.pick([T["saw303"], T["acid"]]), pos=c.u(1, 256), vol=0.7)
        p.filt(c.pick(["LadderAcid", "MgL24", "LadderEMS"]), hz=c.u(900, 3500), reso=c.u(25, 60))
        p.env(2, a=0.0, d=c.u(0.15, 0.5), s=0.2, r=0.1)
        p.mod(SRC_ENV[2], "VoiceFilter", 0, "kParamFreq", c.u(20, 40))
        p.env(1, a=0.001, d=0.8, s=0.8, r=0.15)
        p.glob(volume=c.u(0.34, 0.42), mono=True, legato=True, porta=c.u(0.03, 0.1))
        d, v, dl = style_fx(p, c, "lead")
        standard_macros(p, c, d, v, dl)


def keys(p, c):
    st = c.style
    table = {
        "hollis": [T["fmpiano"], T["tine"], T["bellpluck"], T["harmsmooth"]],
        "mink": [T["fmpiano"], T["opl"], T["organ"], T["dyingsine"]],
        "castles": [T["mario"], T["dulltoy"], T["matrixc64"], DEFAULT],
        "electro": [T["juno"], T["pwmjuno"], T["dxhard"], T["opl"]],
    }[st]
    tbl = c.pick(table)
    p.wt("A", tbl, pos=c.u(1, 256) if tbl != DEFAULT else POS["sqr"], vol=0.65,
         unison=c.pick([1, 2, 3]), detune=c.u(0.03, 0.08))
    p.wt("B", DEFAULT, pos=c.pick([POS["sine"], POS["tri"]]), vol=c.u(0.2, 0.4), octave=c.pick([0, 1]))
    p.filt(c.pick(["MgL12", "L12", "LadderMg"]), hz=c.u(1200, 4000), reso=c.u(0, 15), keytrack=True)
    p.env(1, a=0.001, d=c.u(0.8, 2.5), s=c.u(0.15, 0.5), r=c.u(0.2, 0.6))
    p.env(2, a=0.0, d=c.u(0.3, 1.0), s=c.u(0.1, 0.3), r=0.3)
    p.mod(SRC_ENV[2], "VoiceFilter", 0, "kParamFreq", c.u(15, 35))
    p.mod(SRC_VELO, "VoiceFilter", 0, "kParamFreq", c.u(8, 18))
    if st in ("electro", "mink") and c.chance(0.6):
        p.lfo(1, hz=c.u(0.15, 0.6))
        p.mod(SRC_LFO[1], "Oscillator", 0, "kParamFine", c.u(2, 6), bipolar=True)
    p.glob(volume=c.u(0.36, 0.45), poly=c.pick([8, 12, 16]))
    d, v, dl = style_fx(p, c, "key", dist_drive=c.u(5, 25))
    standard_macros(p, c, d, v, dl)


def pad(p, c):
    st = c.style
    if st == "hollis":
        p.wt("A", c.pick([T["polysaw"], T["synstring"], DEFAULT]), pos=1.0, vol=0.5,
             unison=c.pick([7, 9, 11]), detune=c.u(0.2, 0.35), blend=c.u(70, 95), stereo=100)
        p.wt("B", c.pick([T["vocalhum"], T["harmsmooth"], T["shep"]]), pos=c.u(1, 256), vol=0.35, octave=1,
             unison=3, detune=0.1)
    elif st == "electro":
        p.wt("A", c.pick([T["pwmjuno"], T["juno"], T["solina"]]), pos=c.u(1, 256), vol=0.55,
             unison=c.pick([2, 3, 4]), detune=c.u(0.06, 0.14), stereo=80)
        p.wt("B", T["sawphasey"], pos=c.u(1, 200), vol=0.35, fine=c.u(5, 15))
        p.lfo(1, hz=c.u(0.1, 0.5))
        p.mod(SRC_LFO[1], "WTOsc", 0, "kParamTablePos", c.u(15, 35), bipolar=True)
    elif st == "castles":
        p.wt("A", c.pick([T["pwmc64"], T["mello"], DEFAULT]), pos=c.pick([POS["sqr"], c.u(1, 256)]), vol=0.5,
             unison=c.pick([3, 5]), detune=c.u(0.08, 0.2), stereo=100, warp="kQuantize", warp_amt=c.u(0.1, 0.4))
        p.wt("B", T["mello"], pos=c.u(1, 256), vol=0.35, octave=-1)
    else:  # mink
        p.wt("A", c.pick([T["mello"], T["solina"], T["dyingsaw"]]), pos=c.u(1, 256), vol=0.55,
             unison=c.pick([3, 4, 5]), detune=c.u(0.1, 0.2), stereo=90)
        p.noise(c.pick([NOISE["hum"], NOISE["pink"], NOISE["juno"]]), vol=c.u(0.08, 0.18))
    p.filt(c.pick(["MgL12", "L12", "LadderMg", "MgL18"]), hz=c.u(1500, 6000), reso=c.u(5, 20))
    p.lfo(2, hz=c.u(0.05, 0.2))
    p.mod(SRC_LFO[2], "VoiceFilter", 0, "kParamFreq", c.u(8, 18), bipolar=True)
    p.env(1, a=c.u(0.3, 1.5), d=2.0, s=0.85, r=c.u(1.2, 3.5))
    p.glob(volume=c.u(0.32, 0.4), poly=c.pick([8, 12]))
    d, v, dl = style_fx(p, c, "pad", verb=True)
    standard_macros(p, c, d, v, dl, move="lfo")


def atmos(p, c):
    st = c.style
    tbl = c.pick({
        "hollis": [T["shep"], T["vocalhum"], T["harmsmooth"], T["talkvox"]],
        "mink": [T["generative"], T["dyingsaw"], T["softgrowl"], T["mello"]],
        "castles": [T["elecnoise"], T["bitspeek"], T["hypersqueak"], T["matrixc64"]],
        "electro": [T["generative"], T["squeal"], T["hypa"], T["juno"]],
    }[st])
    p.wt("A", tbl, pos=c.u(1, 256), vol=0.5, unison=c.pick([3, 5, 7]), detune=c.u(0.1, 0.3), stereo=100)
    p.noise(c.pick([NOISE["atmos"], NOISE["atmos2"], NOISE["flow"], NOISE["breath"], NOISE["aircan"]]),
            vol=c.u(0.15, 0.35))
    p.lfo(1, hz=c.u(0.03, 0.15))
    p.mod(SRC_LFO[1], "WTOsc", 0, "kParamTablePos", c.u(30, 60), bipolar=True)
    p.lfo(2, hz=c.u(0.05, 0.25), shape=SHAPE_TRI)
    p.mod(SRC_LFO[2], "VoiceFilter", 0, "kParamFreq", c.u(12, 25), bipolar=True)
    p.filt(c.pick(["MgL12", "B12", "L12", "Phase24P", "CombP"]), hz=c.u(800, 5000), reso=c.u(10, 40))
    p.env(1, a=c.u(1.0, 4.0), d=3.0, s=0.9, r=c.u(2.5, 6.0))
    p.glob(volume=c.u(0.3, 0.38), poly=8)
    d, v, dl = style_fx(p, c, "atmos", verb=True, delay=True)
    # big wet tails on top of the style chain
    p.fx("FXReverb", Type=c.pick(["kSpace", "kHall"]), Wet=c.u(25, 45), Size=c.u(80, 100), Width=100)
    standard_macros(p, c, d, v, dl, move="lfo")


def pluck(p, c, role="pluck"):
    st = c.style
    tbl = c.pick({
        "hollis": [T["richpluck"], T["bellpluck"], T["polysaw"], DEFAULT],
        "mink": [T["dyingsine"], T["opl"], T["xylo"], DEFAULT],
        "castles": [T["pwmc64"], T["mario"], T["fwap8bit"], DEFAULT],
        "electro": [T["saw303"], T["juno"], T["fmsaw"], T["xylo"]],
    }[st])
    pos = POS["sqr"] if (tbl == DEFAULT and st == "castles") else (POS["saw"] if tbl == DEFAULT else c.u(1, 256))
    uni = c.pick([1, 3, 5]) if st == "hollis" else c.pick([1, 2])
    p.wt("A", tbl, pos=pos, vol=0.65, unison=uni, detune=c.u(0.08, 0.2), stereo=80)
    if c.chance(0.5):
        p.wt("B", DEFAULT, pos=c.pick([POS["sine"], POS["sqr"]]), vol=0.3, octave=1)
    p.filt(c.pick(["MgL24", "L24", "LadderMg", "MgL18"]), hz=c.u(300, 900), reso=c.u(10, 35), keytrack=True)
    p.env(2, a=0.0, d=c.u(0.12, 0.4), s=0.0, r=0.15)
    p.mod(SRC_ENV[2], "VoiceFilter", 0, "kParamFreq", c.u(35, 55))
    p.env(1, a=0.0005, d=c.u(0.25, 0.7), s=0.0, r=c.u(0.15, 0.4))
    p.glob(volume=c.u(0.38, 0.46), poly=12)
    d, v, dl = style_fx(p, c, role)
    standard_macros(p, c, d, v, dl)


def arp(p, c):
    pluck(p, c, role="arp")
    p.arp(shape=c.pick(["Up", "UpDown", "Down", "Rand", "UpAndDown", "Played"]),
          octaves=c.pick([1.0, 2.0, 3.0]), gate=c.u(60, 110))


def stab(p, c):
    st = c.style
    if st in ("hollis", "electro") and c.chance(0.4):
        p.wt("A", T["chord"], pos=c.u(1, 256), vol=0.6, unison=3, detune=0.1)
    else:
        p.wt("A", c.pick([T["polysaw"], DEFAULT, T["sawsquare"], T["juno"]]), pos=c.u(1, 120), vol=0.55,
             unison=c.pick([3, 5, 7]), detune=c.u(0.12, 0.25), stereo=90)
        p.wt("B", DEFAULT, pos=POS["sqr"], vol=0.3, octave=-1)
    p.filt(c.pick(["MgL24", "LadderMg", "L18"]), hz=c.u(700, 2500), reso=c.u(10, 30))
    p.env(2, a=0.0, d=c.u(0.15, 0.4), s=c.u(0.0, 0.2), r=0.2)
    p.mod(SRC_ENV[2], "VoiceFilter", 0, "kParamFreq", c.u(30, 50))
    p.env(1, a=0.001, d=c.u(0.3, 0.8), s=c.u(0.0, 0.3), r=c.u(0.15, 0.4))
    p.glob(volume=c.u(0.34, 0.42), poly=12)
    d, v, dl = style_fx(p, c, "stab")
    standard_macros(p, c, d, v, dl)


def sfx(p, c):
    kind = c.pick(["laser", "siren", "glitch", "sweep", "drop"])
    if kind == "laser":
        p.wt("A", DEFAULT, pos=c.pick([POS["sqr"], POS["saw"]]), vol=0.6)
        p.env(3, a=0.0, d=c.u(0.1, 0.4), s=0.0, r=0.1)
        p.mod(SRC_ENV[3], "Oscillator", 0, "kParamCoarsePit", c.u(40, 70))
        p.env(1, a=0.0, d=0.5, s=0.0, r=0.2)
    elif kind == "siren":
        p.wt("A", c.pick([DEFAULT, T["pwmc64"]]), pos=POS["sqr"], vol=0.55)
        p.lfo(1, hz=c.u(0.5, 3.0), shape=SHAPE_TRI)
        p.mod(SRC_LFO[1], "Oscillator", 0, "kParamCoarsePit", c.u(15, 30), bipolar=True)
        p.env(1, a=0.01, d=1.0, s=1.0, r=0.3)
    elif kind == "glitch":
        p.wt("A", c.pick([T["bitspeek"], T["hypersqueak"], T["fwap8bit"]]), pos=c.u(1, 256), vol=0.6)
        p.lfo(1, hz=c.u(6, 14), shape=SHAPE_SQUARE)
        p.mod(SRC_LFO[1], "WTOsc", 0, "kParamTablePos", c.u(40, 80), bipolar=True)
        p.mod(SRC_LFO[1], "Oscillator", 0, "kParamCoarsePit", c.u(6, 14), bipolar=True)
        p.env(1, a=0.0, d=0.4, s=0.6, r=0.1)
    elif kind == "sweep":
        p.noise(c.pick([NOISE["white"], NOISE["juno"], NOISE["aircan"]]), vol=0.6)
        p.wt("A", DEFAULT, pos=POS["saw"], vol=0.0)
        p.lfo(1, hz=c.u(0.08, 0.25), shape=SHAPE_TRI)
        p.mod(SRC_LFO[1], "VoiceFilter", 0, "kParamFreq", c.u(35, 55), bipolar=True)
        p.env(1, a=c.u(0.5, 2.0), d=2.0, s=1.0, r=1.5)
    else:  # drop
        p.wt("A", c.pick([T["sub808"], DEFAULT]), pos=POS["sine"], vol=0.7, octave=-1)
        p.noise(NOISE["white"], vol=0.2)
        p.env(3, a=0.0, d=c.u(0.8, 2.0), s=0.0, r=0.5)
        p.mod(SRC_ENV[3], "Oscillator", 0, "kParamCoarsePit", c.u(30, 50))
        p.env(1, a=0.0, d=2.5, s=0.0, r=0.5)
    p.filt(c.pick(["MgL12", "B12", "LadderMg"]), hz=c.u(1500, 6000), reso=c.u(15, 45))
    p.glob(volume=c.u(0.32, 0.4), poly=4)
    d, v, dl = style_fx(p, c, "fx", verb=True, delay=True)
    standard_macros(p, c, d, v, dl, move="lfo" if kind in ("siren", "glitch", "sweep") else "wt")


# category -> (folder, name prefix, archetype, Serum tags, count)
CATEGORIES = [
    ("Bass", "BS", bass, ["Bass", "Mono"], 45),
    ("Lead", "LD", lead, ["Lead"], 40),
    ("Keys", "KY", keys, ["Keyboard"], 30),
    ("Pad", "PD", pad, ["Pad"], 30),
    ("Arp", "ARP", arp, ["Arp"], 25),
    ("Atmos", "ATM", atmos, ["Soundscape"], 25),
    ("Pluck", "PL", pluck, ["Pluck"], 20),
    ("Synth & Stab", "SY", stab, ["Synth"], 15),
    ("808 & Sub", "808", sub808, ["Bass", "808", "Mono"], 10),
    ("FX", "FX", sfx, ["SFX"], 10),
]
STYLES = ["hollis", "mink", "castles", "electro"]
STYLE_TAGS = {"hollis": "Hyperpop", "mink": "Underground", "castles": "8-Bit", "electro": "Electro"}


def make(category, style, rng, name):
    folder, prefix, fn, tags, _ = next(cat for cat in CATEGORIES if cat[0] == category)
    p = Preset(name, AUTHOR, tags + [STYLE_TAGS[style], "Wavetable"],
               description=f"RecklessSerum2Bank_1 - {category} / {STYLE_TAGS[style]}. "
                           f"Macros: TONE, DIRT, SPACE, MOVE.")
    fn(p, Ctx(rng, style))
    return p
