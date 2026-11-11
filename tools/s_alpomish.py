import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

DUR = 22.0
NIGHT1 = (10, 14, 30); NIGHT2 = (60, 30, 40); MOON = (255, 232, 190); RED = (214, 58, 44); GOLD = (246, 190, 80); CREAM = (252, 240, 220); STEP = (20, 14, 18)

def _bg():
    bg = gradient(W, H, NIGHT1, NIGHT2); d = ImageDraw.Draw(bg)
    d.ellipse((600, H - 760, 960, H - 400), fill=MOON + (255,))
    d.ellipse((600, H - 760, 960, H - 400), outline=(255, 210, 150, 255), width=6)
    pts = [(0, H)] + [(x, H - 420 + 40 * math.sin(x / 220) + 18 * math.sin(x / 61)) for x in range(0, W + 20, 20)] + [(W, H)]
    d.polygon(pts, fill=STEP + (255,))
    # yurt silhouette
    d.rectangle((140, H - 520, 330, H - 420), fill=STEP + (255,)); d.pieslice((130, H - 600, 340, H - 440), 180, 360, fill=STEP + (255,))
    return bg
BG = _bg()

def bow(size, draw_p):
    l = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(l); c = size / 2
    d.arc((c - size * 0.42, c - size * 0.45, c + size * 0.1, c + size * 0.45), 270, 90, fill=GOLD, width=12)
    sx = c - size * 0.16 + size * 0.22 * (1 - draw_p) * 0 - size * 0.18 * draw_p
    d.line((c - size * 0.16, c - size * 0.45, sx, c), fill=CREAM, width=3); d.line((sx, c, c - size * 0.16, c + size * 0.45), fill=CREAM, width=3)
    d.line((sx, c, sx + size * 0.62, c), fill=CREAM, width=5); d.polygon([(sx + size * 0.62, c - 14), (sx + size * 0.68, c), (sx + size * 0.62, c + 14)], fill=RED)
    return l

def draw(t):
    fr = BG.copy()
    PB = lambda s: font('PlayfairBlack', s); PBo = lambda s: font('PlayfairBold', s); PI = lambda s: font('PlayfairItalic', s); G = lambda s: font('GroteskMed', s); MB = lambda s: font('MonoBold', s)

    if t < 4.4:
        put(fr, text_layer('Bu doston', PI(76), GOLD), W / 2, 330, t, -1)
        put(fr, text_layer('ming yil davomida qog\'ozga yozilmagan.', PB(92), CREAM, maxw=W - 110), W / 2, 430, t, -1)
        put(fr, text_layer('Baxshilar uni yoddan aytib kelgan.', PBo(66), GOLD, maxw=W - 160), W / 2, 830, t, -1)

    if 4.4 <= t < 8.8:
        put(fr, text_layer('"ALPOMISH"', PB(130), RED, maxw=W - 60), W / 2, 340, t, 4.45, dur=0.3, slide=0, scale_from=1.3, out_t=8.5)
        put(fr, text_layer('Qo\'ng\'irot elining botiri, uning oti Boychibor va sevgilisi Barchinoy haqida.', PI(60), CREAM, maxw=W - 180), W / 2, 580, t, 5.1, out_t=8.5)

    if 8.8 <= t < 13.6:
        p = clamp((t - 9.0) / 1.2)
        if t < 11.2: put(fr, bow(560, ease(p)), W / 2, 300, t, 8.85, dur=0.3, slide=0, out_t=13.3)
        else:
            d = ImageDraw.Draw(fr); x = W / 2 + (t - 11.2) * 2200
            if x < W + 300: d.line((x - 360, 580, x, 580), fill=CREAM, width=5); d.polygon([(x, 566), (x + 40, 580), (x, 594)], fill=RED)
        put(fr, text_layer('Doston bir avloddan ikkinchisiga og\'zaki o\'tib keldi.', PBo(66), CREAM, maxw=W - 160), W / 2, 890, t, 9.6, out_t=13.3)
        put(fr, text_layer('1928-yilda baxshi Fozil Yo\'ldosh o\'g\'lidan yozib olindi.', G(52), GOLD, maxw=W - 180), W / 2, 1070, t, 10.8, out_t=13.3)

    if 13.6 <= t < 18.2:
        put(fr, text_layer('1999', MB(220), GOLD), W / 2, 330, t, 13.65, dur=0.3, slide=0, scale_from=1.3, out_t=17.9)
        put(fr, text_layer('YUNESKO bilan "Alpomish"ning 1000 yilligi nishonlandi.', PBo(68), CREAM, maxw=W - 160), W / 2, 620, t, 14.2, out_t=17.9)

    if t >= 18.2:
        put(fr, text_layer('Bolaligingizda "Alpomish"ni kim aytib bergan?', PB(80), CREAM, maxw=W - 140), W / 2, 330, t, 18.25, dur=0.3)
        put(fr, text_layer('Kommentda yozing.', PI(62), GOLD), W / 2, 700, t, 18.7)
        pl = Image.new('RGBA', (620, 136), (0, 0, 0, 0)); d = ImageDraw.Draw(pl)
        d.rectangle((0, 0, 619, 135), fill=RED); s = 'booknote.uz'
        d.text(((620 - tw(s, PB(70))) / 2, 20), s, font=PB(70), fill=CREAM)
        put(fr, pl, W / 2, 840, t, 19.3, dur=0.3, slide=0, scale_from=0.8)

    d = ImageDraw.Draw(fr); d.text((70, 100), 'BookNote', font=font('PlayfairBold', 42), fill=CREAM)
    d.rectangle((0, 0, W * t / DUR, 8), fill=RED)
    return fr

