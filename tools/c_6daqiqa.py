import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

DUR = 34.0
CREAM = (246, 241, 231); INK = (29, 29, 31); CORAL = (226, 85, 59); GREY = (150, 145, 138); SAGE = (120, 150, 125); LINE = (226, 219, 205)
BG = Image.new('RGBA', (W, H), CREAM + (255,))
_g = ImageDraw.Draw(BG)
for x in range(0, W, 60): _g.line((x, 0, x, H), fill=(238, 232, 220), width=1)
for y in range(0, H, 60): _g.line((0, y, W, y), fill=(238, 232, 220), width=1)

IS = lambda s: font('Instrument', s); ISI = lambda s: font('InstrumentItalic', s); GR = lambda s: font('Grotesk', s); GM = lambda s: font('GroteskMed', s)

def draw(t):
    fr = BG.copy(); d = ImageDraw.Draw(fr)

    # 0-5: hook
    if t < 5.2:
        put(fr, text_layer('Stressni 68% ga kamaytirish uchun', GM(52), INK, maxw=W - 100), W / 2, 560, t, 0.2, out_t=4.9)
        put(fr, text_layer('6 daqiqa', IS(260), CORAL), W / 2, 690, t, 0.8, dur=0.7, slide=0, scale_from=1.15, out_t=4.9)
        put(fr, text_layer('yetarli ekan.', ISI(96), INK), W / 2, 990, t, 1.6, out_t=4.9)
        put(fr, text_layer('Qanday qilib?', GM(44), GREY), W / 2, 1180, t, 2.8, out_t=4.9)

    # 5.2-11: timer
    if 5.2 <= t < 11.2:
        lt = t - 5.2
        a = clamp(lt / 0.5) * (1 - clamp((t - 10.8) / 0.4))
        cx, cy, r = W / 2, 860, 300
        prog = ease_io((lt - 0.6) / 4.2)
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        dl.ellipse((cx - r, cy - r, cx + r, cy + r), outline=LINE, width=26)
        if prog > 0: dl.arc((cx - r, cy - r, cx + r, cy + r), -90, -90 + 360 * (1 - prog), fill=CORAL, width=26)
        for k in range(60):
            ang = math.radians(k * 6 - 90); r1 = r - 50 - (14 if k % 5 == 0 else 0)
            dl.line((cx + (r - 40) * math.cos(ang), cy + (r - 40) * math.sin(ang), cx + r1 * math.cos(ang), cy + r1 * math.sin(ang)), fill=GREY if k % 5 else INK, width=3)
        secs = int(360 * (1 - prog)); s = '%d:%02d' % (secs // 60, secs % 60)
        f = IS(170); dl.text((cx - tw(s, f) / 2, cy - 110), s, font=f, fill=INK, features=['lnum'])
        fr.alpha_composite(fade(lay, a))
        put(fr, text_layer('Kitob o\'qing. Atigi 6 daqiqa.', GR(60), INK, maxw=W - 160), W / 2, 380, t, 5.3, out_t=10.8)
        put(fr, text_layer('Yurak urishi sekinlashadi, mushaklar bo\'shashadi', GM(42), GREY, maxw=W - 240), W / 2, 1240, t, 7.0, out_t=10.8)

    # 11.2-21: bar chart
    if 11.2 <= t < 21.2:
        lt = t - 11.2
        out = 1 - clamp((t - 20.8) / 0.4)
        put(fr, text_layer('Stressni qancha kamaytiradi?', GR(66), INK, maxw=W - 160), W / 2, 330, t, 11.3, out_t=20.8)
        put(fr, text_layer('Sussex universiteti tadqiqoti, 2009', GM(36), GREY), W / 2, 535, t, 11.6, out_t=20.8)
        rows = [('Kitob o\'qish', 68, CORAL), ('Musiqa tinglash', 61, INK), ('Bir piyola choy', 54, INK), ('Sayr qilish', 42, INK), ('Video o\'yin', 21, INK)]
        x0, maxw = 110, W - 220
        for i, (lab, v, col) in enumerate(rows):
            t0 = 12.4 + i * 0.9 if i else 16.8  # reading last for suspense
            y = 680 + i * 190
            lay = Image.new('RGBA', (W, 180), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
            dl.text((x0, 0), lab, font=GR(46) if i == 0 else GM(44), fill=col)
            dl.rounded_rectangle((x0, 70, x0 + maxw, 120), radius=25, fill=LINE)
            p = ease((t - t0 - 0.2) / 1.0)
            if p > 0:
                dl.rounded_rectangle((x0, 70, x0 + max(50, int(maxw * v / 100 * p)), 120), radius=25, fill=col if i == 0 else (90, 88, 85))
                s = '%d%%' % int(v * p); f = IS(84) if i == 0 else IS(70)
                dl.text((x0 + maxw - tw(s, f), -20 if i == 0 else -12), s, font=f, fill=col, features=['lnum'])
            vis = clamp((t - t0) / 0.4) * out
            if vis > 0: fr.alpha_composite(fade(lay, vis), (0, y))
        if t > 18.2:
            put(fr, text_layer('O\'qish musiqadan ham, choydan ham kuchliroq.', ISI(60), INK, maxw=W - 200), W / 2, 1640, t, 18.2, out_t=20.8)

    # 21.2-28: year in dots
    if 21.2 <= t < 28.2:
        lt = t - 21.2
        out = 1 - clamp((t - 27.8) / 0.4)
        put(fr, text_layer('Kuniga 6 daqiqa', IS(110), INK), W / 2, 300, t, 21.3, out_t=27.8)
        cols, rows_ = 25, 15; gap = 34; gx = (W - (cols - 1) * gap) / 2; gy = 520
        filled = int(365 * ease_io((lt - 0.5) / 2.6))
        lay = Image.new('RGBA', (W, H), (0, 0, 0, 0)); dl = ImageDraw.Draw(lay)
        for k in range(365):
            x = gx + (k % cols) * gap; y = gy + (k // cols) * gap
            dl.ellipse((x - 10, y - 10, x + 10, y + 10), fill=CORAL if k < filled else LINE)
        fr.alpha_composite(fade(lay, clamp(lt / 0.4) * out))
        put(fr, text_layer('= yiliga 36 soat', GR(70), INK), W / 2, 1060, t, 24.0, out_t=27.8)
        # books
        for i in range(8):
            bk = Image.new('RGBA', (70, 170), (0, 0, 0, 0)); dl = ImageDraw.Draw(bk)
            dl.rounded_rectangle((0, 0, 69, 169), radius=8, fill=[CORAL, INK, SAGE, (200, 160, 80)][i % 4])
            dl.line((12, 30, 57, 30), fill=CREAM, width=3); dl.line((12, 140, 57, 140), fill=CREAM, width=3)
            put(fr, bk, W / 2 - 4 * 86 + 43 + i * 86, 1220, t, 25.0 + i * 0.12, dur=0.35, slide=60, out_t=27.8)
        put(fr, text_layer('= taxminan 8 ta kitob', ISI(78), CORAL), W / 2, 1420, t, 26.0, out_t=27.8)
        put(fr, text_layer('o\'rtacha 270 bet, daqiqasiga 1 bet hisobida', GM(34), GREY), W / 2, 1530, t, 26.3, out_t=27.8)

    # 28.2-34: CTA
    if t >= 28.2:
        put(fr, text_layer('Bugundan boshlang.', IS(130), INK, maxw=W - 120), W / 2, 520, t, 28.3)
        put(fr, text_layer('BookNote\'da har kuni o\'qiganingizni belgilang va o\'qish seriyangizni (streak) uzmang.', GM(46), GREY, maxw=W - 220), W / 2, 760, t, 28.9)
        # streak flames row
        for i in range(7):
            on = t > 29.6 + i * 0.18
            c = Image.new('RGBA', (110, 140), (0, 0, 0, 0)); dl = ImageDraw.Draw(c)
            dl.rounded_rectangle((5, 5, 105, 105), radius=26, fill=CORAL if on else LINE)
            dd = ['Du', 'Se', 'Ch', 'Pa', 'Ju', 'Sh', 'Ya'][i]; dl.text((55 - tw(dd, GR(36)) / 2, 33), dd, font=GR(36), fill=CREAM if on else GREY)
            put(fr, c, W / 2 - 3 * 130 + i * 130, 1010, t, 29.4 + i * 0.05, dur=0.3)
        pl = Image.new('RGBA', (600, 130), (0, 0, 0, 0)); dl = ImageDraw.Draw(pl)
        dl.rounded_rectangle((0, 0, 599, 129), radius=65, fill=INK); s = 'booknote.uz'
        dl.text(((600 - tw(s, GR(62))) / 2, 26), s, font=GR(62), fill=CREAM)
        put(fr, pl, W / 2, 1230, t, 31.2, dur=0.6, scale_from=0.85)

    d = ImageDraw.Draw(fr)
    d.text((70, 100), 'BookNote', font=GR(44), fill=INK)
    d.rounded_rectangle((W - 70 - tw('o\'qish ilmi', GM(32)) - 40, 96, W - 70, 150), radius=27, outline=INK, width=2)
    d.text((W - 70 - tw('o\'qish ilmi', GM(32)) - 20, 104), 'o\'qish ilmi', font=GM(32), fill=INK)
    return fr

def rhodes(m_, dur):
    t = np.arange(int(dur * SR)) / SR; f = midi(m_)
    s = (np.sin(2 * np.pi * f * t) + 0.25 * np.sin(2 * np.pi * f * 2 * t) * np.exp(-t * 3) + 0.15 * np.sin(2 * np.pi * f * 7 * t) * np.exp(-t * 12))
    s *= np.exp(-t * 0.9) * (1 + 0.12 * np.sin(2 * np.pi * 4.5 * t))
    a = int(0.01 * SR); s[:a] *= np.linspace(0, 1, a); r = int(0.3 * SR); s[-r:] *= np.linspace(1, 0, r)
    return s

def audio():
    m = Mix(DUR)
    bpm = 80; beat = 60 / bpm; bar = beat * 4
    chords = [[53, 57, 60, 64], [52, 55, 59, 62], [50, 53, 57, 60], [48, 52, 55, 59]]  # Fmaj7 Em7 Dm7 Cmaj7
    for b in range(int(DUR / bar) + 1):
        t0 = b * bar; ch = chords[b % 4]
        for j, n in enumerate(ch): m.add(rhodes(n, bar + 0.4), t0 + j * 0.015, 0.09)
        m.add(rhodes(ch[0] - 12, bar), t0, 0.12)
        if 5.0 < t0 < 30:
            for k in range(4):
                tt = t0 + k * beat
                if k in (0, 2): m.add(lowpass(kick(), 160), tt, 0.5)
                if k in (1, 3): m.add(lowpass(highpass(noise(0.2), 400) * np.exp(-np.linspace(0, 14, int(0.2 * SR))), 3000), tt, 0.16)
                m.add(lowpass(hat(0.04), 6000), tt + beat / 2, 0.06, pan=0.3)
    # vinyl crackle
    cr = np.zeros(int(DUR * SR)); idx = np.random.randint(0, len(cr), 900); cr[idx] = np.random.uniform(-1, 1, 900)
    m.add(lowpass(cr, 4000) + lowpass(noise(DUR), 900) * 0.01, 0, 0.35)
    # clock ticks during timer
    tt = 5.8
    while tt < 10.8: m.add(tick(), tt, 0.35); tt += 0.25
    # bar landing pops
    for i in range(5):
        t0 = 12.4 + i * 0.9 if i else 16.8
        m.add(reverb(chime(76 + [12, 7, 5, 4, 0][i], 1.2), 0.3), t0 + 1.0, 0.12 if i else 0.2)
    # dots fill shimmer, streak pops
    m.add(whoosh(2.6, True), 21.7, 0.25)
    for i in range(7): m.add(chime(72 + [0, 2, 4, 5, 7, 9, 12][i], 0.6), 29.6 + i * 0.18, 0.08)
    m.add(reverb(chime(84, 2.5), 0.4), 31.2, 0.15)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [3.5, 8.5, 19.5, 27.0, 33.5], os.path.join(S, 'prevC.png'))
    else:
        render('C_6_daqiqa_oqish', draw, DUR, audio); print('done C')
