import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

DUR = 22.0
ICE1 = (18, 40, 70); ICE2 = (90, 140, 190); SAND1 = (120, 70, 36); SAND2 = (232, 176, 104)
SNOW = (240, 248, 255); WARM = (255, 236, 200); DEEP = (14, 22, 40); AMBER = (255, 190, 90)

COLD = gradient(W, H, ICE1, ICE2); HOT = gradient(W, H, SAND1, SAND2)
_rs = np.random.RandomState(13)
FLAKES = [(_rs.uniform(0, W), _rs.uniform(0, H), _rs.uniform(2, 6), _rs.uniform(40, 120)) for _ in range(160)]

def bg(t):
    # 0..1 mix from cold (Khorezm) to hot (Mecca) as the story travels
    p = ease_io(clamp((t - 8.4) / 1.2)) 
    fr = Image.blend(COLD, HOT, p)
    d = ImageDraw.Draw(fr)
    if p < 0.95:
        a = int(200 * (1 - p))
        for x, y, r, sp in FLAKES:
            yy = (y + t * sp) % H; xx = x + 10 * math.sin(t + y)
            d.ellipse((xx - r, yy - r, xx + r, yy + r), fill=SNOW + (a,))
    if p > 0.05:  # heat shimmer sun
        a = int(255 * p); d.ellipse((W - 330, 160, W - 110, 380), fill=(255, 230, 170, a))
    return fr, p

def draw(t):
    fr, p = bg(t)
    PB = lambda s: font('PlayfairBlack', s); PBo = lambda s: font('PlayfairBold', s); PI = lambda s: font('PlayfairItalic', s); CI = lambda s: font('CormorantItalic', s); C = lambda s: font('Cormorant', s); G = lambda s: font('GroteskMed', s)
    SH = dict(stroke=3, stroke_fill=DEEP)

    if t < 4.2:
        put(fr, text_layer('Uni "Allohning qo\'shnisi" deb atashgan.', PB(96), SNOW, maxw=W - 120, **SH), W / 2, 430, t, -1)
        put(fr, text_layer('Xorazmlik bir olim.', PI(76), AMBER, **SH), W / 2, 900, t, -1)

    if 4.2 <= t < 8.4:
        put(fr, text_layer('Mahmud az-Zamaxshariy', PB(92), SNOW, maxw=W - 120, **SH), W / 2, 400, t, 4.25, dur=0.3, out_t=8.1)
        put(fr, text_layer('1075-yil, Xorazm, Zamaxshar qishlog\'i', G(52), SNOW, maxw=W - 160, **SH), W / 2, 680, t, 4.8, out_t=8.1)
        put(fr, text_layer('Yoshligida qishki safarda oyog\'ini sovuq oldirib, umrbod yog\'och oyoq bilan yurgan.', C(62), SNOW, maxw=W - 180, **SH), W / 2, 860, t, 5.6, out_t=8.1)

    if 8.4 <= t < 13.4:
        put(fr, text_layer('Lekin ilm yo\'lidan qolmadi.', PBo(76), WARM, maxw=W - 140, **SH), W / 2, 400, t, 8.45, dur=0.3, out_t=13.1)
        put(fr, text_layer('Makkada uzoq yillar yashadi.', PB(84), WARM, maxw=W - 140, **SH), W / 2, 660, t, 9.3, out_t=13.1)
        put(fr, text_layer('Shu sabab laqabi "Jorulloh", ya\'ni "Allohning qo\'shnisi".', PI(60), WARM, maxw=W - 160, **SH), W / 2, 940, t, 10.3, out_t=13.1)

    if 13.4 <= t < 18.0:
        put(fr, text_layer('"Al-Kashshof"', PB(130), WARM, **SH), W / 2, 380, t, 13.45, dur=0.3, slide=0, scale_from=1.2, out_t=17.7)
        put(fr, text_layer('Qur\'oni karim tafsiri. Makkada yakunlangan va asrlar davomida o\'qilgan.', C(62), WARM, maxw=W - 180, **SH), W / 2, 600, t, 14.0, out_t=17.7)
        put(fr, text_layer('"Muqaddimat ul-adab" lug\'atida arabcha so\'zlarga forscha va turkiycha izoh yozgan.', G(48), WARM, maxw=W - 180, **SH), W / 2, 880, t, 15.2, out_t=17.7)

    if t >= 18.0:
        put(fr, text_layer('Qiyinchilik ilmga to\'siq bo\'lmadi.', PB(84), SNOW, maxw=W - 140, **SH), W / 2, 400, t, 18.05, dur=0.3)
        put(fr, text_layer('Sizni o\'qishdan nima to\'xtatib turibdi? Kommentda yozing.', PI(58), WARM, maxw=W - 200, **SH), W / 2, 720, t, 18.5)
        pl = Image.new('RGBA', (620, 136), (0, 0, 0, 0)); d = ImageDraw.Draw(pl)
        d.rounded_rectangle((0, 0, 619, 135), radius=68, fill=DEEP); s = 'booknote.uz'
        d.text(((620 - tw(s, PB(70))) / 2, 20), s, font=PB(70), fill=AMBER)
        put(fr, pl, W / 2, 1000, t, 19.2, dur=0.3, slide=0, scale_from=0.8)

    d = ImageDraw.Draw(fr); d.text((70, 100), 'BookNote', font=font('PlayfairBold', 42), fill=SNOW)
    d.rectangle((0, 0, W * t / DUR, 8), fill=AMBER)
    return fr