def dombira(m_, dur=0.35):
    return highpass(pluck(midi(m_), dur, 0.994) + 0.6 * pluck(midi(m_ + 5), dur, 0.994), 150)

def audio():
    m = Mix(DUR)
    # throat-like drone: low saw through 'o' formant
    n = int((DUR + 1) * SR); s = osc(midi(38), DUR + 1, 'saw')[:n]
    dr = highpass(lowpass(s, 600), 300) + lowpass(s, 250) * 0.6 + highpass(lowpass(s, 2600), 2200) * 0.25 * (0.5 + 0.5 * np.sin(np.linspace(0, 30, n)))
    m.add(dr * env_adsr(n, 0.05, 0.2, 0.9, 2.0), 0, 0.22)
    # dombira gallop: strum pattern long-short-short at 132 bpm (horse rhythm)
    b = 60 / 132; tt = 0.0; i = 0
    tune = [50, 50, 53, 50, 48, 50, 55, 53]
    while tt < DUR - 1:
        root = tune[(i // 4) % 8] if tt > 4.4 else 50
        for k, off in enumerate((0, b * 0.5, b * 0.75)):
            m.add(dombira(root + (12 if k == 0 else 7)), tt + off, 0.2 if k == 0 else 0.12, pan=-0.15)
        tt += b; i += 1
    for tt in (0.0, 4.45, 13.65, 18.25): m.add(reverb(lowpass(kick(), 100), 0.45, 2.6), tt, 0.85)
    m.add(highpass(noise(0.4) * np.exp(-np.linspace(0, 6, int(0.4 * SR))), 1500), 11.2, 0.4)  # arrow release
    m.add(whoosh(0.5, True), 11.2, 0.5)
    for tt in (8.5, 13.3, 17.9): m.add(whoosh(0.5, True), tt, 0.25)
    m.add(reverb(chime(86, 3.0), 0.5), 19.3, 0.18)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [0.0, 7.6, 10.3, 16.8, 21.0], os.path.join(S, 'prevS.png'))
    else:
        render('S_alpomish_ming_yil', draw, DUR, audio); print('done S')
