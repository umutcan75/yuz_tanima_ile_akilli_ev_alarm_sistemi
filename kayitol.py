import face_recognition
import cv2
import tkinter as tk
from tkinter import messagebox
import kayitol
import kullaniciarayuzu
from main import taninan_yuzler, taninan_isimler, taninan_yuz_kodlari


class KayitSayfasi(tk.Tk):
    def __init__(self, ana_sayfa):
        super().__init__()

        self.title("Kayıt Sayfası")
        self.ana_sayfa = ana_sayfa

        self.label = tk.Label(self, text="Kayıt Sayfası")
        self.geometry("500x400")

        adigirin = tk.Label(self)
        adigirin.config(text="Misafir Adı Giriniz")
        adigirin.pack()

        self.adigirinn = tk.Entry(self)
        self.adigirinn.pack()

        soyadgir = tk.Label(self)
        soyadgir.config(text="Soyadı Giriniz")
        soyadgir.pack()

        self.soyad = tk.Entry(self)
        self.soyad.pack()

        yas = tk.Label(self)
        yas.config(text="Yaş Giriniz")
        yas.pack()

        self.yas = tk.Entry(self)
        self.yas.pack()

        kadi = tk.Label(self)
        kadi.config(text="Kullanıcı Adı Giriniz")
        kadi.pack()

        self.kadi = tk.Entry(self)
        self.kadi.pack()

        sifre = tk.Label(self)
        sifre.config(text="Şifre Girin")
        sifre.pack()

        self.sifre = tk.Entry(self)
        self.sifre.pack()

        self.geri_dugmesi = tk.Button(self, text="Geri Dön", command=self.ana_sayfaya_git)
        self.geri_dugmesi.pack()

        self.foto_cek_dugmesi = tk.Button(self, text="Yüzü Kayıt Et", command=self.camera)
        self.foto_cek_dugmesi.pack()

        self.kaydet = tk.Button(self, text="Kayıt Et", command=self.kaydet_et)
        self.kaydet.pack()

    def kaydet_et(self):
        ad = self.adigirinn.get()
        soyad = self.soyad.get()
        yas = self.yas.get()
        kullanici_adi = self.kadi.get()
        sifre = self.sifre.get()

        if not ad or not soyad or not yas or not kullanici_adi or not sifre:
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return

        with open("kayitlar.txt", "r") as dosya:
            kayitlar = dosya.read()

        if f"Kullanıcı Adı: {kullanici_adi}\n" in kayitlar:
            messagebox.showerror("Hata", "Bu kullanıcı adı kullanılmaktadır. Lütfen farklı bir kullanıcı adı seçin.")
            return

        with open("kayitlar.txt", "a") as dosya:
            dosya.write(f"Ad: {ad}\nSoyad: {soyad}\nYaş: {yas}\nKullanıcı Adı: {kullanici_adi}\nŞifre: {sifre}\n\n")

        print("Bilgiler kaydedildi.")

    def camera(self):
        cap = cv2.VideoCapture(0)

        misafir_adi = self.kadi.get()

        foto_counter = 0
        while True:
            ret, frame = cap.read()
            cv2.imshow('Kamera Görüntüsü', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                photo_name = f"{misafir_adi}_foto{foto_counter}.jpg"
                cv2.imwrite(photo_name, frame)
                print(f"{photo_name} kaydedildi.")
                self.kayit_et_ve_tanima_ekle(misafir_adi, photo_name)  # Kaydı ve tanımı ekleyin
                foto_counter += 1

            if foto_counter >= 3:
                break

        cap.release()
        cv2.destroyAllWindows()

    def kayit_et_ve_tanima_ekle(self, kullanici_adi, foto_ad):
        taninan_yuzler.append(face_recognition.load_image_file(foto_ad))
        taninan_isimler.append(kullanici_adi)
        taninan_yuz_kodlari.append(face_recognition.face_encodings(taninan_yuzler[-1])[0])

    def ana_sayfaya_git(self):
        self.destroy()
        from main import AnaSayfa
        ana_sayfa = AnaSayfa()
        ana_sayfa.mainloop()

if __name__ == "__main__":
    kayit_sayfasi = KayitSayfasi(None)
    kayit_sayfasi.mainloop()