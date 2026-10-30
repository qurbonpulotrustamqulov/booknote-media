import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

DUR = 18.0
SKY1 = (6, 8, 24); SKY2 = (30, 22, 60); STAR = (255, 248, 225); GOLD = (244, 200, 110); TEAL = (120, 220, 210); SOFT = (190, 185, 215)

BG = gradient(W, H, SKY1, SKY2)
_rs = np.random.RandomState(5)
STARS = [(_rs.randint(0, W), _rs.randint(0, H), _rs.uniform(0.6, 2.6), _rs.uniform(0, 6.28)) for _ in range(420)]

def sky(t):
    fr = BG.copy(); d = ImageDraw.Draw(fr)
    rot = t * 0.012
    for x, y, r, ph in STARS:
        dx, dy = x - W / 2, y - H * 1.1
        xx = W / 2 + dx * math.cos(rot) - dy * math.sin(rot); yy = H * 1.1 + dx * math.sin(rot) + dy * math.cos(rot)
        a = int(140 + 115 * math.sin(t * 2.2 + ph))
        d.ellipse((xx - r, yy - r, xx + r, yy + r), fill=STAR + (a,))
    return fr

def progress(fr, t):
    d = ImageDraw.Draw(fr); d.rectangle((0, 0, W * t / DUR, 8), fill=GOLD)

