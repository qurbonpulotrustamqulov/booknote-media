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
| 2026-11-05 10:00 | I_usmon_mushafi_toshkent.mp4 | Usmon Mushafi, Toshkent | zumrad-oltin, yo'l xaritasi, ney + daf, 22 s | 414316765 |
| 2026-11-06 10:00 | J_navoiy_100_feol.mp4 | Navoiy, "Muhokamat ul-lug'atayn", 100 fe'l | firuza koshin naqsh, santur, 22 s | 414316800 |
| 2026-11-07 10:00 | K_termiziy_shamoil.mp4 | Imom Termiziy, "Shamoili Muhammadiya" | tun-tong gradienti, fonus, qonun arpedjio, 22 s | 414316854 |
| 2026-11-08 10:00 | L_cholpon_kecha_va_kunduz.mp4 | Cho'lpon, "Kecha va kunduz", yo'qolgan ikkinchi qism | qorong'i stol, chiroq nuri, yozuv mashinkasi, pianino + violonchel, 22 s | 418035056 |
| 2026-11-09 10:00 | M_yassaviy_hikmatlar.mp4 | Yassaviy, "Devoni hikmat" | cho'l shomi, maqbara siluet, shamol + dutor, 22 s | 418035084 |
| 2026-11-10 10:00 | N_qutadgu_bilig.mp4 | "Qutadg'u bilig", 3 qo'lyozma | indigo-oltin, uyg'ur yozuvi yomg'iri, qo'biz + 6/8 doira, 22 s | 418035118 |
| 2026-11-11 10:00 | O_hidoya_marginoniy.mp4 | Marg'inoniy, "Al-Hidoya", 1791 inglizcha tarjima | XVIII asr hujjati, mum muhr, qalam, klavesin, 22 s | 420934953 |
| 2026-11-12 10:00 | P_moturidiy_samarqand.mp4 | Imom Moturidiy, Kembrijdagi yagona qo'lyozma | oq marmar, aylanuvchi girih, xor-pad, 22 s | 420934975 |
| 2026-11-13 10:00 | Q_zamaxshariy_jorulloh.mp4 | Zamaxshariy, "Jorulloh", "Al-Kashshof" | qishdan cho'lga o'tish, qor/quyosh, tor + riq, 22 s | 420934998 |
| 2026-11-14 10:00 | R_buxoriy_ilm_saroyga_bormaydi.mp4 | Imom Buxoriy surgun qilinishi, "Ilm saroyga bormaydi" | sham va yomg'ir, qorong'i, pianino + pad, 22 s | 424740198 |
| 2026-11-15 10:00 | S_alpomish_ming_yil.mp4 | "Alpomish", ming yil og'zaki, 1928 yozib olingan, 1999 1000 yillik | cho'l tuni, oy, kamon-o'q, do'mbira + bo'g'iz drone, 22 s | 424740231 |
| 2026-11-16 10:00 | T_1938_uch_adib.mp4 | 1938: Qodiriy, Cho'lpon, Fitrat | qora-oq xotira, uch sham, violonchel, 22 s | 424740251 |

## Keyingi mavzular uchun g'oyalar (ishlatilganini o'chiring)

- Beruniy: Yer aylanasi o'lchovi, "Hindiston" kitobi.
- O'qish va miya: kitob o'qish so'z boyligi va empatiyaga ta'siri (faqat tekshirilgan tadqiqotlar).
- Dunyodagi eng qadimgi kutubxonalar.
- Ma'naviy kitoblar va allomalar: Imom Moturidiy, Hakim Termiziy, Naqshband, (Yassaviy ishlatildi) (2-tahlildan keyin eng kuchli yo'nalish).
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

### 2-tahlil (2026-11-02, B, D, E; F bugun chiqdi, hali ma'lumot yo'q)
- Instagram B (Buxoriy, 30-okt): 1864 ko'rish, 1601 qamrov, 62 like, 13 saqlash, 7 ulashish, o'rtacha tomosha 6,6 s, view rate 43%.
- Instagram E (O'tkan kunlar, 1-noy): 1789 ko'rish, 1591 qamrov, 35 like, 4 izoh, 6 saqlash, 3 ulashish, 6,0 s, 43%.
- Instagram D (Ibn Sino, 31-okt): 127 ko'rish, 4,5 s, 37%. A va C: 150-180 ko'rish, 23-26%.
- Xulosa: ma'naviy (diniy) kitob va mashhur o'zbek kitobi mavzulari 10 baravar ko'p ko'rildi. Ilm-fan/texnika mavzulari sust.
  Iliq, "qo'lyozma/gazeta" estetikasi va kitobning o'ziga oid kuchli hissiy hook ishladi.
- Qaror: I, J, K mavzulari ma'naviy meros va mashhur kitoblar; davomiylik 22 s (18 s va 33 s o'rtasida), hook 0-kadrda.
- Vaqt: 10:00 hamon eng yaxshi (getBestTime). G 12:00 sinovi 3-tahlilda baholanadi. YouTube metrikalari hali bo'sh.
- Keyingi tahlil: G, H, I chiqqach (2026-11-05 kechqurun).

