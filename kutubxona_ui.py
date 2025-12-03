import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# --- FAYL NOMLARI ---
KITOB_FAYLI = "kitoblar.json"
OQUVCHI_FAYLI = "oquvchilar.json"

# --- RANGLAR (MIDNIGHT THEME) ---
FON_RANGI = "#2c3e50"       # Asosiy to'q ko'k fon
PANEL_RANGI = "#34495e"     # Biroz ochroq to'q ko'k (bloklar uchun)
YOZUV_RANGI = "white"       # Oq yozuv
TUGMA_RANGI = "#2980b9"     # Tugmalar uchun ko'k
KIRITISH_FONI = "white"     # Yozish joyi foni (Entry)
KIRITISH_YOZUVI = "black"   # Yozish joyidagi harflar

# ==========================================
# 1-QISM: KLASSLAR
# ==========================================

class Kitob:
    def __init__(self, nom, muallif, janr, sahifa, yil):
        self.nom = nom
        self.muallif = muallif
        self.janr = janr
        self.sahifa = sahifa
        self.yil = yil

    def lugatga_aylantir(self):
        return {
            "nom": self.nom,
            "muallif": self.muallif,
            "janr": self.janr,
            "sahifa": self.sahifa,
            "yil": self.yil
        }

class Oquvchi:
    def __init__(self, ism, familiya, guruh, telefon):
        self.ism = ism
        self.familiya = familiya
        self.guruh = guruh
        self.telefon = telefon

    def lugatga_aylantir(self):
        return {
            "ism": self.ism,
            "familiya": self.familiya,
            "guruh": self.guruh,
            "telefon": self.telefon
        }

# ==========================================
# 2-QISM: ASOSIY DASTUR
# ==========================================

