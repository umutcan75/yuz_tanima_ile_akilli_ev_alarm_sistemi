import tkinter as tk
from tkinter import messagebox
import cv2
import face_recognition
from main import taninan_yuzler, taninan_isimler, taninan_yuz_kodlari

class KullaniciArayuzu(tk.Tk):
    def __init__(self, kullanici_bilgileri):
        super().__init__()


        self.label = tk.Label(self, text="Misafir Kayıt Sayfası")
        self.geometry("500x400")

        adigirin = tk.Label(self, text="Misafir Adı Giriniz")
        adigirin.pack()

        self.madigir = tk.Entry(self)
        self.madigir.pack()

        soyadgir = tk.Label(self, text="Soyadı Giriniz")
        soyadgir.pack()

        self.soyad = tk.Entry(self)  # soyad özelliğini tanımlayın
        self.soyad.pack()

        self.foto_cek_dugmesi = tk.Button(self, text="Yüzü Kayıt Et", command=self.camera)
        self.foto_cek_dugmesi.pack()

        self.kaydet = tk.Button(self, text="Kayıt Et", command=self.misafir_kaydet_et)
        self.kaydet.pack()

        self.geri_dugmesi = tk.Button(self, text="Çıkış Yap", command=self.ana_sayfaya_git)
        self.geri_dugmesi.pack()

    def misafir_kaydet_et(self):
        ad = self.madigir.get()
        soyad = self.soyad.get()


        if not ad or not soyad :
            messagebox.showerror("Hata", "Lütfen tüm alanları doldurun.")
            return

        with open("misafir_kayitlari.txt", "r") as dosya:
            kayitlar = dosya.read()

        if f"Kullanıcı Adı: {ad}\n" in kayitlar:
            messagebox.showerror("Hata", "Bu kullanıcı adı kullanılmaktadır. Lütfen farklı bir kullanıcı adı seçin.")
            return

        with open("misafir_kayitlari.txt", "a") as dosya:
            dosya.write(f"Ad: {ad}\nSoyad: {soyad}\n")

        print("Bilgiler kaydedildi.")

    def camera(self):
        cap = cv2.VideoCapture(0)

        while True:
            ret, frame = cap.read()
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            yuzler = face_recognition.face_locations(rgb_frame)
            yuz_kodlari = face_recognition.face_encodings(rgb_frame, yuzler)

            for yuz_kodu, (top, right, bottom, left) in zip(yuz_kodlari, yuzler):
                benzerlik = [face_recognition.compare_faces([taninan], yuz_kodu, tolerance=0.6) for taninan in
                             taninan_yuz_kodlari]
                isimler = [taninan_isimler[i] if benzerlik[i][0] else "Bilinmeyen" for i in range(len(taninan_yuz_kodlari))]

                for isim, (top, right, bottom, left) in zip(isimler, yuzler):
                    cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
                    cv2.putText(frame, isim, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

            cv2.imshow('Yuz Tanima', frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    def ana_sayfaya_git(self):
        self.destroy()
        from main import AnaSayfa
        ana_sayfa = AnaSayfa()
        ana_sayfa.mainloop()