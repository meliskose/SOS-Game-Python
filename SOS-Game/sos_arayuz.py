import tkinter as tk

# Uygulama genelinde kullanılan özelleştirilmiş modern mesaj kutusu sınıfı
class OzelMesajKutusu(tk.Toplevel):
    def __init__(self, parent, baslik, mesaj, butonlar, renk="#3498db"):
        super().__init__(parent)
        self.sonuc = None
        self.configure(bg="#1e272e")
        self.overrideredirect(True) # Standart Windows pencere çubuğunu gizler
        self.geometry("540x340")
        self.resizable(False, False)
        self.grab_set() # Diğer pencerelere tıklanmasını engeller (Modal pencere)

        # Pencereyi ekranın ortasına yerleştirme hesaplamaları
        self.update_idletasks()
        w, h = 540, 340
        x = (self.winfo_screenwidth() // 2) - (w // 2)
        y = (self.winfo_screenheight() // 2) - (h // 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

        # Ana çerçeve ve kenarlık tasarımı
        ana = tk.Frame(self, bg="#1e272e", highlightbackground="#52687d", highlightthickness=2)
        ana.pack(fill="both", expand=True)

        # Mesaj kutusu içeriği: Renkli şerit, Başlık ve Mesaj metni
        tk.Frame(ana, bg=renk, height=7).pack(fill="x")
        tk.Label(ana, text=baslik, font=("Verdana", 18, "bold"), bg="#1e272e", fg=renk).pack(pady=(24, 18))
        tk.Label(ana, text=mesaj, font=("Verdana", 12), bg="#1e272e", fg="white", justify="center", wraplength=465).pack(pady=(0, 20))

        # Görsel ayırıcı çizgi
        ayirici = tk.Frame(ana, bg="#34495e", height=1)
        ayirici.pack(fill="x", padx=35, pady=(5, 18))

        # Butonlar için kapsayıcı çerçeve
        btn_frame = tk.Frame(ana, bg="#1e272e")
        btn_frame.pack(pady=(0, 20))

        # Gönderilen buton listesine göre butonları dinamik oluşturma
        for metin, deger in butonlar:
            # Buton tipine göre (onay/red) renk belirleme
            normal_renk = "#27ae60" if deger == "hayir" or deger == "tekrar" else "#e74c3c"
            hover_renk = "#2ecc71" if deger == "hayir" or deger == "tekrar" else "#ff5f52"
            
            b = tk.Button(
                btn_frame, text=metin, font=("Arial", 12, "bold"), bg=normal_renk, fg="white",
                activebackground=hover_renk, activeforeground="white", relief="flat", width=17, height=2, cursor="hand2",
                command=lambda d=deger: self.kapat(d)
            )
            b.pack(side="left", padx=14)
            # Fare üzerine gelince/çıkınca renk değişimi (Hover efekti)
            b.bind("<Enter>", lambda e, btn=b, hr=hover_renk: btn.config(bg=hr))
            b.bind("<Leave>", lambda e, btn=b, nr=normal_renk: btn.config(bg=nr))

    # Seçilen değeri kaydedip pencereyi kapatan metod
    def kapat(self, deger):
        self.sonuc = deger
        self.destroy()

# Oyunun oynandığı ana grafiksel arayüz sınıfı
class SOSArayuz:
    def __init__(self, root, mod="C", boyut=10):
        self.root = root
        self.mod, self.boyut = mod, boyut
        self.hucre = 600 // boyut # Tahta boyutuna göre hücre genişliğini hesaplar
        
        # Mantık katmanını (Logic) içeri aktarma ve başlatma
        from oyun_mantigi import SOSMantigi
        self.mantik = SOSMantigi(boyut=boyut)
        
        self.root.configure(bg="#2c3e50")
        self.root.state('zoomed') # Pencereyi tam ekran yapar
        
        self.ardisik_sos = 0 # Bir turda en fazla 3 SOS yapma kuralı için sayaç
        self.harf_menusu_acik = False
        self.oyun_bitti = False
        self.arayuz_olustur()
        # Pencere kapatma butonuna özel onay mekanizması ekler
        self.root.protocol("WM_DELETE_WINDOW", self.pencere_kapat_onay)

    # Ekran bileşenlerini (Panel, Skorlar, Canvas) oluşturan metod
    def arayuz_olustur(self):
        self.ust_panel = tk.Frame(self.root, bg="#2c3e50", height=80)
        self.ust_panel.pack(fill="x", pady=20)
        self.ust_panel.pack_propagate(False)

        # Ana menüye dönüş butonu
        self.ana_menu_btn = tk.Button(self.ust_panel, text="◀ ANA MENÜ", font=("Arial", 10, "bold"), bg="#34495e", fg="white", relief="flat", command=self.ana_menuye_don_onay)
        self.ana_menu_btn.place(x=50, y=18)

        # Skorların gösterildiği alan
        self.skor_container = tk.Frame(self.ust_panel, bg="#2c3e50")
        self.skor_container.place(relx=0.5, y=5, anchor="n")
        
        p1_isim = "OYUNCU 1: 0" if self.mod != "C" else "OYUNCU: 0"
        p2_isim = "OYUNCU 2: 0" if self.mod != "C" else "BİLGİSAYAR: 0"

        self.p_l = tk.Label(self.skor_container, text=p1_isim, font=("Verdana", 18, "bold"), bg="#e74c3c", fg="white", width=14, pady=5)
        self.p_l.pack(side="left", padx=10)
        self.c_l = tk.Label(self.skor_container, text=p2_isim, font=("Verdana", 18, "bold"), bg="#27ae60", fg="white", width=14, pady=5)
        self.c_l.pack(side="left", padx=10)

        # Mevcut hamle sırasını gösteren etiket
        self.sira_l = tk.Label(self.root, text="", font=("Verdana", 20, "bold"), bg="#2c3e50", fg="white")
        self.sira_l.pack(pady=(0, 10))
        self.sira_guncelle()

        # Bilgisayara karşı modda en yüksek skoru gösterir
        self.hi_l = None
        if self.mod == "C":
            hi = self.mantik.en_yuksek_skoru_getir()
            self.hi_l = tk.Label(self.ust_panel, text=f"HI {hi:05d}", font=("Courier New", 22, "bold"), bg="#2c3e50", fg="#bdc3c7")
            self.hi_l.place(relx=1.0, x=-50, y=16, anchor="ne")

        # Oyunun oynandığı çizim alanı (Canvas)
        self.canvas = tk.Canvas(self.root, width=600, height=600, bg="#1e272e", highlightthickness=2, highlightbackground="#34495e")
        self.canvas.pack(expand=True)
        self.canvas.bind("<Button-1>", self.tiklama) # Fare tıklamasını dinler
        
        # Izgara çizgilerini çizme
        for i in range(self.boyut + 1):
            self.canvas.create_line(0, i*self.hucre, 600, i*self.hucre, fill="#34495e")
            self.canvas.create_line(i*self.hucre, 0, i*self.hucre, 600, fill="#34495e")

    # Sıra değiştiğinde etiketleri ve aktif oyuncu vurgusunu günceller
    def sira_guncelle(self):
        if self.mod == "C":
            aktif = "OYUNCU" if self.mantik.sira == "P" else "BİLGİSAYAR"
        else:
            aktif = "OYUNCU 1" if self.mantik.sira == "P" else "OYUNCU 2"

        self.sira_l.config(text=f"SIRA: {aktif}")

        # Aktif oyuncu skor kutusuna siyah çerçeve (vurgu) ekler
        if self.mantik.sira == "P":
            self.p_l.config(relief="solid", bd=4)
            self.c_l.config(relief="flat", bd=0)
        else:
            self.p_l.config(relief="flat", bd=0)
            self.c_l.config(relief="solid", bd=4)

    # Canvas üzerinde bir hücreye tıklandığında koordinatları hesaplar
    def tiklama(self, event):
        if self.oyun_bitti or (self.mod == "C" and self.mantik.sira == "C"): 
            return
            
        c, r = event.x // self.hucre, event.y // self.hucre
        if 0 <= r < self.boyut and 0 <= c < self.boyut and self.mantik.tahta[r][c] == "":
            self.menu_ac(event.x_root, event.y_root, r, c)

    # Tıklanan hücrenin üzerinde S/O seçimi için küçük bir menü açar
    def menu_ac(self, x, y, r, c):
        if self.harf_menusu_acik: return
        self.harf_menusu_acik = True

        m = tk.Toplevel(self.root)
        m.overrideredirect(True)
        m.geometry(f"140x70+{x}+{y}")
        m.configure(bg="#34495e", padx=2, pady=2)
        m.grab_set()
        m.protocol("WM_DELETE_WINDOW", lambda: [setattr(self, "harf_menusu_acik", False), m.destroy()])

        def sec(harf):
            self.harf_menusu_acik = False
            m.destroy()
            self.hamle_isle(r, c, harf)
        
        tk.Button(m, text="S", font=("Arial", 14, "bold"), bg="#e74c3c", fg="white", command=lambda: sec("S")).pack(side="left", fill="both", expand=True)
        tk.Button(m, text="O", font=("Arial", 14, "bold"), bg="#3498db", fg="white", command=lambda: sec("O")).pack(side="left", fill="both", expand=True)

    # Seçilen harfi tahtaya işleyen ve SOS kontrolü yapan metod
    def hamle_isle(self, r, c, harf):
        if self.oyun_bitti: return
        
        self.mantik.hamle_kaydet(r, c, harf)
        x, y = c * self.hucre + self.hucre // 2, r * self.hucre + self.hucre // 2
        # Harfi ekrana çizer
        self.canvas.create_text(x, y, text=harf, fill="white", font=("Verdana", int(self.hucre * 0.5), "bold"), tags="txt")
        
        # Mantık katmanından SOS kontrolü sonuçlarını alır
        p, soslar = self.mantik.sos_kontrol(r, c, harf)
        
        if p > 0:
            self.mantik.puanlar[self.mantik.sira] += p
            self.ardisik_sos += 1
            # SOS olan kareleri boyar
            for s in soslar: 
                self.blok_boya_ve_ciz(s)
            
            # Skor etiketlerini günceller
            p1_baslik = "OYUNCU 1" if self.mod != "C" else "OYUNCU"
            p2_baslik = "OYUNCU 2" if self.mod != "C" else "BİLGİSAYAR"
            
            self.p_l.config(text=f"{p1_baslik}: {self.mantik.puanlar['P']}")
            self.c_l.config(text=f"{p2_baslik}: {self.mantik.puanlar['C']}")
            
            # En yüksek skor takibi
            if self.mod == "C" and self.hi_l is not None:
                mevcut_hi = self.mantik.en_yuksek_skoru_getir()
                self.hi_l.config(text=f"HI {max(mevcut_hi, self.mantik.puanlar['P']):05d}")
        
        # Tahta dolduysa oyunu bitir
        if self.mantik.tahta_dolu_mu(): 
            self.oyun_sonu()
            return

        # Sıra Değişim Mantığı: Eğer puan alınmadıysa veya ardışık 3 SOS limitine ulaşıldıysa sıra geçer
        if p == 0 or self.ardisik_sos >= 3:
            self.ardisik_sos = 0 
            self.mantik.sira = "C" if self.mantik.sira == "P" else "P"
            self.sira_guncelle()
            
            # Bilgisayarın sırası geldiyse hamle yaptırır
            if self.mod == "C" and self.mantik.sira == "C" and not self.oyun_bitti: 
                self.root.after(600, self.bilgisayar_oyna)
        else:
            self.sira_guncelle()
            # Puan alındığında bilgisayar hamlesi devam ediyorsa
            if self.mod == "C" and self.mantik.sira == "C" and not self.oyun_bitti: 
                self.root.after(600, self.bilgisayar_oyna)

    # SOS yapan blokları renklendiren ve üzerine çizgi çeken metod
    def blok_boya_ve_ciz(self, s):
        r1, c1, r2, c2 = s
        dr, dc = (r2 - r1) // 2, (c2 - c1) // 2
        yol = [(r1, c1), (r1 + dr, c1 + dc), (r2, c2)] # S-O-S hücreleri
        renk = "#e74c3c" if self.mantik.sira == "P" else "#27ae60"
        
        # Hücrelerin arka planını boyar
        for r, c in yol:
            self.canvas.create_rectangle(c*self.hucre, r*self.hucre, (c+1)*self.hucre, (r+1)*self.hucre, fill=renk, outline="#34495e")
        # SOS'un üzerine kırmızı çizgi çeker
        self.canvas.create_line(c1*self.hucre+self.hucre//2, r1*self.hucre+self.hucre//2,
                                 c2*self.hucre+self.hucre//2, r2*self.hucre+self.hucre//2, fill="red", width=4)
        # Harfleri en üste getirir (Boyama altında kalmasınlar diye)
        self.canvas.tag_raise("txt")

    # Bilgisayarın (AI) hamle yapmasını sağlayan metod
    def bilgisayar_oyna(self):
        if self.oyun_bitti: return
        k, h = self.mantik.akilli_hamle_ara() # Mantık katmanından en iyi hamleyi bulur
        if k: 
            self.hamle_isle(k[0], k[1], h)

    # Oyunun o anki durumunu kontrol eden yardımcı metod
    def oyun_devam_ediyor_mu(self):
        return not self.oyun_bitti and any(self.mantik.tahta[r][c] != "" for r in range(self.boyut) for c in range(self.boyut)) and not self.mantik.tahta_dolu_mu()

    # Oyun yarıda bırakıldığında skoru kaydeder
    def yarida_cikis_skor_kaydet(self):
        if self.mod == "C":
            self.mantik.skoru_kaydet()

    # Ana menüye dönüş butonu için onay penceresi
    def ana_menuye_don_onay(self):
        if self.oyun_devam_ediyor_mu():
            mesaj = "Oyunu yarıda bırakırsanız kaybetmiş sayılırsınız."
            if self.mod == "C":
                mesaj += "\nMevcut skorunuz HI SCORE için kaydedilecek."
            mesaj += "\n\nAna menüye dönmek istiyor musunuz?"
        else:
            mesaj = "Ana menüye dönmek istiyor musunuz?"

        d = OzelMesajKutusu(self.root, "ÇIKIŞ UYARISI", mesaj, [("OYUNA DEVAM ET", "hayir"), ("ÇIKIŞ YAP", "evet")], "#f39c12")
        self.root.wait_window(d)
        if d.sonuc == "evet":
            if self.oyun_devam_ediyor_mu():
                self.yarida_cikis_skor_kaydet()
            self.ana_menuye_git()

    # Pencere "X" butonuna basıldığında onay ister
    def pencere_kapat_onay(self):
        if self.oyun_devam_ediyor_mu():
            mesaj = "Oyunu yarıda kapatırsanız kaybetmiş sayılırsınız."
            if self.mod == "C":
                mesaj += "\nMevcut skorunuz HI SCORE için kaydedilecek."
            mesaj += "\n\nOyundan çıkmak istiyor musunuz?"
        else:
            mesaj = "Oyundan çıkmak istiyor musunuz?"

        d = OzelMesajKutusu(self.root, "ÇIKIŞ UYARISI", mesaj, [("OYUNA DEVAM ET", "hayir"), ("ÇIKIŞ YAP", "evet")], "#f39c12")
        self.root.wait_window(d)
        if d.sonuc == "evet":
            if self.oyun_devam_ediyor_mu():
                self.yarida_cikis_skor_kaydet()
            self.root.destroy()

    # Oyun bittiğinde kazananı belirler ve sonucu mesaj kutusuyla gösterir
    def oyun_sonu(self):
        self.oyun_bitti = True
        if self.mod == "C":
            self.mantik.skoru_kaydet()
        p, c = self.mantik.puanlar["P"], self.mantik.puanlar["C"]
        btns = [("TEKRAR OYNA", "tekrar"), ("ANA MENÜ", "menu")]

        # Kazananı belirleme ve renkli mesaj hazırlama
        if p > c:
            kazanan = "OYUNCU 1" if self.mod != "C" else "OYUNCU"
            msg, r = f"TEBRİKLER {kazanan} KAZANDI!\nSkor: {p} - {c}", "#27ae60"
        elif c > p:
            kazanan = "OYUNCU 2" if self.mod != "C" else "BİLGİSAYAR"
            msg, r = f"{kazanan} KAZANDI!\nSkor: {p} - {c}", "#e74c3c"
        else:
            msg, r = f"BERABERE!\nSkor: {p} - {c}", "#3498db"

        # Mesaj kutusundan gelen sonuca göre yönlendirme yapar
        d = OzelMesajKutusu(self.root, "OYUN BİTTİ", msg, btns, r)
        self.root.wait_window(d)
        if d.sonuc == "menu": 
            self.ana_menuye_git()
        elif d.sonuc == "tekrar": 
            self.yeni_oyun()

    # Uygulamayı kapatıp ana menü sınıfını tekrar yükleyen metod
    def ana_menuye_git(self):
        self.oyun_bitti = True
        self.root.destroy()
        import ana_menu
        r = tk.Tk()
        ana_menu.AnaMenu(r)
        r.mainloop()

    # Mevcut oyun oturumunu kapatıp aynı ayarlarla yeni oyun başlatan metod
    def yeni_oyun(self):
        self.oyun_bitti = True
        self.root.destroy()
        r = tk.Tk()
        SOSArayuz(r, self.mod, self.boyut)
        r.mainloop()