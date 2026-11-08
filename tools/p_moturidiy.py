import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

DUR = 22.0
MARBLE = (244, 242, 236); BLACK = (24, 24, 28); GREY = (110, 110, 118); COBALT = (30, 70, 160); LIGHT = (205, 205, 212)

def _bg():
    rs = np.random.RandomState(31)
    n = rs.randn(H // 16, W // 16)
    n = np.array(Image.fromarray(((n - n.min()) / (n.max() - n.min()) * 255).astype(np.uint8)).resize((W, H), Image.BICUBIC), float) / 255
    veins = np.abs(np.sin((np.mgrid[0:H, 0:W][1] * 0.004 + np.mgrid[0:H, 0:W][0] * 0.002 + n * 6)))
    base = np.ones((H, W, 3)) * np.array(MARBLE)[None, None, :] - ((veins < 0.06) * 18)[..., None] - (n * 10)[..., None]
    return Image.fromarray(np.clip(base, 0, 255).astype(np.uint8)).convert('RGBA')
BG = _bg()

def rosette(size, t, alpha=255, n=8):
    l = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(l); c = size / 2
    rot = t * 6
    for ring, rr in enumerate((0.47, 0.33, 0.19)):
        r = size * rr
        for k in range(n):
            a1 = math.radians(rot * (1 if ring % 2 else -1) + k * 360 / n); a2 = a1 + math.radians(360 / n * 3)
            d.line((c + r * math.cos(a1), c + r * math.sin(a1), c + r * math.cos(a2), c + r * math.sin(a2)), fill=(COBALT if ring == 1 else BLACK) + (alpha,), width=3)
    d.ellipse((c - size * 0.06, c - size * 0.06, c + size * 0.06, c + size * 0.06), outline=COBALT + (alpha,), width=3)
    return l

def draw(t):
    fr = BG.copy()
    fr.alpha_composite(rosette(1300, t, 26), ((W - 1300) // 2, (H - 1300) // 2 + 200))
    PB = lambda s: font('PlayfairBlack', s); PBo = lambda s: font('PlayfairBold', s); PI = lambda s: font('PlayfairItalic', s); I = lambda s: font('Instrument', s); II = lambda s: font('InstrumentItalic', s); G = lambda s: font('GroteskMed', s)

    if t < 4.2:
        put(fr, text_layer('Uning asosiy kitobi', II(80), GREY, maxw=W - 160), W / 2, 420, t, -1)
        put(fr, text_layer('dunyoda bitta qo\'lyozmada qolgan.', PB(92), BLACK, maxw=W - 120), W / 2, 530, t, -1)
        put(fr, text_layer('U Angliyada, Kembrij universiteti kutubxonasida.', PBo(70), COBALT, maxw=W - 160), W / 2, 920, t, -1)

    if 4.2 <= t < 8.6:
        put(fr, text_layer('Imom Abu Mansur', II(78), GREY), W / 2, 400, t, 4.25, dur=0.3, out_t=8.3)
        put(fr, text_layer('al-Moturidiy', PB(140), BLACK), W / 2, 500, t, 4.4, dur=0.35, slide=0, scale_from=1.2, out_t=8.3)
        put(fr, text_layer('Samarqand, Moturid mahallasi. Taxminan 870-944-yillar.', G(50), GREY, maxw=W - 180), W / 2, 720, t, 5.0, out_t=8.3)

    if 8.6 <= t < 13.4:
        put(fr, rosette(300, t * 4), W / 2, 330, t, 8.65, dur=0.4, slide=0, scale_from=0.5, out_t=13.1)
        put(fr, text_layer('Aqidadagi moturidiya maktabi', PBo(76), BLACK, maxw=W - 140), W / 2, 680, t, 9.0, out_t=13.1)
        put(fr, text_layer('uning nomi bilan ataladi.', II(66), GREY), W / 2, 900, t, 9.6, out_t=13.1)
        put(fr, text_layer('Bugun dunyodagi millionlab hanafiy musulmonlar shu yo\'ldan boradi.', I(60), COBALT, maxw=W - 180), W / 2, 1020, t, 10.6, out_t=13.1)

    if 13.4 <= t < 18.0:
        books = [('"Kitob at-Tavhid"', 'aqida haqida asosiy asari'), ('"Ta\'vilot ahl as-sunna"', 'Qur\'oni karim tafsiri')]
        for i, (a, b) in enumerate(books):
            c = Image.new('RGBA', (900, 230), (0, 0, 0, 0)); d = ImageDraw.Draw(c)
            d.rectangle((0, 0, 899, 229), fill=(255, 255, 255, 200), outline=BLACK + (255,), width=3)
            d.rectangle((0, 0, 14, 229), fill=COBALT)
            d.text((50, 40), a, font=PBo(64), fill=BLACK); d.text((50, 140), b, font=G(42), fill=GREY)
            put(fr, c, W / 2, 380 + i * 280, t, 13.5 + i * 0.5, dur=0.3, slide=50, out_t=17.7)
        put(fr, text_layer('2000-yilda Samarqandda uning yodgorlik majmuasi barpo etildi.', I(56), BLACK, maxw=W - 180), W / 2, 1000, t, 15.0, out_t=17.7)

    if t >= 18.0:
        put(fr, text_layer('Samarqandga borsangiz, ziyorat qiling.', PB(84), BLACK, maxw=W - 140), W / 2, 400, t, 18.05, dur=0.3)
        put(fr, text_layer('Siz qaysi allomamiz kitobini o\'qigansiz? Kommentda yozing.', II(60), GREY, maxw=W - 200), W / 2, 780, t, 18.5)
        pl = Image.new('RGBA', (620, 136), (0, 0, 0, 0)); d = ImageDraw.Draw(pl)
        d.rectangle((0, 0, 619, 135), fill=BLACK); s = 'booknote.uz'
        d.text(((620 - tw(s, PB(70))) / 2, 20), s, font=PB(70), fill=MARBLE)
        put(fr, pl, W / 2, 1060, t, 19.2, dur=0.3, slide=0, scale_from=0.8)

    d = ImageDraw.Draw(fr); d.text((70, 100), 'BookNote', font=font('PlayfairBold', 42), fill=BLACK)
    d.rectangle((0, 0, W * t / DUR, 8), fill=COBALT)
    return fr

def choir(ms, dur, gain=0.2):
    # vowel 'aa' pad: saw through two formant bands (~730 Hz, ~1090 Hz)
    n = int(dur * SR); s = np.zeros(n)
    for m_ in ms:
        for dt in (-0.1, 0, 0.1): s += osc(midi(m_ + dt), dur, 'saw')[:n]
    s /= len(ms) * 3
    f1 = highpass(lowpass(s, 900), 600); f2 = highpass(lowpass(s, 1300), 950) * 0.5; body = lowpass(s, 400) * 0.6
    return (f1 + f2 + body) * env_adsr(n, 1.2, 0.3, 0.9, 1.5) * gain

def audio():
    m = Mix(DUR)
    chords = [[45, 52, 57, 60], [43, 50, 55, 59], [41, 48, 53, 57], [40, 47, 52, 56], [45, 52, 57, 60], [43, 50, 55, 62]]
    for i, ch in enumerate(chords):
        m.add(reverb(choir(ch, 4.6, 0.5), 0.6, 3.2), i * 3.8)
    for i in range(int(DUR / 1.9)):
        m.add(reverb(chime([69, 72, 76, 74][i % 4], 2.0), 0.5, 2.5), i * 1.9 + 0.2, 0.06)
    for tt in (0.0, 4.4, 8.65, 13.5, 18.05): m.add(reverb(lowpass(kick(), 90), 0.5, 3.0), tt, 0.8)
    for tt in (3.9, 8.3, 13.1, 17.7): m.add(whoosh(0.7, True), tt, 0.25)
    m.add(reverb(chime(81, 3.0), 0.5), 19.2, 0.18)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [0.0, 7.5, 12.5, 16.8, 21.0], os.path.join(S, 'prevP.png'))
    else:
        render('P_moturidiy_samarqand', draw, DUR, audio); print('done P')
