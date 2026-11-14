import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

# Style: kimxob (brocade) - deep wine red, gold pattern woven line by line; loom rhythm, rubob pluck, drone.
DUR = 22.0
WINE1 = (58, 10, 22); WINE2 = (110, 20, 38); GOLD = (236, 186, 92); CREAM = (250, 236, 210); ROSE = (240, 150, 140)

BG = gradient(W, H, WINE1, WINE2)
BG.alpha_composite(vignette(W, H, 0.7))

def _pattern():
    """Gold lattice of lozenges + 8-point stars; drawn row by row via a mask."""
    l = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    step = 180
    for gy in range(-step, H + step, step):
        for gx in range(-step, W + step, step):
            ox = gx + (step // 2 if (gy // step) % 2 else 0)
            c = (ox, gy)
            d.polygon([(c[0], c[1] - 70), (c[0] + 70, c[1]), (c[0], c[1] + 70), (c[0] - 70, c[1])], outline=GOLD + (70,), width=3)
            r1, r2 = 26, 12
            pts = []
            for k in range(16):
                a = math.pi * k / 8; r = r1 if k % 2 == 0 else r2
                pts.append((c[0] + r * math.cos(a), c[1] + r * math.sin(a)))
            d.polygon(pts, fill=GOLD + (55,))
    return l
PAT = _pattern()

def woven(fr, p):
    """reveal pattern from top to bottom like a loom (p 0..1)."""
    if p <= 0: return
    y = int(H * clamp(p))
    m = Image.new('L', (W, H), 0); ImageDraw.Draw(m).rectangle((0, 0, W, y), fill=255)
    l = PAT.copy(); l.putalpha(ImageChops.multiply(l.split()[3], m)); fr.alpha_composite(l)
    if p < 1: ImageDraw.Draw(fr).line((0, y, W, y), fill=GOLD + (200,), width=4)  # shuttle line

def panel(fr, y0, y1, a=200):
    o = Image.new('RGBA', (W, H), (0, 0, 0, 0)); ImageDraw.Draw(o).rectangle((40, y0, W - 40, y1), fill=(30, 4, 12, a))
    fr.alpha_composite(o)

def draw(t):
    fr = BG.copy()
    woven(fr, 0.35 + t / 12)
    PB = lambda s: font('PlayfairBlack', s); PBo = lambda s: font('PlayfairBold', s); PI = lambda s: font('PlayfairItalic', s); G = lambda s: font('GroteskMed', s); CI = lambda s: font('CormorantItalic', s)

    if t < 4.4:
        panel(fr, 260, 1240)
        put(fr, text_layer('Uning butun yo\'li', PI(80), GOLD), W / 2, 320, t, -1)
        put(fr, text_layer('bir jumlaga sig\'adi.', PB(104), CREAM, maxw=W - 100), W / 2, 430, t, -1)
        put(fr, text_layer('"Dil ba yoru,\ndast ba kor."', CI(108), GOLD, maxw=W - 120), W / 2, 820, t, -1)

    if 4.4 <= t < 9.0:
        panel(fr, 280, 1260)
        put(fr, text_layer('Bahouddin Naqshband', PB(92), CREAM, maxw=W - 120), W / 2, 340, t, 4.45, dur=0.3, out_t=8.7)
        put(fr, text_layer('Buxoro, 1318-1389', G(52), GOLD), W / 2, 610, t, 4.9, out_t=8.7)
        put(fr, text_layer('"Naqshband" - "naqsh bog\'lovchi" degani. Rivoyatlarga ko\'ra, oilasi kimxobga naqsh solgan.', PI(62), ROSE, maxw=W - 180), W / 2, 790, t, 5.6, out_t=8.7)

    if 9.0 <= t < 14.0:
        panel(fr, 280, 1360)
        put(fr, text_layer('Dil ba yor', PB(96), GOLD), W / 2, 330, t, 9.05, dur=0.3, out_t=13.7)
        put(fr, text_layer('ko\'ngil Alloh bilan', PI(64), CREAM), W / 2, 460, t, 9.4, out_t=13.7)
        put(fr, text_layer('Dast ba kor', PB(96), GOLD), W / 2, 640, t, 10.4, dur=0.3, out_t=13.7)
        put(fr, text_layer('qo\'l esa mehnatda', PI(64), CREAM), W / 2, 770, t, 10.75, out_t=13.7)
        put(fr, text_layer('Dunyodan qochish emas: odamlar orasida, ish ustida ham qalb hushyor bo\'lsin.', G(50), ROSE, maxw=W - 200), W / 2, 980, t, 11.9, out_t=13.7)

    if 14.0 <= t < 18.4:
        panel(fr, 300, 1240)
        put(fr, text_layer('Naqshbandiya tariqati', PB(84), CREAM, maxw=W - 120), W / 2, 360, t, 14.05, dur=0.3, out_t=18.1)
        put(fr, text_layer('Hindistondan Usmonli yurtlarigacha tarqaldi.', PI(66), GOLD, maxw=W - 160), W / 2, 500, t, 14.6, out_t=18.1)
        put(fr, text_layer('Maqbarasi Buxoro yonidagi Qasri Orifonda. Bugun ham u yerga minglab odam keladi.', G(50), ROSE, maxw=W - 200), W / 2, 830, t, 15.8, out_t=18.1)

    if t >= 18.4:
        panel(fr, 300, 1200)
        put(fr, text_layer('Siz "Dil ba yoru, dast ba kor"ni qanday tushunasiz?', PBo(72), CREAM, maxw=W - 140), W / 2, 360, t, 18.45, dur=0.3)
        put(fr, text_layer('Kommentda yozing.', PI(60), GOLD), W / 2, 680, t, 19.0)
        pl = Image.new('RGBA', (620, 136), (0, 0, 0, 0)); d = ImageDraw.Draw(pl)
        d.rectangle((0, 0, 619, 135), fill=GOLD); s = 'booknote.uz'
        d.text(((620 - tw(s, PB(70))) / 2, 20), s, font=PB(70), fill=WINE1)
        put(fr, pl, W / 2, 900, t, 19.5, dur=0.3, slide=0, scale_from=0.8)

    d = ImageDraw.Draw(fr); d.text((70, 100), 'BookNote', font=font('PlayfairBold', 42), fill=CREAM)
    d.rectangle((0, 0, W * t / DUR, 8), fill=GOLD)
    return fr

def loom():
    """wooden clack of a loom beater"""
    n = int(0.12 * SR); tt = np.arange(n) / SR
    s = np.sin(2 * np.pi * 420 * tt) * np.exp(-tt * 60) + 0.6 * noise(0.12)[:n] * np.exp(-tt * 90)
    return lowpass(s, 2500)

def audio():
    m = Mix(DUR)
    m.add(reverb(pad([38, 45], DUR + 1, 'saw', 420, a=1.0, r=3, gain=0.26), 0.4, 2.5), 0)  # D drone
    # loom in 6/8 at ~ 84 bpm (eighth = 0.238s): beat on 1 and 4
    e = 60 / 84 / 2
    k = 0; tt = 0.0
    while tt < DUR - 1.5:
        if k % 6 == 0: m.add(loom(), tt, 0.5, -0.3)
        elif k % 6 == 3: m.add(loom(), tt, 0.32, 0.3)
        elif k % 6 == 5: m.add(tick(), tt, 0.12)
        if k % 12 == 0 and tt > 4.3: m.add(lowpass(kick(), 120), tt, 0.5)
        tt += e; k += 1
    # rubob melody, D hijaz (D Eb F# G A Bb C)
    sc = [62, 63, 66, 67, 69, 70, 72, 74]
    mel = [4, 3, 2, 1, 2, 3, 2, 1, 0, 0, 1, 2, 4, 5, 4, 3, 2, 3, 1, 0, 2, 1, 0, 0]
    tt = 0.3
    for i, ix in enumerate(mel):
        if tt > DUR - 2.5: break
        dd = e * (3 if i % 4 == 3 else 2) * 1.0
        m.add(reverb(pluck(midi(sc[ix]), dd + 0.6, 0.997), 0.35, 1.8), tt, 0.35, 0.15 * math.sin(i))
        tt += dd
    for tt in (0.0, 4.45, 9.05, 14.05): m.add(reverb(whoosh(0.5), 0.3), max(0, tt - 0.3), 0.18)
    m.add(reverb(chime(74, 3.0), 0.6), 4.5, 0.12)
    m.add(reverb(chime(81, 3.0), 0.6), 19.5, 0.12)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [0.0, 8.0, 12.8, 17.5, 21.0], os.path.join(S, 'prevU.png'))
    else:
        render('U_naqshband_dil_ba_yor', draw, DUR, audio); print('done U')
