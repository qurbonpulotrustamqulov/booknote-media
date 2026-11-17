import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

# Style: saffron/ochre paper, black ink brush strokes, a winding road drawn as he wanders; ghijjak (bowed) + doira.
DUR = 22.0
SAF1 = (238, 196, 120); SAF2 = (206, 138, 60); INK = (28, 20, 16); RUST = (150, 40, 24); PAPER = (252, 238, 206)

BG = gradient(W, H, SAF1, SAF2)
_g = Image.fromarray((np.random.RandomState(4).rand(H, W) * 30).astype(np.uint8)).convert('RGBA'); _g.putalpha(40); BG.alpha_composite(_g)
BG.alpha_composite(vignette(W, H, 0.5, (90, 40, 10)))

ROAD = [(W * (0.5 + 0.32 * math.sin(k / 9.0)), H - 80 - k * 14) for k in range(56)]
CITIES = [(8, 'Namangan'), (26, 'Qashqar'), (44, 'Turkiston'), (62, 'Balx')]

def road(fr, p):
    n = max(2, int(len(ROAD) * clamp(p)))
    d = ImageDraw.Draw(fr)
    for i in range(n - 1):
        w = 10 + 4 * math.sin(i * 1.3)
        d.line((ROAD[i], ROAD[i + 1]), fill=INK + (90,), width=int(w))
    x, y = ROAD[n - 1]; d.ellipse((x - 12, y - 12, x + 12, y + 12), fill=RUST + (255,))

def brush(d, x0, y, x1, h=60, a=200):
    for k in range(6):
        d.line((x0 + k * 3, y + k * h / 6, x1 - k * 5, y + k * h / 6 + 4 * math.sin(k)), fill=INK + (a,), width=int(h / 6) + 2)

def draw(t):
    fr = BG.copy()
    PB = lambda s: font('PlayfairBlack', s); PBo = lambda s: font('PlayfairBold', s); PI = lambda s: font('PlayfairItalic', s); G = lambda s: font('GroteskMed', s); CI = lambda s: font('CormorantItalic', s)
    road(fr, 0.15 + t / 18)

    if t < 4.4:
        put(fr, text_layer('U butun umr yo\'lda yurdi.', PI(78), RUST, maxw=W - 120), W / 2, 330, t, -1)
        put(fr, text_layer('Haq gapi uchun dorga osildi.', PB(104), INK, maxw=W - 100), W / 2, 450, t, -1)

    if 4.4 <= t < 9.6:
        l = Image.new('RGBA', (W, H), (0, 0, 0, 0)); brush(ImageDraw.Draw(l), 120, 330, int(120 + 840 * ease((t - 4.4) / 0.5)), 150, 230)
        fr.alpha_composite(l)
        put(fr, text_layer('Boborahim Mashrab', PB(74), PAPER, maxw=W - 140), W / 2, 345, t, 4.6, dur=0.3, out_t=9.3)
        put(fr, text_layer('1640, Namangan', G(54), INK), W / 2, 540, t, 5.1, out_t=9.3)
        put(fr, text_layer('Darvesh shoir. Qashqar, Turkiston, Balx... shahardan shaharga piyoda kezdi.', PI(64), INK, maxw=W - 180), W / 2, 660, t, 5.8, out_t=9.3)

    if 9.6 <= t < 14.4:
        put(fr, text_layer('Hokimlarga ham, riyokor zohidlarga ham to\'g\'risini aytdi.', PBo(74), INK, maxw=W - 140), W / 2, 340, t, 9.65, dur=0.3, out_t=14.1)
        put(fr, text_layer('1711-yil, Balx. Hokim Mahmud Qatag\'on uni qatl ettirdi.', PI(66), RUST, maxw=W - 170), W / 2, 700, t, 11.2, out_t=14.1)

    if 14.4 <= t < 18.6:
        put(fr, text_layer('Uni o\'ldirdilar. She\'rlari esa o\'lmadi.', PB(86), INK, maxw=W - 120), W / 2, 340, t, 14.45, dur=0.3, out_t=18.3)
        put(fr, text_layer('"Devoni Mashrab" uch asrdan beri qo\'ldan-qo\'lga o\'tib o\'qiladi.', PI(64), RUST, maxw=W - 170), W / 2, 720, t, 15.6, out_t=18.3)

    if t >= 18.6:
        put(fr, text_layer('Mashrabning qaysi satri yodingizda?', PBo(78), INK, maxw=W - 140), W / 2, 360, t, 18.65, dur=0.3)
        put(fr, text_layer('Kommentda yozing.', PI(60), RUST), W / 2, 610, t, 19.1)
        pl = Image.new('RGBA', (620, 136), (0, 0, 0, 0)); d = ImageDraw.Draw(pl)
        d.rectangle((0, 0, 619, 135), fill=INK); s = 'booknote.uz'
        d.text(((620 - tw(s, PB(70))) / 2, 20), s, font=PB(70), fill=SAF1)
        put(fr, pl, W / 2, 780, t, 19.6, dur=0.3, slide=0, scale_from=0.8)

    d = ImageDraw.Draw(fr); d.text((70, 100), 'BookNote', font=font('PlayfairBold', 42), fill=INK)
    d.rectangle((0, 0, W * t / DUR, 8), fill=RUST)
    return fr

