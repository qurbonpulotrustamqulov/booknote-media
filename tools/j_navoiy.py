import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

DUR = 22.0
TQ = (18, 110, 130); TQ2 = (8, 64, 90); COB = (24, 52, 120); WHITE = (250, 248, 240); SAND = (240, 214, 160); OCH = (226, 150, 60)

def _tiles():
    bg = gradient(W, H, TQ2, (6, 36, 60))
    d = ImageDraw.Draw(bg); s = 135
    for r in range(-1, H // s + 2):
        for c in range(-1, W // s + 2):
            cx, cy = c * s + (s / 2 if r % 2 else 0), r * s
            pts = [(cx + s * 0.42 * math.cos(math.radians(a * 45 + 22.5)), cy + s * 0.42 * math.sin(math.radians(a * 45 + 22.5))) for a in range(8)]
            d.polygon(pts, outline=(40, 140, 160, 34), width=2)
            d.polygon([(cx, cy - s * 0.18), (cx + s * 0.18, cy), (cx, cy + s * 0.18), (cx - s * 0.18, cy)], fill=(30, 120, 140, 22))
    bg.alpha_composite(vignette(W, H, 0.7, (2, 16, 28)))
    return bg
BG = _tiles()

def tile_card(text, f, fg, bg, w=None):
    l = text_layer(text, f, fg, maxw=W - 220)
    ww = w or l.size[0] + 80
    c = Image.new('RGBA', (ww, l.size[1] + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
    d.rounded_rectangle((0, 0, ww - 1, l.size[1] + 39), radius=18, fill=bg + (240,), outline=SAND, width=3)
    c.alpha_composite(l, ((ww - l.size[0]) // 2, 20)); return c

def draw(t):
    fr = BG.copy()
    PB = lambda s: font('PlayfairBlack', s); PBo = lambda s: font('PlayfairBold', s); PI = lambda s: font('PlayfairItalic', s); CI = lambda s: font('CormorantItalic', s); C = lambda s: font('Cormorant', s); G = lambda s: font('GroteskMed', s)

    if t < 4.2:
        put(fr, text_layer('Fors tilida bunday so\'z yo\'q.', CI(80), SAND, maxw=W - 160), W / 2, 420, t, -1)
        put(fr, text_layer('Navoiy shunday', PBo(92), WHITE, maxw=W - 120), W / 2, 560, t, -1)
        put(fr, text_layer('100 ta', PB(240), OCH), W / 2, 670, t, -1)
        put(fr, text_layer('turkiy fe\'lni sanab bergan.', PBo(84), WHITE, maxw=W - 140), W / 2, 990, t, -1)

    if 4.2 <= t < 8.4:
        put(fr, text_layer('1499-yil', G(56), SAND), W / 2, 420, t, 4.25, dur=0.3, out_t=8.1)
        put(fr, text_layer('"Muhokamat ul-lug\'atayn"', PB(86), WHITE, maxw=W - 120), W / 2, 500, t, 4.4, dur=0.35, slide=0, scale_from=1.15, out_t=8.1)
        put(fr, text_layer('ya\'ni "Ikki til muhokamasi"', CI(66), SAND), W / 2, 790, t, 5.0, out_t=8.1)
        put(fr, text_layer('O\'sha davrda she\'r asosan forsiyda yozilardi. Navoiy turkiy til ham boy ekanini isbotlab berdi.', C(58), WHITE, maxw=W - 180), W / 2, 940, t, 5.6, out_t=8.1)

    if 8.4 <= t < 14.4:
        put(fr, text_layer('Masalan, yig\'lashning turlari:', PBo(70), WHITE, maxw=W - 160), W / 2, 380, t, 8.45, dur=0.3, out_t=14.1)
        words = [('yig\'lamoq', 'oddiy yig\'lash'), ('ingramoq', 'ovoz chiqarib, sekin'), ('siqtamoq', 'ichdan, siqilib'), ('o\'kurmoq', 'baland ovozda'), ('yig\'lamsinmoq', 'yig\'lagudek bo\'lmoq')]
        for i, (a, b) in enumerate(words):
            row = Image.new('RGBA', (900, 140), (0, 0, 0, 0)); d = ImageDraw.Draw(row)
            d.rounded_rectangle((0, 8, 899, 131), radius=20, fill=(4, 30, 50, 225), outline=SAND + (200,), width=2)
            d.text((36, 22), a, font=PB(58), fill=OCH); d.text((36, 92), b, font=G(32), fill=SAND)
            put(fr, row, W / 2, 600 + i * 160, t, 8.9 + i * 0.7, dur=0.3, slide=40, out_t=14.1)

    if 14.4 <= t < 18.4:
        put(fr, text_layer('Turkiy she\'rlarida', G(56), SAND), W / 2, 380, t, 14.45, dur=0.3, out_t=18.1)
        put(fr, text_layer('Navoiy', PB(150), WHITE), W / 2, 450, t, 14.6, dur=0.3, slide=0, scale_from=1.2, out_t=18.1)
        put(fr, text_layer('Forsiy she\'rlarida', G(56), SAND), W / 2, 720, t, 15.2, dur=0.3, out_t=18.1)
        put(fr, text_layer('Foniy', PB(150), WHITE), W / 2, 790, t, 15.35, dur=0.3, slide=0, scale_from=1.2, out_t=18.1)
        put(fr, text_layer('Ikki tilda ham yozgan, lekin ona tilini tanladi: "Xamsa"ning 5 dostonini turkiyda yozdi.', C(58), SAND, maxw=W - 180), W / 2, 1100, t, 16.0, out_t=18.1)

    if t >= 18.4:
        put(fr, text_layer('Siz eng chiroyli deb bilgan o\'zbekcha so\'z qaysi?', PBo(78), WHITE, maxw=W - 160), W / 2, 420, t, 18.45, dur=0.35)
        put(fr, text_layer('Kommentda yozing.', CI(66), SAND), W / 2, 830, t, 18.9)
        put(fr, tile_card('booknote.uz', PB(74), WHITE, COB, w=620), W / 2, 980, t, 19.5, dur=0.3, slide=0, scale_from=0.8)
        put(fr, text_layer('O\'zbek kitobxonlari tarmog\'i', G(46), SAND), W / 2, 1170, t, 19.9)

    d = ImageDraw.Draw(fr); d.text((70, 100), 'BookNote', font=font('PlayfairBold', 42), fill=WHITE)
    d.rectangle((0, 0, W * t / DUR, 8), fill=OCH)
    return fr

def santur(m_, dur=0.9):
    n = int(dur * SR); tt = np.arange(n) / SR; f = midi(m_)
    s = sum(np.sin(2 * np.pi * f * (1 + dt) * tt) for dt in (-0.002, 0, 0.002)) / 3 + 0.3 * np.sin(2 * np.pi * f * 2 * tt) * np.exp(-tt * 6)
    return s * np.exp(-tt * 3.5) * np.minimum(1, tt * 400)

def audio():
    m = Mix(DUR)
    # Segah-ish on E: E F G A B C D, santur tremolo phrases + daf
    sc = [52, 53, 55, 57, 59, 60, 62, 64, 65, 67]
    m.add(reverb(pad([40, 47], DUR + 1, 'tri', 450, a=0.05, r=3, gain=0.4), 0.3), 0)
    rs = random.Random(3); tt = 0.0; idx = 4
    while tt < DUR - 1:
        idx = max(0, min(len(sc) - 1, idx + rs.choice([-1, -1, 1, 1, 2, -2])))
        rep = 3 if rs.random() < 0.35 else 1
        for r in range(rep): m.add(santur(sc[idx] + 12), tt + r * 0.07, 0.2, pan=rs.uniform(-0.3, 0.3))
        tt += rs.choice([0.25, 0.25, 0.5])
    beat = 60 / 100
    tt = 4.2
    while tt < DUR - 1.2:
        m.add(lowpass(kick(), 180), tt, 0.4); m.add(highpass(tick(), 800), tt + beat * 0.5, 0.15); m.add(highpass(tick(), 800), tt + beat * 0.75, 0.1)
        tt += beat
    for tt in (0.0, 4.4, 14.6, 15.35, 18.45): m.add(reverb(lowpass(kick(), 130), 0.35, 2.2), tt, 0.75)
    for i in range(5): m.add(chime(76 + i * 2, 1.0), 8.9 + i * 0.7, 0.1)
    m.add(reverb(chime(88, 3.0), 0.5), 19.5, 0.2)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [0.0, 7.5, 13.5, 17.6, 21.0], os.path.join(S, 'prevJ.png'))
    else:
        render('J_navoiy_100_feol', draw, DUR, audio); print('done J')
