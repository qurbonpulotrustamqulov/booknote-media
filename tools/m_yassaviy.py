import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

DUR = 22.0
SKY1 = (250, 170, 90); SKY2 = (120, 60, 70); SAND = (214, 160, 100); DARK = (52, 30, 34); TURQ = (70, 190, 200); CREAM = (255, 244, 225); GOLD = (255, 236, 170)

def _bg():
    bg = gradient(W, H, SKY2, SKY1)
    d = ImageDraw.Draw(bg)
    d.ellipse((830, H - 1060, 1030, H - 860), fill=(255, 226, 160, 255))  # low sun
    # dunes
    for k, (y, col) in enumerate([(H - 520, (196, 132, 86)), (H - 420, (170, 108, 72)), (H - 320, (130, 80, 60))]):
        pts = [(0, H)] + [(x, y + 40 * math.sin(x / 180 + k * 2)) for x in range(0, W + 20, 20)] + [(W, H)]
        d.polygon(pts, fill=col + (255,))
    # Yassaviy mausoleum silhouette: big portal + turquoise ribbed dome
    sil = DARK + (255,)
    d.rectangle((200, H - 820, 470, H - 330), fill=sil)
    d.rectangle((270, H - 640, 400, H - 380), fill=(90, 52, 50, 255)); d.pieslice((270, H - 710, 400, H - 580), 180, 360, fill=(90, 52, 50, 255))
    d.rectangle((470, H - 620, 880, H - 330), fill=sil)
    d.rectangle((600, H - 690, 780, H - 610), fill=sil)
    d.chord((590, H - 870, 790, H - 620), 180, 360, fill=TURQ + (255,))
    for k in range(9):
        x = 610 + k * 20; d.line((x, H - 860 + abs(4 - k) * 14, x, H - 745), fill=(40, 130, 140, 255), width=3)
    d.rectangle((686, H - 910, 694, H - 868), fill=sil)
    return bg
BG = _bg()
_rs = np.random.RandomState(9)
GRAINS = [(_rs.uniform(0, W), _rs.uniform(H * 0.4, H), _rs.uniform(60, 160), _rs.uniform(0, 6)) for _ in range(140)]

