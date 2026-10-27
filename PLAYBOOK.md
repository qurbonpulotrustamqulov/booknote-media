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
| 2026-11-01 10:00 | E_otkan_kunlar_birinchi_roman.mp4 | "O'tkan kunlar" — birinchi o'zbek romani | 1920-yillar gazetasi, grammofon vals | (rejalashtiriladi) |

## Keyingi mavzular uchun g'oyalar (ishlatilganini o'chiring)

- Alisher Navoiy "Muhokamat ul-lug'atayn" (1499): turkiy tilni himoya qilgan asar.
- Mirzo Ulug'bek rasadxonasi va "Ziji Ko'ragoniy" yulduzlar jadvali.
- Beruniy: Yer aylanasi o'lchovi, "Hindiston" kitobi.
- Bobur "Boburnoma": hukmdorning kundaligi.
- O'qish va miya: kitob o'qish so'z boyligi va empatiyaga ta'siri (faqat tekshirilgan tadqiqotlar).
- Dunyodagi eng qadimgi kutubxonalar, Usmon Mushafi (Toshkent).
- BookNote imkoniyatlari: streak, yillik maqsad, Ijodxona, referal (animatsion tushuntirish, ilova skrinshotlarisiz).
- Viktorina e'loni (21-noyabr), g'oliblar e'loni (natija Abdullohdan olinadi).
