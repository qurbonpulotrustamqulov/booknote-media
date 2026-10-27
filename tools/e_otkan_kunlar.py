import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

DUR = 33.0
NEWS = (232, 225, 208); INK = (24, 22, 20); RED = (178, 34, 34); GREY = (110, 104, 96)

_rs = np.random.RandomState(11)
def _paper():
    base = np.ones((H, W, 3)) * np.array(NEWS)[None, None, :]
    base += _rs.randn(H, W)[..., None] * 7
    for _ in range(40):  # fibres / spots
        y, x = _rs.randint(0, H), _rs.randint(0, W); r = _rs.randint(1, 4)
        base[max(0, y - r):y + r, max(0, x - r):x + r] -= 25
    img = Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert('RGBA')
    img.alpha_composite(vignette(W, H, 0.5, (60, 45, 25)))
    return img
PAPER = _paper()

def rule(fr, y, x0=70, x1=W - 70, w=3, p=1.0):
    d = ImageDraw.Draw(fr); d.line((x0, y, x0 + (x1 - x0) * p, y), fill=INK, width=w)

def halftone_heart(size, p):
    """Dots forming a heart shape, revealed progressively."""
    l = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    step = 22; k = 0
    for yy in range(0, size, step):
        for xx in range(0, size, step):
            x = (xx - size / 2) / (size / 2.4); y = -(yy - size / 2.2) / (size / 2.4)
            v = (x * x + y * y - 1) ** 3 - x * x * y ** 3
            if v < 0:
                k += 1
                if (k * 37 % 100) / 100 < p:
                    r = 8 * min(1, -v * 4 + 0.4)
                    d.ellipse((xx - r, yy - r, xx + r, yy + r), fill=RED)
    return l

def jitter(t):  # old film gate weave
    return int(2 * math.sin(t * 23)), int(2 * math.cos(t * 17))

