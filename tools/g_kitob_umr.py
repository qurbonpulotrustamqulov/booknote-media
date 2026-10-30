import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

DUR = 18.0
YEL = (255, 214, 10); BLK = (16, 16, 16); RED = (230, 57, 70); WHT = (255, 255, 255); DIM = (90, 80, 30)
BG = Image.new('RGBA', (W, H), YEL + (255,))
_g = ImageDraw.Draw(BG)
for y in range(0, H, 60): _g.line((0, y, W, y), fill=(240, 200, 0, 255), width=2)

def ecg(fr, t, y0, col, amp=110, alpha=255):
    # scrolling heartbeat line across the screen
    d = ImageDraw.Draw(fr); pts = []
    for x in range(0, W + 8, 6):
        ph = ((x / W) * 2.5 - t * 1.0) % 1.0
        v = 0
        if 0.40 < ph < 0.44: v = -0.25
        elif 0.44 < ph < 0.47: v = 1.0
        elif 0.47 < ph < 0.50: v = -0.55
        elif 0.58 < ph < 0.66: v = 0.18 * math.sin((ph - 0.58) / 0.08 * math.pi)
        pts.append((x, y0 - v * amp))
    d.line(pts, fill=col + (alpha,), width=7, joint='curve')

def card(text, f, fg, bg, pad=(44, 22)):
    l = text_layer(text, f, fg, maxw=W - 200)
    c = Image.new('RGBA', (l.size[0] + pad[0] * 2, l.size[1] + pad[1] * 2), bg + (255,))
    c.alpha_composite(l, (pad[0], pad[1])); return c

def people(p, hl=0.0):
    l = Image.new('RGBA', (900, 470), (0, 0, 0, 0)); d = ImageDraw.Draw(l)
    k = 0
    for r in range(10):
        for c in range(20):
            k += 1
            if (k * 53 % 200) / 200 > p: continue
            x, y = 22 + c * 43, 22 + r * 45
            col = RED if hl and (k * 29 % 100) / 100 < 0.5 * hl else BLK
            d.ellipse((x - 9, y - 18, x + 9, y), fill=col); d.rounded_rectangle((x - 13, y + 2, x + 13, y + 22), radius=8, fill=col)
    return l

