"""Theme 2: cinematic arena war-drums. Taiko, BRAAMs, ticking clock, string ostinato,
choir pad, and the game's own crowd chants. Synced to trailer cuts."""
import numpy as np
from scipy.signal import butter, sosfilt, fftconvolve
from scipy.io import wavfile

SR = 44100
DUR = 47.63
N = int(SR * DUR)
BPM = 92
BEAT = 60 / BPM
rng = np.random.default_rng(23)
L = np.zeros(N); R = np.zeros(N)
A = "/mnt/user-data/uploads/Trench League/audio/"

def lp(x, f, o=2): return sosfilt(butter(o, f, 'low', fs=SR, output='sos'), x)
def hp(x, f, o=2): return sosfilt(butter(o, f, 'high', fs=SR, output='sos'), x)
def bp(x, lo, hi, o=2): return sosfilt(butter(o, [lo, hi], 'band', fs=SR, output='sos'), x)
def saw(f, n, ph=0.0):
    t = np.arange(n) / SR
    return 2 * ((t * f + ph) % 1) - 1

def add(sig, t, gain=1.0, pan=0.0):
    i = int(t * SR)
    if i >= N or t < 0: return
    s = sig[:N - i] * gain
    L[i:i+len(s)] += s * (1 - max(pan, 0))
    R[i:i+len(s)] += s * (1 + min(pan, 0))

def load(name):
    sr, x = wavfile.read(A + name)
    x = x.astype(np.float64)
    if x.ndim > 1: x = x.mean(1)
    return x / (np.max(np.abs(x)) + 1e-9)

# ---------- instruments ----------
def taiko(f0=60, d=1.6, tone=1.0):
    n = int(d * SR); t = np.arange(n) / SR
    f = f0 + f0 * 1.2 * np.exp(-t * 25)
    body = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 3.2)
    skin = bp(rng.standard_normal(n), 120, 1800) * np.exp(-t * 18) * 0.8 * tone
    return np.tanh((body + skin) * 2.2) * 0.8

def tom(f0=110):
    return taiko(f0, 0.8, 0.6) * 0.7