def tar(m_, dur=0.5):
    s = pluck(midi(m_), dur, 0.995) + 0.5 * pluck(midi(m_ + 12), dur, 0.993)
    return highpass(lowpass(s, 5000), 180)

def audio():
    m = Mix(DUR)
    # winter: wind + sparse high bells; at 8.4 s turns warm: tar tremolo in Bayati on D + riq
    w = lowpass(noise(9.5), 900); w *= np.linspace(1, 0.2, len(w))
    m.add(w, 0, 0.18)
    for i, n in enumerate([86, 81, 79, 84, 81, 76, 79, 74]): m.add(reverb(chime(n, 2.0), 0.6, 3.0), 0.3 + i * 1.0, 0.06)
    m.add(reverb(pad([38, 45, 50], 9.5, 'tri', 500, a=0.05, r=2, gain=0.35), 0.4), 0)
    m.add(reverb(pad([38, 45, 50, 53], DUR - 8.0, 'saw', 650, a=1.0, r=2.5, gain=0.18), 0.4), 8.2)
    bay = [62, 63.5, 65, 67, 69, 70, 72]
    rs = random.Random(8); tt = 8.4; idx = 3
    while tt < DUR - 1.2:
        idx = max(0, min(6, idx + rs.choice([-1, 1, -1, 1, 2, -2])))
        n = bay[idx]
        for r in range(3 if rs.random() < 0.4 else 1): m.add(tar(n), tt + r * 0.06, 0.18, pan=0.2)
        tt += rs.choice([0.25, 0.25, 0.5])
    beat = 60 / 104; tt = 8.4
    while tt < DUR - 1.2:
        m.add(lowpass(kick(), 200), tt, 0.35); m.add(hat(0.08), tt + beat / 2, 0.15); m.add(hat(0.04), tt + beat * 0.75, 0.08)
        tt += beat
    for tt in (0.0, 8.45, 13.45, 18.05): m.add(reverb(lowpass(kick(), 110), 0.45, 2.6), tt, 0.75)
    m.add(whoosh(1.2, True), 7.6, 0.4)
    for tt in (13.1, 17.7): m.add(whoosh(0.6, True), tt, 0.25)
    m.add(reverb(chime(86, 3.0), 0.5), 19.2, 0.18)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [0.0, 7.5, 12.5, 16.8, 21.0], os.path.join(S, 'prevQ.png'))
    else:
        render('Q_zamaxshariy_jorulloh', draw, DUR, audio); print('done Q')
