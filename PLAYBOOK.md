# BookNote video playbook

Bu repozitoriy BookNote (booknote.uz) Instagram va YouTube videolari uchun.
Videolar `videos/` papkasida turadi; Metricool ularni
`https://raw.githubusercontent.com/qurbonpulotrustamqulov/booknote-media/main/videos/<fayl>.mp4`
havolasidan oladi (bu usul 2026-10-28 da sinab ko'rildi va ishladi).

## Qoidalar (Abdulloh talablari)

- Kitoblar bo'yicha savol-javob / viktorina-test videolari QILINMAYDI. Faktlar va qiziqarli ma'lumotlar ishlatiladi.
- Har bir video o'z vizual uslubi va musiqasiga ega, bitta shablon takrorlanmaydi.
- Abdullohning portret rasmi ishlatilmaydi.
- Diktor ovozi yo'q (sifatli o'zbekcha TTS yo'q); musiqa va effektlar `engine.py` da sintez qilinadi.
- Faktlar faqat ishonchli, tekshirilgan bo'lsin; shubhali raqam bo'lsa "taxminan", "rivoyat qilinishicha" deb yoziladi.
- Auditoriya: o'zbek kitobxonlari; BookNote top kitoblari asosan ma'naviy-diniy adabiyot (Baxtiyor oila, Sohilsiz dengiz, Axloqus Solihiyn, Hadis va Hayot, Saodat Asri Qissalari va b.), lekin badiiy adabiyot ham aralashtiriladi.
- Reklama byudjeti yo'q, o'sish organik. Promo-kod yo'q. CTA: booknote.uz, referal (3 do'st = 1 oy Pro), streak, yillik maqsad.
- Viktorina: 21-noyabr 2026, umumiy sovrin fondi 200 000 so'm (taklif: 100/60/40 ming).

## Metricool

- Brand (blogId): 7696064, vaqt mintaqasi Asia/Tashkent. Tarmoqlar: Instagram @booknoteuz, YouTube.
- Har post: Instagram REEL + YouTube short bitta postda, autoPublish true, madeForKids false, category EDUCATION.
- Boshlang'ich eng yaxshi vaqt: 10:00 (Toshkent). Har 3 postdan keyin metrikalarga qarab o'zgartiriladi.
- Izoh matni tuzilishi: hook + 2-3 qisqa paragraf fakt + savol (komment uchun) + "📚 booknote.uz (havola bio'da)" + 7-8 heshteg.

## Video ishlab chiqarish

`tools/engine.py` (kadr chizish, animatsiya, audio sintez, ffmpeg render). Har video alohida skript:
`python3 tools/<skript>.py preview` (kontakt-varaq PNG) va `python3 tools/<skript>.py` (MP4 render).
Kerak: python3, numpy, scipy, pillow (raqm bilan), ffmpeg. `pip install scipy` kerak bo'lishi mumkin.
Render natijasi `engine.OUT` papkasiga tushadi; keyin `videos/` ga nusxa olib, commit va push qilinadi.

## Jurnal (yangi qatorlarni pastga qo'shing)

| Sana | Fayl | Mavzu | Uslub | Metricool post |
| --- | --- | --- | --- | --- |
| 2026-10-28 10:00 | A_xorazmiy_algoritm.mp4 | Xorazmiy va "algoritm" so'zi | qorong'i texno, glitch, elektron musiqa | 408284941 |
| 2026-10-29 10:00 | C_6_daqiqa_oqish.mp4 | 6 daqiqa o'qish stressni 68% kamaytiradi (Sussex, 2009) | och infografika, lo-fi | 408285734 |
| 2026-10-30 10:00 | B_buxoriy_16_yil.mp4 | Imom Buxoriy, 16 yil, 600 000 hadis | qo'lyozma/pergament, sharqona musiqa (Hijoz) | 408285761 |
| 2026-10-31 10:00 | D_ibn_sino_tib_qonunlari.mp4 | Ibn Sino, "Tib qonunlari" | ko'k chizma (blueprint), kinematik pad + pianino | 408285784 |
| 2026-11-01 10:00 | E_otkan_kunlar_birinchi_roman.mp4 | "O'tkan kunlar" — birinchi o'zbek romani | 1920-yillar gazetasi, grammofon vals | 408287767 |
| 2026-11-02 10:00 | F_ulugbek_yulduz_yili.mp4 | Ulug'bek, yulduz yili 1 daqiqa aniqlikda, Ziji Ko'ragoniy | tungi osmon, lidiy ambient + qo'ng'iroqchalar, 18 s | 411501726 |
| 2026-11-03 12:00 | G_kitob_va_umr.mp4 | Kitob o'qish va umr (Bavishi va b., Yale 2016) | sariq-qora kinetik tipografiya, EKG chizig'i, 120 bpm pop, 18 s | 411501753 |
| 2026-11-04 10:00 | H_boburnoma_kundalik.mp4 | Bobur va "Boburnoma" | miniatyura (qizil-oltin), tanpura + tabla, 18 s | 411501779 |

## Keyingi mavzular uchun g'oyalar (ishlatilganini o'chiring)

- Alisher Navoiy "Muhokamat ul-lug'atayn" (1499): turkiy tilni himoya qilgan asar.
- Beruniy: Yer aylanasi o'lchovi, "Hindiston" kitobi.
- O'qish va miya: kitob o'qish so'z boyligi va empatiyaga ta'siri (faqat tekshirilgan tadqiqotlar).
- Dunyodagi eng qadimgi kutubxonalar, Usmon Mushafi (Toshkent).
- BookNote imkoniyatlari: streak, yillik maqsad, Ijodxona, referal (animatsion tushuntirish, ilova skrinshotlarisiz).
- Viktorina e'loni (21-noyabr), g'oliblar e'loni (natija Abdullohdan olinadi).

## Metrika tahlillari

### 1-tahlil (2026-10-30, A va C videolari; B uchun hali ma'lumot yo'q, YouTube bo'sh)
- Instagram A: 150 ko'rish, 137 qamrov, 3 like, o'rtacha tomosha 4,4 s, view rate 25,9%.
- Instagram C: 173 ko'rish, 147 qamrov, 4 like, 1 saqlash, o'rtacha tomosha 4,3 s, view rate 23,7%.
- Xulosa: 33-36 s videoda odamlar ~4 soniyada ketyapti. Hook sekin (matn bo'sh ekrandan chiqadi), video uzun.
- O'zgarishlar (F, G, H dan boshlab): 18 s davomiylik; hook matni 0-kadrdanoq to'liq ko'rinadi; har ~3,5 s yangi sahna;
  tepada progress chizig'i; kattaroq shrift. C (o'qish ilmi) biroz yaxshiroq, shuning uchun G shu yo'nalishda.
- Vaqt: Instagram eng yaxshi soat 10:00 (11-12 ham kuchli). G 12:00 da sinov sifatida qo'yildi, keyingi tahlilda solishtiriladi.
- Keyingi tahlil: F, G, H chiqqach (2026-11-04 kechqurun).
