import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

DUR = 22.0
IND1 = (16, 14, 44); IND2 = (40, 30, 84); GOLD = (240, 196, 100); IVORY = (248, 240, 222); ROSE = (236, 140, 120); SKY = (150, 170, 240)
BG = gradient(W, H, IND1, IND2)
BG.alpha_composite(vignette(W, H, 0.6, (6, 4, 20)))
_rs = random.Random(4)
COLS = [(_rs.uniform(40, W - 40), _rs.uniform(0, H), _rs.uniform(30, 70), [_rs.randint(0, 3) for _ in range(14)]) for _ in range(22)]

def script_rain(fr, t):
    # stylised vertical Old-Uyghur-like strokes drifting down, very faint
    l = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    for x, y0, sp, glyphs in COLS:
        y = (y0 + t * sp) % (H + 600) - 600
        d.line((x, y, x, y + 14 * 38), fill=GOLD + (40,), width=3)
        for i, g in enumerate(glyphs):
            yy = y + i * 38
            if g == 0: d.line((x, yy, x - 18, yy + 10), fill=GOLD + (40,), width=3)
            elif g == 1: d.line((x, yy, x + 16, yy + 6), fill=GOLD + (40,), width=3)
            elif g == 2: d.ellipse((x - 7, yy, x + 7, yy + 14), outline=GOLD + (40,), width=2)
    fr.alpha_composite(l)

CITIES = [('Vena', 'Hirot nusxasi, 1439, uyg\'ur yozuvi', (300, 700)), ('Qohira', 'arab yozuvi', (420, 1060)), ('Namangan', 'arab yozuvi, 1913-yilda topildi', (790, 860))]

