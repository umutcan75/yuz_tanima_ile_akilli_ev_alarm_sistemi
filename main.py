import face_recognition
import cv2
import tkinter as tk
from tkinter import messagebox
import kayitol
import kullaniciarayuzu
import sunuttum
from playsound import playsound
import yuztanima



# Tanınan yüzleri ve isimlerini yükle
taninan_yuzler = [
    face_recognition.load_image_file("umut.jpg")
]
taninan_isimler = ["umutcan"]

# Tanınan yüzleri kodlara dönüştür
taninan_yuz_kodlari = [face_recognition.face_encodings(yuz)[0] for yuz in taninan_yuzler]


class AnaSayfa(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("500x400")
        self.state("zoomed")
        self.title("Kullanıcı Girişi")

        karsilama = tk.Label(self)
        karsilama.config(text="Hoşgeldiniz, lütfen giriş yapınız.")
        karsilama.pack()

        kadigirin = tk.Label(self)
        kadigirin.config(text="Kullanıcı Adı giriniz.")
        kadigirin.pack()

        self.kadi = tk.Entry(self)
        self.kadi.pack()

        ksifregir = tk.Label(self)
        ksifregir.config(text="Şifre Giriniz")
        ksifregir.pack()

        self.ksifre = tk.Entry(self)
        self.ksifre.pack()

        girisbtn = tk.Button(self)
        girisbtn.config(text="Giriş Yap", command=self.girisYap)
        girisbtn.pack()


        # şifremi unuttum
        sunuttumsbtn = tk.Button(self)
        sunuttumsbtn.config(text="Şifremi unuttum", command=self.sunuttum)
        sunuttumsbtn.pack()



        kytbtn = tk.Button(self)
        kytbtn.config(text="Kayıt Ol", command=self.kayitOl)
        kytbtn.pack()

        evbtn = tk.Button(self)
        evbtn.config(text="Ev Sistemi", command=self.yuztanimagit)
        evbtn.pack(pady=50)



    def gecisYap(self, kullanici_bilgileri):
        self.destroy()  # Ana sayfa penceresini kapat
        kullanici_arayuzu = kullaniciarayuzu.KullaniciArayuzu(kullanici_bilgileri)
        kullanici_arayuzu.mainloop()

    def girisYap(self):
        kullanici_adi = self.kadi.get()
        sifre = self.ksifre.get()

        if not kullanici_adi or not sifre:
            messagebox.showerror("Hata", "Kullanıcı adı ve şifre alanları boş bırakılamaz.")
            return

        with open("kayitlar.txt", "r") as dosya:
            kayitlar = dosya.read()

        if f"Kullanıcı Adı: {kullanici_adi}\nŞifre: {sifre}\n" in kayitlar:
            print("Giriş başarılı!")
            kullanici_bilgileri = {
                "kullanici_adi": kullanici_adi,
                "sifre": sifre
            }

            # Yüz tanıma kontrolü
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            yuzler = face_recognition.face_locations(rgb_frame)
            yuz_kodlari = face_recognition.face_encodings(rgb_frame, yuzler)

            yabanci_kisi = True
            if yuz_kodlari:
                for yuz_kodu in yuz_kodlari:
                    benzerlik = [face_recognition.compare_faces([taninan], yuz_kodu, tolerance=0.5) for taninan in
                                 taninan_yuz_kodlari]
                    if any(benzerlik):
                        yabanci_kisi = False
                        break

            cap.release()
            cv2.destroyAllWindows()

            if not yabanci_kisi:
                self.gecisYap(kullanici_bilgileri)
            else:
                playsound('C:\\Users\\Umutcan\\Desktop\\pythonProject\\alarm.mp3')
                messagebox.showerror("Hata", "Yabancı kişiler sisteme giremez.",playsound())
        else:
            messagebox.showerror("Hata", "Hatalı kullanıcı adı veya şifre.")

    def kayitOl(self):
        self.destroy()  # Ana sayfa penceresini kapat
        kayit_sayfasi = kayitol.KayitSayfasi(self)
        kayit_sayfasi.mainloop()

    def yuztanimagit(self):
        self.withdraw()  # Ana sayfa penceresini gizle
        yuztanimagitt = yuztanima.YuzTanimaUygulamasi(self)
        yuztanimagitt.protocol("WM_DELETE_WINDOW", self.show_main_window)
        yuztanimagitt.mainloop()

    def show_main_window(self):
        self.deiconify()  # Ana sayfa penceresini tekrar göster



    def sunuttum(self):
        self.destroy()  # Ana sayfa penceresini kapat
        sunuttum_penceresi = sunuttum.SifreUnuttum()  # Doğru sınıf adını kullanarak çağırın
        sunuttum_penceresi.mainloop()


if __name__ == "__main__":
    ana_sayfa = AnaSayfa()
    ana_sayfa.mainloop()