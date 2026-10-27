import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

DUR = 34.0
NAVY = (12, 28, 54); NAVY2 = (20, 44, 82); LINE = (150, 190, 235); WHITE = (236, 243, 252); AMBER = (255, 196, 92)

BG = gradient(W, H, NAVY, NAVY2)
_g = ImageDraw.Draw(BG)
for x in range(0, W, 45): _g.line((x, 0, x, H), fill=(40, 70, 115, 255) if x % 225 == 0 else (28, 54, 95, 255), width=1)
for y in range(0, H, 45): _g.line((0, y, W, y), fill=(40, 70, 115, 255) if y % 225 == 0 else (28, 54, 95, 255), width=1)
BG.alpha_composite(vignette(W, H, 0.7, (4, 10, 22)))

def astrolabe(size, t, alpha=90):
    l = Image.new('RGBA', (size, size), (0, 0, 0, 0)); d = ImageDraw.Draw(l); c = size / 2
    col = LINE + (alpha,)
    for rr in (0.49, 0.44, 0.30, 0.12): d.ellipse((c - size * rr, c - size * rr, c + size * rr, c + size * rr), outline=col, width=2)
    for k in range(72):
        a = math.radians(k * 5 + t * 6); r1 = size * (0.44 if k % 6 else 0.41)
        d.line((c + r1 * math.cos(a), c + r1 * math.sin(a), c + size * 0.49 * math.cos(a), c + size * 0.49 * math.sin(a)), fill=col, width=1)
    for k in range(12):
        a = math.radians(k * 30 - t * 10)
        d.line((c + size * 0.12 * math.cos(a), c + size * 0.12 * math.sin(a), c + size * 0.30 * math.cos(a), c + size * 0.30 * math.sin(a)), fill=col, width=1)
    a = math.radians(t * 20)
    d.line((c - size * 0.47 * math.cos(a), c - size * 0.47 * math.sin(a), c + size * 0.47 * math.cos(a), c + size * 0.47 * math.sin(a)), fill=AMBER + (alpha + 40,), width=3)
    return l

def label(text, f, col):
    return text_layer(text, f, col, maxw=W - 180)

