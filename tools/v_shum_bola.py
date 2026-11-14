import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

# Style: dusk blue (loss) that turns into warm paper-cutout mahalla (laughter); music box -> playful pizzicato.
DUR = 22.0
DUSK1 = (18, 26, 52); DUSK2 = (52, 64, 104)
SUN1 = (255, 196, 110); SUN2 = (246, 120, 74)
INK = (40, 24, 30); CREAM = (255, 246, 228); BLUE = (40, 80, 160); KITE = (226, 48, 60); PALE = (190, 200, 230)

BG_SAD = gradient(W, H, DUSK1, DUSK2); BG_SAD.alpha_composite(vignette(W, H, 0.6))
def _warm():
    bg = gradient(W, H, SUN1, SUN2); d = ImageDraw.Draw(bg)
    # paper-cut rooftops of a mahalla
    base = H - 360
    xs = [0, 150, 330, 470, 650, 820, 960, W]
    for i in range(len(xs) - 1):
        x0, x1 = xs[i], xs[i + 1]; h = 120 + 70 * ((i * 37) % 3)
        d.rectangle((x0, base - h, x1, H), fill=(120, 54, 40, 255))
        d.rectangle((x0 + 30, base - h + 40, x0 + 70, base - h + 90), fill=(255, 210, 120, 255))
    d.rectangle((0, base, W, H), fill=(90, 38, 30, 255))
    # tut daraxti (mulberry tree)
    d.rectangle((860, base - 300, 890, base), fill=(70, 40, 30, 255)); d.ellipse((760, base - 470, 1000, base - 250), fill=(70, 110, 50, 255))
    return bg
BG_WARM = _warm()

def kite(fr, t):
    x = 250 + 60 * math.sin(t * 0.9); y = 1180 + 40 * math.sin(t * 1.7)
    l = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    d.polygon([(x, y - 80), (x + 60, y), (x, y + 90), (x - 60, y)], fill=KITE + (255,), outline=CREAM + (255,))
    d.line((x, y - 80, x, y + 90), fill=CREAM + (255,), width=3); d.line((x - 60, y, x + 60, y), fill=CREAM + (255,), width=3)
    pts = [(x + k * 14, y + 90 + k * 30 + 12 * math.sin(t * 4 + k)) for k in range(8)]
    d.line(pts, fill=CREAM + (255,), width=3)
    d.line((x, y + 90, 520, H - 360), fill=(255, 255, 255, 140), width=2)
    fr.alpha_composite(l)

def card(fr, y0, y1, a=235):
    o = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(o).rounded_rectangle((60, y0, W - 60, y1), 28, fill=CREAM + (a,))
    fr.alpha_composite(o)

def draw(t):
    PB = lambda s: font('PlayfairBlack', s); PBo = lambda s: font('PlayfairBold', s); PI = lambda s: font('PlayfairItalic', s); G = lambda s: font('GroteskMed', s); IN = lambda s: font('Instrument', s); INI = lambda s: font('InstrumentItalic', s)
    if t < 4.4:
        fr = BG_SAD.copy()
        put(fr, text_layer('Bolaligida avval otasidan, keyin onasidan ayrildi.', PB(96), CREAM, maxw=W - 100), W / 2, 340, t, -1)
        put(fr, text_layer('Keyin o\'z bolaligini eng kulgili qissaga aylantirdi.', PI(66), PALE, maxw=W - 160), W / 2, 900, t, 1.4, dur=0.6)
    else:
        fr = BG_SAD.copy()
        p = clamp((t - 4.4) / 0.8)
        if p < 1: fr = Image.blend(BG_SAD, BG_WARM, ease_io(p))
        else: fr = BG_WARM.copy()
        kite(fr, t)

    if 4.4 <= t < 9.0:
        card(fr, 300, 980)
        put(fr, text_layer('G\'afur G\'ulom', PB(100), INK), W / 2, 360, t, 4.6, dur=0.3, out_t=8.7)
        put(fr, text_layer('"SHUM BOLA"', G(88), KITE), W / 2, 520, t, 5.0, dur=0.3, slide=0, scale_from=1.3, out_t=8.7)
        put(fr, text_layer('1936-yilda yozilgan qissa', INI(60), BLUE, maxw=W - 200), W / 2, 700, t, 5.7, out_t=8.7)

    if 9.0 <= t < 14.0:
        card(fr, 300, 1040)
        put(fr, text_layer('Qahramoni - ochlik va yetimlik ichida ham hazilini yo\'qotmagan sho\'x bola.', PBo(70), INK, maxw=W - 200), W / 2, 350, t, 9.05, dur=0.3, out_t=13.7)
        put(fr, text_layer('Sahifalarida muallifning o\'z bolaligi bor.', INI(60), BLUE, maxw=W - 200), W / 2, 830, t, 10.6, out_t=13.7)

    if 14.0 <= t < 18.4:
        card(fr, 300, 960)
        put(fr, text_layer('1977-yilda qissa asosida film suratga olindi.', PBo(72), INK, maxw=W - 200), W / 2, 350, t, 14.05, dur=0.3, out_t=18.1)
        put(fr, text_layer('Kulgi ba\'zan yo\'qotishga eng kuchli javob.', INI(62), KITE, maxw=W - 200), W / 2, 680, t, 15.4, out_t=18.1)

    if t >= 18.4:
        card(fr, 300, 1060)
        put(fr, text_layer('"Shum bola"ning qaysi sahnasi esingizda?', PBo(74), INK, maxw=W - 200), W / 2, 350, t, 18.45, dur=0.3)
        put(fr, text_layer('Kommentda yozing.', INI(60), BLUE), W / 2, 620, t, 19.0)
        pl = Image.new('RGBA', (620, 136), (0, 0, 0, 0)); d = ImageDraw.Draw(pl)
        d.rounded_rectangle((0, 0, 619, 135), 24, fill=KITE); s = 'booknote.uz'
        d.text(((620 - tw(s, PB(70))) / 2, 20), s, font=PB(70), fill=CREAM)
        put(fr, pl, W / 2, 790, t, 19.5, dur=0.3, slide=0, scale_from=0.8)

    d = ImageDraw.Draw(fr); d.text((70, 100), 'BookNote', font=font('PlayfairBold', 42), fill=CREAM if t < 4.8 else INK)
    d.rectangle((0, 0, W * t / DUR, 8), fill=KITE)
    return fr