### 3-tahlil (2026-11-05, F, G, H; I bugun chiqdi)
- Instagram H (Boburnoma, 4-noy): 960 ko'rish, 14 like, 9 saqlash, 5 ulashish, 5,2 s, view rate 53,6% (eng yuqori).
- Instagram F (Ulug'bek, 2-noy): 289 ko'rish, 4,6 s, 44%. G (kitob va umr, 3-noy 12:00): 129 ko'rish, 4,5 s, 39%.
- Yangilangan jami: B 1869, E 1822, H 960 ko'rish; qolganlari 127-289.
- Xulosa: "mashhur kitob va uning hikoyasi" formati ishlayapti (Sahihi Buxoriy, O'tkan kunlar, Boburnoma). Olim/fan haqidagi
  videolar (Xorazmiy, Ibn Sino, Ulug'bek, o'qish ilmi) sust. Qisqa format view rate'ni 25% dan 44-54% ga ko'tardi.
- 12:00 sinovi yomon (129 ko'rish), 10:00 qoldi.
- Qaror: L, M, N ham aniq kitob hikoyasi (Kecha va kunduz, Devoni hikmat, Qutadg'u bilig), 22 s, hook 0-kadrda.
- Keyingi tahlil: J, K, L chiqqach (2026-11-08 kechqurun).
- Kelgusi g'oyalar: "Mehrobdan chayon", "Shum bola", "Alpomish", Imom Moturidiy, Naqshband, "Hamsa" dostonlari,
  21-noyabr viktorinasi e'loni (taxminan 17-18-noyabr).

### 4-tahlil (2026-11-08, I, J, K; L bugun chiqdi)
- Instagram I (Usmon Mushafi, 5-noy): 1322 ko'rish, 34 like, 6 saqlash, 6 ulashish, 6,6 s, 50%.
- Instagram K (Termiziy, 7-noy): 1215 ko'rish, 32 like, 12 saqlash, 19 ulashish (rekord), 5,8 s, 50%.
- Instagram J (Navoiy, 6-noy): 715 ko'rish, 17 like, 3 ulashish, 5,4 s, 40%. H Boburnoma 1152 ga yetdi.
- Xulosa: ma'naviy-diniy kitoblar va allomalar barqaror 1000+ ko'rish beradi va eng ko'p ulashiladi.
  Adabiyot (Navoiy) o'rtacha. Fan sust. Format (22 s, hook 0-kadrda, 10:00) o'zgarmaydi.
- Qaror: O, P, Q ham ma'naviy allomalar va ularning kitoblari.
- Keyingi tahlil: M, N, O chiqqach (2026-11-11 kechqurun). 17-18-noyabrda 21-noyabr viktorinasi e'loni videosi kerak.

### 5-tahlil (2026-11-11, L, M, N; O bugun chiqdi)
- Instagram L (Kecha va kunduz, 8-noy): 1762 ko'rish, 58 like, 6 izoh, 8 saqlash, 10 ulashish, o'rtacha 8,8 s (rekord), 54%.
- Instagram M (Yassaviy, 9-noy): 1232 ko'rish, 24 like, 11 saqlash, 6,9 s, 54%.
- Instagram N (Qutadg'u bilig, 10-noy): 162 ko'rish, 3,7 s, 32% (sust; hook sanalar/raqamdan iborat, insoniy drama yo'q).
- Xulosa: hookda inson dramasi (yo'qotish, qurbonlik, sir) bo'lsa ko'rish va tomosha vaqti eng yuqori.
  "950 yil oldin..." kabi quruq sana hooklari ishlamaydi.
- Qaror: R, S, T hooklari insoniy drama bilan (surgun, ming yil yoddan, bir kechada uch adib).
- Keyingi tahlil: P, Q, R chiqqach (2026-11-14 kechqurun). Viktorina tafsilotlari Abdullohdan so'raldi (8-noyabr), javob yo'q.
