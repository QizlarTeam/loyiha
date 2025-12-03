# Kutubxona Boshqaruv Tizimi

Bu loyiha Python dasturlash tilida **Obyektga Yo'naltirilgan Dasturlash (OOP)** tamoyillarini o'rganish uchun yaratilgan amaliy loyiha.

## Loyiha maqsadi

Kutubxona boshqaruv tizimi orqali kitoblar va o'quvchilar bazasini yuritish, OOP tamoyillarini amaliy ko'rsatish. Loyiha boshlang'ich darajadagi o'quvchilar uchun mo'ljallangan.

## Loyiha xususiyatlari

### Asosiy funksiyalar:
- **Grafikli foydalanuvchi interfeysi (GUI)** - zamonaviy tungi dizayn
- **Kitoblar boshqaruvi** - kitob qo'shish, o'chirish, qidirish
- **O'quvchilar boshqaruvi** - o'quvchi qo'shish, o'chirish, kitob biriktirish
- **Qidiruv tizimi** - nom, muallif, janr bo'yicha qidirish
- **Statistika** - jami kitoblar, o'quvchilar, o'rtacha sahifalar
- **Ma'lumotlarni saqlash** - barcha ma'lumotlarni JSON faylga saqlash
- **Ma'lumotlarni yuklash** - saqlangan ma'lumotlarni avtomatik yuklash

### OOP tamoyillari:
- `Kitob` klassi `Muallif` obyektini o'z ichiga oladi (Kompozitsiya)
- `O'quvchi` klassi `Kitob` obyektlari bilan bog'langan (Assotsiatsiya)
- Bu Kompozitsiya va Assotsiatsiya tamoyillarining amaliy namoyishi

## Fayllar tuzilishi

```
kutubxona/
├── Loyiha.py               # Oddiy konsol dasturi (asosiy misol)
├── kutubxona_ui.py         # To'liq GUI dasturi (asosiy dastur)
├── kitoblar.json           # Kitoblar bazasi fayli
├── oquvchilar.json         # O'quvchilar bazasi fayli
└── README.md               # Loyiha hujjatlari
```

## Qanday ishlatishingiz mumkin?

### 1. Loyihani ko'chirib oling:
```bash
git clone https://github.com/Mavludaxon-jamoasi/loyiha_ishi
```

### 2. Loyiha papkasiga kiring:
```bash
cd kutubxona
```

### 3. Dasturni ishga tushiring:

#### Asosiy GUI dasturi (tavsiya etiladi):
```bash
python kutubxona_ui.py
```

#### Oddiy konsol dasturi:
```bash
python Loyiha.py
```

## Dasturdan foydalanish

### `kutubxona_ui.py` - Asosiy GUI dasturi

#### Kitoblar bo'limi:
1. **Kitob qo'shish:**
   - "➕ Yangi Kitob" tugmasini bosing
   - Barcha maydonlarni to'ldiring
   - "Saqlash" tugmasini bosing

2. **Kitob qidirish:**
   - Qidiruv maydoniga so'z kiriting
   - Qidiruv turini tanlang (Nom/Muallif/Janr)
   - "🔍 Izlash" tugmasini bosing

3. **Kitob haqida ma'lumot:**
   - Jadvaldan kitobni tanlang
   - "ℹ️ Batafsil" tugmasini bosing

4. **Kitobni o'chirish:**
   - Jadvaldan kitobni tanlang
   - "🗑️ O'chirish" tugmasini bosing
   - Tasdiqlang

#### O'quvchilar bo'limi:
1. **O'quvchi qo'shish:**
   - "👤 Yangi O'quvchi" tugmasini bosing
   - Ma'lumotlarni kiriting
   - "Qo'shish" tugmasini bosing

2. **Kitob biriktirish:**
   - Konsol versiyasida "O'quvchiga kitob biriktirish" bo'limiga o'ting
   - O'quvchini va kitobni tanlang

3. **O'quvchi kitoblarini ko'rish:**
   - Konsol versiyasida "O'quvchi o'qiyotgan kitoblarini ko'rish" tanlang

### `Loyiha.py` - Konsol dasturi

Konsol dasturida 5 ta asosiy bo'lim mavjud:
1. Kitoblar bo'limi
2. O'quvchilar bo'limi
3. Qidirish
4. Statistika
5. Chiqish

## Texnologiyalar

- **Python 3.12**
- **tkinter** - Grafikli foydalanuvchi interfeysi
- **json** - Ma'lumotlarni saqlash va yuklash
- **OOP (Object Oriented Programming)** - Obyektga yo'naltirilgan dasturlash tamoyillari

## O'rganiladigan tushunchalar

- Klasslar va obyektlar
- Kompozitsiya (Composition) tamoyili
- Assotsiatsiya (Association) tamoyili
- GUI dasturlash (tkinter)
- Fayllar bilan ishlash (JSON)
- Ma'lumotlar strukturasi (List, Dictionary)
- Event handling (Hodisalarni boshqarish)

## Klasslar tuzilishi

### `Muallif` klassi:
```python
class Muallif:
    def __init__(self, ism: str, davlat: str):
        self.ism = ism
        self.davlat = davlat
```

### `Kitob` klassi:
```python
class Kitob:
    def __init__(self, nom: str, sahifa: int, muallif: Muallif, janr: str, yil: int):
        self.nom = nom
        self.sahifa = sahifa
        self.muallif = muallif  # Kompozitsiya!
        self.janr = janr
        self.yil = yil
```

### `Oquvchi` klassi:
```python
class Oquvchi:
    def __init__(self, ism: str):
        self.ism = ism
        self.kitoblar: list[Kitob] = []  # Assotsiatsiya!
```

## Loyiha topshirig'ini bajaruvchilar

**Omonjonova Mavludaxon, Ibrohimjonova Dilrabo, A'zamova Sevinch**

## Litsenziya

Bu loyiha o'quv maqsadida yaratilgan.

## Hissa qo'shish

Agar loyihani yaxshilash bo'yicha takliflaringiz bo'lsa, pull request yuborishingiz mumkin!

---