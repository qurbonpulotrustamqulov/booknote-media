import math, os, random, subprocess, wave
import numpy as np
from PIL import Image, ImageDraw, ImageFont, ImageFilter, ImageChops

S = os.path.dirname(os.path.abspath(__file__))
FD = os.path.join(S, 'fonts')
OUT = '/mnt/project-files/booknote-marketing/namunalar-v2/'
os.makedirs(OUT, exist_ok=True)
W, H, FPS, SR = 1080, 1920, 30, 44100

_fc = {}
def font(name, size):
    k = (name, size)
    if k not in _fc:
        path = os.path.join(FD, name + '.ttf')
        if not os.path.exists(path): path = '/usr/share/fonts/opentype/inter/' + name + '.otf'
        _fc[k] = ImageFont.truetype(path, size)
    return _fc[k]

_d = ImageDraw.Draw(Image.new('RGB', (1, 1)))
FEAT = ['lnum']
def tw(s, f): return _d.textlength(s, font=f, features=FEAT)

def ease(t): t = max(0.0, min(1.0, t)); return 1 - (1 - t) ** 3
def ease_io(t): t = max(0.0, min(1.0, t)); return t * t * (3 - 2 * t)
def clamp(t): return max(0.0, min(1.0, t))

def wrap(text, f, maxw):
    out = []
    for para in text.split('\n'):
        cur = ''
        for wd in para.split():
            test = (cur + ' ' + wd).strip()
            if tw(test, f) <= maxw: cur = test
            else: out.append(cur); cur = wd
        out.append(cur)
    return out

def text_layer(text, f, fill, maxw=W - 160, align='c', lh=1.12, chars=None, stroke=0, stroke_fill=(0, 0, 0)):
    """Render wrapped text; chars limits visible characters (typewriter)."""
    lines = wrap(text, f, maxw)
    asc, desc = f.getmetrics(); lhpx = int((asc + desc) * lh)
    w = int(max(tw(l, f) for l in lines)) + 24 + stroke * 2
    layer = Image.new('RGBA', (w, lhpx * len(lines) + 16), (0, 0, 0, 0))
    d = ImageDraw.Draw(layer)
    left = chars if chars is not None else 10 ** 9
    for i, l in enumerate(lines):
        vis = l[:max(0, left)]; left -= len(l) + 1
        x = (w - tw(l, f)) / 2 if align == 'c' else 12
        if vis: d.text((x, i * lhpx + 4), vis, font=f, fill=fill, stroke_width=stroke, stroke_fill=stroke_fill, features=FEAT)
    return layer

def fade(layer, p):
    if p >= 1: return layer
    l = layer.copy(); l.putalpha(l.split()[3].point(lambda v: int(v * p))); return l

def put(frame, layer, cx, y, t, t0, dur=0.5, slide=40, out_t=None, out_dur=0.35, scale_from=1.0, anchor='top'):
    p = ease((t - t0) / dur) if dur > 0 else (1.0 if t >= t0 else 0.0)
    if out_t is not None: p *= 1 - ease((t - out_t) / out_dur)
    if p <= 0.001: return
    l = layer
    if scale_from != 1.0:
        s = scale_from + (1 - scale_from) * p
        l = layer.resize((max(1, int(layer.size[0] * s)), max(1, int(layer.size[1] * s))), Image.LANCZOS)
    l = fade(l, p)
    yy = y - (l.size[1] / 2 if anchor == 'mid' else 0)
    frame.alpha_composite(l, (int(cx - l.size[0] / 2), int(yy + (1 - p) * slide + (layer.size[1] - l.size[1]) / 2 * (anchor == 'top'))))

def gradient(w, h, c1, c2, vertical=True):
    a = np.linspace(0, 1, h if vertical else w)[:, None] if vertical else np.linspace(0, 1, w)[None, :]
    arr = np.array(c1)[None, None, :] * (1 - a[..., None]) + np.array(c2)[None, None, :] * a[..., None]
    arr = np.broadcast_to(arr, (h, w, 3)).astype(np.uint8)
    return Image.fromarray(arr, 'RGB').convert('RGBA')

def vignette(w, h, strength=0.6, color=(0, 0, 0)):
    y, x = np.ogrid[:h, :w]
    r = np.sqrt(((x - w / 2) / (w / 2)) ** 2 + ((y - h / 2) / (h / 2)) ** 2)
    a = (np.clip((r - 0.55) / 0.9, 0, 1) ** 1.5 * 255 * strength).astype(np.uint8)
    v = Image.new('RGBA', (w, h), color + (0,)); v.putalpha(Image.fromarray(a, 'L')); return v

# ---------------- audio ----------------
def env_adsr(n, a, d, s, r, sr=SR):
    a, d, r = int(a * sr), int(d * sr), int(r * sr)
    e = np.ones(n) * s
    e[:min(a, n)] = np.linspace(0, 1, min(a, n))
    if a < n: e[a:min(a + d, n)] = np.linspace(1, s, min(a + d, n) - a)
    if r and n > r: e[-r:] *= np.linspace(1, 0, r)
    return e

def midi(m): return 440.0 * 2 ** ((m - 69) / 12)

def osc(freq, dur, kind='sine', detune=0.0):
    t = np.arange(int(dur * SR)) / SR
    ph = 2 * np.pi * freq * t
    if kind == 'sine': return np.sin(ph)
    if kind == 'saw':
        out = np.zeros_like(t)
        for k in range(1, 18): out += (-1) ** (k + 1) * np.sin(k * ph) / k
        return out * 0.6
    if kind == 'tri': return 2 / np.pi * np.arcsin(np.sin(ph))
    if kind == 'square': return np.sign(np.sin(ph)) * 0.5

