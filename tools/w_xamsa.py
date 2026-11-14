import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

# Style: lapis lazuli night, five gold gems forming a pentagon (five dostons), drifting gold dust; chang arpeggios + tabla.
DUR = 22.0
LAP1 = (8, 18, 64); LAP2 = (22, 46, 120); GOLD = (244, 200, 100); CREAM = (250, 242, 222); SKY = (150, 190, 255); CORAL = (255, 140, 110)

BG = gradient(W, H, LAP1, LAP2)
_rs = np.random.RandomState(7)
DUST = [(_rs.rand() * W, _rs.rand() * H, 2 + _rs.rand() * 4, _rs.rand() * 6.28) for _ in range(90)]
BG.alpha_composite(vignette(W, H, 0.7))

DOSTONS = ['Hayrat ul-abror', 'Farhod va Shirin', 'Layli va Majnun', 'Sab\'ai sayyor', 'Saddi Iskandariy']

def dust(fr, t):
    l = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    for x, y, r, ph in DUST:
        yy = (y - t * 25) % H; a = int(120 + 100 * math.sin(t * 2 + ph))
        d.ellipse((x - r, yy - r, x + r, yy + r), fill=GOLD + (a,))
    fr.alpha_composite(l)

def gem(d, cx, cy, r, a=255, lit=1.0):
    pts = [(cx, cy - r), (cx + r * 0.8, cy), (cx, cy + r), (cx - r * 0.8, cy)]
    col = tuple(int(c * (0.6 + 0.4 * lit)) for c in GOLD)
    d.polygon(pts, fill=col + (a,), outline=CREAM + (a,))
    d.line((cx - r * 0.8, cy, cx + r * 0.8, cy), fill=CREAM + (a // 2,), width=2)

def pentagon(fr, t, t0, cx, cy, R, labels=False, out_t=None):
    l = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    pos = [(cx + R * math.sin(2 * math.pi * k / 5), cy - R * math.cos(2 * math.pi * k / 5)) for k in range(5)]
    shown = [k for k in range(5) if t >= t0 + k * 0.55]
    for i in range(len(shown) - 1):
        d.line((pos[shown[i]], pos[shown[i + 1]]), fill=GOLD + (150,), width=3)
    if len(shown) == 5: d.line((pos[4], pos[0]), fill=GOLD + (150,), width=3)
    for k in shown:
        p = ease((t - t0 - k * 0.55) / 0.4); gem(d, pos[k][0], pos[k][1], 34 * p + 1, 255, 0.7 + 0.3 * math.sin(t * 3 + k))
    if out_t is not None and t > out_t: l = fade(l, 1 - ease((t - out_t) / 0.35))
    fr.alpha_composite(l)
    return pos

def draw(t):
    fr = BG.copy(); dust(fr, t)
    PB = lambda s: font('PlayfairBlack', s); PBo = lambda s: font('PlayfairBold', s); PI = lambda s: font('PlayfairItalic', s); G = lambda s: font('GroteskMed', s); CO = lambda s: font('Cormorant', s); CI = lambda s: font('CormorantItalic', s)

    if t < 4.4:
        put(fr, text_layer('Dostonlar asosan forsiyda yozilardi.', PI(72), SKY, maxw=W - 120), W / 2, 270, t, -1)
        put(fr, text_layer('U turkiyda 5 ta doston yozdi.', PB(100), CREAM, maxw=W - 100), W / 2, 480, t, -1)
        put(fr, text_layer('Taxminan 2 yilda.', PB(100), GOLD, maxw=W - 100), W / 2, 790, t, -1)
        pentagon(fr, t + 3, 0, W / 2, 1250, 170)

    if 4.4 <= t < 10.0:
        put(fr, text_layer('Alisher Navoiy, "XAMSA"', PB(80), GOLD, maxw=W - 100), W / 2, 260, t, 4.45, dur=0.3, out_t=9.7)
        put(fr, text_layer('1483-1485', G(52), SKY), W / 2, 380, t, 4.8, out_t=9.7)
        for i, n in enumerate(DOSTONS):
            put(fr, text_layer(n, CI(70), CREAM), W / 2, 500 + i * 100, t, 5.2 + i * 0.55, dur=0.35, out_t=9.7)
        pentagon(fr, t, 5.2, W / 2, 1360, 190, out_t=9.7)

    if 10.0 <= t < 14.6:
        n = int(50000 * ease(clamp((t - 10.2) / 2.0)) / 1000) * 1000
        put(fr, text_layer('Besh dostonda jami', PI(72), SKY), W / 2, 340, t, 10.05, dur=0.3, out_t=14.3)
        put(fr, text_layer(format(n, ',').replace(',', ' ') + ('+' if n >= 50000 else ''), PB(190), GOLD), W / 2, 460, t, 10.05, dur=0.2, slide=0, out_t=14.3)
        put(fr, text_layer('misra', PI(72), SKY), W / 2, 720, t, 10.05, dur=0.3, out_t=14.3)
        put(fr, text_layer('Turkiy tildagi birinchi to\'liq "Xamsa".', PBo(66), CREAM, maxw=W - 160), W / 2, 960, t, 12.4, out_t=14.3)

    if 14.6 <= t < 18.6:
        put(fr, text_layer('Forsiyda bu yo\'lni Nizomiy boshlagan va o\'nlab yillar yozgan.', PBo(70), CREAM, maxw=W - 140), W / 2, 340, t, 14.65, dur=0.3, out_t=18.3)
        put(fr, text_layer('Navoiy esa turkiy til ham bunga qodirligini ko\'rsatdi.', PI(66), GOLD, maxw=W - 160), W / 2, 760, t, 15.9, out_t=18.3)

    if t >= 18.6:
        put(fr, text_layer('Beshtadan qaysi birini o\'qigansiz?', PBo(80), CREAM, maxw=W - 140), W / 2, 360, t, 18.65, dur=0.3)
        put(fr, text_layer('Kommentda yozing.', PI(60), SKY), W / 2, 600, t, 19.1)
        pl = Image.new('RGBA', (620, 136), (0, 0, 0, 0)); d = ImageDraw.Draw(pl)
        d.rectangle((0, 0, 619, 135), fill=GOLD); s = 'booknote.uz'
        d.text(((620 - tw(s, PB(70))) / 2, 20), s, font=PB(70), fill=LAP1)
        put(fr, pl, W / 2, 780, t, 19.6, dur=0.3, slide=0, scale_from=0.8)
        pentagon(fr, t + 10, 0, W / 2, 1300, 150)

    d = ImageDraw.Draw(fr); d.text((70, 100), 'BookNote', font=font('PlayfairBold', 42), fill=CREAM)
    d.rectangle((0, 0, W * t / DUR, 8), fill=GOLD)
    return fr

def tabla(high=True):
    n = int(0.3 * SR); tt = np.arange(n) / SR
    f = (330 if high else 95) * (1 + 0.25 * np.exp(-tt * 40))
    s = np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * (14 if high else 8))
    return s + 0.2 * noise(0.3)[:n] * np.exp(-tt * 60)

def audio():
    m = Mix(DUR)
    m.add(reverb(pad([45, 52, 57], DUR + 1, 'saw', 500, a=0.8, r=3, gain=0.22), 0.4, 2.8), 0)
    # tabla groove, 96 bpm, 8 steps per bar
    s = 60 / 96 / 2; pat = [(0, False), (2, True), (3, True), (4, False), (6, True), (7, True)]
    bar = 0; tt0 = 4.4
    while tt0 < DUR - 1.5:
        for st, hi in pat:
            if tt0 + st * s < DUR - 1.5: m.add(tabla(hi), tt0 + st * s, 0.32 if hi else 0.5, 0.25 if hi else -0.1)
        tt0 += 8 * s; bar += 1
    # chang arpeggios, A minor pentatonic-ish
    chords = [[57, 60, 64, 69, 72], [55, 59, 62, 67, 71], [53, 57, 60, 65, 69], [52, 56, 59, 64, 68]]
    tt = 0.2; k = 0
    while tt < DUR - 1.8:
        ch = chords[(k // 10) % 4]; n = ch[[0, 2, 4, 3, 1, 2, 4, 3, 2, 1][k % 10]]
        m.add(reverb(pluck(midi(n + 12), 1.2, 0.996), 0.4, 2.0), tt, 0.22, 0.4 * math.sin(k))
        tt += s; k += 1
    for k in range(5): m.add(reverb(chime(76 + [0, 3, 5, 7, 10][k], 2.5), 0.5), 5.2 + k * 0.55, 0.11)
    for tt in (4.45, 10.05, 14.65): m.add(reverb(whoosh(0.5), 0.3), tt - 0.3, 0.16)
    m.add(reverb(chime(81, 3.0), 0.6), 19.6, 0.12)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [0.0, 8.5, 13.0, 17.5, 21.0], os.path.join(S, 'prevW.png'))
    else:
        render('W_navoiy_xamsa_2_yil', draw, DUR, audio); print('done W')
