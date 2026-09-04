# -*- coding: utf-8 -*-
"""
Davlatlar bazasi — "Davlat Botu" uchun.

Har bir davlat quyidagi maydonlarga ega:
    id           — ichki identifikator (ISO-ga yaqin, kichik harflarda)
    flag         — davlat bayrog'i emoji ko'rinishida
    name         — foydalanuvchiga ko'rsatiladigan nomi (o'zbek tilida)
    aliases      — foydalanuvchi yozishi mumkin bo'lgan variantlar
                    (KICHIK harflarda, apostroflarsiz — normalize() shu
                    ko'rinishga keltiradi, shuning uchun bu yerda ham
                    xuddi shunday yozilgan)
    capital      — poytaxti
    nationality  — millati (demonim)
    language     — tili
    religion     — dini
    currency     — pul birligi
    leader       — davlat rahbari (lavozimi va ismi)
    area         — maydoni (formatlangan matn, km²)

YANGI DAVLAT QO'SHISH: shu ro'yxatga xuddi shu shakldagi yangi dict
qo'shish kifoya — botning qolgan qismini o'zgartirish shart emas.

ESLATMA: "leader" maydoni vaqt o'tishi bilan eskiradi (saylovlar,
almashinuvlar). Ma'lumotlar 2026-yil avgust holatiga ko'ra tekshirilgan.
Yangilab turish tavsiya etiladi.
"""