def draw(t):
    fr = BG.copy(); script_rain(fr, t)
    PB = lambda s: font('PlayfairBlack', s); PBo = lambda s: font('PlayfairBold', s); PI = lambda s: font('PlayfairItalic', s); CI = lambda s: font('CormorantItalic', s); C = lambda s: font('Cormorant', s); G = lambda s: font('GroteskMed', s)

    if t < 4.2:
        put(fr, text_layer('950 yil oldin yozilgan kitob,', CI(78), SKY, maxw=W - 140), W / 2, 420, t, -1)
        put(fr, text_layer('nomi: "Baxtga eltuvchi bilim"', PB(96), IVORY, maxw=W - 100), W / 2, 540, t, -1)
        put(fr, text_layer('Dunyoda uning faqat 3 ta qo\'lyozmasi qolgan.', PBo(64), GOLD, maxw=W - 160), W / 2, 860, t, -1)

    if 4.2 <= t < 8.6:
        put(fr, text_layer('"Qutadg\'u bilig"', PB(120), GOLD), W / 2, 400, t, 4.25, dur=0.35, slide=0, scale_from=1.2, out_t=8.3)
        put(fr, text_layer('Yusuf Xos Hojib, 1069-1070-yillar', PI(60), IVORY, maxw=W - 160), W / 2, 600, t, 4.8, out_t=8.3)
        put(fr, text_layer('Qashqarda yozib, Qoraxoniylar xoniga taqdim etgan. 6 500 baytdan ortiq.', C(62), IVORY, maxw=W - 180), W / 2, 760, t, 5.6, out_t=8.3)

    if 8.6 <= t < 13.8:
        put(fr, text_layer('3 ta qo\'lyozma', PB(100), IVORY), W / 2, 380, t, 8.65, dur=0.3, out_t=13.5)
        d = ImageDraw.Draw(fr); k = 1 - ease((t - 13.5) / 0.3)
        for i, (n, info, (x, y)) in enumerate(CITIES):
            t0 = 9.2 + i * 1.1
            if t < t0: continue
            q = ease((t - t0) / 0.4) * k
            rr = 26 + 6 * math.sin(t * 4 + i); d.ellipse((x - rr, y - rr, x + rr, y + rr), outline=GOLD + (int(160 * q),), width=3)
            d.ellipse((x - 12, y - 12, x + 12, y + 12), fill=GOLD + (int(255 * q),))
            la = text_layer(n, PBo(64), IVORY); lb = text_layer(info, G(36), SKY, maxw=420, align='c')
            fr.alpha_composite(fade(la, q), (int(x - la.size[0] / 2), int(y + 40))); fr.alpha_composite(fade(lb, q), (int(x - lb.size[0] / 2), int(y + 120)))
        put(fr, text_layer('Namangan nusxasi bugun Toshkentda saqlanadi.', CI(60), GOLD, maxw=W - 180), W / 2, 1360, t, 12.0, out_t=13.5)

    if 13.8 <= t < 18.0:
        put(fr, text_layer('Kitobning 4 qahramoni', CI(70), SKY), W / 2, 360, t, 13.85, dur=0.3, out_t=17.7)
        heroes = [('Kuntug\'di', 'adolat'), ('Oyto\'ldi', 'baxt, davlat'), ('O\'gdulmish', 'aql'), ('O\'zg\'urmish', 'qanoat, oqibat')]
        for i, (a, b) in enumerate(heroes):
            c = Image.new('RGBA', (440, 230), (0, 0, 0, 0)); dd = ImageDraw.Draw(c)
            dd.rounded_rectangle((0, 0, 439, 229), radius=24, fill=(255, 255, 255, 18), outline=GOLD + (200,), width=3)
            dd.text(((440 - tw(a, PBo(54))) / 2, 46), a, font=PBo(54), fill=IVORY); dd.text(((440 - tw(b, G(38))) / 2, 136), b, font=G(38), fill=ROSE)
            put(fr, c, W / 2 + (i % 2 * 2 - 1) * 235, 500 + (i // 2) * 260, t, 14.3 + i * 0.35, dur=0.3, slide=0, scale_from=0.7, out_t=17.7)
        put(fr, text_layer('Davlatni qanday boshqarish va qanday yashash haqida.', C(58), IVORY, maxw=W - 180), W / 2, 1060, t, 15.8, out_t=17.7)

    if t >= 18.0:
        put(fr, text_layer('Bilim baxtga eltadi.', PB(96), GOLD, maxw=W - 140), W / 2, 400, t, 18.05, dur=0.3)
        put(fr, text_layer('Siz shu yil qaysi kitobdan eng ko\'p narsa o\'rgandingiz? Kommentda yozing.', CI(62), IVORY, maxw=W - 200), W / 2, 580, t, 18.5)
        pl = Image.new('RGBA', (620, 136), (0, 0, 0, 0)); d = ImageDraw.Draw(pl)
        d.rounded_rectangle((0, 0, 619, 135), radius=20, fill=GOLD); s = 'booknote.uz'
        d.text(((620 - tw(s, PB(70))) / 2, 20), s, font=PB(70), fill=IND1)
        put(fr, pl, W / 2, 900, t, 19.2, dur=0.3, slide=0, scale_from=0.8)

    d = ImageDraw.Draw(fr); d.text((70, 100), 'BookNote', font=font('PlayfairBold', 42), fill=IVORY)
    d.rectangle((0, 0, W * t / DUR, 8), fill=GOLD)
    return fr

def kobuz(m_, dur):
    n = int(dur * SR); tt = np.arange(n) / SR
    f = midi(m_) * (1 + 0.008 * np.sin(2 * np.pi * 5.5 * tt) * np.clip(tt * 3 - 0.3, 0, 1))
    ph = np.cumsum(f) / SR; s = 2 * (ph % 1) - 1
    s = highpass(lowpass(s, 2200), 200) + lowpass(noise(dur), 3000)[:n] * 0.08
    return s * env_adsr(n, 0.12, 0.2, 0.75, 0.3)

def audio():
    m = Mix(DUR)
    m.add(reverb(pad([38, 45], DUR + 1, 'tri', 380, a=0.05, r=3, gain=0.45), 0.3), 0)
    # 6/8 frame drum
    e = 60 / 150
    for i in range(int((DUR - 1) / e)):
        tt = i * e
        if tt < 0.2: continue
        pos = i % 6
        if pos == 0: m.add(lowpass(kick(), 160), tt, 0.45)
        elif pos == 3: m.add(lowpass(kick(), 220), tt, 0.3)
        else: m.add(highpass(tick(), 600), tt, 0.1 if pos in (2, 5) else 0.06)
    # kobuz phrases in D phrygian-ish
    phr = [(62, 1.2), (63, 0.6), (65, 0.6), (67, 1.2), (65, 0.6), (63, 0.6), (62, 2.4)]
    for st in (0.4, 8.6, 14.0):
        tt = st
        for n, dd in phr: m.add(reverb(kobuz(n, dd + 0.2), 0.4, 2.2), tt, 0.14, pan=0.15); tt += dd
    for tt in (0.0, 4.25, 8.65, 13.85, 18.05): m.add(reverb(lowpass(kick(), 110), 0.45, 2.6), tt, 0.75)
    for i in range(3): m.add(reverb(chime(74 + i * 5, 2.0), 0.4), 9.2 + i * 1.1, 0.14)
    for i in range(4): m.add(chime(81 + i * 2, 1.0), 14.3 + i * 0.35, 0.08)
    m.add(reverb(chime(86, 3.0), 0.5), 19.2, 0.2)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [0.0, 7.6, 12.8, 16.8, 21.0], os.path.join(S, 'prevN.png'))
    else:
        render('N_qutadgu_bilig', draw, DUR, audio); print('done N')
