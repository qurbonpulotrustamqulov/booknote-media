import sys; sys.path.insert(0, __import__('os').path.dirname(__file__))
from engine import *

DUR = 22.0
NIGHT = (20, 22, 52); DAWN = (196, 118, 96); PEACH = (255, 214, 170); CREAM = (255, 246, 230); GOLD = (250, 196, 110); LILAC = (200, 186, 230)

BASE = gradient(W, H, NIGHT, (60, 40, 80))
DAWNIMG = gradient(W, H, (52, 46, 96), DAWN)

def lantern(t, x, y, s=1.0):
    l = Image.new('RGBA', (int(260 * s), int(420 * s)), (0, 0, 0, 0)); d = ImageDraw.Draw(l); c = l.size[0] / 2
    fl = 0.85 + 0.15 * math.sin(t * 9 + x)
    for r in range(int(120 * s), 0, -8):
        d.ellipse((c - r, 230 * s - r, c + r, 230 * s + r), fill=GOLD + (int(10 * fl),))
    d.line((c, 0, c, 90 * s), fill=GOLD + (200,), width=3)
    d.polygon([(c - 50 * s, 120 * s), (c + 50 * s, 120 * s), (c + 70 * s, 230 * s), (c + 50 * s, 340 * s), (c - 50 * s, 340 * s), (c - 70 * s, 230 * s)], outline=GOLD, fill=(255, 190, 90, int(150 * fl)))
    d.polygon([(c - 40 * s, 90 * s), (c + 40 * s, 90 * s), (c + 50 * s, 120 * s), (c - 50 * s, 120 * s)], fill=GOLD)
    return l

def bg(t):
    p = ease_io(clamp((t - 4) / 16))
    fr = Image.blend(BASE, DAWNIMG, p)
    d = ImageDraw.Draw(fr)
    # domes and minaret silhouette (Termiz mausoleum style, simple)
    sil = (14, 12, 34, 255)
    d.rectangle((0, H - 220, W, H), fill=sil)
    d.rectangle((340, H - 380, 740, H - 220), fill=sil); d.pieslice((400, H - 520, 680, H - 240), 180, 360, fill=sil)
    d.pieslice((220, H - 450, 360, H - 330), 180, 360, fill=sil); d.rectangle((220, H - 390, 360, H - 220), fill=sil)
    d.pieslice((720, H - 450, 860, H - 330), 180, 360, fill=sil); d.rectangle((720, H - 390, 860, H - 220), fill=sil)
    d.rectangle((910, H - 620, 945, H - 220), fill=sil); d.polygon([(902, H - 620), (953, H - 620), (927, H - 680)], fill=sil)
    return fr

