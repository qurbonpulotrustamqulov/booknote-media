import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

DUR = 35.0
BLACK = (6, 9, 13); CYAN = (60, 240, 208); WHITE = (240, 246, 250); DIM = (90, 110, 120); MAG = (255, 70, 140)
BEAT = 0.5  # 120 bpm

rng = random.Random(7)
# code rain columns
COLS = [(x, rng.uniform(0, H), rng.uniform(120, 340), [rng.choice('0123456789ABCDEF') for _ in range(40)]) for x in range(20, W, 54)]
MONO_S = font('Mono', 30)

def rain(frame, t, alpha=60):
    layer = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(layer)
    for x, y0, sp, chars in COLS:
        head = (y0 + t * sp) % (H + 600) - 300
        for k in range(14):
            y = head - k * 40
            if -40 < y < H:
                a = int(alpha * (1 - k / 14))
                d.text((x, y), chars[(k + int(t * 6)) % 40], font=MONO_S, fill=CYAN + (a,))
    frame.alpha_composite(layer)

SCAN = Image.new('RGBA', (W, H), (0, 0, 0, 0))
_sd = ImageDraw.Draw(SCAN)
for y in range(0, H, 4): _sd.line((0, y, W, y), fill=(0, 0, 0, 40))
VIG = vignette(W, H, 0.85)

def glitch(layer, amt):
    if amt <= 0: return layer
    r, g, b, a = layer.split()
    off = int(amt * 18)
    base = Image.new('RGBA', layer.size, (0, 0, 0, 0))
    red = Image.merge('RGBA', (r, Image.new('L', layer.size, 0), Image.new('L', layer.size, 0), a.point(lambda v: v * 0.8)))
    blu = Image.merge('RGBA', (Image.new('L', layer.size, 0), g, b, a.point(lambda v: v * 0.8)))
    base.alpha_composite(red, (min(layer.size[0] - 1, off), 0)); base.alpha_composite(blu, (0, 0))
    out = Image.new('RGBA', (layer.size[0] + off, layer.size[1]), (0, 0, 0, 0)); out.alpha_composite(base, (0, 0))
    # slice displacement
    for _ in range(3):
        y = rng.randint(0, max(1, layer.size[1] - 20)); h = rng.randint(6, 26)
        sl = out.crop((0, y, out.size[0], y + h)); out.paste((0, 0, 0, 0), (0, y, out.size[0], y + h)); out.alpha_composite(sl, (rng.randint(-off, off) % 8, y))
    return out

def gput(frame, layer, cx, y, t, t0, out_t=None, gl=0.18):
    g = 1 - clamp((t - t0) / gl)
    if out_t is not None and t > out_t: g = clamp((t - out_t) / gl)
    if t < t0 or (out_t is not None and t > out_t + gl): return
    l = glitch(layer, g) if g > 0.02 else layer
    if g > 0.6 and int(t * 60) % 2: return  # flicker
    frame.alpha_composite(l, (int(cx - l.size[0] / 2), int(y)))

def typed(text, f, fill, t, t0, cps=28, maxw=W - 140, cursor=True):
    n = int(max(0, t - t0) * cps)
    s = text if n >= len(text) else text[:n]
    show_cursor = cursor and (n < len(text) or int(t * 2.5) % 2 == 0)
    return text_layer(s + ('_' if show_cursor else ''), f, fill, maxw=maxw)