COUNTRIES = [
    {
        "id": "uz", "flag": "\U0001F1FA\U0001F1FF", "name": "Oʻzbekiston",
        "aliases": ["ozbekiston", "uzbekiston"],
        "capital": "Toshkent", "nationality": "Oʻzbek", "language": "Oʻzbek tili",
        "religion": "Islom", "currency": "Oʻzbek soʻmi (UZS)",
        "leader": "Prezident — Shavkat Mirziyoyev", "area": "448 978 km²",
    },
    {
        "id": "kz", "flag": "\U0001F1F0\U0001F1FF", "name": "Qozogʻiston",
        "aliases": ["qozogiston", "qozoqiston", "kazakhstan"],
        "capital": "Astana", "nationality": "Qozoq", "language": "Qozoq tili",
        "religion": "Islom", "currency": "Qozogʻiston tengesi (KZT)",
        "leader": "Prezident — Qosim-Jomart Toqayev", "area": "2 724 900 km²",
    },
    {
        "id": "kg", "flag": "\U0001F1F0\U0001F1EC", "name": "Qirgʻiziston",
        "aliases": ["qirgiziston", "kirgiziston", "kyrgyzstan"],
        "capital": "Bishkek", "nationality": "Qirgʻiz", "language": "Qirgʻiz tili",
        "religion": "Islom", "currency": "Qirgʻiziston somi (KGS)",
        "leader": "Prezident — Sadir Japarov", "area": "199 951 km²",
    },
    {
        "id": "tj", "flag": "\U0001F1F9\U0001F1EF", "name": "Tojikiston",
        "aliases": ["tojikiston", "tajikistan"],
        "capital": "Dushanbe", "nationality": "Tojik", "language": "Tojik tili",
        "religion": "Islom", "currency": "Tojikiston somonisi (TJS)",
        "leader": "Prezident — Emomali Rahmon", "area": "141 400 km²",
    },
    {
        "id": "tm", "flag": "\U0001F1F9\U0001F1F2", "name": "Turkmaniston",
        "aliases": ["turkmaniston", "turkmenistan"],
        "capital": "Ashxobod", "nationality": "Turkman", "language": "Turkman tili",
        "religion": "Islom", "currency": "Turkmaniston manati (TMT)",
        "leader": "Prezident — Serdar Berdimuhamedov", "area": "491 210 km²",
    },
    {
        "id": "af", "flag": "\U0001F1E6\U0001F1EB", "name": "Afgʻoniston",
        "aliases": ["afgoniston", "afghanistan"],
        "capital": "Kobul", "nationality": "Afgʻon", "language": "Dari va Pushtu tillari",
        "religion": "Islom", "currency": "Afgʻoniston afgʻoniysi (AFN)",
        "leader": "Oliy rahbar — Hibatullo Oxundzoda", "area": "652 864 km²",
    },
    {
        "id": "ru", "flag": "\U0001F1F7\U0001F1FA", "name": "Rossiya",
        "aliases": ["rossiya", "russia"],
        "capital": "Moskva", "nationality": "Rus", "language": "Rus tili",
        "religion": "Xristianlik (pravoslavlik)", "currency": "Rossiya rubli (RUB)",
        "leader": "Prezident — Vladimir Putin", "area": "17 098 246 km²",
    },
    {
        "id": "cn", "flag": "\U0001F1E8\U0001F1F3", "name": "Xitoy",
        "aliases": ["xitoy", "china"],
        "capital": "Pekin", "nationality": "Xitoylik", "language": "Xitoy tili (mandarin)",
        "religion": "Dinsiz / anʻanaviy eʻtiqodlar", "currency": "Xitoy yuani (CNY)",
        "leader": "Raisi — Si Szinpin", "area": "9 596 961 km²",
    },
    {
        "id": "in", "flag": "\U0001F1EE\U0001F1F3", "name": "Hindiston",
        "aliases": ["hindiston", "india"],
        "capital": "Yangi Dehli", "nationality": "Hind", "language": "Hind va ingliz tillari",
        "religion": "Hinduizm", "currency": "Hindiston rupiyasi (INR)",
        "leader": "Bosh vazir — Narendra Modi", "area": "3 287 263 km²",
    },
    {
        "id": "pk", "flag": "\U0001F1F5\U0001F1F0", "name": "Pokiston",
        "aliases": ["pokiston", "pakistan"],
        "capital": "Islomobod", "nationality": "Pokistonlik", "language": "Urdu va ingliz tillari",
        "religion": "Islom", "currency": "Pokiston rupiyasi (PKR)",
        "leader": "Bosh vazir — Shahbaz Sharif", "area": "881 913 km²",
    },
    {
        "id": "ir", "flag": "\U0001F1EE\U0001F1F7", "name": "Eron",
        "aliases": ["eron", "iran"],
        "capital": "Tehron", "nationality": "Eronlik", "language": "Fors tili",
        "religion": "Islom", "currency": "Eron riali (IRR)",
        "leader": "Prezident — Masʻud Pezeshkiyon", "area": "1 648 195 km²",
    },
    {
        "id": "tr", "flag": "\U0001F1F9\U0001F1F7", "name": "Turkiya",
        "aliases": ["turkiya", "turkey"],
        "capital": "Anqara", "nationality": "Turk", "language": "Turk tili",
        "religion": "Islom", "currency": "Turk lirasi (TRY)",
        "leader": "Prezident — Rajab Tayyib Erdoʻgʻon", "area": "783 562 km²",
    },
    {
        "id": "fr", "flag": "\U0001F1EB\U0001F1F7", "name": "Fransiya",
        "aliases": ["fransiya", "france"],
        "capital": "Parij", "nationality": "Fransuz", "language": "Fransuz tili",
        "religion": "Xristianlik (katoliklik)", "currency": "Yevro (EUR)",
        "leader": "Prezident — Emmanuel Makron", "area": "551 695 km²",
    },
    {
        "id": "de", "flag": "\U0001F1E9\U0001F1EA", "name": "Germaniya",
        "aliases": ["germaniya", "germany", "olmoniya"],
        "capital": "Berlin", "nationality": "Nemis", "language": "Nemis tili",
        "religion": "Xristianlik", "currency": "Yevro (EUR)",
        "leader": "Federal kansler — Fridrix Merts", "area": "357 022 km²",
    },
    {
        "id": "gb", "flag": "\U0001F1EC\U0001F1E7", "name": "Buyuk Britaniya",
        "aliases": ["buyuk britaniya", "angliya", "britaniya", "uk", "england"],
        "capital": "London", "nationality": "Britaniyalik", "language": "Ingliz tili",
        "religion": "Xristianlik (anglikanlik)", "currency": "Funt sterling (GBP)",
        "leader": "Bosh vazir — Endi Bernam", "area": "243 610 km²",
    },
    {
        "id": "it", "flag": "\U0001F1EE\U0001F1F9", "name": "Italiya",
        "aliases": ["italiya", "italy"],
        "capital": "Rim", "nationality": "Italyan", "language": "Italyan tili",
        "religion": "Xristianlik (katoliklik)", "currency": "Yevro (EUR)",
        "leader": "Bosh vazir — Jorja Meloni", "area": "301 340 km²",
    },
    {
        "id": "es", "flag": "\U0001F1EA\U0001F1F8", "name": "Ispaniya",
        "aliases": ["ispaniya", "spain"],
        "capital": "Madrid", "nationality": "Ispan", "language": "Ispan tili",
        "religion": "Xristianlik (katoliklik)", "currency": "Yevro (EUR)",
        "leader": "Bosh vazir — Pedro Sanches", "area": "505 990 km²",
    },
    {
        "id": "ua", "flag": "\U0001F1FA\U0001F1E6", "name": "Ukraina",
        "aliases": ["ukraina", "ukraine"],
        "capital": "Kiyev", "nationality": "Ukrainalik", "language": "Ukrain tili",
        "religion": "Xristianlik (pravoslavlik)", "currency": "Ukraina grivnasi (UAH)",
        "leader": "Prezident — Volodimir Zelenskiy", "area": "603 500 km²",
    },
    {
        "id": "pl", "flag": "\U0001F1F5\U0001F1F1", "name": "Polsha",
        "aliases": ["polsha", "poland"],
        "capital": "Varshava", "nationality": "Polyak", "language": "Polyak tili",
        "religion": "Xristianlik (katoliklik)", "currency": "Polsha zlotiysi (PLN)",
        "leader": "Prezident — Karol Navrotski", "area": "312 696 km²",
    },
    {
        "id": "us", "flag": "\U0001F1FA\U0001F1F8", "name": "AQSH",
        "aliases": ["aqsh", "amerika", "usa", "america", "qoshma shtatlar"],
        "capital": "Vashington", "nationality": "Amerikalik", "language": "Ingliz tili",
        "religion": "Xristianlik", "currency": "AQSH dollari (USD)",
        "leader": "Prezident — Donald Tramp", "area": "9 833 517 km²",
    },
    {
        "id": "ca", "flag": "\U0001F1E8\U0001F1E6", "name": "Kanada",
        "aliases": ["kanada", "canada"],
        "capital": "Ottava", "nationality": "Kanadalik", "language": "Ingliz va fransuz tillari",
        "religion": "Xristianlik", "currency": "Kanada dollari (CAD)",
        "leader": "Bosh vazir — Mark Karni", "area": "9 984 670 km²",
    },
    {
        "id": "br", "flag": "\U0001F1E7\U0001F1F7", "name": "Braziliya",
        "aliases": ["braziliya", "brazil"],
        "capital": "Braziliya (Brasilia)", "nationality": "Braziliyalik", "language": "Portugal tili",
        "religion": "Xristianlik (katoliklik)", "currency": "Braziliya reali (BRL)",
        "leader": "Prezident — Lula da Silva", "area": "8 515 767 km²",
    },
    {
        "id": "ar", "flag": "\U0001F1E6\U0001F1F7", "name": "Argentina",
        "aliases": ["argentina"],
        "capital": "Buenos-Ayres", "nationality": "Argentinalik", "language": "Ispan tili",
        "religion": "Xristianlik (katoliklik)", "currency": "Argentina pesosi (ARS)",
        "leader": "Prezident — Xavyer Mile", "area": "2 780 400 km²",
    },
    {
        "id": "jp", "flag": "\U0001F1EF\U0001F1F5", "name": "Yaponiya",
        "aliases": ["yaponiya", "japan"],
        "capital": "Tokio", "nationality": "Yapon", "language": "Yapon tili",
        "religion": "Sintoizm va buddizm", "currency": "Yaponiya iyenasi (JPY)",
        "leader": "Bosh vazir — Sanae Takaichi", "area": "377 975 km²",
    },
    {
        "id": "kr", "flag": "\U0001F1F0\U0001F1F7", "name": "Janubiy Koreya",
        "aliases": ["janubiy koreya", "koreya", "korea", "south korea"],
        "capital": "Seul", "nationality": "Koreys", "language": "Koreys tili",
        "religion": "Dinsiz / buddizm / xristianlik", "currency": "Koreya voni (KRW)",
        "leader": "Prezident — Lee Jae-myung", "area": "100 363 km²",
    },
    {
        "id": "id", "flag": "\U0001F1EE\U0001F1E9", "name": "Indoneziya",
        "aliases": ["indoneziya", "indonesia"],
        "capital": "Jakarta", "nationality": "Indoneziyalik", "language": "Indonez tili",
        "religion": "Islom", "currency": "Indoneziya rupiyasi (IDR)",
        "leader": "Prezident — Prabowo Subianto", "area": "1 904 569 km²",
    },
    {
        "id": "sa", "flag": "\U0001F1F8\U0001F1E6", "name": "Saudiya Arabistoni",
        "aliases": ["saudiya arabistoni", "saudiya", "saudi arabia"],
        "capital": "Ar-Riyod", "nationality": "Saudiyalik", "language": "Arab tili",
        "religion": "Islom", "currency": "Saudiya riyoli (SAR)",
        "leader": "Qirol — Salmon bin Abdulaziz Al Saʻud", "area": "2 149 690 km²",
    },
    {
        "id": "ae", "flag": "\U0001F1E6\U0001F1EA", "name": "Birlashgan Arab Amirliklari",
        "aliases": ["baa", "birlashgan arab amirliklari", "uae"],
        "capital": "Abu-Dabi", "nationality": "Amirlik", "language": "Arab tili",
        "religion": "Islom", "currency": "BAA dirhami (AED)",
        "leader": "Prezident — Muhammad bin Zoyid Al Nahyon", "area": "83 600 km²",
    },
    {
        "id": "au", "flag": "\U0001F1E6\U0001F1FA", "name": "Avstraliya",
        "aliases": ["avstraliya", "australia"],
        "capital": "Kanberra", "nationality": "Avstraliyalik", "language": "Ingliz tili",
        "religion": "Xristianlik", "currency": "Avstraliya dollari (AUD)",
        "leader": "Bosh vazir — Entoni Albanezi", "area": "7 692 024 km²",
    },
    {
        "id": "eg", "flag": "\U0001F1EA\U0001F1EC", "name": "Misr",
        "aliases": ["misr", "egypt"],
        "capital": "Qohira", "nationality": "Misrlik", "language": "Arab tili",
        "religion": "Islom", "currency": "Misr funti (EGP)",
        "leader": "Prezident — Abdel Fattah as-Sisi", "area": "1 002 450 km²",
    },
]

COUNTRIES_BY_ID = {c["id"]: c for c in COUNTRIES}

# /start va "topilmadi" xabarlarida ko'rsatiladigan tanlangan davlatlar
POPULAR_IDS = ["jp", "uz", "fr", "br", "ru", "us", "tr", "kr"]
