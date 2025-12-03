"""
Kutubxona loyihasi (konsol versiyasi)

Minimal, tushunarli va boshlovchi uchun mos UI:
- Muallif
- Kitob
- O'quvchi
klasslari asosida ishlaydi.
"""


# ======== MODELLAR (klasslar) ========


class Muallif:
    """Kitob muallifi haqida ma'lumot beradi: ism, davlat."""

    def __init__(self, ism: str, davlat: str):
        self.ism = ism
        self.davlat = davlat

    def __repr__(self) -> str:
        return f"Muallif: {self.ism}, Davlati: {self.davlat}"


class Kitob:
    """Kitob haqida ma'lumot: nomi, sahifa soni, janri, yili va muallifi."""

    def __init__(self, nom: str, sahifa: int, muallif: Muallif, janr: str, yil: int):
        self.nom = nom
        self.sahifa = sahifa
        self.muallif = muallif
        self.janr = janr
        self.yil = yil

    def qisqa_info(self) -> str:
        return f"'{self.nom}' ({self.yil}), janri: {self.janr}"

    def __repr__(self) -> str:
        return (
            f"Kitob nomi: {self.nom}\n"
            f"Sahifasi: {self.sahifa}\n"
            f"Janri: {self.janr}\n"
            f"Yili: {self.yil}\n"
            f"{self.muallif}"
        )


class Oquvchi:
    """Kutubxona foydalanuvchisi, o'qiyotgan kitoblari ro'yxat bilan saqlanadi."""

    def __init__(self, ism: str):
        self.ism = ism
        self.kitoblar: list[Kitob] = []  # o'qiyotgan kitoblari

    def kitob_olish(self, kitob: Kitob) -> None:
        self.kitoblar.append(kitob)

    def kitoblar_royxati(self) -> None:
        if not self.kitoblar:
            print(f"{self.ism} hali hech qanday kitob o‘qimayapti.")
        else:
            print(f"{self.ism} o‘qiyotgan kitoblar:")
            for i, kitob in enumerate(self.kitoblar, start=1):
                print(f"{i}. {kitob.qisqa_info()}")

    def __repr__(self) -> str:
        return f"O'quvchi: {self.ism}\nO'qiyotgan kitoblari soni: {len(self.kitoblar)} ta"


# ======== MA'LUMOT SAQLASH (xotiradagi bazalar) ========

kitoblar: list[Kitob] = []
oquvchilar: list[Oquvchi] = []


def boshlangich_malumotlar() -> None:
    """Dastur ishga tushganda bir nechta tayyor obyektlar qo'shib qo'yamiz."""
    global kitoblar, oquvchilar

    muallif1 = Muallif("Muhammad Bo'zdag'", "Turkiya")
    muallif2 = Muallif("Mehmed Yildiz", "Turkiya")

    kitob1 = Kitob("Ishq imtihoni", 192, muallif1, "Roman", 2020)
    kitob2 = Kitob("Izlash", 176, muallif2, "Roman", 2018)

    kitoblar.extend([kitob1, kitob2])

    oquvchi1 = Oquvchi("Tanzila")
    oquvchi1.kitob_olish(kitob1)
    oquvchi1.kitob_olish(kitob2)

    oquvchilar.append(oquvchi1)


# ======== FOYDALI FUNKSIYALAR (UI uchun) ========


def chiziq() -> None:
    print("-" * 40)


def sarlavha(matn: str) -> None:
    chiziq()
    print(matn)
    chiziq()


def int_kiritish(savol: str, xato_matn: str = "Butun son kiriting!") -> int:
    """Takror-takror so'raydi, to'g'ri butun son kiritilmaguncha."""
    while True:
        qiymat = input(savol)
        try:
            return int(qiymat)
        except ValueError:
            print(xato_matn)


# ======== KITOBLAR BO'LIMI ========


def kitob_qoshish() -> None:
    sarlavha("YANGI KITOB QO‘SHISH")
    nom = input("Kitob nomi: ")
    sahifa = int_kiritish("Sahifalar soni: ")
    janr = input("Janri: ")
    yil = int_kiritish("Chop etilgan yili: ")

    muallif_ism = input("Muallif ismi: ")
    muallif_davlat = input("Muallif davlati: ")
    muallif = Muallif(muallif_ism, muallif_davlat)

    kitob = Kitob(nom, sahifa, muallif, janr, yil)
    kitoblar.append(kitob)
    print("✅ Kitob muvaffaqiyatli qo‘shildi.")


