import tkinter as tk
from tkinter import messagebox

from app.services.auth_service import AuthService
from app.ui.main_window import MainWindow


class LoginWindow:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Login - Controle de Estoque')
        self.root.geometry('400x250')
        self.root.configure(bg='#f4f6f8')

        container = tk.Frame(self.root, bg='white', padx=20, pady=20)
        container.pack(expand=True, padx=20, pady=20)

        tk.Label(container, text='Sistema de Controle de Estoque', font=('Arial', 14, 'bold'), bg='white').pack(pady=10)
        tk.Label(container, text='Usuário', bg='white').pack(anchor='w')
        self.username_entry = tk.Entry(container, width=30)
        self.username_entry.pack(pady=5)

        tk.Label(container, text='Senha', bg='white').pack(anchor='w')
        self.password_entry = tk.Entry(container, width=30, show='*')
        self.password_entry.pack(pady=5)

        tk.Button(container, text='Entrar', command=self.login, bg='#1f4e79', fg='white', width=15).pack(pady=15)
        tk.Label(container, text='Login padrão: admin | Senha: admin123', bg='white', fg='gray').pack()

    def login(self):
        username = self.username_entry.get().strip()
        password = self.password_entry.get().strip()

        if not username or not password:
            messagebox.showerror('Erro', 'Informe usuário e senha.')
            return

        user = AuthService.login(username, password)
        if not user:
            messagebox.showerror('Erro', 'Usuário ou senha inválidos.')
            return

        self.root.destroy()
        app = MainWindow(user)
        app.run()

    def run(self):
        self.root.mainloop()