def draw(t):
    fr = PAPER.copy()
    PB = lambda s: font('PlayfairBlack', s); PBo = lambda s: font('PlayfairBold', s); PI = lambda s: font('PlayfairItalic', s); CB = lambda s: font('Cormorant', s); CI = lambda s: font('CormorantItalic', s)

    # masthead
    d = ImageDraw.Draw(fr)
    s = 'KITOB VAQTI'; d.text(((W - tw(s, PB(86))) / 2, 120), s, font=PB(86), fill=INK)
    rule(fr, 240, w=4); rule(fr, 250, w=1)
    meta = ['BookNote nashri', 'Toshkent', 'Narxi: bepul']
    d.text((80, 262), meta[0], font=CI(34), fill=GREY); d.text(((W - tw(meta[1], CI(34))) / 2, 262), meta[1], font=CI(34), fill=GREY)
    d.text((W - 80 - tw(meta[2], CI(34)), 262), meta[2], font=CI(34), fill=GREY)
    rule(fr, 315, w=1)

    if t < 6.0:
        put(fr, text_layer('FAVQULODDA YANGILIK', font('Grotesk', 44), RED), W / 2, 420, t, 0.2, dur=0.3, slide=0, out_t=5.7)
        put(fr, text_layer('Birinchi o\'zbek romani bosilib chiqdi!', PB(104), INK, maxw=W - 140), W / 2, 500, t, 0.6, dur=0.5, slide=0, scale_from=1.3, out_t=5.7)
        put(fr, text_layer('"O\'tkan kunlar". Muallif: Abdulla Qodiriy', PI(56), INK, maxw=W - 160), W / 2, 1000, t, 2.0, out_t=5.7)
        put(fr, text_layer('Bu sarlavha 100 yil oldin shunday yozilishi mumkin edi.', CI(48), GREY, maxw=W - 200), W / 2, 1160, t, 3.4, out_t=5.7)

    if 6.0 <= t < 12.5:
        put(fr, text_layer('1926', PB(300), INK), W / 2, 420, t, 6.1, dur=0.5, slide=0, scale_from=1.25, out_t=12.2)
        rule(fr, 790, 200, W - 200, 3, ease((t - 6.6) / 0.6) * (1 - clamp((t - 12.2) / 0.3)))
        put(fr, text_layer('Roman to\'liq kitob bo\'lib chiqdi. Undan oldin boblari jurnalda bosilib, qo\'lma-qo\'l o\'qilgan.', CB(58), INK, maxw=W - 200), W / 2, 830, t, 7.0, out_t=12.2)
        put(fr, text_layer('O\'zbek adabiyotida roman janri shu kitobdan boshlangan.', CI(56), RED, maxw=W - 200), W / 2, 1160, t, 9.2, out_t=12.2)

    if 12.5 <= t < 19.5:
        put(fr, text_layer('Voqealar', CI(64), GREY), W / 2, 400, t, 12.6, out_t=19.2)
        put(fr, text_layer('XIX asr o\'rtalari', PB(96), INK), W / 2, 470, t, 12.9, out_t=19.2)
        # two-column "city" box
        for i, (city, who) in enumerate([('TOSHKENT', 'Otabek'), ('MARG\'ILON', 'Kumush')]):
            box = Image.new('RGBA', (420, 300), (0, 0, 0, 0)); bd = ImageDraw.Draw(box)
            bd.rectangle((0, 0, 419, 299), outline=INK, width=3)
            bd.text(((420 - tw(city, font('Grotesk', 46))) / 2, 50), city, font=font('Grotesk', 46), fill=INK)
            bd.line((60, 130, 360, 130), fill=INK, width=1)
            bd.text(((420 - tw(who, PI(78))) / 2, 160), who, font=PI(78), fill=RED)
            put(fr, box, W / 2 + (i * 2 - 1) * 240, 700, t, 13.6 + i * 0.4, out_t=19.2)
        if t > 15.0:
            hh = halftone_heart(300, clamp((t - 15.0) / 1.5))
            fr.alpha_composite(fade(hh, 1 - clamp((t - 19.2) / 0.3)), ((W - 300) // 2, 1040))
        put(fr, text_layer('Sevgi, oila va jamiyat haqidagi roman', CI(58), INK, maxw=W - 200), W / 2, 1380, t, 16.0, out_t=19.2)

    if 19.5 <= t < 26.5:
        put(fr, text_layer('Muallif taqdiri', font('Grotesk', 46), RED), W / 2, 430, t, 19.6, out_t=26.2)
        put(fr, text_layer('Abdulla Qodiriy 1938-yilda qatag\'on qurboni bo\'ldi.', PB(78), INK, maxw=W - 160), W / 2, 520, t, 20.0, dur=0.6, out_t=26.2)
        rule(fr, 900, 300, W - 300, 2, ease((t - 21.2) / 0.5) * (1 - clamp((t - 26.2) / 0.3)))
        put(fr, text_layer('Kitoblari yillar davomida taqiqlandi.', CB(60), INK, maxw=W - 200), W / 2, 940, t, 21.6, out_t=26.2)
        put(fr, text_layer('Ammo "O\'tkan kunlar" bugun ham eng ko\'p o\'qiladigan o\'zbek romanlaridan biri.', PI(58), RED, maxw=W - 200), W / 2, 1110, t, 23.0, dur=0.8, out_t=26.2)

    if t >= 26.5:
        put(fr, text_layer('Siz "O\'tkan kunlar"ni o\'qiganmisiz?', PB(84), INK, maxw=W - 160), W / 2, 460, t, 26.6, dur=0.6)
        put(fr, text_layer('Unga 10 dan necha baho berasiz? Kommentda yozing.', CI(58), GREY, maxw=W - 220), W / 2, 720, t, 27.3)
        stamp = Image.new('RGBA', (560, 200), (0, 0, 0, 0)); sd = ImageDraw.Draw(stamp)
        sd.rounded_rectangle((6, 6, 553, 193), radius=18, outline=RED, width=7)
        s = 'booknote.uz'; sd.text(((560 - tw(s, PB(74))) / 2, 46), s, font=PB(74), fill=RED)
        st = stamp.rotate(-6, resample=Image.BICUBIC, expand=True)
        put(fr, st, W / 2, 980, t, 28.4, dur=0.25, slide=0, scale_from=1.6)
        put(fr, text_layer('O\'zbek kitobxonlari ijtimoiy tarmog\'i', CI(50), INK), W / 2, 1260, t, 29.2)

    # film weave + grain flicker
    dx, dy = jitter(t)
    if dx or dy: fr = ImageChops.offset(fr, dx, dy)
    return fr

def audio():
    m = Mix(DUR)
    # vintage: piano ragtime-ish waltz in D major through lowpass + crackle, 3/4 at 132 bpm
    from c_6daqiqa import rhodes
    beat = 60 / 132
    prog = [(50, [62, 66, 69]), (55, [62, 67, 71]), (57, [61, 64, 69]), (50, [62, 66, 69])]
    melody = [74, 76, 78, 81, 78, 76, 74, 73, 71, 69, 71, 73]
    tt, bar = 0.0, 0
    while tt < DUR:
        root, ch = prog[(bar // 2) % 4]
        m.add(lowpass(rhodes(root - 12, beat * 1.2), 1800), tt, 0.22)
        for k in (1, 2):
            for n in ch: m.add(lowpass(rhodes(n, beat * 0.8), 2200), tt + k * beat, 0.05)
        if 6.0 <= tt < 26.0:
            for k in range(3):
                n = melody[(bar * 3 + k) % len(melody)]
                m.add(lowpass(rhodes(n, beat * 1.1), 2600), tt + k * beat, 0.08)
        tt += beat * 3; bar += 1
    # gramophone hiss & crackle
    cr = np.zeros(int(DUR * SR)); idx = np.random.randint(0, len(cr), 1500); cr[idx] = np.random.uniform(-1, 1, 1500)
    m.add(lowpass(cr, 5000) + highpass(lowpass(noise(DUR), 6000), 1500) * 0.03, 0, 0.5)
    # printing press thunks at headline + stamp
    for tt in (0.6, 6.1, 28.4):
        k = lowpass(kick(), 300); nz = lowpass(noise(0.12), 1500) * np.exp(-np.linspace(0, 8, int(0.12 * SR))); k[:len(nz)] += nz
        m.add(k, tt, 0.7)
    # typewriter run under text
    for start, n in ((7.0, 22), (21.6, 18)):
        for i in range(n): m.add(tick(), start + i * 0.085 + random.uniform(0, 0.02), 0.22)
    m.add(chime(86, 1.0), start + 18 * 0.085 + 0.1, 0.1)
    # dramatic low note on author fate
    m.add(reverb(pad([38, 45], 6.0, 'saw', 400, a=1.0, r=2.0, gain=0.5), 0.4), 19.6)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [3.0, 10.5, 17.5, 24.5, 31.5], os.path.join(S, 'prevE.png'))
    else:
        render('E_otkan_kunlar_birinchi_roman', draw, DUR, audio); print('done E')