def barcha_kitoblar() -> None:
    sarlavha("BARCHA KITOBLAR")
    if not kitoblar:
        print("Hali birorta kitob yo‘q.")
        return

    for i, k in enumerate(kitoblar, start=1):
        print(f"{i}. {k.qisqa_info()}")


def kitoblar_menyu() -> None:
    while True:
        sarlavha("KITOBLAR BO'LIMI")
        print("1. Yangi kitob qo‘shish")
        print("2. Barcha kitoblarni ko‘rish")
        print("3. Orqaga qaytish")
        tanlov = input("Tanlovingiz: ")

        if tanlov == "1":
            kitob_qoshish()
        elif tanlov == "2":
            barcha_kitoblar()
        elif tanlov == "3":
            break
        else:
            print("Noto‘g‘ri tanlov, qaytadan urinib ko‘ring.")


# ======== O'QUVCHILAR BO'LIMI ========


def oquvchi_qoshish() -> None:
    sarlavha("YANGI O‘QUVCHI QO‘SHISH")
    ism = input("O‘quvchi ismi: ")
    oquvchi = Oquvchi(ism)
    oquvchilar.append(oquvchi)
    print("✅ O‘quvchi muvaffaqiyatli qo‘shildi.")


def barcha_oquvchilar() -> None:
    sarlavha("BARCHA O‘QUVCHILAR")
    if not oquvchilar:
        print("Hali birorta o‘quvchi yo‘q.")
        return
    for i, o in enumerate(oquvchilar, start=1):
        print(f"{i}. {o.ism} (kitoblari: {len(o.kitoblar)} ta)")


def oquvchiga_kitob_biriktirish() -> None:
    sarlavha("O‘QUVCHIGA KITOB BIRIKTIRISH")
    if not oquvchilar:
        print("Avval o‘quvchi qo‘shing.")
        return
    if not kitoblar:
        print("Avval kamida bitta kitob qo‘shing.")
        return

    # O‘quvchini tanlash
    barcha_oquvchilar()
    tanlov_oquvchi = int_kiritish("O‘quvchi raqamini tanlang: ")
    if not (1 <= tanlov_oquvchi <= len(oquvchilar)):
        print("Bunday raqamli o‘quvchi yo‘q.")
        return
    oquvchi = oquvchilar[tanlov_oquvchi - 1]

    # Kitobni tanlash
    barcha_kitoblar()
    tanlov_kitob = int_kiritish("Kitob raqamini tanlang: ")
    if not (1 <= tanlov_kitob <= len(kitoblar)):
        print("Bunday raqamli kitob yo‘q.")
        return
    kitob = kitoblar[tanlov_kitob - 1]

    oquvchi.kitob_olish(kitob)
    print(f"✅ '{kitob.nom}' kitobi {oquvchi.ism} ga biriktirildi.")


def oquvchi_kitoblari_korish() -> None:
    sarlavha("O‘QUVCHI KITOBLARINI KO‘RISH")
    if not oquvchilar:
        print("Hali o‘quvchi yo‘q.")
        return
    barcha_oquvchilar()
    tanlov = int_kiritish("O‘quvchi raqamini tanlang: ")
    if not (1 <= tanlov <= len(oquvchilar)):
        print("Bunday raqamli o‘quvchi yo‘q.")
        return
    oquvchi = oquvchilar[tanlov - 1]
    oquvchi.kitoblar_royxati()


def oquvchilar_menyu() -> None:
    while True:
        sarlavha("O‘QUVCHILAR BO'LIMI")
        print("1. Yangi o‘quvchi qo‘shish")
        print("2. Barcha o‘quvchilarni ko‘rish")
        print("3. O‘quvchiga kitob biriktirish")
        print("4. O‘quvchi o‘qiyotgan kitoblarini ko‘rish")
        print("5. Orqaga qaytish")
        tanlov = input("Tanlovingiz: ")

        if tanlov == "1":
            oquvchi_qoshish()
        elif tanlov == "2":
            barcha_oquvchilar()
        elif tanlov == "3":
            oquvchiga_kitob_biriktirish()
        elif tanlov == "4":
            oquvchi_kitoblari_korish()
        elif tanlov == "5":
            break
        else:
            print("Noto‘g‘ri tanlov, qaytadan urinib ko‘ring.")


