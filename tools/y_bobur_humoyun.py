import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

# Style: deep green-black night, a single white circle traced three times (walking around the bed), soft lamp glow;
# solo piano + low strings.
DUR = 22.0
NG1 = (6, 20, 18); NG2 = (16, 44, 38); IVORY = (244, 238, 222); JADE = (120, 200, 170); LAMP = (255, 200, 120); DIM = (150, 170, 160)

BG = gradient(W, H, NG1, NG2); BG.alpha_composite(vignette(W, H, 0.75))
def _glow():
    y, x = np.ogrid[:H, :W]; r = np.sqrt((x - W / 2) ** 2 + (y - 1380) ** 2)
    a = (np.clip(1 - r / 520, 0, 1) ** 2 * 120).astype(np.uint8)
    g = Image.new('RGBA', (W, H), LAMP + (0,)); g.putalpha(Image.fromarray(a, 'L')); return g
GLOW = _glow()

def circles(fr, t, t0, cx=W / 2, cy=1380, R=230):
    l = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    d.rounded_rectangle((cx - 90, cy - 40, cx + 90, cy + 40), 16, fill=IVORY + (60,))  # bed
    total = clamp((t - t0) / 6.0) * 3
    for k in range(3):
        p = clamp(total - k)
        if p <= 0: break
        r = R + k * 26
        d.arc((cx - r, cy - r * 0.55, cx + r, cy + r * 0.55), -90, -90 + 360 * p, fill=IVORY + (150 + 35 * k,), width=4)
        if p < 1:
            a = math.radians(-90 + 360 * p); px, py = cx + r * math.cos(a), cy + r * 0.55 * math.sin(a)
            d.ellipse((px - 10, py - 10, px + 10, py + 10), fill=LAMP + (255,))
    fr.alpha_composite(l)

def draw(t):
    fr = BG.copy(); fr.alpha_composite(GLOW)
    PB = lambda s: font('PlayfairBlack', s); PBo = lambda s: font('PlayfairBold', s); PI = lambda s: font('PlayfairItalic', s); G = lambda s: font('GroteskMed', s); CI = lambda s: font('CormorantItalic', s)

    if t < 4.4:
        put(fr, text_layer('O\'g\'li o\'lim to\'shagida yotardi.', PI(76), JADE, maxw=W - 120), W / 2, 320, t, -1)
        put(fr, text_layer('Ota Allohdan uning o\'rniga o\'z jonini so\'radi.', PB(96), IVORY, maxw=W - 100), W / 2, 440, t, -1)
        circles(fr, t + 1.5, 0)

    if 4.4 <= t < 9.6:
        put(fr, text_layer('1530-yil, Agra.', G(56), JADE), W / 2, 330, t, 4.45, dur=0.3, out_t=9.3)
        put(fr, text_layer('Zahiriddin Muhammad Bobur', PB(80), IVORY, maxw=W - 120), W / 2, 440, t, 4.8, out_t=9.3)
        put(fr, text_layer('o\'g\'li Humoyun og\'ir kasal bo\'lganda, uning to\'shagi atrofida uch marta aylandi va duo qildi.', PI(62), DIM, maxw=W - 170), W / 2, 730, t, 5.6, out_t=9.3)
        circles(fr, t, 4.6)

    if 9.6 <= t < 14.4:
        put(fr, text_layer('Humoyun tuzaldi.', PB(100), IVORY), W / 2, 340, t, 9.65, dur=0.3, out_t=14.1)
        put(fr, text_layer('Bobur esa o\'sha yili, 1530-yil dekabrida vafot etdi.', PI(68), LAMP, maxw=W - 160), W / 2, 520, t, 10.9, out_t=14.1)
        circles(fr, 30, 0)

    if 14.4 <= t < 18.6:
        put(fr, text_layer('Bu voqeani Boburning qizi Gulbadan begim yozib qoldirgan.', PBo(72), IVORY, maxw=W - 140), W / 2, 340, t, 14.45, dur=0.3, out_t=18.3)
        put(fr, text_layer('Kitobi: "Humoyunnoma".', PI(70), JADE, maxw=W - 160), W / 2, 700, t, 15.7, out_t=18.3)

    if t >= 18.6:
        put(fr, text_layer('Siz uchun kim shunday fidoyi?', PBo(80), IVORY, maxw=W - 140), W / 2, 360, t, 18.65, dur=0.3)
        put(fr, text_layer('Kommentda yozing.', PI(60), JADE), W / 2, 600, t, 19.1)
        pl = Image.new('RGBA', (620, 136), (0, 0, 0, 0)); d = ImageDraw.Draw(pl)
        d.rectangle((0, 0, 619, 135), fill=IVORY); s = 'booknote.uz'
        d.text(((620 - tw(s, PB(70))) / 2, 20), s, font=PB(70), fill=NG1)
        put(fr, pl, W / 2, 770, t, 19.6, dur=0.3, slide=0, scale_from=0.8)

    d = ImageDraw.Draw(fr); d.text((70, 100), 'BookNote', font=font('PlayfairBold', 42), fill=IVORY)
    d.rectangle((0, 0, W * t / DUR, 8), fill=LAMP)
    return fr

def piano(m_, dur=2.5):
    t = np.arange(int(dur * SR)) / SR; f = midi(m_)
    s = sum(a * np.sin(2 * np.pi * f * h * t) * np.exp(-t * (1.2 + h * 0.9)) for h, a in ((1, 1), (2, 0.45), (3, 0.22), (4, 0.1)))
    a = int(0.004 * SR); s[:a] *= np.linspace(0, 1, a); r = int(0.2 * SR); s[-r:] *= np.linspace(1, 0, r)
    return s

def audio():
    m = Mix(DUR)
    m.add(reverb(pad([38, 45, 50], DUR + 1, 'saw', 450, a=1.5, r=3, gain=0.22), 0.5, 3.0), 0)
    # D minor piano, 66 bpm
    b = 60 / 66
    prog = [[50, 57, 62, 65], [46, 53, 58, 62], [48, 55, 60, 64], [45, 52, 57, 61]]
    tt = 0.2; bar = 0
    while tt < DUR - 2:
        ch = prog[bar % 4]
        for i, n in enumerate([ch[0], ch[1], ch[2], ch[3], ch[2], ch[1]]):
            m.add(reverb(piano(n, 2.2), 0.45, 2.6), tt + i * b / 2, 0.22 if i else 0.3, -0.2 + 0.08 * i)
        tt += 3 * b; bar += 1
    mel = [(74, 1.5), (72, .5), (70, 1), (69, 3), (69, 1.5), (70, .5), (72, 1), (74, 3), (77, 2), (76, 1), (74, 3), (73, 3)]
    tt = 4.4
    for n, dd in mel:
        if tt > DUR - 2: break
        m.add(reverb(piano(n, dd * b + 1), 0.5, 2.8), tt, 0.2, 0.15); tt += dd * b
    m.add(reverb(lowpass(kick(), 70), 0.6, 3.5), 9.65, 0.7)
    m.add(reverb(chime(81, 3.0), 0.6), 19.6, 0.12)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [0.0, 8.0, 13.0, 17.5, 21.0], os.path.join(S, 'prevY.png'))
    else:
        render('Y_bobur_humoyun_jon', draw, DUR, audio); print('done Y')
