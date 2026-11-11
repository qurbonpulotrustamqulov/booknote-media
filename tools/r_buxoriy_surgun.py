import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

DUR = 22.0
DARK = (20, 14, 12); FLAME = (255, 196, 110); WAX = (236, 222, 196); CREAM = (250, 236, 210); AMBER = (232, 160, 70); RAIN = (170, 160, 150)

BG = gradient(W, H, (12, 10, 14), (34, 22, 16))
_rs = np.random.RandomState(17)
DROPS = [(_rs.uniform(0, W), _rs.uniform(0, H), _rs.uniform(700, 1100), _rs.uniform(30, 70)) for _ in range(140)]

def candle(fr, t, cx, base_y):
    fl = 1 + 0.08 * math.sin(t * 13) + 0.05 * math.sin(t * 29)
    glow = Image.new('RGBA', (W, H), (0, 0, 0, 0)); g = ImageDraw.Draw(glow)
    for r in range(520, 40, -40):
        g.ellipse((cx - r * fl, base_y - 160 - r * fl, cx + r * fl, base_y - 160 + r * fl), fill=FLAME + (int(9 * (1 - r / 560)),))
    fr.alpha_composite(glow)
    d = ImageDraw.Draw(fr)
    d.rounded_rectangle((cx - 55, base_y - 90, cx + 55, H + 20), radius=14, fill=WAX + (255,))
    d.line((cx, base_y - 90, cx, base_y - 112), fill=(40, 30, 20, 255), width=4)
    h = 120 * fl; sway = 6 * math.sin(t * 3)
    d.polygon([(cx - 22, base_y - 112), (cx + sway, base_y - 112 - h), (cx + 22, base_y - 112)], fill=FLAME + (255,))
    d.polygon([(cx - 9, base_y - 114), (cx + sway * 0.5, base_y - 114 - h * 0.5), (cx + 9, base_y - 114)], fill=(255, 250, 230, 255))