# ======== QIDIRISH BO'LIMI ========


def qidirish_kitob_nomi_boyicha() -> None:
    sarlavha("KITOB NOMI BO‘YICHA QIDIRISH")
    if not kitoblar:
        print("Hali kitoblar yo‘q.")
        return
    q = input("Qidirayotgan nom (qismi ham bo‘lishi mumkin): ").lower()
    natijalar = [k for k in kitoblar if q in k.nom.lower()]
    if not natijalar:
        print("Mos keladigan kitob topilmadi.")
    else:
        print("Topilgan kitoblar:")
        for k in natijalar:
            print("----")
            print(k)


def qidirish_muallif_boyicha() -> None:
    sarlavha("MUALLIF BO‘YICHA QIDIRISH")
    if not kitoblar:
        print("Hali kitoblar yo‘q.")
        return
    q = input("Muallif ismi (qismi ham bo‘lishi mumkin): ").lower()
    natijalar = [k for k in kitoblar if q in k.muallif.ism.lower()]
    if not natijalar:
        print("Mos keladigan kitob topilmadi.")
    else:
        print("Topilgan kitoblar:")
        for k in natijalar:
            print("----")
            print(k)


def qidirish_menyu() -> None:
    while True:
        sarlavha("QIDIRISH BO'LIMI")
        print("1. Kitob nomi bo‘yicha qidirish")
        print("2. Muallif bo‘yicha qidirish")
        print("3. Orqaga qaytish")
        tanlov = input("Tanlovingiz: ")

        if tanlov == "1":
            qidirish_kitob_nomi_boyicha()
        elif tanlov == "2":
            qidirish_muallif_boyicha()
        elif tanlov == "3":
            break
        else:
            print("Noto‘g‘ri tanlov, qaytadan urinib ko‘ring.")


# ======== STATISTIKA BO'LIMI ========


def statistika_korsatish() -> None:
    sarlavha("STATISTIKA")
    jami_kitoblar = len(kitoblar)
    jami_oquvchilar = len(oquvchilar)

    print(f"Jami kitoblar soni: {jami_kitoblar}")
    print(f"Jami o‘quvchilar soni: {jami_oquvchilar}")

    if kitoblar:
        ortacha_sahifa = sum(k.sahifa for k in kitoblar) / len(kitoblar)
        print(f"Kitoblarning o‘rtacha sahifalar soni: {ortacha_sahifa:.1f}")

    if oquvchilar:
        # lambda ishlatmaslik uchun oddiy sikl orqali topamiz
        eng_kop_oquvchi = None
        eng_kop_kitob_soni = -1
        for oquvchi in oquvchilar:
            kitob_soni = len(oquvchi.kitoblar)
            if kitob_soni > eng_kop_kitob_soni:
                eng_kop_kitob_soni = kitob_soni
                eng_kop_oquvchi = oquvchi

        if eng_kop_oquvchi is not None:
            print(
                f"Eng ko‘p kitob o‘qiyotgan o‘quvchi: "
                f"{eng_kop_oquvchi.ism} ({eng_kop_kitob_soni} ta kitob)"
            )


# ======== ASOSIY MENYU ========


def asosiy_menyu() -> None:
    boshlangich_malumotlar()

    while True:
        sarlavha("=== KUTUBXONA DASTURI ===")
        print("1. Kitoblar bo‘limi")
        print("2. O‘quvchilar bo‘limi")
        print("3. Qidirish")
        print("4. Statistika")
        print("5. Chiqish")
        tanlov = input("Tanlovingiz: ")

        if tanlov == "1":
            kitoblar_menyu()
        elif tanlov == "2":
            oquvchilar_menyu()
        elif tanlov == "3":
            qidirish_menyu()
        elif tanlov == "4":
            statistika_korsatish()
        elif tanlov == "5":
            print("Dasturdan chiqildi. Xayr!")
            break
        else:
            print("Noto‘g‘ri tanlov, qaytadan urinib ko‘ring.")


if __name__ == "__main__":
    asosiy_menyu()