def draw(t):
    fr = Image.new('RGBA', (W, H), BLACK + (255,))
    rain(fr, t, 55 if t < 30 else 30)
    G = font('Grotesk', 82); GM = font('GroteskMed', 46); M = font('Mono', 44); MB = font('MonoBold', 150)

    # 0-4.5: hook
    if t < 4.6:
        HK = font('Grotesk', 92)
        fr.alpha_composite(typed('Telefoningizdagi', HK, WHITE, t, 0.2, cps=22, cursor=t < 1.0), ((W - text_layer('Telefoningizdagi_', HK, WHITE).size[0]) // 2, 560))
        if t > 0.95: fr.alpha_composite(typed('har bir ilova', HK, WHITE, t, 0.95, cps=22, cursor=t < 1.6), ((W - text_layer('har bir ilova_', HK, WHITE).size[0]) // 2, 670))
        if t > 1.7: gput(fr, text_layer('bir xorazmlik olimning', G, CYAN), W / 2, 830, t, 1.7, out_t=4.3)
        if t > 2.4: gput(fr, text_layer('ismini olib yuradi.', G, CYAN), W / 2, 930, t, 2.4, out_t=4.3)
        # phone outline icon
        ph = Image.new('RGBA', (220, 400), (0, 0, 0, 0)); d = ImageDraw.Draw(ph)
        d.rounded_rectangle((4, 4, 216, 396), radius=36, outline=CYAN + (200,), width=5)
        for i in range(3):
            for j in range(3): d.rounded_rectangle((34 + j * 56, 70 + i * 70, 78 + j * 56, 114 + i * 70), radius=10, fill=CYAN + (120 if (i + j + int(t * 4)) % 3 else 220,))
        put(fr, ph, W / 2, 1150, t, 2.9, out_t=4.2)

    # 4.5-9: year rewind
    if 4.5 <= t < 9.2:
        lt = t - 4.5
        yr = int(2026 - (2026 - 820) * ease_io(lt / 2.2))
        put(fr, text_layer('yil', GM, DIM), W / 2, 560, t, 4.5, out_t=8.9)
        gput(fr, text_layer(str(yr), MB, CYAN if lt > 2.2 else WHITE), W / 2, 640, t, 4.5, out_t=8.9)
        if lt > 2.4: put(fr, text_layer('Bag\'dod. "Bayt ul-Hikma"', font('Grotesk', 64), WHITE), W / 2, 900, t, 6.9, out_t=8.9)
        if lt > 2.9: put(fr, text_layer('o\'sha davrning eng yirik ilm markazlaridan biri', GM, DIM), W / 2, 1000, t, 7.4, out_t=8.9)

    # 9-14: name
    if 9.2 <= t < 14.2:
        put(fr, text_layer('Muhammad ibn Muso', font('GroteskMed', 60), DIM), W / 2, 640, t, 9.3, out_t=13.9)
        gput(fr, text_layer('AL-XORAZMIY', font('Grotesk', 128), WHITE), W / 2, 730, t, 9.6, out_t=13.9)
        if t > 10.8: put(fr, text_layer('Xorazmda tug\'ilgan matematik va astronom', GM, CYAN, maxw=W - 200), W / 2, 920, t, 10.8, out_t=13.9)
        if t > 11.8:
            bx = text_layer('Hind raqamlari bilan hisoblash haqida kitob yozdi', font('Mono', 38), WHITE, maxw=W - 220)
            put(fr, bx, W / 2, 1110, t, 11.8, out_t=13.9)

    # 14-21: algoritmi etymology chain
    if 14.2 <= t < 21.2:
        put(fr, text_layer('XII asr. Kitob lotinchaga tarjima qilindi:', GM, DIM, maxw=W - 160), W / 2, 420, t, 14.3, out_t=20.9)
        lat = typed('"Algoritmi de numero Indorum"', font('Mono', 46), WHITE, t, 14.8, cps=26, maxw=W - 120)
        fr.alpha_composite(fade(lat, clamp((20.9 - t) / 0.3)), ((W - text_layer('"Algoritmi de numero Indorum"__', font('Mono', 46), WHITE, maxw=W - 120).size[0]) // 2, 560))
        chain = [('al-Xorazmiy', WHITE), ('Algoritmi', CYAN), ('Algorithm', CYAN), ('ALGORITM', MAG)]
        for i, (w_, c) in enumerate(chain):
            t0 = 16.6 + i * 0.75
            y = 760 + i * 190
            if t >= t0:
                gput(fr, text_layer(w_, font('MonoBold', 84 if i < 3 else 110), c), W / 2, y, t, t0, out_t=20.9)
                if i < 3 and t > t0 + 0.35:
                    d = ImageDraw.Draw(fr); p = clamp((t - t0 - 0.35) / 0.3) * (1 - clamp((t - 20.9) / 0.3))
                    d.line((W / 2, y + 112, W / 2, y + 112 + 60 * p), fill=CYAN + (int(255 * p),), width=4)
                    if p > 0.95: d.polygon([(W / 2 - 14, y + 160), (W / 2 + 14, y + 160), (W / 2, y + 178)], fill=CYAN)

    # 21-26.5: algebra
    if 21.2 <= t < 26.6:
        put(fr, text_layer('Yana bir kitobi:', GM, DIM), W / 2, 520, t, 21.3, out_t=26.3)
        put(fr, text_layer('"al-Kitob al-muxtasar fi hisob al-jabr val-muqobala"', font('Mono', 40), WHITE, maxw=W - 180), W / 2, 610, t, 21.6, out_t=26.3)
        if t > 22.9:
            jl = text_layer('al-jabr', font('MonoBold', 96), CYAN)
            gput(fr, jl, W / 2, 860, t, 22.9, out_t=26.3)
        if t > 23.6:
            gput(fr, text_layer('ALGEBRA', font('Grotesk', 170), MAG), W / 2, 1020, t, 23.6, out_t=26.3)
        if t > 24.4: put(fr, text_layer('Bugun dunyoning har bir maktabida o\'qitiladi', GM, WHITE, maxw=W - 200), W / 2, 1270, t, 24.4, out_t=26.3)

    # 26.6-30.5: three beats
    if 26.6 <= t < 30.6:
        for i, (s, c) in enumerate([('1 ta kitob.', WHITE), ('1200 yil.', CYAN), ('Hali ham ishlayapti.', MAG)]):
            t0 = 26.7 + i * 0.9
            if t >= t0: gput(fr, text_layer(s, font('Grotesk', 104 if i < 2 else 86), c), W / 2, 640 + i * 170, t, t0, out_t=30.3)

    # 30.6-35: CTA
    if t >= 30.6:
        put(fr, text_layer('Kitoblar dunyoni o\'zgartiradi.', font('Grotesk', 70), WHITE, maxw=W - 160), W / 2, 560, t, 30.7)
        put(fr, text_layer('Siz hozir qaysi kitobni o\'qiyapsiz?', GM, CYAN, maxw=W - 200), W / 2, 760, t, 31.2)
        term = Image.new('RGBA', (820, 150), (0, 0, 0, 0)); d = ImageDraw.Draw(term)
        d.rounded_rectangle((0, 0, 819, 149), radius=22, fill=(16, 24, 30, 235), outline=CYAN + (180,), width=3)
        s = '> booknote.uz'; n = int(max(0, t - 31.9) * 16)
        d.text((44, 42), s[:n] + ('_' if int(t * 2.5) % 2 == 0 else ' '), font=font('MonoBold', 60), fill=CYAN)
        put(fr, term, W / 2, 960, t, 31.8)
        put(fr, text_layer('O\'qiganingizni yozib boring, baho bering, ulashing', font('GroteskMed', 40), DIM, maxw=W - 220), W / 2, 1160, t, 32.6)

    # brand + scanlines + vignette
    d = ImageDraw.Draw(fr)
    d.text((64, 96), 'BookNote', font=font('Grotesk', 42), fill=WHITE)
    d.text((64 + tw('BookNote', font('Grotesk', 42)) + 16, 106), '// faktlar', font=font('Mono', 32), fill=CYAN)
    fr.alpha_composite(SCAN); fr.alpha_composite(VIG)
    return fr

def audio():
    m = Mix(DUR)
    # driving bass arpeggio A minor - F - C - G, 16th notes at 120bpm
    prog = [(45, [57, 60, 64]), (41, [53, 57, 60]), (48, [55, 60, 64]), (43, [55, 59, 62])]
    sixteenth = BEAT / 4
    bar = BEAT * 4
    nbars = int(DUR / bar) + 1
    for b in range(nbars):
        root, chord = prog[b % 4]; t0 = b * bar
        start_full = t0 >= 4.5
        # pad
        m.add(pad(chord, bar + 0.6, 'saw', 1400 if start_full else 700, a=0.3, r=0.6, gain=0.11), t0)
        for k in range(16):
            tt = t0 + k * sixteenth
            if tt > DUR: break
            note = root + [0, 12, 7, 12][k % 4]
            s = osc(midi(note), sixteenth * 0.9, 'saw') * env_adsr(int(sixteenth * 0.9 * SR), 0.003, 0.05, 0.4, 0.03)
            m.add(lowpass(s, 900 + 600 * (k % 4 == 0)), tt, 0.16 if start_full else 0.08)
            if start_full and tt < 30.4:
                if k % 4 == 0: m.add(kick(), tt, 0.55)
                if k % 2 == 1: m.add(hat(), tt, 0.10, pan=0.3)
                if k in (4, 12): m.add(highpass(noise(0.18), 1500) * np.exp(-np.linspace(0, 10, int(0.18 * SR))), tt, 0.18)
    # glitch hits on scene changes
    for tt in (1.7, 2.4, 4.5, 9.6, 16.6, 17.35, 18.1, 18.85, 22.9, 23.6, 26.7, 27.6, 28.5):
        g = np.sign(np.sin(2 * np.pi * 1800 * np.arange(int(0.08 * SR)) / SR)) * np.random.uniform(0.3, 1, int(0.08 * SR))
        m.add(g * np.exp(-np.linspace(0, 6, len(g))), tt, 0.10, pan=random.uniform(-0.5, 0.5))
    # typing clicks
    for start, n, cps in ((14.8, 30, 26), (31.9, 13, 16)):
        for i in range(n): m.add(tick(), start + i / cps, 0.25, pan=random.uniform(-0.3, 0.3))
    for i in range(27): m.add(tick(), (0.2 + i / 22) if i < 16 else (0.95 + (i - 16) / 22), 0.25)
    # rewind riser
    m.add(whoosh(2.2, True), 4.5, 0.6)
    m.add(whoosh(0.9, False), 30.4, 0.5)
    # final chime
    m.add(reverb(chime(81, 3.0), 0.4), 31.8, 0.25)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [2.0, 3.6, 7.5, 12.5, 15.8, 20.0, 25.0, 29.0, 34.0], os.path.join(S, 'prevA.png'))
    else:
        render('A_xorazmiy_algoritm', draw, DUR, audio); print('done A')