def rain(fr, t, a=90):
    l = Image.new('RGBA', (W, H), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    for x, y, sp, ln in DROPS:
        yy = (y + t * sp) % (H + 100) - 100; xx = x - (yy - y) * 0.08 % W
        d.line((xx, yy, xx - 6, yy + ln), fill=RAIN + (a,), width=2)
    fr.alpha_composite(l)

def draw(t):
    fr = BG.copy(); rain(fr, t); candle(fr, t, W / 2, 1640)
    PB = lambda s: font('PlayfairBlack', s); PBo = lambda s: font('PlayfairBold', s); PI = lambda s: font('PlayfairItalic', s); C = lambda s: font('Cormorant', s); G = lambda s: font('GroteskMed', s)

    if t < 4.4:
        put(fr, text_layer('Hokim uni saroyga chaqirdi.', PI(66), AMBER, maxw=W - 160), W / 2, 330, t, -1)
        put(fr, text_layer('"Ilm saroyga bormaydi" dedi', PB(96), CREAM, maxw=W - 120), W / 2, 450, t, -1)
        put(fr, text_layer('va o\'z shahridan quvildi.', PBo(80), AMBER, maxw=W - 140), W / 2, 800, t, -1)

    if 4.4 <= t < 8.8:
        put(fr, text_layer('Imom', PI(70), AMBER), W / 2, 330, t, 4.45, dur=0.3, out_t=8.5)
        put(fr, text_layer('al-Buxoriy', PB(140), CREAM), W / 2, 420, t, 4.6, dur=0.35, slide=0, scale_from=1.2, out_t=8.5)
        put(fr, text_layer('Buxoro hokimi undan saroyga kelib, faqat o\'z bolalariga dars berishni talab qildi.', C(62), CREAM, maxw=W - 180), W / 2, 640, t, 5.2, out_t=8.5)

    if 8.8 <= t < 13.6:
        put(fr, text_layer('Rivoyatlarga ko\'ra, javobi:', PI(62), AMBER), W / 2, 330, t, 8.85, dur=0.3, out_t=13.3)
        put(fr, text_layer('"Ilmni xor qilmayman. Kim o\'rganmoqchi bo\'lsa, masjidga yoki uyimga kelsin."', PBo(68), CREAM, maxw=W - 160), W / 2, 450, t, 9.2, dur=0.5, out_t=13.3)
        put(fr, text_layer('Shundan keyin u Buxorodan chiqarib yuborildi.', G(50), AMBER, maxw=W - 180), W / 2, 920, t, 11.0, out_t=13.3)

    if 13.6 <= t < 18.2:
        put(fr, text_layer('U Samarqand yaqinidagi Xartang qishlog\'iga bordi.', C(64), CREAM, maxw=W - 180), W / 2, 330, t, 13.65, dur=0.3, out_t=17.9)
        put(fr, text_layer('870-yil, Ramazon hayiti kechasi', PBo(72), AMBER, maxw=W - 160), W / 2, 560, t, 14.6, out_t=17.9)
        put(fr, text_layer('o\'sha yerda vafot etdi.', PI(70), CREAM), W / 2, 840, t, 15.4, out_t=17.9)

    if t >= 18.2:
        put(fr, text_layer('Uning kitobini bugun butun dunyo o\'qiydi.', PB(80), CREAM, maxw=W - 140), W / 2, 340, t, 18.25, dur=0.3)
        put(fr, text_layer('Siz "Sahihi Buxoriy"dan biror hadisni bilasizmi? Kommentda yozing.', PI(56), AMBER, maxw=W - 200), W / 2, 620, t, 18.7)
        pl = Image.new('RGBA', (620, 136), (0, 0, 0, 0)); d = ImageDraw.Draw(pl)
        d.rounded_rectangle((0, 0, 619, 135), radius=68, fill=AMBER); s = 'booknote.uz'
        d.text(((620 - tw(s, PB(70))) / 2, 20), s, font=PB(70), fill=DARK)
        put(fr, pl, W / 2, 980, t, 19.3, dur=0.3, slide=0, scale_from=0.8)

    d = ImageDraw.Draw(fr); d.text((70, 100), 'BookNote', font=font('PlayfairBold', 42), fill=CREAM)
    d.rectangle((0, 0, W * t / DUR, 8), fill=AMBER)
    return fr

def audio():
    from c_6daqiqa import rhodes
    m = Mix(DUR)
    r = highpass(lowpass(noise(DUR + 1), 6000), 400); m.add(r, 0, 0.09)  # rain
    for i in range(40): m.add(highpass(tick(), 2000), random.uniform(0, DUR - 1), 0.05)  # drips
    for i, ch in enumerate([[38, 45, 50], [36, 43, 48], [34, 41, 46], [33, 40, 45], [38, 45, 50], [36, 43, 48]]):
        m.add(reverb(pad(ch, 4.5, 'saw', 520, a=0.05 if i == 0 else 1.2, r=1.8, gain=0.22), 0.5, 2.8), i * 3.8)
    mel = [(62, 1.5), (65, 0.75), (64, 0.75), (62, 1.5), (60, 1.5), (58, 1.5), (57, 3.0)]
    for st in (0.4, 8.8, 13.7):
        tt = st
        for n, dd in mel:
            if tt > DUR - 1.5: break
            m.add(reverb(rhodes(n, dd + 1.0), 0.55, 2.8), tt, 0.13); tt += dd
    for tt in (0.0, 4.6, 9.2, 14.6, 18.25): m.add(reverb(lowpass(kick(), 90), 0.5, 3.0), tt, 0.8)
    m.add(reverb(chime(74, 3.0), 0.5), 19.3, 0.15)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [0.0, 7.6, 12.6, 17.0, 21.0], os.path.join(S, 'prevR.png'))
    else:
        render('R_buxoriy_ilm_saroyga_bormaydi', draw, DUR, audio); print('done R')
