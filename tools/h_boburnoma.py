import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

DUR = 18.0
MAR = (92, 14, 26); MAR2 = (140, 28, 40); GOLD = (228, 180, 82); CREAM = (250, 236, 206); INK = (60, 24, 18); GREEN = (40, 110, 80); LAP = (36, 70, 140)

def _bg():
    bg = gradient(W, H, MAR2, MAR)
    d = ImageDraw.Draw(bg)
    # miniature frame: double gold border + corner rosettes + floral vine
    for m, w in ((34, 6), (52, 2), (W // 2 * 0 + 70, 2)):
        d.rectangle((m, m, W - m, H - m), outline=GOLD, width=w)
    for cx, cy in ((70, 70), (W - 70, 70), (70, H - 70), (W - 70, H - 70)):
        for k in range(8):
            a = math.radians(k * 45); d.ellipse((cx + 22 * math.cos(a) - 9, cy + 22 * math.sin(a) - 9, cx + 22 * math.cos(a) + 9, cy + 22 * math.sin(a) + 9), fill=GOLD)
        d.ellipse((cx - 10, cy - 10, cx + 10, cy + 10), fill=LAP)
    for y in range(140, H - 140, 70):
        for x in (43, W - 43):
            d.ellipse((x - 6, y - 6, x + 6, y + 6), fill=GOLD); d.ellipse((x - 3, y + 30, x + 3, y + 36), fill=CREAM)
    bg.alpha_composite(vignette(W, H, 0.5, (30, 0, 6)))
    return bg
BG = _bg()

def panel(h):
    p = Image.new('RGBA', (W - 200, h), (0, 0, 0, 0)); d = ImageDraw.Draw(p)
    d.rounded_rectangle((0, 0, W - 201, h - 1), radius=30, fill=CREAM + (250,), outline=GOLD, width=6)
    d.rounded_rectangle((16, 16, W - 217, h - 17), radius=22, outline=GOLD + (160,), width=2)
    return p

def cypress(h, p):
    l = Image.new('RGBA', (120, h), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    hh = int(h * ease(p)); d.ellipse((20, h - hh, 100, h), fill=GREEN); d.rectangle((54, h - 30, 66, h), fill=INK)
    return l

def draw(t):
    fr = BG.copy()
    PB = lambda s: font('PlayfairBlack', s); PBo = lambda s: font('PlayfairBold', s); PI = lambda s: font('PlayfairItalic', s); CB = lambda s: font('Cormorant', s); CI = lambda s: font('CormorantItalic', s); G = lambda s: font('GroteskMed', s)

    if t < 3.6:
        put(fr, text_layer('Bir podshoh', CI(92), GOLD), W / 2, 420, t, -1)
        put(fr, text_layer('kundalik yozgan.', PB(100), CREAM, maxw=W - 180), W / 2, 530, t, -1)
        put(fr, text_layer('O\'sha kitob 500 yildan beri o\'qiladi.', PBo(74), GOLD, maxw=W - 180), W / 2, 820, t, -1)
        put(fr, text_layer('Va u turkiy tilda, ona tilimizda yozilgan.', CI(70), CREAM, maxw=W - 180), W / 2, 1100, t, 1.2, dur=0.35, out_t=3.3)

    if 3.6 <= t < 7.6:
        put(fr, panel(620), W / 2, 420, t, 3.65, dur=0.3, slide=0, scale_from=0.95, out_t=7.3)
        put(fr, text_layer('Zahiriddin Muhammad Bobur', PB(80), INK, maxw=W - 300), W / 2, 470, t, 3.75, dur=0.3, out_t=7.3)
        put(fr, text_layer('1483-yil, Andijon', CI(66), MAR2), W / 2, 720, t, 4.1, out_t=7.3)
        put(fr, text_layer('12 yoshga to\'lmay Farg\'ona taxtiga o\'tirdi.', G(52), INK, maxw=W - 320), W / 2, 830, t, 4.6, out_t=7.3)
        put(fr, text_layer('1526-yilda Hindistonda Boburiylar saltanatiga asos soldi.', CB(66), CREAM, maxw=W - 200), W / 2, 1140, t, 5.4, out_t=7.3)

    if 7.6 <= t < 11.6:
        put(fr, text_layer('"Boburnoma"', PB(130), GOLD), W / 2, 380, t, 7.65, dur=0.3, slide=0, scale_from=1.2, out_t=11.3)
        items = ['Andijon va Samarqand', 'Hindiston mevalari va qushlari', 'janglar va do\'stlar', 'o\'z xatolari ham']
        for i, s in enumerate(items):
            row = Image.new('RGBA', (820, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(row)
            d.ellipse((10, 38, 44, 72), fill=GOLD); d.text((76, 18), s, font=CB(62), fill=CREAM)
            put(fr, row, W / 2, 620 + i * 130, t, 8.2 + i * 0.45, dur=0.3, slide=30, out_t=11.3)
        put(fr, text_layer('Hammasini yashirmay, ochiq yozgan.', CI(64), GOLD, maxw=W - 200), W / 2, 1200, t, 10.1, out_t=11.3)
        for i, x in enumerate((140, W - 260)):
            put(fr, cypress(300, clamp((t - 8.0 - i * 0.2) / 1.0)), x + 60, 1360, t, 7.9, dur=0.2, slide=0, out_t=11.3)

    if 11.6 <= t < 14.8:
        put(fr, text_layer('Tarjimalari', CI(80), GOLD), W / 2, 400, t, 11.65, dur=0.3, out_t=14.5)
        langs = [('forscha', '1589'), ('inglizcha', '1826'), ('nemischa', ''), ('fransuzcha', ''), ('ruscha', ''), ('turkcha', '')]
        for i, (a, b) in enumerate(langs):
            s = a + ('  ' + b if b else '')
            c = Image.new('RGBA', (440, 110), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
            d.rounded_rectangle((0, 0, 439, 109), radius=55, fill=CREAM, outline=GOLD, width=4)
            d.text(((440 - tw(s, G(46))) / 2, 26), s, font=G(46), fill=INK, features=['lnum'])
            put(fr, c, W / 2 + (i % 2 * 2 - 1) * 235, 560 + (i // 2) * 150, t, 11.9 + i * 0.25, dur=0.25, slide=0, scale_from=0.6, out_t=14.5)
        put(fr, text_layer('Akbarshoh buyrug\'i bilan forschaga o\'girilgan.', CB(60), CREAM, maxw=W - 200), W / 2, 1060, t, 13.2, out_t=14.5)

    if t >= 14.8:
        put(fr, text_layer('Bobur o\'z hayotini yozib qoldirdi.', PBo(80), CREAM, maxw=W - 180), W / 2, 420, t, 14.85, dur=0.35)
        put(fr, text_layer('Siz o\'qiganlaringizni yozib borasizmi?', CI(70), GOLD, maxw=W - 200), W / 2, 680, t, 15.3)
        pl = panel(150).resize((640, 150)); d = ImageDraw.Draw(pl); s = 'booknote.uz'
        d.text(((640 - tw(s, PB(74))) / 2, 26), s, font=PB(74), fill=MAR)
        put(fr, pl, W / 2, 950, t, 15.9, dur=0.3, slide=0, scale_from=0.8)
        put(fr, text_layer('Kitob kundaligingiz shu yerda.', G(46), CREAM), W / 2, 1150, t, 16.4)

    d = ImageDraw.Draw(fr); d.text((96, 100), 'BookNote', font=font('PlayfairBold', 42), fill=GOLD)
    d.rectangle((52, H - 62, 52 + (W - 104) * t / DUR, H - 54), fill=GOLD)
    return fr

def tabla(kind):
    n = int(0.5 * SR); tt = np.arange(n) / SR
    if kind == 'dha':
        f = 90 + 70 * np.exp(-tt * 25); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 7)
        s += 0.4 * np.sin(2 * np.pi * 330 * tt) * np.exp(-tt * 14)
    elif kind == 'na':
        s = (np.sin(2 * np.pi * 520 * tt) + 0.5 * np.sin(2 * np.pi * 1040 * tt) + 0.3 * np.sin(2 * np.pi * 1560 * tt)) * np.exp(-tt * 18)
    else:  # ge, bass with upward bend
        f = 70 + 40 * (1 - np.exp(-tt * 10)); s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * 5)
    s[:40] *= np.linspace(0, 1, 40); return s

def audio():
    m = Mix(DUR)
    # tanpura drone on D (Pa-Sa-Sa-Sa), Kafi-style melody
    for i in range(int(DUR / 2.4) + 1):
        for k, n in enumerate([45, 50, 50, 38]):
            m.add(reverb(pluck(midi(n), 2.4, 0.9995), 0.4, 2.2), i * 2.4 + k * 0.6, 0.18, pan=-0.3 + k * 0.2)
    teental = ['dha', 'dhin', 'dhin', 'dha', 'dha', 'dhin', 'dhin', 'dha', 'na', 'tin', 'tin', 'na', 'ta', 'dhin', 'dhin', 'dha']
    beat = 60 / 112 / 2
    for i in range(int(DUR / beat)):
        b = teental[i % 16]; tt = i * beat
        if b.startswith('dh'): m.add(tabla('dha'), tt, 0.35); m.add(tabla('ge'), tt, 0.3)
        else: m.add(tabla('na'), tt, 0.18)
        if i % 4 == 3: m.add(tabla('na'), tt + beat / 2, 0.08)
    mel = [62, 64, 65, 67, 69, 67, 65, 64, 62, 60, 62, 65, 64, 62]
    for i, n in enumerate(mel * 3):
        tt = 3.6 + i * beat * 2
        if tt > 14.6: break
        m.add(reverb(lowpass(pluck(midi(n + 12), 0.9, 0.997), 4500), 0.35, 1.8), tt, 0.16, pan=0.2)
    for tt in (0.0, 3.65, 7.65, 11.65, 14.85): m.add(reverb(lowpass(kick(), 160), 0.4, 2.2), tt, 0.7)
    for tt in (3.3, 7.3, 11.3, 14.5): m.add(whoosh(0.6, False), tt, 0.3)
    for i in range(6): m.add(chime(74 + i * 2, 1.2), 11.9 + i * 0.25, 0.08)
    m.add(reverb(chime(86, 3.0), 0.5), 15.9, 0.2)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [0.0, 6.5, 10.8, 13.8, 17.0], os.path.join(S, 'prevH.png'))
    else:
        render('H_boburnoma_kundalik', draw, DUR, audio); print('done H')
