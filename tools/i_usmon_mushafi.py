import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

DUR = 22.0
EM1 = (6, 40, 32); EM2 = (14, 78, 60); GOLD = (232, 190, 96); CREAM = (246, 236, 210); MINT = (150, 210, 180)
BG = gradient(W, H, EM1, EM2)
_g = Image.new('RGBA', (W, H), (0, 0, 0, 0)); _d = ImageDraw.Draw(_g)
for y in range(-200, H + 200, 160):  # faint diamond lattice
    for x in range(-200, W + 200, 160):
        o = 80 if (y // 160) % 2 else 0
        _d.polygon([(x + o, y - 70), (x + o + 70, y), (x + o, y + 70), (x + o - 70, y)], outline=GOLD + (22,), width=2)
BG.alpha_composite(_g); BG.alpha_composite(vignette(W, H, 0.7, (0, 12, 8)))

def glow(t):
    l = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    for k in range(8):
        a = math.radians(-90 + (k - 3.5) * 9 + 3 * math.sin(t * 0.6 + k))
        d.polygon([(W / 2, -100), (W / 2 + 2200 * math.cos(a - 0.03), -100 - 2200 * math.sin(-a + 0.03) * -1), (W / 2 + 2200 * math.cos(a + 0.03), -100 + 2200 * math.sin(a + 0.03) * -1)], fill=GOLD + (10,))
    return l.filter(ImageFilter.GaussianBlur(12))
GLOWS = [glow(i * 0.5) for i in range(12)]

def page(p):
    # parchment page with kufic-like strokes, revealed line by line
    w, h = 760, 520
    l = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    d.rounded_rectangle((0, 0, w - 1, h - 1), radius=10, fill=(222, 200, 156, 255), outline=GOLD, width=4)
    rs = random.Random(7)
    for row in range(6):
        if row / 6 > p: break
        y = 70 + row * 70; x = w - 60
        while x > 70:
            seg = rs.randint(40, 120); d.line((x - seg, y, x, y), fill=(60, 36, 20), width=9)
            if rs.random() < 0.6: d.line((x - 4, y, x - 4, y - rs.randint(20, 42)), fill=(60, 36, 20), width=8)
            if rs.random() < 0.25: d.ellipse((x - seg / 2 - 6, y - 30, x - seg / 2 + 6, y - 18), fill=(150, 30, 30))
            x -= seg + rs.randint(18, 34)
    return l

STOPS = [('Madina', 'VII asr', (240, 1260)), ('Samarqand', 'Amir Temur davri', (700, 1010)), ('Sankt-Peterburg', '1869', (300, 500)), ('Toshkent', '1924', (840, 750))]

def draw(t):
    fr = BG.copy(); fr.alpha_composite(GLOWS[int(t * 2) % 12])
    PB = lambda s: font('PlayfairBlack', s); PBo = lambda s: font('PlayfairBold', s); CI = lambda s: font('CormorantItalic', s); C = lambda s: font('Cormorant', s); G = lambda s: font('GroteskMed', s)

    if t < 4.2:
        put(fr, text_layer('Toshkentda', CI(96), MINT), W / 2, 430, t, -1)
        put(fr, text_layer('eng qadimgi Qur\'on qo\'lyozmalaridan biri saqlanadi.', PB(92), CREAM, maxw=W - 140), W / 2, 550, t, -1)
        put(fr, text_layer('Uning yo\'li 1300 yildan oshadi.', G(56), GOLD, maxw=W - 180), W / 2, 1080, t, 1.0, dur=0.35, out_t=3.9)

    if 4.2 <= t < 8.4:
        put(fr, text_layer('"Usmon Mushafi"', PB(112), GOLD), W / 2, 380, t, 4.25, dur=0.35, slide=0, scale_from=1.2, out_t=8.1)
        put(fr, page(clamp((t - 4.6) / 2.0)), W / 2, 600, t, 4.5, dur=0.3, slide=30, out_t=8.1)
        put(fr, text_layer('Teriga, kufiy xatida yozilgan katta hajmli mushaf', C(60), CREAM, maxw=W - 180), W / 2, 1180, t, 5.2, out_t=8.1)

    if 8.4 <= t < 14.6:
        put(fr, text_layer('Uning yo\'li', CI(80), MINT), W / 2, 330, t, 8.45, dur=0.3, out_t=14.3)
        d = ImageDraw.Draw(fr); k = 1 - ease((t - 14.3) / 0.3)
        for i in range(len(STOPS)):
            t0 = 8.7 + i * 1.3
            if t < t0: break
            (n, yr, (x, y)) = STOPS[i]; q = ease((t - t0) / 0.4) * k
            if i:
                px, py = STOPS[i - 1][2]; pp = ease((t - t0 + 0.3) / 0.6)
                for s in range(0, 40):
                    if s / 40 > pp: break
                    if s % 2 == 0:
                        x1 = px + (x - px) * s / 40; y1 = py + (y - py) * s / 40; x2 = px + (x - px) * (s + 1) / 40; y2 = py + (y - py) * (s + 1) / 40
                        d.line((x1, y1, x2, y2), fill=GOLD + (int(220 * k),), width=5)
            r = 18 + 6 * math.sin(t * 5) if i == len(STOPS) - 1 else 16
            d.ellipse((x - r, y - r, x + r, y + r), fill=GOLD + (int(255 * q),))
            la = text_layer(n, PBo(58), CREAM); lb = text_layer(yr, G(40), MINT)
            ox = -la.size[0] - 30 if x > W / 2 else 30
            fr.alpha_composite(fade(la, q), (int(x + ox), int(y - 60))); fr.alpha_composite(fade(lb, q), (int(x + ox + (la.size[0] - lb.size[0] if x > W / 2 else 0)), int(y + 8)))
        put(fr, text_layer('1869-yilda Rossiyaga olib ketildi, 1924-yilda Toshkentga qaytarildi.', G(48), CREAM, maxw=W - 200), W / 2, 1430, t, 11.4, out_t=14.3)

    if 14.6 <= t < 18.4:
        put(fr, text_layer('1997-yil', PB(150), GOLD), W / 2, 450, t, 14.65, dur=0.3, slide=0, scale_from=1.25, out_t=18.1)
        put(fr, text_layer('YUNESKO "Jahon xotirasi" ro\'yxatiga kiritildi.', PBo(70), CREAM, maxw=W - 160), W / 2, 680, t, 15.0, dur=0.35, out_t=18.1)
        put(fr, text_layer('Bugun Hazrati Imom majmuasidagi Muyi Muborak kutubxonasida saqlanadi.', CI(62), MINT, maxw=W - 200), W / 2, 980, t, 15.8, out_t=18.1)

    if t >= 18.4:
        put(fr, text_layer('Siz uni borib ko\'rganmisiz?', PB(84), CREAM, maxw=W - 160), W / 2, 420, t, 18.45, dur=0.35)
        put(fr, text_layer('BookNote kitobxonlari 10 baho bergan:', G(46), MINT, maxw=W - 100), W / 2, 680, t, 18.9)
        for i, b in enumerate(['Xatmi Qur\'onga marhabo', 'Allohning Qur\'ondagi mo\'jizalari']):
            put(fr, text_layer(b, CI(66), GOLD, maxw=W - 160), W / 2, 790 + i * 100, t, 19.2 + i * 0.3)
        pl = Image.new('RGBA', (620, 136), (0, 0, 0, 0)); d = ImageDraw.Draw(pl)
        d.rounded_rectangle((0, 0, 619, 135), radius=68, fill=GOLD); s = 'booknote.uz'
        d.text(((620 - tw(s, PB(70))) / 2, 20), s, font=PB(70), fill=EM1)
        put(fr, pl, W / 2, 1080, t, 19.9, dur=0.3, slide=0, scale_from=0.8)

    d = ImageDraw.Draw(fr); d.text((70, 100), 'BookNote', font=font('PlayfairBold', 42), fill=CREAM)
    d.rectangle((0, 0, W * t / DUR, 8), fill=GOLD)
    return fr

def ney(m_, dur):
    n = int(dur * SR); tt = np.arange(n) / SR; f = midi(m_) * (1 + 0.006 * np.sin(2 * np.pi * 5 * tt) * np.clip(tt - 0.3, 0, 1))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) + 0.3 * np.sin(4 * np.pi * np.cumsum(f) / SR)
    s += lowpass(noise(dur), 2500)[:n] * 0.25
    return s * env_adsr(n, 0.25, 0.2, 0.8, 0.5)