def clap():
    n = int(0.4 * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for k, off in enumerate((0, 0.011, 0.023)):
        i = int(off * SR)
        s[i:] += bp(rng.standard_normal(n - i), 800, 5000) * np.exp(-t[:n - i] * (60 if k < 2 else 14))
    return np.tanh(s * 1.5) * 0.55

def braam(root=36.71, d=4.0, bright=1.0):
    n = int(d * SR); t = np.arange(n) / SR
    s = np.zeros(n)
    for m, g in ((1, 1), (1.5, 0.7), (2, 0.8), (2.378, 0.5), (3, 0.4)):   # root, 5th, oct, min3, 5th
        for det in (-0.004, 0, 0.005):
            s += saw(root * m * (1 + det), n, rng.uniform()) * g
    s = np.tanh(s * 0.9)
    cut = 180 + 2200 * bright * np.exp(-t * 1.4) * (1 - np.exp(-t * 18))
    out = np.zeros(n); ch = 1024
    for i in range(0, n, ch):
        seg = s[max(0, i - ch):i + ch]
        out[i:i+ch] = lp(seg, max(cut[i], 60))[-len(s[i:i+ch]):]
    e = (1 - np.exp(-t * 30)) * np.exp(-t * 0.55)
    return out * e * 0.5

def tick():
    n = int(0.05 * SR); t = np.arange(n) / SR
    return hp(rng.standard_normal(n), 4000) * np.exp(-t * 150) * 0.35 + np.sin(2*np.pi*2400*t)*np.exp(-t*200)*0.2

def pluck(f, d, cutoff):
    n = int(d * SR); t = np.arange(n) / SR
    s = saw(f, n) + saw(f * 1.004, n)
    s = lp(s, cutoff) * np.exp(-t * 9)
    return s * 0.22

def choir(freqs, d, vowel=((700, 1220), (450, 1000))):
    n = int(d * SR); t = np.arange(n) / SR
    src = sum(saw(f * (1 + 0.003 * np.sin(2*np.pi*(4.7+k)*t)), n) for k, f in enumerate(freqs)) / len(freqs)
    out = np.zeros(n)
    for f1, f2 in vowel:
        out += bp(src, f1 * 0.8, f1 * 1.2) + 0.6 * bp(src, f2 * 0.85, f2 * 1.15)
    e = np.minimum(1, t / 1.2) * np.minimum(1, (d - t) / 1.0)
    return out * e * 0.6

def sub_drop(d=2.0):
    n = int(d * SR); t = np.arange(n) / SR
    f = 70 * np.exp(-t * 1.5) + 25
    return np.sin(2*np.pi*np.cumsum(f)/SR) * np.exp(-t * 1.2) * 0.8

def whoosh(d, rev=False):
    n = int(d * SR); t = np.arange(n) / SR
    x = rng.standard_normal(n); out = np.zeros(n); ch = 2048
    for i in range(0, n, ch):
        f = 300 * (40) ** (i / n)
        out[i:i+ch] = bp(x[i:i+ch], f, min(f * 2, 20000))
    e = (t / d) ** 2.5
    s = out * e * 0.3
    return s[::-1] if rev else s

def gate_slam():   # metallic cage slam for big hits
    n = int(2.5 * SR); t = np.arange(n) / SR
    s = sum(np.sin(2*np.pi*f*t + rng.uniform(0, 6)) * np.exp(-t * (1.5 + k*0.7)) for k, f in enumerate((97, 163, 251, 389, 577, 853)))
    s += lp(rng.standard_normal(n), 2500) * np.exp(-t * 20)
    return np.tanh(s * 0.9) * 0.6

# D minor ostinato (16ths): D A F A D A E A ...
OST = [146.8, 220.0, 174.6, 220.0, 146.8, 220.0, 164.8, 220.0,
       146.8, 220.0, 174.6, 220.0, 130.8, 196.0, 164.8, 196.0]

def ostinato(t0, t1, c0, c1, gain=1.0, octave=1):
    s16 = BEAT / 4; k = 0; total = (t1 - t0) / s16
    while t0 + k * s16 < t1 - 0.01:
        c = c0 + (c1 - c0) * (k / total)
        add(pluck(OST[k % 16] * octave, s16 * 1.6, c), t0 + k * s16, gain, pan=(0.25 if k % 2 else -0.25))
        k += 1

def drums(t0, t1, pattern, gain=1.0, claps=True):
    """pattern: list of (beat_offset_in_bar, 'T'|'t') over a 2-bar (8 beat) cycle"""
    bar2 = 8 * BEAT; c = 0
    while t0 + c * bar2 < t1 - 0.01:
        base = t0 + c * bar2
        for off, kind in pattern:
            tt = base + off * BEAT
            if tt >= t1 - 0.01: continue
            if kind == 'T': add(taiko(55), tt, gain, pan=0.0)
            elif kind == 't': add(tom(rng.choice([95, 120, 140])), tt, 0.8 * gain, pan=rng.uniform(-0.5, 0.5))
            elif kind == 'C' and claps: add(clap(), tt, 0.8 * gain, pan=0.1)
        c += 1

def tom_roll(t0, t1, g0=0.2, g1=1.0, div=4):
    k = 0; total = (t1 - t0) / (BEAT / div)
    while t0 + k * (BEAT / div) < t1 - 0.01:
        add(tom(100 + 60 * (k / total)), t0 + k * (BEAT / div), g0 + (g1 - g0) * k / total, pan=(-0.4 if k % 2 else 0.4))
        k += 1

def ticks(t0, t1, gain=1.0, div=2):
    k = 0
    while t0 + k * (BEAT / div) < t1 - 0.01:
        add(tick(), t0 + k * (BEAT / div), gain * (1.0 if k % div == 0 else 0.6), pan=0.4)
        k += 1

GROOVE = [(0, 'T'), (1.5, 't'), (2, 'C'), (3, 'T'), (3.5, 'T'), (4, 'T'), (5.5, 't'), (6, 'C'), (7, 't'), (7.5, 't')]
SPARSE = [(0, 'T'), (4, 'T')]
WAR    = [(0, 'T'), (0.5, 't'), (1, 'T'), (1.5, 't'), (2, 'C'), (2.5, 't'), (3, 'T'), (3.5, 'T'),
          (4, 'T'), (4.5, 't'), (5, 'T'), (5.5, 't'), (6, 'C'), (6.5, 't'), (7, 'T'), (7.25, 't'), (7.5, 'T'), (7.75, 't')]

chant_trench = load('chant_trench.wav'); chant_breach = load('chant_breach.wav')
chant_brawl = load('chant_brawl.wav'); chant_nofuture = load('chant_nofuture.wav')

# ---------- TIMELINE ----------
# 0-4.4  cold open: one BRAAM, ticking clock creeping in, whoosh into the first hit
add(braam(36.71, 4.4, 0.6), 0.05, 0.8)
ticks(1.5, 4.36, gain=0.7)
add(whoosh(1.4), 2.96)
T1 = 4.36
# 4.4-15.3  ARENA: taiko groove + ostinato (mid) + chant
add(taiko(45, 2.5), T1, 1.2); add(gate_slam(), T1, 0.7)
drums(T1, 15.3, GROOVE, 0.9)
ostinato(T1, 15.3, 700, 1600, gain=0.8)
add(chant_trench * 0.5, 6.2, 0.55, pan=-0.2)       # crowd reacts around breach at ~6 s
add(braam(43.65, 3.0, 0.5), 10.9, 0.5)            # F braam mid-section
# 15.3-16.4 drop-out: reverse whoosh + sub drop
add(sub_drop(1.2), 15.25, 0.9)
add(whoosh(1.1), 15.3)
T2 = 16.4
# 16.4-26  LOW: no drums, choir pad, slow heartbeat taiko, ticking, distant chant
add(gate_slam(), T2, 0.5)
add(choir((146.8, 174.6, 220.0), 9.8), T2, 0.9)
drums(T2, 26.0, SPARSE, 0.55, claps=False)
ticks(T2 + 2 * BEAT, 26.0, gain=0.45)
add(chant_nofuture * 0.4, 18.5, 0.5, pan=0.3)
ostinato(21.6, 26.0, 300, 500, gain=0.5)
# 26-31.7  BUILD: ostinato opens up, toms roll, BRAAM swell, ticks double
add(choir((164.8, 196.0, 246.9), 5.9, vowel=((700, 1220),)), 26.0, 0.9)
drums(26.0, 29.0, GROOVE, 0.85)
ostinato(26.0, 31.7, 600, 4500, gain=0.9)
ticks(26.0, 31.6, gain=0.6, div=4)
tom_roll(29.0, 31.65, 0.25, 1.1, div=4)
add(whoosh(3.2), 28.5)
add(braam(36.71, 3.0, 0.4), 28.7, 0.45)
# 31.7-32.3 SILENCE
T3 = 32.3
# 32.3-37.8 PEAK: double BRAAM, war drums, octave-up ostinato, chant
add(braam(36.71, 4.0, 1.0), T3, 1.0); add(braam(73.42, 3.0, 1.0), T3, 0.5)
add(taiko(42, 3.0), T3, 1.3); add(gate_slam(), T3, 0.8)
drums(T3, 37.8, WAR, 1.0)
ostinato(T3, 37.8, 3000, 5000, gain=0.9, octave=2)
add(chant_brawl * 0.6, 33.0, 0.6, pan=-0.3)
# 37.8-41.0 CLIMAX: new BRAAM on cut, faster roll, chant_breach
add(braam(43.65, 3.2, 1.0), 37.8, 0.9); add(gate_slam(), 37.8, 0.6)
drums(37.8, 40.0, WAR, 1.05)
ostinato(37.8, 41.0, 4000, 7000, gain=0.9, octave=2)
tom_roll(39.6, 40.95, 0.4, 1.2, div=8)
add(whoosh(1.6), 39.4)
# 41.0-41.6 SILENCE  ->  41.6 END CARD
T4 = 41.6
add(braam(36.71, 6.0, 1.0), T4, 1.1); add(braam(18.35, 6.0, 0.6), T4, 0.6)
add(taiko(40, 4.0), T4, 1.4); add(gate_slam(), T4, 1.0)
add(chant_breach * 0.7, T4 + 0.3, 0.7)

# ---------- MASTER ----------
mix = np.stack([L, R], 1)
ir_n = int(2.2 * SR)
ir = lp(rng.standard_normal((ir_n, 2)).T, 4500)
ir = ir * np.exp(-np.arange(ir_n) / SR * 2.6) * 0.022
for c in range(2):
    mix[:, c] += fftconvolve(mix[:, c], ir[c])[:N]
def duck(a,b,lvl=0.04,r=0.03):
    i0,i1=int(a*SR),int(b*SR); rr=int(r*SR)
    g=np.ones(N); g[i0:i1]=lvl; g[i0-rr:i0]=np.linspace(1,lvl,rr); g[i1:i1+rr]=np.linspace(lvl,1,rr)
    return g
G=duck(31.72,32.28)*duck(41.0,41.58)*duck(15.35,16.38,0.35,0.1)
mix *= G[:,None]
mix = mix / np.max(np.abs(mix)); mix = np.tanh(mix * 1.6)
mix /= np.max(np.abs(mix)) / 0.92
fade = int(2.5 * SR); mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
wavfile.write('tl_trailer_music3.wav', SR, (mix * 32767).astype(np.int16))
print('ok')
