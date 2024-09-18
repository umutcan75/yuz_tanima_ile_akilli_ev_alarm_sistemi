import cv2
import face_recognition
import pygame
import threading
import tkinter as tk
from PIL import Image, ImageTk
import time

class YuzTanimaUygulamasi(tk.Tk):
    def __init__(self, ana_pencere):
        self.ana_pencere = ana_pencere
        self.ana_pencere.title("Yüz Tanıma ve Alarm")

        self.taninan_yuzler = [
            face_recognition.load_image_file("umut.jpg"),

        ]
        self.taninan_isimler = ["umutcan"]

        self.taninan_yuz_kodlari = [face_recognition.face_encodings(yuz)[0] for yuz in self.taninan_yuzler]

        self.alarm_caldi = False
        self.son_alarm_zamani = 0
        self.alarm_araligi = 3

        self.kamera = cv2.VideoCapture(0)

        self.video_etiketi = tk.Label(ana_pencere)
        self.video_etiketi.pack()

        self.yuzleri_kontrol_et()

    def alarm_sesi_cal(self):
        if not self.alarm_caldi:

            pygame.mixer.init()
            pygame.mixer.music.load('alarm.mp3')
            pygame.mixer.music.play()
            self.alarm_caldi = True
           # messagebox.showerror("Hata", "Yabancı Yüzler tespit edildi.")
    def alarmi_sifirla(self):
        self.alarm_caldi = False

    def yuzleri_kontrol_et(self):
        ret, cerceve = self.kamera.read()
        if ret:
            rgb_cerceve = cv2.cvtColor(cerceve, cv2.COLOR_BGR2RGB)

            yuzler = face_recognition.face_locations(rgb_cerceve)
            yuz_kodlari = face_recognition.face_encodings(rgb_cerceve, yuzler)

            alarm_aktif = False

            for yuz_kodu, (ust, sag, alt, sol) in zip(yuz_kodlari, yuzler):
                benzerlik = [face_recognition.compare_faces([taninan], yuz_kodu, tolerance=0.6) for taninan in self.taninan_yuz_kodlari]
                isimler = [self.taninan_isimler[i] if benzerlik[i][0] else "Bilinmeyen" for i in range(len(self.taninan_yuz_kodlari))]

                for isim, (ust, sag, alt, sol) in zip(isimler, yuzler):
                    cv2.rectangle(cerceve, (sol, ust), (sag, alt), (0, 255, 0), 2)
                    cv2.putText(cerceve, isim, (sol, ust - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

                    if isim == "Bilinmeyen":
                        su_an = time.time()
                        if not alarm_aktif or su_an - self.son_alarm_zamani >= self.alarm_araligi:
                            self.alarm_sesi_cal()
                            self.son_alarm_zamani = su_an
                            alarm_aktif = True

            if not alarm_aktif:
                self.alarmi_sifirla()

            self.cerceveyi_goster(cerceve)

    def cerceveyi_goster(self, cerceve):
        cerceve = cv2.cvtColor(cerceve, cv2.COLOR_BGR2RGB)
        img = Image.fromarray(cerceve)
        img_tk = ImageTk.PhotoImage(image=img)
        self.video_etiketi.img_tk = img_tk
        self.video_etiketi.config(image=img_tk)
        self.ana_pencere.after(10, self.yuzleri_kontrol_et)

if __name__ == "__main__":
    ana_pencere = tk.Tk()
    uygulama = YuzTanimaUygulamasi(ana_pencere)
    ana_pencere.mainloop()