def draw(t):
    fr = BG.copy()
    G = lambda s: font('Grotesk', s); GM = lambda s: font('GroteskMed', s); PB = lambda s: font('PlayfairBlack', s); MO = lambda s: font('MonoBold', s)
    # beat-synced zoom punch every 0.5 s on 120 bpm
    beat = (t % 0.5) / 0.5

    if t < 3.6:
        ecg(fr, t, 1500, BLK)
        put(fr, card('YEL UNIVERSITETI · 2016', MO(40), YEL, BLK), W / 2, 330, t, -1)
        put(fr, text_layer('Kitob o\'qiydiganlar', GM(96), BLK, maxw=W - 100), W / 2, 470, t, -1)
        put(fr, text_layer('uzoqroq', PB(200), RED), W / 2, 590, t, -1, slide=0)
        put(fr, text_layer('yashagan.', GM(96), BLK, maxw=W - 100), W / 2, 860, t, -1)
        put(fr, text_layer('Qancha? Oxirigacha ko\'ring.', G(52), DIM), W / 2, 1060, t, 1.2, dur=0.3, out_t=3.3)

    if 3.6 <= t < 7.4:
        put(fr, text_layer('12 yil kuzatuv', PB(110), BLK), W / 2, 380, t, 3.65, dur=0.3, out_t=7.1)
        put(fr, text_layer('3 635 kishi, 50 yoshdan katta', GM(64), BLK, maxw=W - 120), W / 2, 560, t, 3.9, dur=0.3, out_t=7.1)
        put(fr, people(clamp((t - 4.0) / 1.2), clamp((t - 5.6) / 0.8)), W / 2, 720, t, 4.0, dur=0.2, slide=0, out_t=7.1)
        put(fr, text_layer('Kimdir kitob o\'qigan, kimdir faqat gazeta-jurnal, kimdir umuman o\'qimagan.', G(50), BLK, maxw=W - 160), W / 2, 1260, t, 5.0, out_t=7.1)

    if 7.4 <= t < 11.4:
        n = int(round(23 * ease(clamp((t - 7.6) / 1.4))))
        put(fr, text_layer('Kitobxonlar o\'rtacha', GM(72), BLK, maxw=W - 120), W / 2, 420, t, 7.45, dur=0.3, out_t=11.1)
        big = text_layer('+%d oy' % n, PB(260), RED)
        sc = 1 + 0.03 * (1 - beat) if t > 9.0 else 1
        put(fr, big.resize((int(big.size[0] * sc), int(big.size[1] * sc))), W / 2, 560, t, 7.5, dur=0.2, slide=0, out_t=11.1)
        put(fr, text_layer('ko\'proq yashagan.', GM(72), BLK, maxw=W - 120), W / 2, 880, t, 7.9, dur=0.3, out_t=11.1)
        put(fr, card('Deyarli 2 yil!', GM(70), YEL, BLK), W / 2, 1060, t, 9.0, dur=0.25, slide=0, scale_from=1.4, out_t=11.1)
        ecg(fr, t, 1500, RED, 90)

    if 11.4 <= t < 14.8:
        put(fr, text_layer('Haftasiga 3,5 soatdan ko\'p o\'qiganlarda', GM(66), BLK, maxw=W - 140), W / 2, 380, t, 11.45, dur=0.3, out_t=14.5)
        put(fr, text_layer('o\'lim xavfi', GM(66), BLK), W / 2, 600, t, 11.7, dur=0.3, out_t=14.5)
        put(fr, text_layer('23% past', PB(190), RED), W / 2, 690, t, 12.0, dur=0.25, slide=0, scale_from=1.3, out_t=14.5)
        put(fr, card('Bu kuniga taxminan 30 daqiqa', GM(56), YEL, BLK), W / 2, 980, t, 12.7, dur=0.3, out_t=14.5)
        put(fr, text_layer('Bu bog\'liqlik, kafolat emas. Lekin aynan kitob o\'qish ta\'siri gazeta-jurnaldan kuchliroq chiqqan.', G(44), DIM, maxw=W - 180), W / 2, 1190, t, 13.2, out_t=14.5)

    if t >= 14.8:
        put(fr, text_layer('Kuniga 30 daqiqa.', PB(110), BLK, maxw=W - 100), W / 2, 420, t, 14.85, dur=0.3)
        put(fr, text_layer('BookNote\'da kunlik streak boshlang va o\'qiganlaringizni belgilang.', GM(58), BLK, maxw=W - 160), W / 2, 620, t, 15.3)
        put(fr, card('booknote.uz', PB(84), YEL, BLK, pad=(70, 26)), W / 2, 960, t, 15.9, dur=0.25, slide=0, scale_from=0.7)
        put(fr, text_layer('Siz kuniga necha daqiqa o\'qiysiz? Kommentda yozing.', G(48), BLK, maxw=W - 200), W / 2, 1210, t, 16.4)
        ecg(fr, t, 1560, RED, 70)

    d = ImageDraw.Draw(fr)
    d.text((70, 120), 'BookNote', font=font('PlayfairBold', 44), fill=BLK)
    d.rectangle((0, 0, W * t / DUR, 10), fill=RED)
    return fr

def audio():
    m = Mix(DUR)
    beat = 0.5  # 120 bpm upbeat pop
    bass = [40, 40, 43, 45, 36, 36, 38, 43]
    for i in range(int(DUR / beat)):
        tt = i * beat
        m.add(kick(), tt, 0.55)
        if i % 2: m.add(highpass(noise(0.14) * np.exp(-np.linspace(0, 10, int(0.14 * SR))), 1200), tt, 0.25)  # clap
        m.add(hat(), tt + beat / 2, 0.18); m.add(hat(0.03), tt + beat * 0.75, 0.08)
        m.add(lowpass(osc(midi(bass[(i // 2) % 8]), beat * 0.9, 'saw'), 500) * np.exp(-np.linspace(0, 3, int(beat * 0.9 * SR))), tt, 0.25)
    lead = [64, 67, 71, 72, 71, 67, 64, 62]
    for i in range(int(DUR / 0.25)):
        if 3.6 <= i * 0.25 < 14.8 and i % 3 != 2:
            m.add(lowpass(pluck(midi(lead[i % 8] + 12), 0.4), 5000), i * 0.25, 0.12, pan=0.3 * ((i % 2) * 2 - 1))
    for tt in (0.0, 1.0, 2.0, 3.0): m.add(lowpass(kick(), 90), tt + 0.25, 0.6)  # heartbeat double thump
    for tt in (3.3, 7.1, 11.1, 14.5): m.add(whoosh(0.6, True), tt, 0.35)
    for i in range(14): m.add(tick(), 7.6 + i * 0.1, 0.2)
    m.add(reverb(chime(84, 2.0), 0.4), 9.0, 0.25); m.add(reverb(chime(88, 2.0), 0.4), 15.9, 0.25)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [0.0, 6.2, 10.0, 13.8, 17.0], os.path.join(S, 'prevG.png'))
    else:
        render('G_kitob_va_umr', draw, DUR, audio); print('done G')