def draw(t):
    fr = bg(t)
    fr.alpha_composite(lantern(t, 1, 0, 0.7), (60, 120)); fr.alpha_composite(lantern(t, 2, 0, 0.55), (W - 220, 220))
    PB = lambda s: font('PlayfairBlack', s); PBo = lambda s: font('PlayfairBold', s); CI = lambda s: font('CormorantItalic', s); C = lambda s: font('Cormorant', s); G = lambda s: font('GroteskMed', s)

    if t < 4.2:
        put(fr, text_layer('Payg\'ambarimizning qiyofasi va odatlarini', CI(74), PEACH, maxw=W - 160), W / 2, 430, t, -1)
        put(fr, text_layer('so\'z bilan chizgan kitob', PB(96), CREAM, maxw=W - 80), W / 2, 640, t, -1)
        put(fr, text_layer('Muallifi termizlik olim.', PBo(76), GOLD, maxw=W - 160), W / 2, 1000, t, -1)

    if 4.2 <= t < 8.6:
        put(fr, text_layer('Imom Abu Iso', CI(76), PEACH), W / 2, 420, t, 4.25, dur=0.3, out_t=8.3)
        put(fr, text_layer('at-Termiziy', PB(130), CREAM), W / 2, 510, t, 4.4, dur=0.35, slide=0, scale_from=1.2, out_t=8.3)
        put(fr, text_layer('824-yil, Termiz yaqinidagi Bug\' qishlog\'i', G(50), LILAC, maxw=W - 180), W / 2, 720, t, 4.9, out_t=8.3)
        put(fr, text_layer('Imom Buxoriyning shogirdi bo\'lgan.', C(64), CREAM, maxw=W - 180), W / 2, 900, t, 5.8, out_t=8.3)

    if 8.6 <= t < 13.6:
        put(fr, text_layer('"Sunani Termiziy"', PB(96), CREAM, maxw=W - 140), W / 2, 420, t, 8.65, dur=0.35, out_t=13.3)
        put(fr, text_layer('Hadis ilmidagi 6 asosiy kitob, "Kutubi sitta"dan biri', C(62), PEACH, maxw=W - 180), W / 2, 580, t, 9.1, out_t=13.3)
        for i in range(6):
            x = W / 2 + (i - 2.5) * 140; hl = i in (0, 3)
            bk = Image.new('RGBA', (110, 220), (0, 0, 0, 0)); d = ImageDraw.Draw(bk)
            d.rounded_rectangle((0, 0, 109, 219), radius=10, fill=(GOLD if hl else LILAC) + (255 if hl else 120,))
            d.line((14, 30, 95, 30), fill=NIGHT, width=3); d.line((14, 190, 95, 190), fill=NIGHT, width=3)
            put(fr, bk, x, 810, t, 9.6 + i * 0.18, dur=0.3, slide=40, out_t=13.3)
        put(fr, text_layer('Buxoriy', G(40), GOLD), W / 2 - 2.5 * 140, 1050, t, 10.9, out_t=13.3)
        put(fr, text_layer('Termiziy', G(40), GOLD), W / 2 + 0.5 * 140, 1050, t, 10.9, out_t=13.3)
        put(fr, text_layer('Ikkisi ham shu zamindan.', CI(64), CREAM), W / 2, 1140, t, 11.5, out_t=13.3)

    if 13.6 <= t < 18.0:
        put(fr, text_layer('"Shamoili Muhammadiya"', PB(84), CREAM, maxw=W - 120), W / 2, 420, t, 13.65, dur=0.35, out_t=17.7)
        put(fr, text_layer('400 ga yaqin hadis: Payg\'ambarimizning tashqi ko\'rinishi, kiyimi, taomi, kulgisi, odob-axloqi haqida.', C(60), PEACH, maxw=W - 180), W / 2, 700, t, 14.1, out_t=17.7)
        put(fr, text_layer('Umrining oxirida ko\'zi ojiz bo\'lib qolgan, lekin ilmdan to\'xtamagan.', G(48), CREAM, maxw=W - 200), W / 2, 1080, t, 15.4, out_t=17.7)

    if t >= 18.0:
        put(fr, text_layer('Siz bu kitobni o\'qiganmisiz?', PB(84), CREAM, maxw=W - 160), W / 2, 420, t, 18.05, dur=0.35)
        put(fr, text_layer('BookNote\'da 10 baho olgan "Hadis va Hayot" ham shu ruhda.', C(60), PEACH, maxw=W - 200), W / 2, 720, t, 18.5)
        pl = Image.new('RGBA', (620, 136), (0, 0, 0, 0)); d = ImageDraw.Draw(pl)
        d.rounded_rectangle((0, 0, 619, 135), radius=68, fill=CREAM); s = 'booknote.uz'
        d.text(((620 - tw(s, PB(70))) / 2, 20), s, font=PB(70), fill=NIGHT)
        put(fr, pl, W / 2, 960, t, 19.2, dur=0.3, slide=0, scale_from=0.8)

    d = ImageDraw.Draw(fr); d.text((W / 2 - tw('BookNote', font('PlayfairBold', 42)) / 2, 100), 'BookNote', font=font('PlayfairBold', 42), fill=CREAM)
    d.rectangle((0, 0, W * t / DUR, 8), fill=GOLD)
    return fr

def kanun(m_, dur=1.4):
    s = pluck(midi(m_), dur, 0.998)
    return lowpass(s, 5000)

def audio():
    m = Mix(DUR)
    # Nahawand on C (minor-ish), gentle kanun arpeggios + strings, no drums until 4s, soft daf after
    chords = [[48, 55, 60, 63], [44, 51, 56, 60], [46, 53, 58, 62], [43, 50, 55, 59]]
    for i in range(6):
        m.add(reverb(pad(chords[i % 4], 4.8, 'saw', 700, a=0.05 if i == 0 else 1.0, r=1.5, gain=0.16), 0.5, 2.5), i * 4.0)
    arp = [0, 2, 3, 1, 2, 3]
    tt = 0.0
    while tt < DUR - 1:
        ch = chords[int(tt / 4.0) % 4]
        for k, a in enumerate(arp):
            m.add(reverb(kanun(ch[a] + 12), 0.35, 1.8), tt + k * 0.333, 0.16, pan=0.3 * math.sin(k))
        tt += 2.0
    beat = 60 / 90; tt = 4.2
    while tt < DUR - 1.5:
        m.add(lowpass(kick(), 160), tt, 0.3); m.add(tick(), tt + beat * 0.5, 0.08)
        tt += beat
    for tt in (0.0, 4.4, 8.65, 13.65, 18.05): m.add(reverb(lowpass(kick(), 120), 0.4, 2.5), tt, 0.7)
    for i in range(6): m.add(chime(72 + [0, 3, 7, 10, 12, 15][i], 1.2), 9.6 + i * 0.18, 0.08)
    m.add(reverb(chime(84, 3.0), 0.5), 19.2, 0.2)
    return m

if __name__ == '__main__':
    if 'preview' in sys.argv:
        preview(draw, [0.0, 6.5, 12.0, 16.5, 21.0], os.path.join(S, 'prevK.png'))
    else:
        render('K_termiziy_shamoil', draw, DUR, audio); print('done K')