def lowpass(x, cutoff):
    from scipy.signal import butter, lfilter
    b, a = butter(2, cutoff / (SR / 2)); return lfilter(b, a, x)

def highpass(x, cutoff):
    from scipy.signal import butter, lfilter
    b, a = butter(2, cutoff / (SR / 2), 'high'); return lfilter(b, a, x)

def reverb(x, wet=0.3, decay=1.8):
    from scipy.signal import fftconvolve
    n = int(decay * SR); ir = np.random.randn(n) * np.exp(-np.linspace(0, 7, n)); ir = lowpass(ir, 5000)
    ir /= np.abs(ir).sum() ** 0.5 * 4
    y = fftconvolve(x, ir)[:len(x)]
    return x * (1 - wet) + y * wet * 3

def pluck(freq, dur, decay=0.996):
    n = int(dur * SR); N = max(2, int(SR / freq))
    buf = np.random.uniform(-1, 1, N); out = np.zeros(n)
    for i in range(n):
        out[i] = buf[i % N]
        buf[i % N] = decay * 0.5 * (buf[i % N] + buf[(i + 1) % N])
    return out

class Mix:
    def __init__(self, dur): self.buf = np.zeros((int(dur * SR) + SR, 2))
    def add(self, sig, t, gain=1.0, pan=0.0):
        if sig.ndim == 1: sig = np.stack([sig * (1 - max(0, pan)), sig * (1 + min(0, pan))], 1)
        i = int(t * SR); j = min(len(self.buf), i + len(sig))
        if j > i: self.buf[i:j] += sig[:j - i] * gain
    def write(self, path, dur, fade_out=1.5):
        b = self.buf[:int(dur * SR)].copy()
        f = int(fade_out * SR); b[-f:] *= np.linspace(1, 0, f)[:, None]
        b /= max(1e-9, np.abs(b).max()) / 0.89
        with wave.open(path, 'wb') as w:
            w.setnchannels(2); w.setsampwidth(2); w.setframerate(SR)
            w.writeframes((b * 32767).astype(np.int16).tobytes())

def noise(dur): return np.random.uniform(-1, 1, int(dur * SR))

def whoosh(dur=0.6, up=True):
    n = noise(dur); t = np.linspace(0, 1, len(n))
    e = np.sin(np.pi * t) ** 2
    # crude band sweep: mix of smoothed noise at varying smoothness
    k = np.convolve(n, np.ones(8) / 8, 'same'); k2 = n - np.convolve(n, np.ones(40) / 40, 'same')
    sweep = t if up else 1 - t
    return (k * (1 - sweep) + k2 * sweep) * e * 0.5

def tick(): s = noise(0.03) * np.exp(-np.linspace(0, 12, int(0.03 * SR))); return s - np.convolve(s, np.ones(6) / 6, 'same')
def kick():
    t = np.arange(int(0.35 * SR)) / SR; f = 50 + 90 * np.exp(-t * 30)
    return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-t * 9)
def hat(dur=0.05): s = noise(dur); s = s - np.convolve(s, np.ones(3) / 3, 'same'); return s * np.exp(-np.linspace(0, 9, len(s)))
def chime(m, dur=2.5):
    t = np.arange(int(dur * SR)) / SR; f = midi(m)
    return (np.sin(2 * np.pi * f * t) + 0.4 * np.sin(2 * np.pi * f * 2.76 * t) * np.exp(-t * 4) + 0.2 * np.sin(2 * np.pi * f * 5.4 * t) * np.exp(-t * 8)) * np.exp(-t * 2.2)
def pad(ms, dur, kind='saw', cutoff=900, a=1.2, r=1.5, gain=0.15):
    n = int(dur * SR); s = np.zeros(n)
    for m in ms:
        for dt in (-0.08, 0.0, 0.08):
            s += osc(midi(m + dt), dur, kind)[:n]
    s = lowpass(s / (len(ms) * 3), cutoff)
    return s * env_adsr(n, a, 0.2, 1.0, r) * gain

def render(name, draw_fn, dur, audio_fn, preview_ts=()):
    import glob, shutil
    tmp = os.path.join(S, 'frames_' + name)
    shutil.rmtree(tmp, ignore_errors=True); os.makedirs(tmp)
    for i in range(int(dur * FPS)):
        fr = draw_fn(i / FPS)
        fr.convert('RGB').save(os.path.join(tmp, '%05d.jpg' % i), quality=93)
    wav = os.path.join(S, name + '.wav'); audio_fn().write(wav, dur)
    subprocess.run(['ffmpeg', '-y', '-loglevel', 'error', '-framerate', str(FPS), '-i', os.path.join(tmp, '%05d.jpg'), '-i', wav,
                    '-c:v', 'libx264', '-pix_fmt', 'yuv420p', '-crf', '19', '-preset', 'medium', '-c:a', 'aac', '-b:a', '192k',
                    '-shortest', '-movflags', '+faststart', os.path.join(OUT, name + '.mp4')], check=True)

def preview(draw_fn, ts, path, scale=3):
    ims = [draw_fn(t).convert('RGB').resize((W // scale, H // scale)) for t in ts]
    cols = min(5, len(ims)); rows = (len(ims) + cols - 1) // cols
    sheet = Image.new('RGB', (cols * (W // scale + 8), rows * (H // scale + 8)), 'white')
    for i, im in enumerate(ims): sheet.paste(im, ((i % cols) * (W // scale + 8), (i // cols) * (H // scale + 8)))
    sheet.save(path)
