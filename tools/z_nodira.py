import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

# Style: ivory-rose garden page with falling rose petals that darken to plum at the tragedy; harp + soft "aah" choir.
DUR = 22.0
IV = (250, 240, 236); ROSE1 = (244, 206, 210); PLUM = (70, 22, 48); PLUM2 = (120, 40, 70); CRIM = (196, 40, 74); INK = (60, 20, 40); PINK = (255, 190, 205)

BG_L = gradient(W, H, IV, ROSE1)
BG_D = gradient(W, H, PLUM, PLUM2); BG_D.alpha_composite(vignette(W, H, 0.6))
_rs = np.random.RandomState(11)
PET = [(_rs.rand() * W, _rs.rand() * H, 14 + _rs.rand() * 16, _rs.rand() * 6.28, 40 + _rs.rand() * 60) for _ in range(34)]

def petals(fr, t, col):
    l = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    for x, y, r, ph, sp in PET:
        yy = (y + t * sp) % (H + 60) - 30; xx = x + 30 * math.sin(t * 0.8 + ph)
        rot = math.sin(t + ph)
        d.ellipse((xx - r, yy - r * (0.5 + 0.3 * rot), xx + r, yy + r * (0.5 + 0.3 * rot)), fill=col + (150 if yy > 1050 else 45,))
    fr.alpha_composite(l)

def dark_amt(t):
    return ease_io(clamp((t - 9.2) / 0.8)) * (1 - ease_io(clamp((t - 14.2) / 1.0)) * 0.0)

def draw(t):
    k = dark_amt(t)
    fr = Image.blend(BG_L, BG_D, k) if 0 < k < 1 else (BG_D.copy() if k >= 1 else BG_L.copy())
    petals(fr, t, CRIM if k < 0.5 else PINK)
    PB = lambda s: font('PlayfairBlack', s); PBo = lambda s: font('PlayfairBold', s); PI = lambda s: font('PlayfairItalic', s); G = lambda s: font('GroteskMed', s); CI = lambda s: font('CormorantItalic', s)
    TX = INK if k < 0.5 else IV; AC = CRIM if k < 0.5 else PINK

    if t < 4.4:
        put(fr, text_layer('U malika edi. Shoira edi.', PI(80), CRIM, maxw=W - 120), W / 2, 320, t, -1)
        put(fr, text_layer('Uni o\'g\'illari bilan birga qatl etishdi.', PB(98), INK, maxw=W - 100), W / 2, 450, t, -1)

    if 4.4 <= t < 9.2:
        put(fr, text_layer('Nodirabegim', PB(110), INK), W / 2, 330, t, 4.45, dur=0.3, out_t=8.9)
        put(fr, text_layer('1792-1842, Qo\'qon', G(54), CRIM), W / 2, 500, t, 4.9, out_t=8.9)
        put(fr, text_layer('O\'zbek va fors tillarida she\'r yozdi. Taxalluslari: Nodira, Komila, Maknuna.', PI(62), INK, maxw=W - 170), W / 2, 640, t, 5.5, out_t=8.9)

    if 9.2 <= t < 14.4:
        put(fr, text_layer('1842-yil.', G(60), PINK), W / 2, 300, t, 9.6, dur=0.3, out_t=14.1)
        put(fr, text_layer('Buxoro amiri Nasrulloxon Qo\'qonni egalladi.', PBo(76), IV, maxw=W - 140), W / 2, 440, t, 9.9, out_t=14.1)
        put(fr, text_layer('Nodira o\'g\'illari bilan birga o\'ldirildi.', PI(70), PINK, maxw=W - 160), W / 2, 760, t, 11.4, out_t=14.1)

    if 14.4 <= t < 18.6:
        put(fr, text_layer('Ammo uning devoni saqlanib qoldi.', PB(88), IV, maxw=W - 120), W / 2, 340, t, 14.45, dur=0.3, out_t=18.3)
        put(fr, text_layer('Bugun ham Nodiraning g\'azallari kitob bo\'lib o\'qiladi.', PI(66), PINK, maxw=W - 170), W / 2, 680, t, 15.7, out_t=18.3)

    if t >= 18.6:
        put(fr, text_layer('Siz o\'zbek shoiralaridan kimni o\'qigansiz?', PBo(78), IV, maxw=W - 140), W / 2, 360, t, 18.65, dur=0.3)
        put(fr, text_layer('Kommentda yozing.', PI(60), PINK), W / 2, 610, t, 19.1)
        pl = Image.new('RGBA', (620, 136), (0, 0, 0, 0)); d = ImageDraw.Draw(pl)
        d.rectangle((0, 0, 619, 135), fill=PINK); s = 'booknote.uz'
        d.text(((620 - tw(s, PB(70))) / 2, 20), s, font=PB(70), fill=PLUM)
        put(fr, pl, W / 2, 780, t, 19.6, dur=0.3, slide=0, scale_from=0.8)

    d = ImageDraw.Draw(fr); d.text((70, 100), 'BookNote', font=font('PlayfairBold', 42), fill=TX)
    d.rectangle((0, 0, W * t / DUR, 8), fill=AC)
    return fr

def aah(ms, dur, gain=0.2):
    n = int(dur * SR); tt = np.arange(n) / SR; s = np.zeros(n)
    for m_ in ms:
        f = midi(m_) * (1 + 0.006 * np.sin(2 * np.pi * 5 * tt + m_))
        ph = np.cumsum(f) / SR
        s += sum(np.sin(2 * np.pi * ph * h) * a for h, a in ((1, 1), (2, 0.5), (3, 0.35), (4, 0.15)))
    s = lowpass(s / len(ms), 1400)
    return s * env_adsr(n, 0.8, 0.3, 0.9, 1.2) * gain

def audio():
    m = Mix(DUR)
    # harp arpeggios: bright (E major-ish) until 9.2, then E minor
    s = 0.19; tt = 0.1; k = 0
    while tt < DUR - 1.8:
        ch = [52, 56, 59, 64, 68, 71] if tt < 9.2 else ([52, 55, 59, 64, 67, 71] if tt < 14.4 else [48, 52, 55, 60, 64, 67])
        n = ch[[0, 1, 2, 3, 4, 5, 4, 3][k % 8]]
        m.add(reverb(pluck(midi(n + 12), 1.4, 0.997), 0.45, 2.2), tt, 0.22, 0.5 * math.sin(k * 0.7))
        tt += s; k += 1
    m.add(reverb(aah([64, 68, 71], 9.6, 0.16), 0.5, 3.0), 0)
    m.add(reverb(aah([64, 67, 71], 5.4, 0.2), 0.5, 3.0), 9.2)
    m.add(reverb(aah([60, 64, 67], 7.0, 0.18), 0.5, 3.0), 14.4)
    m.add(reverb(pad([40, 47], DUR + 1, 'sine', 400, a=1, r=3, gain=0.3), 0.4, 2.5), 0)
    m.add(reverb(lowpass(kick(), 70), 0.6, 3.5), 9.6, 0.8); m.add(reverb(lowpass(kick(), 70), 0.6, 3.5), 11.4, 0.6)
    m.add(reverb(chime(83, 3.0), 0.6), 19.6, 0.12)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [0.0, 8.0, 13.0, 17.5, 21.0], os.path.join(S, 'prevZ.png'))
    else:
        render('Z_nodira_devon', draw, DUR, audio); print('done Z')
