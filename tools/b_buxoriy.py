import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

DUR = 36.0
PAPER = (239, 227, 200); INK = (58, 36, 20); GOLD = (176, 128, 40); SOFT = (120, 92, 60); DEEPRED = (120, 30, 24)

# parchment texture
_rs = np.random.RandomState(3)
def _tex():
    base = np.array(PAPER, float)[None, None, :] * np.ones((H, W, 3))
    n = _rs.randn(H // 8, W // 8)
    n = np.array(Image.fromarray(((n - n.min()) / (n.max() - n.min()) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), float) / 255
    fine = _rs.randn(H, W) * 6
    base = base * (0.9 + 0.12 * n[..., None]) + fine[..., None]
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8), 'RGB').convert('RGBA')
    img.alpha_composite(vignette(W, H, 0.75, (70, 40, 15)))
    return img
PAPER_IMG = _tex()

def star8(size, col, width=3, alpha=255):
    l = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(l); c = size / 2
    for rr, ww in ((0.48, width), (0.34, max(1, width - 1))):
        r = size * rr
        for rot in (0, 45):
            pts = [(c + r * math.cos(math.radians(rot + 45 + 90 * k)), c + r * math.sin(math.radians(rot + 45 + 90 * k))) for k in range(4)]
            d.polygon(pts, outline=col + (alpha,), width=ww)
    d.ellipse((c - size * 0.2, c - size * 0.2, c + size * 0.2, c + size * 0.2), outline=col + (alpha,), width=max(1, width - 1))
    for k in range(16):
        a = math.radians(k * 22.5); r1, r2 = size * 0.2, size * 0.27
        d.line((c + r1 * math.cos(a), c + r1 * math.sin(a), c + r2 * math.cos(a), c + r2 * math.sin(a)), fill=col + (alpha,), width=max(1, width - 1))
    return l

BIGSTAR = star8(1500, GOLD, 4, 40)

