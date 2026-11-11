import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

DUR = 22.0
INK = (12, 12, 14); PAPER = (236, 233, 226); GREY = (130, 128, 124); RED = (232, 72, 64)
BG = Image.new('RGBA', (W, H), INK + (255,))
_g = Image.fromarray((np.random.RandomState(2).rand(H, W) * 14).astype(np.uint8)).convert('RGBA'); _g.putalpha(60)
BG.alpha_composite(_g)

PEOPLE = [('Abdulla Qodiriy', '"O\'tkan kunlar"'), ('Abdulhamid Cho\'lpon', '"Kecha va kunduz"'), ('Abdurauf Fitrat', '"Abulfayzxon"')]

def flame(fr, x, y, t, k, a=1.0):
    d = ImageDraw.Draw(fr); f = 1 + 0.1 * math.sin(t * 11 + k * 2)
    d.rectangle((x - 16, y, x + 16, y + 150), fill=PAPER + (int(230 * a),))
    d.polygon([(x - 12, y - 4), (x + 3 * math.sin(t * 3 + k), y - 60 * f), (x + 12, y - 4)], fill=(255, 200, 120, int(255 * a)))

def draw(t):
    fr = BG.copy()
    PB = lambda s: font('PlayfairBlack', s); PBo = lambda s: font('PlayfairBold', s); PI = lambda s: font('PlayfairItalic', s); MO = lambda s: font('Mono', s); MB = lambda s: font('MonoBold', s); G = lambda s: font('GroteskMed', s)

    if t < 4.4:
        put(fr, text_layer('1938-yil, oktabr. Bir kecha.', MB(48), GREY, maxw=W - 80), W / 2, 360, t, -1)
        put(fr, text_layer('O\'zbek adabiyotining uch ustuni otib tashlandi.', PB(96), PAPER, maxw=W - 110), W / 2, 480, t, -1)
        for k in range(3): flame(fr, W / 2 + (k - 1) * 200, 1100, t, k)

    if 4.4 <= t < 13.4:
        for i, (n, b) in enumerate(PEOPLE):
            t0 = 4.5 + i * 2.6
            put(fr, text_layer(n, PBo(78), PAPER, maxw=W - 140), W / 2, 380 + i * 300, t, t0, dur=0.4, out_t=13.1)
            put(fr, text_layer(b, PI(58), RED), W / 2, 480 + i * 300, t, t0 + 0.6, out_t=13.1)
        for k in range(3):
            if t > 4.5 + k * 2.6: flame(fr, W / 2 + (k - 1) * 200, 1420, t, k, 1 - clamp((t - 13.1) / 0.3))

    if 13.4 <= t < 18.2:
        put(fr, text_layer('Kitoblari taqiqlandi, nomlari tilga olinmadi.', PBo(72), PAPER, maxw=W - 140), W / 2, 360, t, 13.45, dur=0.3, out_t=17.9)
        put(fr, text_layer('Ular otilgan joyda bugun "Shahidlar xotirasi" majmuasi turibdi.', G(54), GREY, maxw=W - 180), W / 2, 640, t, 14.4, out_t=17.9)
        put(fr, text_layer('Kitoblari esa yana o\'qilmoqda.', PI(66), RED, maxw=W - 160), W / 2, 940, t, 15.6, out_t=17.9)

    if t >= 18.2:
        put(fr, text_layer('Ularni o\'qish ham bir xotira.', PB(84), PAPER, maxw=W - 140), W / 2, 360, t, 18.25, dur=0.3)
        put(fr, text_layer('Uchalasidan qaysi birini o\'qigansiz? Kommentda yozing.', PI(58), GREY, maxw=W - 200), W / 2, 680, t, 18.7)
        pl = Image.new('RGBA', (620, 136), (0, 0, 0, 0)); d = ImageDraw.Draw(pl)
        d.rectangle((0, 0, 619, 135), fill=PAPER); s = 'booknote.uz'
        d.text(((620 - tw(s, PB(70))) / 2, 20), s, font=PB(70), fill=INK)
        put(fr, pl, W / 2, 920, t, 19.3, dur=0.3, slide=0, scale_from=0.8)

    d = ImageDraw.Draw(fr); d.text((70, 100), 'BookNote', font=font('PlayfairBold', 42), fill=PAPER)
    d.rectangle((0, 0, W * t / DUR, 8), fill=RED)
    return fr

def cello(m_, dur):
    n = int(dur * SR); tt = np.arange(n) / SR; f = midi(m_) * (1 + 0.005 * np.sin(2 * np.pi * 5 * tt) * np.clip(tt * 2 - 0.3, 0, 1))
    ph = np.cumsum(f) / SR; s = 2 * (ph % 1) - 1
    return lowpass(s, 1200) * env_adsr(n, 0.4, 0.3, 0.8, 0.8)

def audio():
    from c_6daqiqa import rhodes
    m = Mix(DUR)
    m.add(reverb(pad([33, 40, 45], DUR + 1, 'saw', 380, a=0.05, r=3, gain=0.28), 0.5, 3.0), 0)
    line = [(57, 3.0), (55, 1.5), (53, 1.5), (52, 3.0), (50, 3.0), (52, 1.5), (53, 1.5), (52, 4.0)]
    tt = 0.5
    for n, dd in line:
        if tt > DUR - 2: break
        m.add(reverb(cello(n - 12, dd + 0.4), 0.45, 2.6), tt, 0.2); tt += dd
    for k in range(3): m.add(reverb(rhodes(69 - k * 3, 3.0), 0.6, 3.0), 4.5 + k * 2.6, 0.14)
    for tt in (0.0, 13.45): m.add(reverb(lowpass(kick(), 80), 0.6, 3.5), tt, 0.9)
    m.add(reverb(chime(76, 3.0), 0.6), 19.3, 0.14)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [0.0, 12.5, 16.8, 21.0], os.path.join(S, 'prevT.png'))
    else:
        render('T_1938_uch_adib', draw, DUR, audio); print('done T')
