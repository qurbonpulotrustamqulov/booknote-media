import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

DUR = 22.0
DESK = (22, 18, 16); LAMP = (255, 214, 150); PAPER = (236, 228, 208); INK = (30, 26, 24); RED = (232, 78, 64); GREY = (150, 140, 128)

def _desk():
    bg = Image.new('RGBA', (W, H), DESK + (255,))
    a = np.zeros((H, W)); yy, xx = np.mgrid[0:H, 0:W]
    a = np.clip(1 - np.sqrt(((xx - W * 0.5) / (W * 0.9)) ** 2 + ((yy - H * 0.38) / (H * 0.55)) ** 2), 0, 1) ** 1.6
    glow = np.zeros((H, W, 4), np.uint8); glow[..., 0], glow[..., 1], glow[..., 2] = LAMP; glow[..., 3] = (a * 90).astype(np.uint8)
    bg.alpha_composite(Image.fromarray(glow, 'RGBA'))
    return bg
BG = _desk()

def sheet(w, h, torn=False, lines=0, seed=1):
    l = Image.new('RGBA', (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    if torn:
        rs = random.Random(seed); pts = [(0, 0), (w, 0), (w, h * 0.55)]
        x = w
        while x > 0:
            x -= rs.randint(20, 50); pts.append((max(0, x), h * 0.55 + rs.randint(-30, 30)))
        d.polygon(pts, fill=PAPER + (255,))
    else:
        d.rectangle((0, 0, w - 1, h - 1), fill=PAPER + (255,))
    rs = random.Random(seed + 7)
    for i in range(lines):
        y = 60 + i * 42
        if torn and y > h * 0.5: break
        d.line((50, y, 50 + rs.randint(int(w * 0.5), w - 100), y), fill=(120, 110, 100, 255), width=6)
    return l

def draw(t):
    fr = BG.copy()
    PB = lambda s: font('PlayfairBlack', s); PBo = lambda s: font('PlayfairBold', s); PI = lambda s: font('PlayfairItalic', s); MO = lambda s: font('Mono', s); MB = lambda s: font('MonoBold', s); CI = lambda s: font('CormorantItalic', s)

    if t < 4.2:
        put(fr, text_layer('Bu romanning', CI(90), LAMP), W / 2, 420, t, -1)
        put(fr, text_layer('ikkinchi qismi', PB(120), PAPER, maxw=W - 100), W / 2, 530, t, -1)
        put(fr, text_layer('hech qachon topilmadi.', PBo(90), RED, maxw=W - 120), W / 2, 700, t, -1)
        put(fr, sheet(520, 420, torn=True, lines=9, seed=3).rotate(-4, expand=True, resample=Image.BICUBIC), W / 2, 980, t, 0.6, dur=0.4, out_t=3.9)

    if 4.2 <= t < 8.6:
        n = int(clamp((t - 4.4) / 1.4) * 22)
        put(fr, text_layer('KECHA VA KUNDUZ'[:max(0, min(15, n))], MB(84), PAPER), W / 2, 420, t, 4.25, dur=0.1, slide=0, out_t=8.3)
        put(fr, text_layer('Cho\'lpon, 1936-yil', PI(70), LAMP), W / 2, 580, t, 5.6, out_t=8.3)
        put(fr, text_layer('Ikki qismli roman bo\'lishi kerak edi: "Kecha" va "Kunduz".', MO(46), PAPER, maxw=W - 180), W / 2, 760, t, 6.2, out_t=8.3)
        put(fr, text_layer('Faqat birinchi qismi, "Kecha", bosilib chiqdi.', MO(46), LAMP, maxw=W - 180), W / 2, 980, t, 7.0, out_t=8.3)

    if 8.6 <= t < 13.6:
        put(fr, text_layer('1937', PB(240), RED), W / 2, 380, t, 8.65, dur=0.25, slide=0, scale_from=1.3, out_t=13.3)
        put(fr, text_layer('Cho\'lpon qamoqqa olindi. 1938-yilda otib tashlandi.', PBo(64), PAPER, maxw=W - 160), W / 2, 700, t, 9.2, out_t=13.3)
        put(fr, text_layer('Aytilishicha, "Kunduz" qo\'lyozmasi o\'shanda yo\'qolgan.', CI(64), LAMP, maxw=W - 180), W / 2, 960, t, 10.4, out_t=13.3)

    if 13.6 <= t < 18.0:
        put(fr, text_layer('Kitoblari yarim asr taqiqlandi.', PBo(72), PAPER, maxw=W - 160), W / 2, 400, t, 13.65, dur=0.3, out_t=17.7)
        put(fr, text_layer('Ular faqat 1990-yillar boshida qayta nashr qilindi.', MO(48), LAMP, maxw=W - 180), W / 2, 660, t, 14.4, out_t=17.7)
        put(fr, text_layer('Bugun "Kecha va kunduz" eng sevimli o\'zbek romanlaridan biri.', PI(64), PAPER, maxw=W - 180), W / 2, 860, t, 15.4, out_t=17.7)

    if t >= 18.0:
        put(fr, text_layer('Siz "Kecha"ni o\'qiganmisiz?', PB(84), PAPER, maxw=W - 160), W / 2, 420, t, 18.05, dur=0.3)
        put(fr, text_layer('"Kunduz" qanday tugaganini o\'ylab ko\'rganmisiz? Kommentda yozing.', CI(62), LAMP, maxw=W - 200), W / 2, 680, t, 18.5)
        pl = Image.new('RGBA', (620, 136), (0, 0, 0, 0)); d = ImageDraw.Draw(pl)
        d.rectangle((0, 0, 619, 135), fill=PAPER); s = 'booknote.uz'
        d.text(((620 - tw(s, MB(70))) / 2, 24), s, font=MB(70), fill=INK)
        put(fr, pl, W / 2, 940, t, 19.2, dur=0.3, slide=0, scale_from=0.8)

    d = ImageDraw.Draw(fr); d.text((70, 100), 'BookNote', font=font('PlayfairBold', 42), fill=PAPER)
    d.rectangle((0, 0, W * t / DUR, 8), fill=RED)
    return fr

def cello(m_, dur):
    n = int(dur * SR); tt = np.arange(n) / SR; f = midi(m_) * (1 + 0.005 * np.sin(2 * np.pi * 5.2 * tt) * np.clip(tt * 2 - 0.3, 0, 1))
    ph = np.cumsum(f) / SR; s = 2 * (ph % 1) - 1
    return lowpass(s, 1400) * env_adsr(n, 0.35, 0.3, 0.8, 0.6)

def audio():
    from c_6daqiqa import rhodes
    m = Mix(DUR)
    # D minor: Dm Bb Gm A, slow piano + cello line
    ch = [[50, 53, 57], [46, 50, 53], [43, 46, 50], [45, 49, 52]]
    for i in range(6):
        c = ch[i % 4]
        for k, n in enumerate(c + [c[1] + 12]):
            m.add(reverb(rhodes(n + 12, 2.0), 0.5, 2.5), i * 4.0 + k * 0.5, 0.12)
    line = [(62, 2), (60, 2), (58, 2), (57, 2), (55, 2), (57, 4), (62, 2), (65, 2), (64, 2)]
    tt = 4.2
    for n, dd in line:
        if tt > DUR - 2: break
        m.add(reverb(cello(n - 12, dd + 0.4), 0.4, 2.0), tt, 0.16); tt += dd
    for i in range(15): m.add(tick(), 4.4 + i * 0.09, 0.3)  # typewriter
    m.add(chime(86, 1.0), 4.4 + 15 * 0.09 + 0.1, 0.1)
    for tt in (0.0, 8.65): m.add(reverb(lowpass(kick(), 100), 0.5, 3.0), tt, 0.9)
    m.add(highpass(noise(0.5) * np.exp(-np.linspace(0, 5, int(0.5 * SR))), 2000), 0.6, 0.15)  # paper tear
    for tt in (3.9, 8.3, 13.3, 17.7): m.add(whoosh(0.5, False), tt, 0.25)
    m.add(reverb(chime(81, 3.0), 0.5), 19.2, 0.18)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [0.0, 7.8, 12.5, 16.8, 21.0], os.path.join(S, 'prevL.png'))
    else:
        render('L_cholpon_kecha_va_kunduz', draw, DUR, audio); print('done L')
