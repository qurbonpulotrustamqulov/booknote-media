import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

DUR = 22.0
VEL = (243, 233, 210); INK = (34, 30, 44); WAX = (156, 24, 32); NAVY = (28, 44, 86); SEPIA = (120, 96, 70); GOLD = (184, 140, 60)

def _bg():
    rs = np.random.RandomState(21)
    base = np.ones((H, W, 3)) * np.array(VEL)[None, None, :] + rs.randn(H, W)[..., None] * 4
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert('RGBA')
    d = ImageDraw.Draw(img)
    for m, w in ((40, 3), (54, 1)): d.rectangle((m, m, W - m, H - m), outline=NAVY + (255,), width=w)
    for y in range(260, H - 120, 64): d.line((90, y, W - 90, y), fill=(200, 190, 170, 255), width=1)  # ledger rules
    img.alpha_composite(vignette(W, H, 0.45, (90, 70, 40)))
    return img
BG = _bg()

def seal(size, txt):
    l = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(l); c = size / 2
    pts = [(c + (size * 0.48 + (8 if k % 2 else 0)) * math.cos(k * math.pi / 14), c + (size * 0.48 + (8 if k % 2 else 0)) * math.sin(k * math.pi / 14)) for k in range(28)]
    d.polygon(pts, fill=WAX + (255,)); d.ellipse((c - size * 0.36, c - size * 0.36, c + size * 0.36, c + size * 0.36), outline=(220, 120, 110, 255), width=4)
    f = font('PlayfairBlack', int(size * 0.2)); d.text((c - tw(txt, f) / 2, c - size * 0.14), txt, font=f, fill=(250, 220, 200), features=['lnum'])
    return l

def quill(fr, x, y, p):
    d = ImageDraw.Draw(fr)
    d.line((x, y, x + 120, y - 300), fill=SEPIA + (255,), width=4)
    d.polygon([(x + 40, y - 100), (x + 160, y - 330), (x + 110, y - 330), (x + 20, y - 120)], fill=(250, 248, 240, 230), outline=SEPIA + (255,))
    d.line((90, y + 8, 90 + (x - 90) * p, y + 8), fill=INK + (200,), width=3)