def audio():
    m = Mix(DUR)
    m.add(reverb(pad([38, 45, 50], DUR + 1, 'tri', 500, a=0.05, r=3.0, gain=0.45), 0.35), 0)
    # Rast-ish ney phrases on D
    ph = [(62, 1.2), (64, 0.6), (65, 0.6), (67, 1.6), (65, 0.8), (64, 0.8), (62, 2.0)]
    for st in (0.3, 8.5, 15.0):
        tt = st
        for n, dd in ph: m.add(reverb(ney(n + 12, dd + 0.3), 0.5, 2.6), tt, 0.13); tt += dd
    beat = 60 / 90
    tt = 4.2
    while tt < DUR - 1.5:
        m.add(lowpass(kick(), 200), tt, 0.4); m.add(tick(), tt + beat / 2, 0.12); m.add(tick(), tt + beat * 0.75, 0.08)
        tt += beat
    for tt in (0.0, 4.25, 14.65, 18.45): m.add(reverb(lowpass(kick(), 120), 0.4, 2.5), tt, 0.8)
    for i in range(4): m.add(reverb(chime(74 + [0, 3, 5, 7][i], 1.6), 0.4), 8.7 + i * 1.3, 0.12)
    m.add(reverb(chime(86, 3.0), 0.5), 19.9, 0.2)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [0.0, 6.5, 13.8, 17.0, 21.0], os.path.join(S, 'prevI.png'))
    else:
        render('I_usmon_mushafi_toshkent', draw, DUR, audio); print('done I')