class KutubxonaApp:
    def __init__(self, root):
        self.root = root
        self.root.title("🎓 Smart Kutubxona (Tungi Rejim)")
        self.root.geometry("1000x650")
        self.root.configure(bg=FON_RANGI) # Asosiy oyna foni
        
        # Dizayn stilini sozlash
        self.stil_yaratish()

        self.kitoblar = []
        self.oquvchilar = []
        self.fayldan_yuklash()

        # --- ASOSIY TABLAR ---
        self.tab_boshqaruv = ttk.Notebook(self.root)
        self.tab_boshqaruv.pack(expand=1, fill="both", padx=10, pady=10)

        # 1-Tab: Kitoblar
        self.tab_kitoblar = tk.Frame(self.tab_boshqaruv, bg=FON_RANGI)
        self.tab_boshqaruv.add(self.tab_kitoblar, text="📚 Kitoblar Fondi")

        # 2-Tab: O'quvchilar
        self.tab_oquvchilar = tk.Frame(self.tab_boshqaruv, bg=FON_RANGI)
        self.tab_boshqaruv.add(self.tab_oquvchilar, text="👥 O'quvchilar")

        self.kitoblar_oynasini_chizish()
        self.oquvchilar_oynasini_chizish()

    def stil_yaratish(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Jadval (Treeview) stili - Qora fon, Oq yozuv
        style.configure("Treeview", 
                        background=PANEL_RANGI,      # Jadval ichi
                        foreground="white",          # Jadval yozuvi
                        fieldbackground=PANEL_RANGI, # Bo'sh joylar foni
                        rowheight=25,
                        font=("Arial", 11))
        
        # Jadval sarlavhasi
        style.configure("Treeview.Heading", 
                        font=("Arial", 11, "bold"),
                        background="black",
                        foreground="white")
        
        # Tanlanganda ko'k rang bo'lsin
        style.map('Treeview', background=[('selected', '#1abc9c')])

        # Tablar (Notebook) stili
        style.configure("TNotebook", background=FON_RANGI)
        style.configure("TNotebook.Tab", background=PANEL_RANGI, foreground="white", padding=[10, 5])
        style.map("TNotebook.Tab", background=[("selected", TUGMA_RANGI)])

    # ==========================================
    # 3-QISM: KITOBLAR OYNASI
    # ==========================================

    def kitoblar_oynasini_chizish(self):
        # Qidiruv paneli
        panel = tk.Frame(self.tab_kitoblar, bg=FON_RANGI, pady=10)
        panel.pack(fill=tk.X)

        # Label (Yozuv) - OQ rangda
        tk.Label(panel, text="Qidiruv:", bg=FON_RANGI, fg=YOZUV_RANGI, font=("Arial", 12)).pack(side=tk.LEFT, padx=10)
        
        self.k_qidiruv_entry = tk.Entry(panel, font=("Arial", 12), width=20, bg=KIRITISH_FONI, fg=KIRITISH_YOZUVI)
        self.k_qidiruv_entry.pack(side=tk.LEFT, padx=5)

        self.k_saralash_turi = ttk.Combobox(panel, values=["Nom bo'yicha", "Muallif bo'yicha", "Janr bo'yicha"], state="readonly", font=("Arial", 11))
        self.k_saralash_turi.current(0)
        self.k_saralash_turi.pack(side=tk.LEFT, padx=5)

        tk.Button(panel, text="🔍 Izlash", bg=TUGMA_RANGI, fg="white", font=("Arial", 10, "bold"), command=self.kitob_qidirish).pack(side=tk.LEFT, padx=5)
        tk.Button(panel, text="🔄 Yangilash", bg="#7f8c8d", fg="white", font=("Arial", 10, "bold"), command=self.kitob_jadvalini_yangilash).pack(side=tk.LEFT, padx=5)

        # Jadval
        columns = ("nom", "muallif", "janr", "sahifa", "yil")
        self.k_jadval = ttk.Treeview(self.tab_kitoblar, columns=columns, show="headings")
        
        titles = {"nom": "Kitob Nomi", "muallif": "Muallif", "janr": "Janr", "sahifa": "Sahifa", "yil": "Yil"}
        widths = {"nom": 250, "muallif": 200, "janr": 150, "sahifa": 80, "yil": 80}

        for col, text in titles.items():
            self.k_jadval.heading(col, text=text)
            self.k_jadval.column(col, width=widths[col], anchor="center" if col in ["sahifa", "yil"] else "w")

        self.k_jadval.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)

        # Scrollbar
        scrollbar = ttk.Scrollbar(self.k_jadval, orient="vertical", command=self.k_jadval.yview)
        self.k_jadval.configure(yscrollcommand=scrollbar.set)
        scrollbar.pack(side="right", fill="y")

        # Tugmalar paneli
        btn_frame = tk.Frame(self.tab_kitoblar, bg=FON_RANGI, pady=10)
        btn_frame.pack(fill=tk.X)

        tk.Button(btn_frame, text="➕ Yangi Kitob", bg="#27ae60", fg="white", font=("Arial", 12), command=self.kitob_qoshish_oynasi).pack(side=tk.LEFT, padx=20)
        tk.Button(btn_frame, text="🗑️ O'chirish", bg="#c0392b", fg="white", font=("Arial", 12), command=self.kitob_ochirish).pack(side=tk.RIGHT, padx=20)
        tk.Button(btn_frame, text="ℹ️ Batafsil", bg="#f39c12", fg="white", font=("Arial", 12), command=self.kitob_haqida).pack(side=tk.RIGHT, padx=5)

        self.kitob_jadvalini_yangilash()

    def kitob_jadvalini_yangilash(self, data=None):
        for i in self.k_jadval.get_children():
            self.k_jadval.delete(i)
        
        if data is None:
            data = self.kitoblar

        for k in data:
            self.k_jadval.insert("", tk.END, values=(k.nom, k.muallif, k.janr, k.sahifa, k.yil))

    def kitob_qidirish(self):
        soz = self.k_qidiruv_entry.get().lower()
        turi = self.k_saralash_turi.get()

        natija = []
        for kitob in self.kitoblar:
            qoshish = False
            if "Nom" in turi and soz in kitob.nom.lower(): qoshish = True
            elif "Muallif" in turi and soz in kitob.muallif.lower(): qoshish = True
            elif "Janr" in turi and soz in kitob.janr.lower(): qoshish = True
            
            if qoshish: natija.append(kitob)
        
        if "Janr" in turi: natija.sort(key=lambda x: x.janr)
        elif "Muallif" in turi: natija.sort(key=lambda x: x.muallif)
        else: natija.sort(key=lambda x: x.nom)

        if not natija: messagebox.showinfo("Natija", "Hech narsa topilmadi.")
        self.kitob_jadvalini_yangilash(natija)

    def kitob_qoshish_oynasi(self):
        # Kichik oyna (Modal) dizayni
        top = tk.Toplevel(self.root)
        top.title("Yangi Kitob")
        top.geometry("350x450")
        top.configure(bg=FON_RANGI) # Kichik oyna ham to'q rangda

        entries = {}
        fields = ["Kitob nomi", "Muallif", "Janr", "Sahifa", "Yil"]

        for field in fields:
            # Label oq rangda, foni to'q rangda
            tk.Label(top, text=field, bg=FON_RANGI, fg=YOZUV_RANGI, font=("Arial", 10)).pack(anchor="w", padx=20, pady=(10,0))
            ent = tk.Entry(top, font=("Arial", 11), bg=KIRITISH_FONI, fg=KIRITISH_YOZUVI)
            ent.pack(fill=tk.X, padx=20, pady=5)
            entries[field] = ent

        def saqlash():
            vals = {f: entries[f].get() for f in fields}
            if all(vals.values()):
                yangi = Kitob(vals["Kitob nomi"], vals["Muallif"], vals["Janr"], vals["Sahifa"], vals["Yil"])
                self.kitoblar.append(yangi)
                self.faylga_saqlash()
                self.kitob_jadvalini_yangilash()
                top.destroy()
                messagebox.showinfo("Muvaffaqiyat", "Kitob qo'shildi!")
            else:
                messagebox.showerror("Xato", "Barcha maydonlarni to'ldiring!")

        tk.Button(top, text="SAQLASH", bg="#27ae60", fg="white", font=("Arial", 12, "bold"), command=saqlash).pack(pady=20, fill=tk.X, padx=20)

    def kitob_haqida(self):
        tanlangan = self.k_jadval.selection()
        if tanlangan:
            item = self.k_jadval.item(tanlangan)
            val = item['values']
            text = f"📖 Nom: {val[0]}\n✍️ Muallif: {val[1]}\n🎭 Janr: {val[2]}\n📄 Sahifa: {val[3]}\n📅 Yil: {val[4]}"
            messagebox.showinfo("Kitob Ma'lumoti", text)
        else:
            messagebox.showwarning("Diqqat", "Kitob tanlang.")

    def kitob_ochirish(self):
        tanlangan = self.k_jadval.selection()
        if tanlangan:
            javob = messagebox.askyesno("O'chirish", "Haqiqatan ham o'chirmoqchimisiz?")
            if javob:
                item = self.k_jadval.item(tanlangan)
                nom = item['values'][0]
                for k in self.kitoblar:
                    if k.nom == nom:
                        self.kitoblar.remove(k)
                        break
                self.faylga_saqlash()
                self.kitob_jadvalini_yangilash()

    # ==========================================
    # 4-QISM: O'QUVCHILAR OYNASI
    # ==========================================
    
    def oquvchilar_oynasini_chizish(self):
        panel = tk.Frame(self.tab_oquvchilar, bg=FON_RANGI, pady=10)
        panel.pack(fill=tk.X)
        
        tk.Button(panel, text="👤 Yangi O'quvchi", bg="#8e44ad", fg="white", font=("Arial", 11, "bold"), command=self.oquvchi_qoshish_oynasi).pack(side=tk.LEFT, padx=20)

        columns = ("ism", "familiya", "guruh", "telefon")
        self.o_jadval = ttk.Treeview(self.tab_oquvchilar, columns=columns, show="headings")

        self.o_jadval.heading("ism", text="Ism")
        self.o_jadval.heading("familiya", text="Familiya")
        self.o_jadval.heading("guruh", text="Guruh")
        self.o_jadval.heading("telefon", text="Telefon Raqam")

        self.o_jadval.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        self.oquvchi_jadvalini_yangilash()
        
        tk.Button(self.tab_oquvchilar, text="🗑️ O'quvchini O'chirish", bg="#c0392b", fg="white", command=self.oquvchi_ochirish).pack(pady=10)

    def oquvchi_qoshish_oynasi(self):
        top = tk.Toplevel(self.root)
        top.title("O'quvchi Qo'shish")
        top.geometry("300x350")
        top.configure(bg=FON_RANGI)
        
        entries = {}
        fields = ["Ism", "Familiya", "Guruh", "Telefon"]
        
        for field in fields:
            tk.Label(top, text=field, bg=FON_RANGI, fg=YOZUV_RANGI).pack(anchor="w", padx=20, pady=5)
            ent = tk.Entry(top, bg=KIRITISH_FONI, fg=KIRITISH_YOZUVI)
            ent.pack(fill=tk.X, padx=20)
            entries[field] = ent
            
        def saqlash():
            vals = {f: entries[f].get() for f in fields}
            if all(vals.values()):
                yangi = Oquvchi(vals["Ism"], vals["Familiya"], vals["Guruh"], vals["Telefon"])
                self.oquvchilar.append(yangi)
                self.faylga_saqlash()
                self.oquvchi_jadvalini_yangilash()
                top.destroy()
            else:
                messagebox.showerror("Xato", "To'ldiring!")

        tk.Button(top, text="Qo'shish", bg="#8e44ad", fg="white", command=saqlash).pack(pady=20)

    def oquvchi_jadvalini_yangilash(self):
        for i in self.o_jadval.get_children():
            self.o_jadval.delete(i)
        for o in self.oquvchilar:
            self.o_jadval.insert("", tk.END, values=(o.ism, o.familiya, o.guruh, o.telefon))

    def oquvchi_ochirish(self):
        tanlangan = self.o_jadval.selection()
        if tanlangan:
            item = self.o_jadval.item(tanlangan)
            tel = item['values'][3]
            for o in self.oquvchilar:
                if str(o.telefon) == str(tel):
                    self.oquvchilar.remove(o)
                    break
            self.faylga_saqlash()
            self.oquvchi_jadvalini_yangilash()

    # ==========================================
    # 5-QISM: FAYL
    # ==========================================

    def faylga_saqlash(self):
        with open(KITOB_FAYLI, "w", encoding="utf-8") as f:
            json.dump([k.lugatga_aylantir() for k in self.kitoblar], f, indent=4)
        with open(OQUVCHI_FAYLI, "w", encoding="utf-8") as f:
            json.dump([o.lugatga_aylantir() for o in self.oquvchilar], f, indent=4)

    def fayldan_yuklash(self):
        if os.path.exists(KITOB_FAYLI):
            try:
                with open(KITOB_FAYLI, "r", encoding="utf-8") as f:
                    self.kitoblar = [Kitob(d["nom"], d["muallif"], d["janr"], d["sahifa"], d["yil"]) for d in json.load(f)]
            except: pass
        if os.path.exists(OQUVCHI_FAYLI):
            try:
                with open(OQUVCHI_FAYLI, "r", encoding="utf-8") as f:
                    self.oquvchilar = [Oquvchi(d["ism"], d["familiya"], d["guruh"], d["telefon"]) for d in json.load(f)]
            except: pass

if __name__ == "__main__":
    root = tk.Tk()
    app = KutubxonaApp(root)
    root.mainloop()