import tkinter as tk
from ana_menu import AnaMenu

if __name__ == "__main__":
    # Uygulamanın ana penceresini oluşturur
    root = tk.Tk()
    
    # Ana menü sınıfını başlatır (Modüler yapı gereği)
    app = AnaMenu(root)
    
    # Olay döngüsünü başlatır
    root.mainloop()