# Davlat Botu 🌍

Davlatlar haqida maʼlumot beruvchi Telegram bot. Foydalanuvchi davlat
nomini yozadi (masalan, *Yaponiya* yoki *Oʻzbekiston*), bot esa quyidagi
maʼlumotlarni qaytaradi:

- 🏳️ Bayrogʻi
- 📍 Poytaxti
- 👥 Millati
- 🗣 Tili
- ✨ Dini
- 💰 Pul birligi
- 🏛 Davlat rahbari
- 📐 Maydoni

Bot bazasida 30 ta davlat bor (Markaziy Osiyo davlatlari + dunyoning
yirik davlatlari). Agar aniq mos kelmasa, botning "topilmadi" holati
imlosi yaqin davlatlarni taklif qiladi.

## 1. Talablar

- Python 3.10 yoki undan yuqori
- Telegram bot tokeni ([@BotFather](https://t.me/BotFather) orqali olinadi)

## 2. Oʻrnatish

```bash
# 1) Arxivni oching va papkaga kiring
cd davlat-botu

# 2) (tavsiya etiladi) virtual muhit yarating
python3 -m venv venv
source venv/bin/activate        # Windows: venv\Scripts\activate

# 3) Kerakli kutubxonalarni oʻrnating
pip install -r requirements.txt
```

## 3. Tokenni sozlash

1. Telegramda [@BotFather](https://t.me/BotFather) bilan suhbat oching,
   `/newbot` buyrugʻi bilan yangi bot yarating va u bergan tokenni nusxalang.
2. `.env.example` faylini `.env` deb nomlang:

   ```bash
   cp .env.example .env
   ```

3. `.env` faylini oching va `BOT_TOKEN=` qatoriga tokeningizni yozing:

   ```
   BOT_TOKEN=123456789:AAExampleTokenHere
   ```

## 4. Ishga tushirish

```bash
python bot.py
```

Terminalda `Davlat Botu ishga tushdi — 30 ta davlat bazada.` degan
xabarni koʻrsangiz, bot ishlayapti. Endi Telegramda botingizga oʻting va
`/start` buyrugʻini yuboring.

Botni toʻxtatish uchun terminalda `Ctrl+C` bosing.

## 5. Buyruqlar

| Buyruq     | Vazifasi                                   |
|------------|---------------------------------------------|
| `/start`   | Botni ishga tushirish, tanishtirish xabari  |
| `/royxat`  | Bazadagi barcha davlatlar roʻyxati          |
| `/help`    | Yordam xabari                               |

Bulardan tashqari, istalgan vaqt oddiy matn sifatida davlat nomini
yozishingiz mumkin.

## 6. Loyiha tuzilmasi

```
davlat-botu/
├── bot.py              — botning asosiy kodi (handlerlar, ishga tushirish)
├── countries_data.py   — davlatlar bazasi (bu faylni tahrirlab, yangi
│                          davlat qoʻshishingiz mumkin)
├── requirements.txt    — Python kutubxonalari roʻyxati
├── .env.example        — token uchun namuna fayl (lokal ishga tushirish uchun)
├── Procfile             — Railway/Heroku uchun: qaysi buyruq bilan ishga tushirish
├── railway.json         — Railway uchun build/deploy sozlamalari
├── .python-version      — Railway/Nixpacks uchun Python versiyasi
└── README.md            — ushbu fayl
```

## 7. Yangi davlat qoʻshish

`countries_data.py` faylidagi `COUNTRIES` roʻyxatiga xuddi shu
formatdagi yangi `dict` qoʻshing — botning qolgan qismini oʻzgartirish
shart emas:

```python
{
    "id": "eg",                       # ichki identifikator, unikal
    "flag": "\U0001F1EA\U0001F1EC",   # bayroq emoji (mamlakat kodi)
    "name": "Misr",                   # koʻrsatiladigan nomi
    "aliases": ["misr", "egypt"],     # qidiruv uchun, kichik harflarda
    "capital": "Qohira",
    "nationality": "Misrlik",
    "language": "Arab tili",
    "religion": "Islom",
    "currency": "Misr funti (EGP)",
    "leader": "Prezident — Abdel Fattah as-Sisi",
    "area": "1 002 450 km²",
},
```

## 8. Muhim eslatma

`leader` (davlat rahbari) maydoni vaqt oʻtishi bilan eskirishi mumkin
(saylovlar, hukumat almashinuvi va h.k.). Maʼlumotlar 2026-yil avgust
holatiga koʻra tekshirilgan — vaqti-vaqti bilan yangilab turish tavsiya
etiladi.

## 9. Railway'ga joylash

Bu loyiha Railway'da ishga tushirishga tayyor holda kelgan — `Procfile`,
`railway.json` va `.python-version` fayllari allaqachon qoʻshilgan.
Bot `run_polling()` rejimida ishlaydi, ya'ni **Worker** turidagi xizmat
sifatida ishlaydi — unga tashqi domen yoki port kerak emas, shuning
uchun Railway'ning "Generate Domain" tugmasini bosish shart emas.

### A) GitHub orqali (eng qulay usul)

1. Ushbu papkadagi fayllarni yangi GitHub repozitoriyga yuklang:

   ```bash
   cd davlat-botu
   git init
   git add .
   git commit -m "Davlat Botu"
   git branch -M main
   git remote add origin https://github.com/<foydalanuvchi-nomi>/davlat-botu.git
   git push -u origin main
   ```

   ⚠️ `.env` faylini **hech qachon** GitHub'ga yuklamang — u `.gitignore`
   fayli tufayli avtomatik e'tiborga olinmaydi, token shu tarzda maxfiy
   qoladi.

2. [railway.app](https://railway.app) saytiga kiring → **New Project** →
   **Deploy from GitHub repo** → yuklagan repozitoriyani tanlang.
3. Railway `railway.json` faylini oʻqib, avtomatik ravishda
   `pip install -r requirements.txt` va `python bot.py` buyruqlarini
   bajaradi.
4. Loyiha ochilgach, **Variables** boʻlimiga oʻting va yangi oʻzgaruvchi
   qoʻshing:

   ```
   BOT_TOKEN = @BotFather bergan tokeningiz
   ```

5. Saqlagach, Railway avtomatik qayta deploy qiladi. **Deployments** →
   **View Logs** boʻlimida `Davlat Botu ishga tushdi — 30 ta davlat
   bazada.` xabarini koʻrsangiz — bot Railway serverida ishlayapti.

### B) Railway CLI orqali (GitHub'siz, toʻgʻridan-toʻgʻri papkadan)

```bash
npm install -g @railway/cli
cd davlat-botu
railway login
railway init
railway variables --set "BOT_TOKEN=@BotFather bergan tokeningiz"
railway up
```

`railway up` joriy papkani (`.env` va `.gitignore`dagi fayllar bundan
mustasno) toʻgʻridan-toʻgʻri Railway'ga yuklab, deploy qiladi.

### Muhim eslatmalar

- Bir vaqtning oʻzida bitta tokenni faqat **bitta joyda** ishga
  tushiring (yoki lokal kompyuteringizda, yoki Railway'da) — Telegram
  bir xil tokendan ikkita parallel `polling` ulanishiga yoʻl qoʻymaydi
  va `Conflict` xatosini beradi. Railway'ga joylagach, lokal
  kompyuteringizdagi `python bot.py` jarayonini toʻxtating.
- `.env` fayli faqat **lokal** ishga tushirish uchun kerak — Railway'da
  token `.env` fayli orqali emas, **Variables** boʻlimi orqali
  beriladi (kod ikkalasini ham qoʻllab-quvvatlaydi, oʻzgartirish shart
  emas).
- Agar kelajakda `webhook` rejimiga oʻtish kerak boʻlsa,
  `python-telegram-bot` hujjatlaridagi `run_webhook()` boʻlimiga qarang.
