import os
import random

# Oyunun tüm matematiksel ve mantıksal kurallarını yöneten sınıf
class SOSMantigi:
    def __init__(self, boyut=10):
        self.boyut = boyut
        # Oyun tahtasını belirtilen boyutta boş bir matris olarak oluşturur
        self.tahta = [["" for _ in range(boyut)] for _ in range(boyut)]
        self.sira = "P" # P: Oyuncu (Player), C: Bilgisayar (Computer)
        self.puanlar = {"P": 0, "C": 0} # Skor takibi için sözlük (dictionary)
        self.dosya_adi = "skorlar.txt" # En yüksek skorun saklanacağı dosya

    # Kalıcı depolamadan (txt dosyası) en yüksek skoru okur
    def en_yuksek_skoru_getir(self):
        if not os.path.exists(self.dosya_adi): return 0
        try:
            with open(self.dosya_adi, "r") as f:
                icerik = f.read().strip()
                # Dosya içeriği sayısal ise döndür, değilse 0 döndür (Hata yönetimi)
                return int(icerik) if icerik else 0
        except: return 0 # Okuma sırasında hata oluşursa programın çökmesini engeller

    # Eğer yeni bir rekor kırıldıysa bunu dosyaya kaydeder
    def skoru_kaydet(self):
        mevcut_hi = self.en_yuksek_skoru_getir()
        # Mevcut oyuncu puanı rekordan büyükse dosyayı günceller
        if self.puanlar["P"] > mevcut_hi:
            with open(self.dosya_adi, "w") as f: f.write(str(self.puanlar["P"]))

    # Tahtaya konulan son harfin bir SOS oluşturup oluşturmadığını kontrol eder
    def sos_kontrol(self, r, c, harf):
        puan = 0
        soslar = [] # Oluşan SOS'ların koordinatlarını saklar (boyama işlemi için)
        # Kontrol edilecek yönler: Yatay, Dikey, Sağ Çapraz, Sol Çapraz
        yonler = [(0, 1), (1, 0), (1, 1), (1, -1)]
        
        if harf == "S":
            # S harfi eklendiğinde ileri veya geri yönde O-S dizilimi aranır
            for dr, dc in yonler:
                for yon in [1, -1]:
                    nr1, nc1, nr2, nc2 = r+dr*yon, c+dc*yon, r+dr*2*yon, c+dc*2*yon
                    # Tahta sınırları içerisinde mi kontrolü
                    if 0 <= nr2 < self.boyut and 0 <= nc2 < self.boyut:
                        if self.tahta[nr1][nc1] == "O" and self.tahta[nr2][nc2] == "S":
                            puan += 1
                            soslar.append((r, c, nr2, nc2))
        else: # Harf "O" ise
            # O harfi eklendiğinde iki yanında S-S olup olmadığına bakılır
            for dr, dc in yonler:
                nr1, nc1, nr2, nc2 = r+dr, c+dc, r-dr, c-dc
                if 0 <= nr1 < self.boyut and 0 <= nc1 < self.boyut and 0 <= nr2 < self.boyut and 0 <= nc2 < self.boyut:
                    if self.tahta[nr1][nc1] == "S" and self.tahta[nr2][nc2] == "S":
                        puan += 1
                        soslar.append((nr1, nc1, nr2, nc2))
        return puan, soslar

    # Belirtilen koordinata harfi yerleştirir
    def hamle_kaydet(self, r, c, harf):
        self.tahta[r][c] = harf

    # Tahtada boş yer kalıp kalmadığını kontrol eder (Oyun bitiş şartı)
    def tahta_dolu_mu(self):
        return all(self.tahta[r][c] != "" for r in range(self.boyut) for c in range(self.boyut))

    # Bilgisayarın hamle kararını veren yapay zeka algoritması (Heuristic AI)
    def akilli_hamle_ara(self):
        # 1. Öncelik: Bilgisayar kendi SOS yapabiliyorsa o hamleyi seçer (Hücum)
        for r in range(self.boyut):
            for c in range(self.boyut):
                if self.tahta[r][c] == "":
                    for h in ["S", "O"]:
                        self.tahta[r][c] = h
                        p, _ = self.sos_kontrol(r, c, h)
                        self.tahta[r][c] = "" # Simülasyonu geri al
                        if p > 0: return (r, c), h

        # 2. Öncelik: Rakibin SOS yapabileceği kritik kareleri tespit eder ve engeller (Savunma)
        for r in range(self.boyut):
            for c in range(self.boyut):
                if self.tahta[r][c] == "":
                    for h in ["S", "O"]:
                        self.tahta[r][c] = h
                        # Rakibin bir sonraki hamlede puan kazanıp kazanmayacağını test eder
                        p, _ = self.sos_kontrol(r, c, h)
                        self.tahta[r][c] = ""
                        if p > 0: 
                            # Rakibin tehlikeli hamlesini bulduğunda o kareyi kapatır
                            return (r, c), h

        # 3. Öncelik: Eğer ne hücum ne savunma fırsatı varsa rastgele bir boş kareye oynar
        boslar = [(r, c) for r in range(self.boyut) for c in range(self.boyut) if self.tahta[r][c] == ""]
        if boslar: return random.choice(boslar), random.choice(["S", "O"])
        return None, None