def draw(t):
    fr = BG.copy()
    PB = lambda s: font('PlayfairBlack', s); PBo = lambda s: font('PlayfairBold', s); PI = lambda s: font('PlayfairItalic', s); CI = lambda s: font('CormorantItalic', s); C = lambda s: font('Cormorant', s); MO = lambda s: font('Mono', s)

    if t < 4.2:
        put(fr, text_layer('Marg\'ilonlik olimning kitobi bilan', CI(80), SEPIA, maxw=W - 160), W / 2, 400, t, -1)
        put(fr, text_layer('inglizlar Hindistonda sud qilgan.', PB(92), INK, maxw=W - 140), W / 2, 620, t, -1)
        put(fr, seal(260, '1791'), W / 2, 1060, t, -1)

    if 4.2 <= t < 8.6:
        put(fr, text_layer('Burhoniddin al-Marg\'inoniy', PB(84), INK, maxw=W - 140), W / 2, 380, t, 4.25, dur=0.3, out_t=8.3)
        put(fr, text_layer('1123-yil, Farg\'ona vodiysi, Rishton', PI(58), NAVY, maxw=W - 160), W / 2, 640, t, 4.8, out_t=8.3)
        put(fr, text_layer('Uning "Al-Hidoya" kitobi hanafiy fiqhining eng mashhur darsliklaridan biri.', C(64), INK, maxw=W - 180), W / 2, 790, t, 5.6, out_t=8.3)

    if 8.6 <= t < 13.4:
        put(fr, text_layer('13 yil', PB(220), WAX), W / 2, 380, t, 8.65, dur=0.3, slide=0, scale_from=1.25, out_t=13.1)
        put(fr, text_layer('Kitob shuncha yil davomida yozilgan.', PBo(66), INK, maxw=W - 160), W / 2, 680, t, 9.1, out_t=13.1)
        put(fr, text_layer('Rivoyat qilinishicha, olim bu yillar davomida ro\'za tutib, buni hech kimga bildirmagan.', CI(64), SEPIA, maxw=W - 180), W / 2, 900, t, 10.0, out_t=13.1)
        if t > 9.0: quill(fr, 760, 1460, clamp((t - 9.0) / 3.5) * (1 - clamp((t - 13.1) / 0.3)))

    if 13.4 <= t < 18.0:
        put(fr, seal(200, '1791'), W / 2, 330, t, 13.45, dur=0.2, slide=0, scale_from=1.8, out_t=17.7)
        put(fr, text_layer('"THE HEDAYA"', MO(70), NAVY), W / 2, 580, t, 13.9, out_t=17.7)
        put(fr, text_layer('Charlz Hamilton kitobni inglizchaga tarjima qildi.', PBo(64), INK, maxw=W - 160), W / 2, 700, t, 14.3, out_t=17.7)
        put(fr, text_layer('Britaniya Hindistoni sudlari musulmonlar ishini shu tarjima asosida ko\'rgan.', C(62), INK, maxw=W - 180), W / 2, 920, t, 15.2, out_t=17.7)

    if t >= 18.0:
        put(fr, text_layer('8 asrdan beri o\'qilmoqda.', PB(86), INK, maxw=W - 140), W / 2, 400, t, 18.05, dur=0.3)
        put(fr, text_layer('Siz buyuk ajdodlarimiz kitoblaridan qaysi birini o\'qigansiz? Kommentda yozing.', CI(62), SEPIA, maxw=W - 200), W / 2, 690, t, 18.5)
        pl = Image.new('RGBA', (620, 136), (0, 0, 0, 0)); d = ImageDraw.Draw(pl)
        d.rectangle((0, 0, 619, 135), fill=NAVY); s = 'booknote.uz'
        d.text(((620 - tw(s, PB(70))) / 2, 20), s, font=PB(70), fill=VEL)
        put(fr, pl, W / 2, 1000, t, 19.2, dur=0.3, slide=0, scale_from=0.8)

    d = ImageDraw.Draw(fr); d.text((90, 110), 'BookNote', font=font('PlayfairBold', 42), fill=INK)
    d.rectangle((54, 54, 54 + (W - 108) * t / DUR, 62), fill=WAX)
    return fr

def harpsichord(m_, dur=0.9):
    n = int(dur * SR); tt = np.arange(n) / SR; f = midi(m_)
    s = sum((1 / k) * np.sin(2 * np.pi * f * k * tt) * np.exp(-tt * (2 + k * 1.5)) for k in range(1, 9))
    return highpass(s * np.minimum(1, tt * 2000), 150)

def audio():
    m = Mix(DUR)
    # G minor baroque: Gm Cm D Gm / Eb Cm D Gm, broken-chord 16ths at 100 bpm
    prog = [[55, 58, 62], [48, 55, 60, 63], [50, 54, 57, 62], [55, 58, 62], [51, 55, 58, 63], [48, 51, 55, 60], [50, 54, 57, 62], [43, 55, 58, 62]]
    six = 60 / 100 / 4; tt = 0.0; bar = 0
    while tt < DUR - 1:
        ch = prog[bar % 8]
        m.add(harpsichord(ch[0] - 12, 1.6), tt, 0.22)
        seq = [ch[1], ch[2], ch[-1] + 12 if len(ch) > 3 else ch[0] + 12, ch[2]] * 4
        for k, n in enumerate(seq):
            if tt + k * six < DUR - 1: m.add(harpsichord(n + 12, 0.6), tt + k * six, 0.09, pan=0.25 * ((k % 2) * 2 - 1))
        tt += six * 16; bar += 1
    for tt in (0.0, 8.65, 13.45): m.add(reverb(lowpass(kick(), 120), 0.4, 2.2), tt, 0.8)
    for tt in (3.9, 8.3, 13.1, 17.7): m.add(whoosh(0.5, True), tt, 0.25)
    sc = highpass(noise(3.5), 3000) * 0.06
    m.add(sc * (0.5 + 0.5 * np.sin(np.linspace(0, 40, len(sc)))), 9.0, 0.6)  # quill scratching
    m.add(reverb(chime(79, 3.0), 0.5), 19.2, 0.18)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [0.0, 7.5, 12.5, 16.8, 21.0], os.path.join(S, 'prevO.png'))
    else:
        render('O_hidoya_marginoniy', draw, DUR, audio); print('done O')
