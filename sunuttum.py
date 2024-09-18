import tkinter as tk
from tkinter import messagebox

class SifreUnuttum(tk.Tk):
    def __init__(self):
        super().__init__()

        self.geometry("300x200")
        self.title("Şifremi Unuttum")

        self.label = tk.Label(self, text="Lütfen e-posta adresinizi girin:")
        self.label.pack()

        self.email_entry = tk.Entry(self)
        self.email_entry.pack()

        self.reset_button = tk.Button(self, text="Şifremi Sıfırla", command=self.sifre_sifirla)
        self.reset_button.pack()

    def sifre_sifirla(self):
        email = self.email_entry.get()

        # Burada e-posta adresinin geçerli bir e-posta olup olmadığını kontrol etmek
        # ve gerekli işlemleri yapmak gerekebilir.

        if email:
            messagebox.showinfo("Bilgi", "Şifre sıfırlama talimatları e-posta adresinize gönderildi.")
        else:
            messagebox.showerror("Hata", "Lütfen geçerli bir e-posta adresi girin.")

if __name__ == "__main__":
    sifre_unuttum_penceresi = SifreUnuttum()
    sifre_unuttum_penceresi.mainloop()