def draw(t):
    fr = BG.copy()
    fr.alpha_composite(astrolabe(1300, t, 55), ((W - 1300) // 2, (H - 1300) // 2 + 120))
    CB = lambda s: font('Cormorant', s); CI = lambda s: font('CormorantItalic', s); MO = lambda s: font('Mono', s); PB = lambda s: font('PlayfairBlack', s)

    if t < 4.4:
        put(fr, label('Bu kitob', CI(80), LINE), W / 2, 560, t, 0.2, dur=0.8, out_t=4.1)
        put(fr, label('500 yil', PB(220), AMBER), W / 2, 660, t, 0.7, dur=0.9, slide=0, scale_from=1.12, out_t=4.1)
        put(fr, label('Yevropa shifokorlarini o\'qitdi.', CB(76), WHITE), W / 2, 930, t, 1.6, dur=0.8, out_t=4.1)
        put(fr, label('[ va uni bir buxorolik yozgan ]', MO(36), LINE), W / 2, 1120, t, 2.6, out_t=4.1)

    if 4.4 <= t < 9.4:
        put(fr, label('FIG. 1', MO(34), AMBER), W / 2, 540, t, 4.5, out_t=9.1)
        put(fr, label('Abu Ali ibn Sino', PB(112), WHITE), W / 2, 610, t, 4.7, dur=0.8, out_t=9.1)
        put(fr, text_layer('980-yil, Buxoro yaqinidagi Afshona qishlog\'i', CI(54), LINE, maxw=W - 100), W / 2, 790, t, 5.6, dur=0.8, out_t=9.1)
        d = ImageDraw.Draw(fr); p = ease((t - 6.2) / 1.0) * (1 - ease((t - 9.1) / 0.3))
        d.line((W / 2 - 300 * p, 900, W / 2 + 300 * p, 900), fill=AMBER + (int(255 * p),), width=3)
        put(fr, label('Yevropada uni "Avitsenna" deb atashadi', MO(38), WHITE), W / 2, 950, t, 6.8, out_t=9.1)

    if 9.4 <= t < 15.4:
        put(fr, label('Yoshligida Buxoro amirini davoladi.', CB(72), WHITE), W / 2, 520, t, 9.5, dur=0.8, out_t=15.1)
        put(fr, label('Mukofoti?', CI(90), AMBER), W / 2, 760, t, 10.8, dur=0.7, out_t=15.1)
        # library shelves drawing
        if t > 11.8:
            lay = Image.new('RGBA', (760, 420), (0, 0, 0, 0)); d = ImageDraw.Draw(lay)
            p = clamp((t - 11.8) / 1.4)
            for row in range(3):
                d.line((0, 130 + row * 140, 760, 130 + row * 140), fill=LINE + (220,), width=3)
                for k in range(int(18 * p)):
                    h = 70 + (k * 37 % 40); x = 10 + k * 41
                    d.rectangle((x, 128 + row * 140 - h, x + 32, 128 + row * 140), outline=LINE + (220,), width=2)
            put(fr, lay, W / 2, 900, t, 11.8, dur=0.4, out_t=15.1)
        put(fr, label('Saroy kutubxonasidan foydalanish huquqi.', CB(64), WHITE), W / 2, 1370, t, 13.0, dur=0.8, out_t=15.1)

    if 15.4 <= t < 22.0:
        put(fr, label('"Tib qonunlari"', PB(110), WHITE), W / 2, 430, t, 15.5, dur=0.8, out_t=21.7)
        put(fr, label('1025-yilda yakunlangan, 5 kitobdan iborat', CI(58), LINE), W / 2, 600, t, 16.2, out_t=21.7)
        names = ['Umumiy tibbiyot', 'Dorilar', 'A\'zolar kasalliklari', 'Umumiy kasalliklar', 'Murakkab dorilar']
        for i, nm in enumerate(names):
            row = Image.new('RGBA', (840, 120), (0, 0, 0, 0)); d = ImageDraw.Draw(row)
            d.rectangle((0, 10, 839, 109), outline=LINE + (200,), width=2)
            d.text((30, 30), 'KITOB %d' % (i + 1), font=MO(38), fill=AMBER, features=['lnum'])
            d.text((290, 26), nm, font=CB(52), fill=WHITE)
            put(fr, row, W / 2, 740 + i * 140, t, 16.9 + i * 0.35, dur=0.45, slide=30, out_t=21.7)

    if 22.0 <= t < 28.4:
        put(fr, label('Uning yo\'li', CI(70), LINE), W / 2, 380, t, 22.1, out_t=28.1)
        steps = [('XI asr', 'Jurjon va Hamadonda yozildi'), ('XII asr', 'Toledoda lotinchaga tarjima qilindi'), ('XV asr', 'kitob sifatida bosib chiqarildi'), ('XVII asrgacha', 'Yevropa universitetlarida darslik')]
        x0 = 200
        d = ImageDraw.Draw(fr)
        p = ease((t - 22.5) / 3.0) * (1 - ease((t - 28.1) / 0.3))
        d.line((x0, 560, x0, 560 + 790 * p), fill=AMBER + (int(255 * p),), width=4)
        for i, (a, b) in enumerate(steps):
            t0 = 22.6 + i * 0.75; y = 540 + i * 250
            if t >= t0:
                q = ease((t - t0) / 0.4) * (1 - ease((t - 28.1) / 0.3))
                d.ellipse((x0 - 16, y + 20 - 16, x0 + 16, y + 20 + 16), fill=AMBER + (int(255 * q),))
                la = text_layer(a, MO(44), AMBER, align='l', maxw=700); lb = text_layer(b, CB(56), WHITE, align='l', maxw=760)
                fr.alpha_composite(fade(la, q), (x0 + 50, y - 10)); fr.alpha_composite(fade(lb, q), (x0 + 50, y + 55))

    if t >= 28.4:
        put(fr, label('Buyuk ajdodlarimiz kitob o\'qigan', CB(76), WHITE), W / 2, 560, t, 28.5, dur=0.8)
        put(fr, label('va kitob yozgan.', CI(84), AMBER), W / 2, 760, t, 29.1, dur=0.8)
        put(fr, label('Siz bu yil nechta kitob o\'qidingiz?', CB(62), LINE), W / 2, 950, t, 29.8, dur=0.8)
        pl = Image.new('RGBA', (600, 124), (0, 0, 0, 0)); d = ImageDraw.Draw(pl)
        d.rectangle((0, 0, 599, 123), outline=AMBER, width=3); s = 'booknote.uz'
        d.text(((600 - tw(s, MO(58))) / 2, 26), s, font=font('MonoBold', 58), fill=AMBER)
        put(fr, pl, W / 2, 1180, t, 30.6, dur=0.6, scale_from=0.9)
        put(fr, label('Yillik o\'qish maqsadingizni qo\'ying', MO(36), WHITE), W / 2, 1350, t, 31.2)

    d = ImageDraw.Draw(fr)
    d.text((70, 100), 'BookNote', font=font('PlayfairBold', 44), fill=WHITE)
    s = 'ARXIV // 1025'; d.text((W - 70 - tw(s, MO(30)), 112), s, font=MO(30), fill=LINE)
    return fr

def audio():
    m = Mix(DUR)
    # A minor cinematic: low strings pad + piano motif
    chords = [[45, 52, 57, 60], [41, 48, 53, 57], [43, 50, 55, 59], [40, 47, 52, 56]]  # Am F G E
    bar = 4.0
    for b in range(int(DUR / bar) + 1):
        ch = chords[b % 4]
        m.add(reverb(pad(ch, bar + 1.5, 'saw', 650, a=1.5, r=1.6, gain=0.22), 0.5, 2.5), b * bar)
    motif = [69, 72, 76, 74, 72, 71, 72, 69]
    for b in range(int(DUR / bar)):
        if b == 0: continue
        for k, n in enumerate(motif):
            tt = b * bar + k * 0.5
            nn = n + (0 if b % 2 else -5 if k % 4 == 3 else 0)
            from c_6daqiqa import rhodes
            m.add(reverb(rhodes(nn, 1.6), 0.45, 2.0), tt, 0.10)
    # low boom on big reveals
    for tt in (0.7, 4.7, 15.5, 28.5):
        m.add(reverb(lowpass(kick(), 120), 0.4, 2.5), tt, 0.9)
    for tt in (4.3, 9.3, 15.3, 21.9, 28.3): m.add(whoosh(0.9, True), tt - 0.3, 0.3)
    for i in range(5): m.add(tick(), 16.9 + i * 0.35, 0.3)
    m.add(reverb(chime(81, 3.0), 0.5), 30.6, 0.18)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [3.0, 7.5, 13.8, 19.5, 26.0, 33.0], os.path.join(S, 'prevD.png'))
    else:
        render('D_ibn_sino_tib_qonunlari', draw, DUR, audio); print('done D')
