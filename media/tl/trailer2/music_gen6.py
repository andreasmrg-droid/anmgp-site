"""War-drum theme v2: drums from frame 0, continuous escalation, accents on every breach/cut."""
src = open('/home/claude/tr/music_gen3.py').read().split('# ---------- TIMELINE')[0]
exec(src.replace('BPM = 92','BPM = 120'))
import numpy as np
chant_reclaim = load('chant_reclaim.wav')

BREACHES = [3.5, 6.5, 16.0, 22.0]
CUTS = [4.25, 8.5, 16.5, 22.5, 28.0, 32.5, 38.0]
END = 41.5

# pattern per 2-bar cycle; global grid from t=0 so nothing "restarts"
GROOVE_A = [(0,'T'),(1.5,'t'),(2,'C'),(3,'T'),(3.5,'T'),(4,'T'),(5.5,'t'),(6,'C'),(7,'t'),(7.5,'t')]
GROOVE_B = GROOVE_A + [(0.5,'t'),(2.5,'t'),(4.5,'t'),(6.5,'t'),(7.25,'t'),(7.75,'t')]
WAR_A = WAR
WAR_B = WAR + [(0.25,'t'),(1.25,'t'),(2.25,'t'),(3.25,'t'),(4.25,'t'),(5.25,'t'),(6.25,'t'),(6.75,'t')]

PULSE = [(0,'T'),(1,'T'),(2,'T'),(3,'T'),(4,'T'),(5,'T'),(6,'T'),(7,'T'),(7.5,'t')]
def section_pattern(t):
    if t < 4.25: return PULSE, 0.8
    if t < 8.5:  return GROOVE_A, 0.9
    if t < 16.5: return GROOVE_B, 0.95
    if t < 22.5: return GROOVE_B, 1.0
    if t < 28.0: return WAR_A, 0.95
    if t < 32.2: return WAR_B, 1.0
    if t < 38.0: return WAR_B, 1.05
    if t < 41.5: return WAR_B, 1.1
    return None, 0

bar2 = 8 * BEAT
c = 0
while c * bar2 < END:
    base = c * bar2
    for off, kind in section_pattern(base)[0] or []:
        tt = base + off * BEAT
        pat, g = section_pattern(tt)
        if pat is None: continue
        if kind == 'T': add(taiko(55), tt, g)
        elif kind == 't': add(tom(rng.choice([95, 120, 140])), tt, 0.8 * g, pan=rng.uniform(-0.5, 0.5))
        elif kind == 'C': add(clap(), tt, 0.8 * g, pan=0.1)
    c += 1

# pulse underneath from the first frame: ticking + low braams every 2 bars, getting brighter
ticks(0.0, 8.5, gain=0.55)
ticks(8.5, 28.0, gain=0.5, div=4)
ticks(28.0, 32.5, gain=0.7, div=4)
for k, tt in enumerate(np.arange(0, 32.2, bar2)):
    add(braam([36.71, 43.65, 32.70, 36.71][k % 4], bar2 * 0.98, 0.35 + 0.05 * k), tt, 0.45 + 0.03 * k)

# string ostinato enters at the first cut and opens up continuously (no reset)
ostinato(4.25, 16.5, 500, 1200, gain=0.6)
ostinato(16.5, 28.0, 1200, 2600, gain=0.75)
ostinato(28.0, 32.5, 2600, 6000, gain=0.85)
ostinato(32.5, 41.5, 4000, 7500, gain=0.9, octave=2)

# choir layers in the middle for weight
add(choir((146.8, 174.6, 220.0), 6.0), 16.5, 0.6)
add(choir((164.8, 196.0, 246.9), 9.7, vowel=((700, 1220),)), 22.5, 0.7)

# fills into the cuts
for t in CUTS:
    if t in (32.5, 38.0): continue
    tom_roll(t - BEAT, t - 0.02, 0.3, 0.8, div=4)

# BREACH accents: big taiko + cage slam + crowd chant
chants = [chant_trench, chant_breach, chant_brawl, chant_trench]
for k, t in enumerate(BREACHES):
    add(taiko(42, 2.5), t, 1.15)
    add(gate_slam(), t, 0.6 + 0.05 * k)
    add(sub_drop(1.5), t, 0.6)

# BUILD 28-32.2: toms accelerate, whoosh, braam swell -> short breath -> PEAK at 32.5
tom_roll(29.6, 32.48, 0.3, 1.2, div=4)
tom_roll(31.5, 32.48, 0.6, 1.25, div=8)
add(whoosh(2.0), 30.5, 1.0)
add(whoosh(3.0), 29.2)
add(braam(36.71, 3.0, 0.5), 29.2, 0.5)
add(braam(36.71, 4.0, 1.0), 32.5, 1.0); add(braam(73.42, 3.0, 1.0), 32.5, 0.5)
add(taiko(40, 3.0), 32.5, 1.3); add(gate_slam(), 32.5, 0.85)
add(chant_reclaim * 0.8, 32.55, 0.75)

# CLIMAX 38-41: new braam on lava cut, roll, then silence and final breach hit on the end card
add(braam(43.65, 3.0, 1.0), 38.0, 0.9); add(gate_slam(), 38.0, 0.7); add(taiko(42, 2.0), 38.0, 1.2)
tom_roll(39.5, 41.48, 0.4, 1.3, div=8)
add(whoosh(2.1), 39.4)
add(braam(36.71, 6.0, 1.0), END, 1.1); add(braam(18.35, 6.0, 0.6), END, 0.6)
add(taiko(38, 4.0), END, 1.45); add(gate_slam(), END, 1.0); add(sub_drop(3.0), END, 0.9)
# end-card heartbeat taiko fading
for k in range(4):
    add(taiko(50, 1.5), END + 1.6 + k * 1.1, 0.5 - 0.1 * k)

# ---------- MASTER ----------
mix = np.stack([L, R], 1)
ir_n = int(2.2 * SR)
ir = lp(rng.standard_normal((ir_n, 2)).T, 4500) * np.exp(-np.arange(ir_n) / SR * 2.6) * 0.022
for ch in range(2):
    mix[:, ch] += fftconvolve(mix[:, ch], ir[ch])[:N]
def duck(a, b, lvl=0.04, r=0.03):
    i0, i1 = int(a * SR), int(b * SR); rr = int(r * SR)
    g = np.ones(N); g[i0:i1] = lvl; g[i0-rr:i0] = np.linspace(1, lvl, rr); g[i1:i1+rr] = np.linspace(lvl, 1, rr)
    return g
mix = mix / np.max(np.abs(mix)); mix = np.tanh(mix * 1.6)
mix /= np.max(np.abs(mix)) / 0.92
fade = int(2.5 * SR); mix[-fade:] *= np.linspace(1, 0, fade)[:, None]
wavfile.write('tl_trailer_music6.wav', SR, (mix * 32767).astype(np.int16))
print('ok')