def divider(w=420, col=GOLD):
    l = Image.new('RGBA', (w, 40), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    d.line((0, 20, w / 2 - 30, 20), fill=col, width=3); d.line((w / 2 + 30, 20, w, 20), fill=col, width=3)
    d.polygon([(w / 2, 6), (w / 2 + 14, 20), (w / 2, 34), (w / 2 - 14, 20)], fill=col)
    return l

PARTS = [(_rs.uniform(0, W), _rs.uniform(0, H), _rs.uniform(2, 6), _rs.uniform(10, 40), _rs.uniform(0, 6.28)) for _ in range(60)]

def dust(fr, t):
    l = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    for x, y, r, sp, ph in PARTS:
        yy = (y - t * sp) % H; xx = x + 20 * math.sin(t * 0.5 + ph)
        a = int(110 * (0.5 + 0.5 * math.sin(t * 1.3 + ph)))
        d.ellipse((xx - r, yy - r, xx + r, yy + r), fill=(205, 160, 70, a))
    fr.alpha_composite(l.filter(ImageFilter.GaussianBlur(1.5)))

def frame_border(fr, alpha=1.0):
    d = ImageDraw.Draw(fr)
    a = int(255 * alpha)
    d.rectangle((48, 48, W - 48, H - 48), outline=GOLD + (a,), width=3)
    d.rectangle((62, 62, W - 62, H - 62), outline=GOLD + (int(a * 0.5),), width=1)
    for (x, y) in ((48, 48), (W - 48, 48), (48, H - 48), (W - 48, H - 48)):
        d.polygon([(x, y - 18), (x + 18, y), (x, y + 18), (x - 18, y)], fill=GOLD + (a,))

def draw(t):
    # slow push-in
    fr = PAPER_IMG.copy()
    st = BIGSTAR.rotate(t * 3, resample=Image.BICUBIC)
    fr.alpha_composite(st, ((W - 1500) // 2, (H - 1500) // 2))
    dust(fr, t)
    PB = lambda s: font('PlayfairBlack', s); PI = lambda s: font('PlayfairItalic', s); C = lambda s: font('Cormorant', s); CI = lambda s: font('CormorantItalic', s)

    if t < 5.6:
        put(fr, text_layer('Bir kitob uchun', CI(86), INK), W / 2, 560, t, 0.3, dur=0.9, out_t=5.2, out_dur=0.5)
        put(fr, text_layer('16 yil', PB(250), GOLD), W / 2, 680, t, 1.1, dur=1.0, slide=0, scale_from=1.12, out_t=5.2, out_dur=0.5)
        put(fr, divider(), W / 2, 1010, t, 2.0, dur=0.8, slide=0, out_t=5.2)
        put(fr, text_layer('IX asr. Buxorolik olim va uning eng mashhur kitobi', C(52), SOFT, maxw=W - 260), W / 2, 1080, t, 2.4, dur=0.9, out_t=5.2, out_dur=0.5)

    if 5.6 <= t < 11.2:
        lt = t - 5.6
        n = int(600000 * ease_io(lt / 2.4)); n = (n // 1000) * 1000 if lt < 2.4 else 600000
        put(fr, text_layer('U o\'rgangan hadislar soni', CI(64), INK), W / 2, 560, t, 5.7, dur=0.7, out_t=10.8)
        put(fr, text_layer('{:,}'.format(n).replace(',', ' '), PB(196), GOLD), W / 2, 660, t, 5.8, dur=0.5, slide=0, out_t=10.8)
        put(fr, divider(), W / 2, 930, t, 8.0, slide=0, out_t=10.8)
        put(fr, text_layer('Muhammad ibn Ismoil al-Buxoriy', C(62), INK, maxw=W - 200), W / 2, 990, t, 8.2, dur=0.8, out_t=10.8)
        put(fr, text_layer('Buxoro, 810-yilda tug\'ilgan', CI(52), SOFT), W / 2, 1080, t, 8.6, dur=0.8, out_t=10.8)

    if 11.2 <= t < 17.8:
        d = ImageDraw.Draw(fr); p = ease((t - 11.3) / 1.0) * (1 - ease((t - 17.4) / 0.4))
        d.line((150, 560, 150, 560 + 620 * p), fill=GOLD + (int(255 * p),), width=5)
        _q = text_layer('Rivoyat qilinishicha,', CI(64), SOFT, align='l', maxw=W - 300); put(fr, _q, 180 + _q.size[0] / 2, 560, t, 11.4, dur=0.8, out_t=17.4)
        _q = text_layer('har bir hadisni kitobga yozishdan oldin', PI(66), INK, align='l', maxw=W - 300); put(fr, _q, 180 + _q.size[0] / 2, 660, t, 12.2, dur=0.9, out_t=17.4)
        _q = text_layer('g\'usl qilib, ikki rakat namoz o\'qigan.', PB(74), DEEPRED, align='l', maxw=W - 300); put(fr, _q, 180 + _q.size[0] / 2, 880, t, 13.6, dur=1.0, out_t=17.4)

    if 17.8 <= t < 24.4:
        lt = t - 17.8
        d = ImageDraw.Draw(fr)
        shrink = ease_io((lt - 1.4) / 2.0)
        r = 330 - 110 * shrink
        cx, cy = W / 2, 900
        a = int(255 * clamp(lt / 0.6) * (1 - clamp((t - 24.0) / 0.4)))
        d.ellipse((cx - r, cy - r, cx + r, cy + r), outline=GOLD + (a,), width=6)
        d.ellipse((cx - r + 18, cy - r + 18, cx + r - 18, cy + r - 18), outline=GOLD + (a // 2,), width=2)
        label = '600 000' if shrink < 0.5 else '7 000+'
        lay = text_layer(label, PB(int(130 - 40 * shrink)), INK if shrink < 0.5 else DEEPRED)
        fr.alpha_composite(fade(lay, a / 255), (int(cx - lay.size[0] / 2), int(cy - lay.size[1] / 2)))
        put(fr, text_layer('Ulardan faqat eng ishonchlilari tanlab olindi', CI(62), INK, maxw=W - 220), W / 2, 380, t, 17.9, dur=0.8, out_t=24.0)
        put(fr, text_layer('7 000 dan sal ko\'proq hadis kitobga kirdi (takrorlanganlari bilan)', C(48), SOFT, maxw=W - 260), W / 2, 1300, t, 20.6, dur=0.8, out_t=24.0)

    if 24.4 <= t < 30.4:
        frame_border(fr, clamp((t - 24.5) / 0.8) * (1 - clamp((t - 30.0) / 0.4)))
        put(fr, star8(220, GOLD, 4), W / 2, 450, t, 24.6, dur=0.8, slide=0, scale_from=0.6, out_t=30.0)
        put(fr, text_layer('"Sahihi Buxoriy"', PB(112), INK, maxw=W - 160), W / 2, 720, t, 25.0, dur=0.9, slide=20, out_t=30.0)
        put(fr, divider(500), W / 2, 900, t, 25.6, slide=0, out_t=30.0)
        put(fr, text_layer('Ahli sunnada Qur\'oni karimdan keyingi eng ishonchli kitob sanaladi', CI(60), SOFT, maxw=W - 240), W / 2, 970, t, 26.0, dur=0.9, out_t=30.0)
        put(fr, text_layer('12 asrdan beri o\'qilmoqda', C(54), GOLD), W / 2, 1220, t, 27.2, dur=0.9, out_t=30.0)

    if t >= 30.4:
        put(fr, text_layer('Siz qaysi kitobni', CI(72), INK), W / 2, 440, t, 30.5, dur=0.8)
        put(fr, text_layer('qayta-qayta o\'qiysiz?', PB(84), INK), W / 2, 530, t, 30.8, dur=0.8)
        put(fr, divider(), W / 2, 700, t, 31.3, slide=0)
        put(fr, text_layer('BookNote kitobxonlari 10 dan 10 bergan kitoblar:', C(48), SOFT, maxw=W - 240), W / 2, 770, t, 31.5)
        for i, b in enumerate(['Hadis va Hayot', 'Saodat Asri Qissalari', 'Amallar niyatga bog\'liqdir']):
            put(fr, text_layer(b, PI(60), DEEPRED), W / 2, 900 + i * 92, t, 32.0 + i * 0.35)
        pl = Image.new('RGBA', (560, 120), (0, 0, 0, 0)); d = ImageDraw.Draw(pl)
        d.rounded_rectangle((0, 0, 559, 119), radius=60, fill=INK); s = 'booknote.uz'; f = font('PlayfairBold', 58)
        d.text(((560 - tw(s, f)) / 2, 22), s, font=f, fill=PAPER)
        put(fr, pl, W / 2, 1230, t, 33.4, dur=0.7, scale_from=0.85)

    d = ImageDraw.Draw(fr)
    d.text((W / 2 - tw('BookNote', font('PlayfairBold', 40)) / 2, 100), 'BookNote', font=font('PlayfairBold', 40), fill=INK)
    d.text((W / 2 - tw('kitoblar tarixidan', font('CormorantItalic', 34)) / 2, 150), 'kitoblar tarixidan', font=font('CormorantItalic', 34), fill=SOFT)
    return fr

def audio():
    m = Mix(DUR)
    # Hijaz on D: D Eb F# G A Bb C
    D = 50
    hij = [0, 1, 4, 5, 7, 8, 10, 12]
    # drone
    dr = pad([D - 12, D - 5], DUR + 1, 'tri', 500, a=3.0, r=3.0, gain=0.5)
    m.add(reverb(dr, 0.3), 0)
    # second pad layer enters at 11s
    m.add(reverb(pad([D, D + 7], DUR - 11, 'saw', 700, a=4, r=3, gain=0.12), 0.4), 11)
    # oud-like melody (plucked), phrases
    phrase1 = [(0, 0.0), (1, 0.5), (4, 1.0), (5, 1.5), (4, 2.25), (1, 2.75), (0, 3.25)]
    phrase2 = [(7, 0.0), (8, 0.5), (7, 1.0), (5, 1.5), (4, 2.0), (5, 2.5), (4, 3.0), (1, 3.5), (0, 4.0)]
    starts = [(1.0, phrase1), (5.8, phrase2), (11.6, phrase1), (17.9, phrase2), (24.6, phrase1), (30.5, phrase2)]
    for st, ph in starts:
        for deg, off in ph:
            n = pluck(midi(D + 12 + hij[deg % 8 if deg < 8 else 7]), 1.6, 0.9965)
            m.add(reverb(n, 0.35, 1.4), st + off, 0.33, pan=-0.15)
    # frame drum: doum on beats from 5.6s, tek lighter
    bpm = 84; beat = 60 / bpm
    tt = 5.6
    while tt < DUR - 2:
        dt = tt - 5.6
        k = round(dt / beat) % 8
        if k in (0, 3, 6):
            m.add(lowpass(kick(), 220), tt, 0.5)
        elif k in (2, 5, 7):
            m.add(lowpass(hat(0.09), 3500), tt, 0.18, pan=0.2)
        tt += beat
    # shimmer at title reveal
    m.add(reverb(chime(86, 3.5), 0.5), 24.6, 0.18); m.add(reverb(chime(81, 3.0), 0.5), 33.4, 0.18)
    for tt in (5.5, 11.2, 17.8, 24.4, 30.4): m.add(whoosh(1.0, True), tt - 0.4, 0.25)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [3.5, 9.5, 15.5, 18.6, 23.0, 28.5, 35.0], os.path.join(S, 'prevB.png'))
    else:
        render('B_buxoriy_16_yil', draw, DUR, audio); print('done B')