def musicbox(m_, dur=1.6):
    t = np.arange(int(dur * SR)) / SR; f = midi(m_)
    return (np.sin(2 * np.pi * f * t) + 0.3 * np.sin(2 * np.pi * f * 4 * t) * np.exp(-t * 6)) * np.exp(-t * 3)

def pizz(m_, dur=0.35):
    return pluck(midi(m_), dur, 0.990)

def clar(m_, dur):
    n = int(dur * SR); s = osc(midi(m_), dur, 'square')[:n]
    return lowpass(s, 1800) * env_adsr(n, 0.03, 0.05, 0.8, 0.08)

def audio():
    m = Mix(DUR)
    # sad music box in A minor (0 - 4.4 s)
    for i, n in enumerate([76, 72, 69, 71, 72, 69, 64, 68]):
        m.add(reverb(musicbox(n), 0.5, 2.5), 0.1 + i * 0.5, 0.25)
    m.add(reverb(pad([57, 60, 64], 5.0, 'sine', 600, a=0.5, r=1.5, gain=0.3), 0.5, 2.5), 0)
    m.add(reverb(whoosh(0.8), 0.3), 3.9, 0.25)
    # playful section, C major, 112 bpm
    b = 60 / 112; t0 = 4.4
    bass = [48, 55, 53, 55, 45, 52, 50, 55]
    tt = t0; k = 0
    while tt < DUR - 1.2:
        bn = bass[(k // 2) % len(bass)]
        m.add(pizz(bn, 0.4), tt, 0.5, -0.2)
        m.add(pizz(bn + 12 + (4 if k % 2 else 7), 0.25), tt + b / 2, 0.25, 0.2)
        m.add(hat(), tt + b / 2, 0.08, 0.4)
        if k % 4 == 0: m.add(lowpass(kick(), 150), tt, 0.35)
        tt += b; k += 1
    tune = [(72, .5), (74, .5), (76, 1), (79, .5), (76, .5), (74, 1), (72, .5), (74, .5), (76, .5), (72, .5), (69, 1.5), (0, .5),
            (77, .5), (76, .5), (74, 1), (72, .5), (74, .5), (76, 1), (79, 1), (77, .5), (76, .5), (74, 2)]
    tt = t0 + 2 * b
    for n, dd in tune:
        if tt > DUR - 2: break
        if n: m.add(reverb(clar(n, dd * b * 0.9), 0.2, 1.2), tt, 0.13, 0.1)
        tt += dd * b
    m.add(reverb(chime(84, 2.0), 0.5), 5.0, 0.12)
    m.add(reverb(chime(79, 3.0), 0.5), 19.5, 0.12)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [0.0, 2.5, 8.0, 12.8, 17.5, 21.0], os.path.join(S, 'prevV.png'))
    else:
        render('V_shum_bola_gafur_gulom', draw, DUR, audio); print('done V')