def ghijjak(m_, dur):
    n = int(dur * SR); tt = np.arange(n) / SR
    f = midi(m_) * (1 + 0.008 * np.sin(2 * np.pi * 5.5 * tt) * np.clip(tt * 3 - 0.2, 0, 1))
    ph = np.cumsum(f) / SR; s = 2 * (ph % 1) - 1
    s = lowpass(s, 2200) + 0.05 * noise(dur)[:n]
    return s * env_adsr(n, 0.12, 0.2, 0.75, 0.25)

def doira(low=True):
    n = int(0.25 * SR); tt = np.arange(n) / SR
    s = (np.sin(2 * np.pi * (80 if low else 220) * tt) * np.exp(-tt * (10 if low else 25)))
    jing = highpass(noise(0.25)[:n], 5000) * np.exp(-tt * 18) * 0.5
    return s + jing

def audio():
    m = Mix(DUR)
    m.add(reverb(pad([43, 50], DUR + 1, 'saw', 350, a=0.6, r=3, gain=0.24), 0.4, 2.4), 0)
    # doira: aksak 7/8 (2+2+3), eighth = 0.21
    e = 0.21; tt = 0.0; k = 0; pat = [1, 0, 2, 0, 1, 0, 2]
    while tt < DUR - 1.5:
        v = pat[k % 7]
        if v == 1: m.add(doira(True), tt, 0.55, -0.1)
        elif v == 2: m.add(doira(False), tt, 0.3, 0.2)
        else: m.add(highpass(hat(), 3000), tt, 0.06)
        tt += e; k += 1
    # ghijjak melody, G segah-like (G Ab B C D Eb F#)
    sc = [55, 56, 59, 60, 62, 63, 66, 67]
    mel = [(4, 3), (3, 1), (2, 1), (1, 2), (0, 5), (2, 2), (3, 2), (4, 3), (5, 1), (4, 1), (3, 2), (2, 2), (1, 2), (0, 6), (4, 2), (6, 2), (7, 3), (6, 1), (5, 2), (4, 6)]
    tt = 0.3
    for ix, dd in mel:
        if tt > DUR - 2.2: break
        m.add(reverb(ghijjak(sc[ix], dd * e + 0.15), 0.35, 2.0), tt, 0.16, 0.1)
        tt += dd * e
    for tt in (4.4, 9.65, 14.45): m.add(reverb(whoosh(0.5), 0.3), tt - 0.3, 0.16)
    m.add(reverb(lowpass(kick(), 90), 0.6, 3.0), 11.2, 0.8)
    m.add(reverb(chime(79, 3.0), 0.6), 19.6, 0.12)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [0.0, 8.0, 13.0, 17.5, 21.0], os.path.join(S, 'prevX.png'))
    else:
        render('X_mashrab_balx_1711', draw, DUR, audio); print('done X')