def sextant(t, p):
    # meridian arc of the Samarkand observatory, drawn progressively
    l = Image.new('RGBA', (900, 620), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    cx, cy, R = 450, 40, 540
    d.arc((cx - R, cy - R, cx + R, cy + R), 30, 30 + 120 * p, fill=GOLD, width=8)
    d.arc((cx - R + 40, cy - R + 40, cx + R - 40, cy + R - 40), 30, 30 + 120 * p, fill=GOLD + (120,), width=3)
    for k in range(int(25 * p) + 1):
        a = math.radians(30 + k * 5)
        d.line((cx + (R - 40) * math.cos(a), cy + (R - 40) * math.sin(a), cx + R * math.cos(a), cy + R * math.sin(a)), fill=GOLD, width=2)
    return l

def draw(t):
    fr = sky(t)
    PB = lambda s: font('PlayfairBlack', s); PI = lambda s: font('PlayfairItalic', s); G = lambda s: font('Grotesk', s); GM = lambda s: font('GroteskMed', s); MO = lambda s: font('MonoBold', s)

    # 0-3.6 hook (fully visible on frame 0)
    if t < 3.6:
        put(fr, text_layer('Teleskop yo\'q edi.', PB(104), STAR, maxw=W - 60), W / 2, 540, t, -1, out_t=3.3)
        put(fr, text_layer('Lekin u yil uzunligini', GM(70), SOFT, maxw=W - 140), W / 2, 780, t, -1, out_t=3.3)
        put(fr, text_layer('1 daqiqa', PB(190), GOLD), W / 2, 870, t, -1, dur=0.35, slide=0, out_t=3.3)
        put(fr, text_layer('aniqlikda hisobladi.', GM(70), SOFT, maxw=W - 140), W / 2, 1120, t, -1, dur=0.3, out_t=3.3)

    # 3.6-7.4 who and where
    if 3.6 <= t < 7.4:
        put(fr, text_layer('Mirzo Ulug\'bek', PB(124), STAR), W / 2, 500, t, 3.65, dur=0.35, out_t=7.1)
        put(fr, text_layer('Samarqand rasadxonasi, 1420-yillar', PI(58), TEAL, maxw=W - 140), W / 2, 670, t, 3.9, dur=0.35, out_t=7.1)
        if t > 4.2:
            put(fr, sextant(t, ease((t - 4.2) / 1.6)), W / 2, 800, t, 4.2, dur=0.3, slide=0, out_t=7.1)
        put(fr, text_layer('Asboblari yer ostiga qazilgan ulkan yoy edi.', G(54), STAR, maxw=W - 180), W / 2, 1380, t, 5.0, dur=0.35, out_t=7.1)

    # 7.4-11.6 the numbers
    if 7.4 <= t < 11.6:
        put(fr, text_layer('Yulduz yili', GM(64), SOFT), W / 2, 440, t, 7.45, dur=0.3, out_t=11.3)
        rows = [('ULUG\'BEK', '365 kun 6 soat 10 daq 8 s', GOLD), ('BUGUN', '365 kun 6 soat 9 daq 10 s', TEAL)]
        for i, (a, b, c) in enumerate(rows):
            box = Image.new('RGBA', (960, 230), (0, 0, 0, 0)); bd = ImageDraw.Draw(box)
            bd.rounded_rectangle((0, 0, 959, 229), radius=26, fill=(255, 255, 255, 22), outline=c + (200,), width=3)
            bd.text((40, 26), a, font=G(42), fill=c)
            bd.text((40, 96), b, font=MO(60), fill=STAR, features=['lnum'])
            put(fr, box, W / 2, 560 + i * 280, t, 7.8 + i * 0.6, dur=0.3, slide=60, out_t=11.3)
        put(fr, text_layer('Farqi bir daqiqa ham emas.', PB(76), GOLD, maxw=W - 80), W / 2, 1150, t, 9.2, dur=0.3, slide=0, scale_from=1.25, out_t=11.3)
        put(fr, text_layer('Bu 600 yil oldin, qo\'lda hisoblangan.', PI(56), SOFT, maxw=W - 180), W / 2, 1300, t, 9.9, out_t=11.3)

    # 11.6-14.8 star catalogue
    if 11.6 <= t < 14.8:
        p = clamp((t - 11.8) / 1.8); n = int(round(1018 * ease(p)))
        put(fr, text_layer('"Ziji Ko\'ragoniy"', PB(104), STAR), W / 2, 480, t, 11.65, dur=0.3, out_t=14.5)
        put(fr, text_layer('%d' % n, MO(230), GOLD), W / 2, 680, t, 11.8, dur=0.2, slide=0, out_t=14.5)
        put(fr, text_layer('yulduz o\'rni yozilgan jadval', GM(62), SOFT, maxw=W - 160), W / 2, 990, t, 12.0, out_t=14.5)
        put(fr, text_layer('Asrlar davomida Yevropada ham ko\'chirilib, o\'rganildi.', G(52), STAR, maxw=W - 180), W / 2, 1200, t, 12.9, out_t=14.5)

    # 14.8-18 CTA
    if t >= 14.8:
        put(fr, text_layer('Buyuk kashfiyot ham bitta kitobdan boshlanadi.', PB(80), STAR, maxw=W - 140), W / 2, 460, t, 14.85, dur=0.35)
        put(fr, text_layer('Siz hozir nima o\'qiyapsiz? Kommentda yozing.', GM(56), SOFT, maxw=W - 180), W / 2, 880, t, 15.4)
        pl = Image.new('RGBA', (640, 140), (0, 0, 0, 0)); d = ImageDraw.Draw(pl)
        d.rounded_rectangle((0, 0, 639, 139), radius=70, fill=GOLD); s = 'booknote.uz'
        d.text(((640 - tw(s, PB(70))) / 2, 22), s, font=PB(70), fill=SKY1)
        put(fr, pl, W / 2, 1120, t, 15.9, dur=0.3, slide=0, scale_from=0.8)
        put(fr, text_layer('O\'zbek kitobxonlari tarmog\'i', G(44), SOFT), W / 2, 1310, t, 16.3)

    d = ImageDraw.Draw(fr); d.text((70, 60), 'BookNote', font=font('PlayfairBold', 40), fill=STAR)
    progress(fr, t)
    return fr

def audio():
    m = Mix(DUR)
    # E lydian ambient: shimmering pad + arpeggio
    for i, ch in enumerate([[40, 47, 52, 56, 58], [42, 49, 54, 58, 61], [44, 51, 56, 59, 63], [42, 49, 54, 58, 61]]):
        m.add(reverb(pad(ch, 6.0, 'saw', 900, a=0.05 if i == 0 else 1.0, r=2.0, gain=0.2), 0.5, 2.6), i * 4.5)
    arp = [64, 68, 70, 71, 75, 71, 70, 68]
    tt, k = 0.0, 0
    while tt < DUR - 1:
        m.add(reverb(chime(arp[k % 8] + (12 if (k // 16) % 2 else 0), 1.4), 0.4, 2.0), tt, 0.06, pan=0.4 * math.sin(k))
        tt += 0.25; k += 1
    for tt in (0.0, 0.5, 3.65, 7.45, 9.2, 11.65, 14.85):
        m.add(reverb(lowpass(kick(), 140), 0.35, 2.5), tt, 0.8)
    for tt in (3.3, 7.1, 11.3, 14.5): m.add(whoosh(0.7, True), tt, 0.35)
    for i in range(18): m.add(tick(), 11.8 + i * 0.1, 0.15)
    m.add(reverb(chime(83, 3.0), 0.5), 15.9, 0.2)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [0.0, 1.5, 5.8, 10.3, 14.2, 17.0], os.path.join(S, 'prevF.png'))
    else:
        render('F_ulugbek_yulduz_yili', draw, DUR, audio); print('done F')
