import tkinter as tk
import os
from sos_arayuz import SOSArayuz

# Oyunun kurallarını gösteren yardımcı pencere sınıfı
class KurallarPenceresi(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("SOS - Nasıl Oynanır?")
        self.geometry("500x560")
        self.configure(bg="#1e272e")
        self.resizable(False, False) # Pencere boyutunun değiştirilmesini engeller
        
        # Pencereyi ekranın ortasına konumlandırma hesaplamaları
        self.update_idletasks()
        x = (self.winfo_screenwidth() // 2) - 250
        y = (self.winfo_screenheight() // 2) - 280
        self.geometry(f"+{x}+{y}")

        # Görsel tasarım: Üst mavi şerit
        tk.Frame(self, bg="#3498db", height=5).pack(fill="x")
        
        # Başlık etiketi
        tk.Label(self, text="NASIL OYNANIR?", font=("Verdana", 18, "bold"), bg="#1e272e", fg="#3498db").pack(pady=(25, 15))

        # Oyun kurallarını içeren metin bloğu
        kurallar = (
            "• Sırası gelen oyuncu boş bir kareye 'S' veya 'O' harfi yerleştirir.\n\n"
            "• Yatay, dikey veya çapraz olarak yan yana 'S-O-S' harflerini getiren oyuncu 1 puan kazanır.\n\n"
            "• SOS yapan oyuncu, hamle sırasını kaybetmez ve bir kez daha oynama hakkı kazanır.\n\n"
            "• Tahtadaki tüm kareler dolduğunda oyun biter.\n\n"
            "• Oyun sonunda en yüksek puana sahip olan taraf kazanır.\n\n"
            "• Bilgisayar (Yapay Zeka) senin SOS yapmanı engellemek için akıllı hamleler yapacaktır!"
        )

        # Kuralları ekrana yazdıran etiket
        tk.Label(self, text=kurallar, font=("Verdana", 10), bg="#1e272e", fg="white", justify="left", wraplength=400).pack(pady=10, padx=45)

        # Görsel ipucu: S-O-S örneği
        ipucu_frame = tk.Frame(self, bg="#34495e", padx=20, pady=10)
        ipucu_frame.pack(pady=20)
        tk.Label(ipucu_frame, text="S - O - S", font=("Courier New", 22, "bold"), bg="#34495e", fg="#2ecc71").pack()

        # Kapatma butonu
        kapat_btn = tk.Button(self, text="ANLADIM", font=("Arial", 11, "bold"), bg="#27ae60", fg="white", relief="flat", cursor="hand2", padx=40, pady=10, command=self.destroy)
        kapat_btn.pack(pady=20)

# Uygulamanın ana giriş menüsünü yöneten sınıf
class AnaMenu:
    def __init__(self, root):
        self.root = root
        self.root.title("SOS Oyunu - Ana Menü")
        self.root.state('zoomed') # Pencereyi tam ekran modunda başlatır
        self.root.configure(bg="#2c3e50")

        # Ana içerik çerçevesi (Ekranın ortasında toplanır)
        self.f = tk.Frame(root, bg="#2c3e50")
        self.f.place(relx=0.5, rely=0.5, anchor="center")

        # Oyunun dev başlığı
        tk.Label(self.f, text="SOS OYUNU", font=("Verdana", 50, "bold"), bg="#2c3e50", fg="white").pack(pady=(0, 30))

        # Seçim değişkenleri (Tkinter StringVar ve IntVar ile kontrol edilir)
        self.mod = tk.StringVar(value="C") # Varsayılan: Bilgisayara karşı (C)
        self.boyut = tk.IntVar(value=10)   # Varsayılan tahta boyutu: 10x10

        # Oyun Modu seçim alanı
        tk.Label(self.f, text="OYUN MODU", font=("Arial", 10, "bold"), bg="#2c3e50", fg="#bdc3c7").pack()
        m_f = tk.Frame(self.f, bg="#2c3e50")
        m_f.pack(pady=10)
        
        tk.Radiobutton(m_f, text="Bilgisayara Karşı", variable=self.mod, value="C", font=("Arial", 12), bg="#2c3e50", fg="white", selectcolor="#34495e").pack(side="left", padx=20)
        tk.Radiobutton(m_f, text="2 Oyuncu (Lokal)", variable=self.mod, value="P2", font=("Arial", 12), bg="#2c3e50", fg="white", selectcolor="#34495e").pack(side="left", padx=20)

        # Tahta Boyutu seçim alanı (5x5, 10x10, 15x15)
        tk.Label(self.f, text="TAHTA BOYUTU", font=("Arial", 10, "bold"), bg="#2c3e50", fg="#bdc3c7").pack(pady=(20, 10))
        b_f = tk.Frame(self.f, bg="#2c3e50")
        b_f.pack()
        
        for b_val in [5, 10, 15]:
            tk.Radiobutton(b_f, text=f"{b_val}x{b_val}", variable=self.boyut, value=b_val, indicatoron=0, width=12, height=2, bg="#34495e", fg="white", selectcolor="#3498db", font=("Arial", 10, "bold")).pack(side="left", padx=5)

        # Butonlar için kapsayıcı çerçeve
        self.btn_container = tk.Frame(self.f, bg="#2c3e50")
        self.btn_container.pack(pady=40)

        # Nasıl Oynanır butonu
        nasil_btn = tk.Button(self.btn_container, text="NASIL OYNANIR?", font=("Verdana", 14, "bold"), bg="#27ae60", fg="white", width=22, height=2, relief="flat", cursor="hand2", command=self.nasil_oynanir_ac)
        nasil_btn.pack(pady=10)

        # Oyunu Başlat butonu
        baslat_btn = tk.Button(self.btn_container, text="OYUNU BAŞLAT", font=("Verdana", 14, "bold"), bg="#e74c3c", fg="white", width=22, height=2, relief="flat", cursor="hand2", command=self.basla)
        baslat_btn.pack(pady=10)

        # Hover (Üzerine gelme) efektleri için event binding
        baslat_btn.bind("<Enter>", lambda e: baslat_btn.config(bg="#ff5e4d"))
        baslat_btn.bind("<Leave>", lambda e: baslat_btn.config(bg="#e74c3c"))
        nasil_btn.bind("<Enter>", lambda e: nasil_btn.config(bg="#2ecc71"))
        nasil_btn.bind("<Leave>", lambda e: nasil_btn.config(bg="#27ae60"))

    # Kurallar penceresini açan metod
    def nasil_oynanir_ac(self):
        KurallarPenceresi(self.root)

    # Seçilen ayarlarla oyun ekranına geçiş yapan metod
    def basla(self):
        m, b = self.mod.get(), self.boyut.get()
        self.root.destroy() # Ana menüyü kapat
        r = tk.Tk()         # Yeni bir Tkinter oturumu başlat
        SOSArayuz(r, mod=m, boyut=b) # Oyun arayüzünü yükle
        r.mainloop()