def draw(t):
    fr = BG.copy(); d = ImageDraw.Draw(fr)
    for x, y, sp, ph in GRAINS:
        xx = (x + t * sp) % W; yy = y + 8 * math.sin(t * 2 + ph)
        d.ellipse((xx - 2, yy - 2, xx + 2, yy + 2), fill=(255, 230, 190, 120))
    PB = lambda s: font('PlayfairBlack', s); PBo = lambda s: font('PlayfairBold', s); CI = lambda s: font('CormorantItalic', s); C = lambda s: font('Cormorant', s); G = lambda s: font('GroteskMed', s)
    SH = dict(stroke=3, stroke_fill=(80, 34, 36))

    if t < 4.2:
        put(fr, text_layer('Rivoyat qilinishicha, 63 yoshida', CI(70), CREAM, maxw=W - 140, **SH), W / 2, 330, t, -1)
        put(fr, text_layer('u yer ostidagi hujraga tushdi', PB(92), CREAM, maxw=W - 100, **SH), W / 2, 440, t, -1)
        put(fr, text_layer('va umrining oxirigacha o\'sha yerda yashadi.', PBo(64), GOLD, maxw=W - 160, **SH), W / 2, 720, t, -1)

    if 4.2 <= t < 8.6:
        put(fr, text_layer('Xoja Ahmad', CI(84), CREAM, **SH), W / 2, 330, t, 4.25, dur=0.3, out_t=8.3)
        put(fr, text_layer('Yassaviy', PB(150), CREAM, **SH), W / 2, 420, t, 4.4, dur=0.3, slide=0, scale_from=1.2, out_t=8.3)
        put(fr, text_layer('XII asr. Sayram, keyin Yassi (hozirgi Turkiston) shahri.', G(50), CREAM, maxw=W - 180, **SH), W / 2, 650, t, 5.0, out_t=8.3)
        put(fr, text_layer('63 yosh: Payg\'ambarimiz vafot etgan yosh.', CI(62), GOLD, maxw=W - 180, **SH), W / 2, 820, t, 6.0, out_t=8.3)

    if 8.6 <= t < 13.6:
        put(fr, text_layer('"Devoni hikmat"', PB(110), CREAM, maxw=W - 120, **SH), W / 2, 330, t, 8.65, dur=0.35, out_t=13.3)
        put(fr, text_layer('O\'sha davrda ilmiy kitoblar arab va fors tilida yozilardi.', C(60), CREAM, maxw=W - 180, **SH), W / 2, 520, t, 9.2, out_t=13.3)
        put(fr, text_layer('Yassaviy hikmatlarini oddiy xalq tushunadigan turkiy tilda aytdi.', PBo(64), GOLD, maxw=W - 160, **SH), W / 2, 700, t, 10.2, out_t=13.3)

    if 13.6 <= t < 18.0:
        put(fr, text_layer('Uning maqbarasini', CI(72), CREAM, **SH), W / 2, 330, t, 13.65, dur=0.3, out_t=17.7)
        put(fr, text_layer('Amir Temur qurdirgan.', PB(92), CREAM, maxw=W - 120, **SH), W / 2, 420, t, 13.9, dur=0.3, out_t=17.7)
        put(fr, text_layer('2003-yildan YUNESKO Jahon merosi ro\'yxatida.', G(52), GOLD, maxw=W - 180, **SH), W / 2, 720, t, 14.8, out_t=17.7)

    if t >= 18.0:
        put(fr, text_layer('Siz "Hikmatlar"dan biror satrni yoddan bilasizmi?', PBo(74), CREAM, maxw=W - 160, **SH), W / 2, 330, t, 18.05, dur=0.3)
        put(fr, text_layer('Kommentda yozing.', CI(64), GOLD, **SH), W / 2, 590, t, 18.5)
        pl = Image.new('RGBA', (620, 136), (0, 0, 0, 0)); dd = ImageDraw.Draw(pl)
        dd.rounded_rectangle((0, 0, 619, 135), radius=68, fill=TURQ); s = 'booknote.uz'
        dd.text(((620 - tw(s, PB(70))) / 2, 20), s, font=PB(70), fill=DARK)
        put(fr, pl, W / 2, 730, t, 19.0, dur=0.3, slide=0, scale_from=0.8)

    d = ImageDraw.Draw(fr); d.text((70, 100), 'BookNote', font=font('PlayfairBold', 42), fill=CREAM)
    d.rectangle((0, 0, W * t / DUR, 8), fill=TURQ)
    return fr

def dutar(m_, dur=1.2):
    a = pluck(midi(m_), dur, 0.997); b = pluck(midi(m_ + 7), dur, 0.997) * 0.5
    return lowpass(a + b, 4000)

def audio():
    m = Mix(DUR)
    # wind
    w = lowpass(noise(DUR + 1), 700); w *= 0.5 + 0.5 * np.sin(np.linspace(0, 9, len(w))) ** 2
    m.add(w, 0, 0.12)
    m.add(reverb(pad([45, 52, 57], DUR + 1, 'tri', 420, a=0.05, r=3, gain=0.4), 0.3), 0)
    # dutar: strummed pattern in A (Ushshoq-like, minor with raised 6th)
    sc = [57, 59, 60, 62, 64, 66, 67, 69]
    rs = random.Random(5); beat = 60 / 96
    tt = 0.0; i = 0
    while tt < DUR - 1:
        pat = [1, 0, 1, 1, 0, 1, 1, 0]
        if pat[i % 8]:
            n = sc[rs.choice([0, 2, 4, 3, 4, 5, 7, 4])] if tt > 4.2 else 57
            m.add(dutar(n), tt, 0.22, pan=-0.2); m.add(dutar(45), tt, 0.1)
        tt += beat / 2; i += 1
    for tt in (0.0, 4.4, 8.65, 13.9, 18.05): m.add(reverb(lowpass(kick(), 110), 0.45, 2.6), tt, 0.75)
    for tt in (3.9, 8.3, 13.3, 17.7): m.add(whoosh(0.8, True), tt, 0.3)
    m.add(reverb(chime(81, 3.0), 0.5), 19.0, 0.18)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [0.0, 7.6, 12.5, 16.9, 21.0], os.path.join(S, 'prevM.png'))
    else:
        render('M_yassaviy_hikmatlar', draw, DUR, audio); print('done M')
