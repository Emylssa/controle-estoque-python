import tkinter as tk
from tkinter import ttk, messagebox

from app.models.product_model import ProductModel
from app.models.movement_model import MovementModel
from app.models.user_model import UserModel
from app.services.stock_service import StockService


class MainWindow:
    def __init__(self, user):
        self.user = user
        self.root = tk.Tk()
        self.root.title('Sistema de Controle de Estoque')
        self.root.geometry('1100x650')
        self.root.configure(bg='#f4f6f8')
        self.selected_product_id = None

        self._build_header()
        self._build_tabs()
        self.load_products()
        self.load_movements()
        if self.user['profile'] == 'Administrador':
            self.load_users()

    def _build_header(self):
        header = tk.Frame(self.root, bg='#1f4e79', height=70)
        header.pack(fill='x')
        tk.Label(
            header,
            text=f"Controle de Estoque | Usuário: {self.user['name']} ({self.user['profile']})",
            bg='#1f4e79', fg='white', font=('Arial', 14, 'bold')
        ).pack(side='left', padx=20, pady=20)
        tk.Button(header, text='Sair', command=self.root.destroy, bg='white').pack(side='right', padx=20)

    def _build_tabs(self):
        self.notebook = ttk.Notebook(self.root)
        self.notebook.pack(fill='both', expand=True, padx=15, pady=15)

        self.products_tab = tk.Frame(self.notebook, bg='white')
        self.movements_tab = tk.Frame(self.notebook, bg='white')
        self.report_tab = tk.Frame(self.notebook, bg='white')
        self.users_tab = tk.Frame(self.notebook, bg='white')

        self.notebook.add(self.products_tab, text='Produtos')
        self.notebook.add(self.movements_tab, text='Movimentações')
        self.notebook.add(self.report_tab, text='Alertas')
        if self.user['profile'] == 'Administrador':
            self.notebook.add(self.users_tab, text='Usuários')

        self._build_products_tab()
        self._build_movements_tab()
        self._build_report_tab()
        if self.user['profile'] == 'Administrador':
            self._build_users_tab()

    def _build_products_tab(self):
        form = tk.LabelFrame(self.products_tab, text='Cadastro / Edição de Produto', padx=10, pady=10, bg='white')
        form.pack(fill='x', padx=10, pady=10)

        self.name_var = tk.StringVar()
        self.category_var = tk.StringVar()
        self.quantity_var = tk.StringVar()
        self.min_quantity_var = tk.StringVar()
        self.unit_var = tk.StringVar()
        self.search_var = tk.StringVar()

        fields = [
            ('Nome*', self.name_var),
            ('Categoria*', self.category_var),
            ('Quantidade inicial*', self.quantity_var),
            ('Quantidade mínima*', self.min_quantity_var),
            ('Unidade*', self.unit_var),
        ]

        for i, (label, var) in enumerate(fields):
            tk.Label(form, text=label, bg='white').grid(row=0, column=i, padx=5, sticky='w')
            tk.Entry(form, textvariable=var, width=18).grid(row=1, column=i, padx=5)

        tk.Button(form, text='Salvar produto', command=self.save_product, bg='#1f7a1f', fg='white').grid(row=1, column=5, padx=8)
        tk.Button(form, text='Atualizar produto', command=self.edit_product, bg='#f0ad4e').grid(row=1, column=6, padx=8)
        tk.Button(form, text='Limpar', command=self.clear_product_form).grid(row=1, column=7, padx=8)

        search_frame = tk.Frame(self.products_tab, bg='white')
        search_frame.pack(fill='x', padx=10)
        tk.Label(search_frame, text='Pesquisar:', bg='white').pack(side='left')
        tk.Entry(search_frame, textvariable=self.search_var, width=30).pack(side='left', padx=5)
        tk.Button(search_frame, text='Buscar', command=self.search_products).pack(side='left')
        tk.Button(search_frame, text='Mostrar todos', command=self.load_products).pack(side='left', padx=5)

        self.products_tree = ttk.Treeview(
            self.products_tab,
            columns=('id', 'name', 'category', 'quantity', 'min_quantity', 'unit', 'status'),
            show='headings',
            height=18
        )
        headings = [
            ('id', 'ID'), ('name', 'Nome'), ('category', 'Categoria'), ('quantity', 'Estoque'),
            ('min_quantity', 'Mínimo'), ('unit', 'Unidade'), ('status', 'Status')
        ]
        for col, title in headings:
            self.products_tree.heading(col, text=title)
        self.products_tree.column('id', width=50)
        self.products_tree.bind('<<TreeviewSelect>>', self.on_select_product)
        self.products_tree.tag_configure('low_stock', background='#ffd6d6')
        self.products_tree.pack(fill='both', expand=True, padx=10, pady=10)

    def _build_movements_tab(self):
        form = tk.LabelFrame(self.movements_tab, text='Entrada / Saída de Estoque', padx=10, pady=10, bg='white')
        form.pack(fill='x', padx=10, pady=10)

        self.move_product_var = tk.StringVar()
        self.move_type_var = tk.StringVar(value='Entrada')
        self.move_qty_var = tk.StringVar()
        self.note_var = tk.StringVar()

        tk.Label(form, text='Produto (ID)', bg='white').grid(row=0, column=0, padx=5, sticky='w')
        tk.Entry(form, textvariable=self.move_product_var, width=15).grid(row=1, column=0, padx=5)
        tk.Label(form, text='Tipo', bg='white').grid(row=0, column=1, padx=5, sticky='w')
        ttk.Combobox(form, textvariable=self.move_type_var, values=['Entrada', 'Saída'], state='readonly', width=12).grid(row=1, column=1, padx=5)
        tk.Label(form, text='Quantidade', bg='white').grid(row=0, column=2, padx=5, sticky='w')
        tk.Entry(form, textvariable=self.move_qty_var, width=15).grid(row=1, column=2, padx=5)
        tk.Label(form, text='Observação', bg='white').grid(row=0, column=3, padx=5, sticky='w')
        tk.Entry(form, textvariable=self.note_var, width=40).grid(row=1, column=3, padx=5)
        tk.Button(form, text='Registrar movimentação', command=self.register_movement, bg='#1f4e79', fg='white').grid(row=1, column=4, padx=10)

        self.movements_tree = ttk.Treeview(
            self.movements_tab,
            columns=('id', 'product', 'type', 'quantity', 'user', 'note', 'created_at'),
            show='headings',
            height=20
        )
        for col, title in [
            ('id', 'ID'), ('product', 'Produto'), ('type', 'Tipo'), ('quantity', 'Quantidade'),
            ('user', 'Usuário'), ('note', 'Observação'), ('created_at', 'Data/Hora')
        ]:
            self.movements_tree.heading(col, text=title)
        self.movements_tree.pack(fill='both', expand=True, padx=10, pady=10)

    def _build_report_tab(self):
        tk.Label(
            self.report_tab,
            text='Produtos abaixo do estoque mínimo aparecem destacados.',
            bg='white', font=('Arial', 12, 'bold')
        ).pack(anchor='w', padx=10, pady=10)

        self.alerts_tree = ttk.Treeview(
            self.report_tab,
            columns=('id', 'name', 'quantity', 'min_quantity', 'category'),
            show='headings',
            height=20
        )
        for col, title in [
            ('id', 'ID'), ('name', 'Produto'), ('quantity', 'Estoque atual'),
            ('min_quantity', 'Mínimo'), ('category', 'Categoria')
        ]:
            self.alerts_tree.heading(col, text=title)
        self.alerts_tree.tag_configure('alert', background='#ffe08a')
        self.alerts_tree.pack(fill='both', expand=True, padx=10, pady=10)

    def _build_users_tab(self):
        form = tk.LabelFrame(self.users_tab, text='Cadastro de Usuários (somente administrador)', padx=10, pady=10, bg='white')
        form.pack(fill='x', padx=10, pady=10)

        self.user_name_var = tk.StringVar()
        self.user_username_var = tk.StringVar()
        self.user_password_var = tk.StringVar()
        self.user_profile_var = tk.StringVar(value='Comum')

        for i, (label, var) in enumerate([
            ('Nome*', self.user_name_var), ('Usuário*', self.user_username_var), ('Senha*', self.user_password_var)
        ]):
            tk.Label(form, text=label, bg='white').grid(row=0, column=i, padx=5, sticky='w')
            tk.Entry(form, textvariable=var, width=20, show='*' if 'Senha' in label else '').grid(row=1, column=i, padx=5)

        tk.Label(form, text='Perfil*', bg='white').grid(row=0, column=3, padx=5, sticky='w')
        ttk.Combobox(form, textvariable=self.user_profile_var, values=['Administrador', 'Comum'], state='readonly', width=15).grid(row=1, column=3, padx=5)
        tk.Button(form, text='Cadastrar usuário', command=self.register_user, bg='#1f7a1f', fg='white').grid(row=1, column=4, padx=10)

        self.users_tree = ttk.Treeview(self.users_tab, columns=('id', 'name', 'username', 'profile', 'created_at'), show='headings', height=18)
        for col, title in [('id', 'ID'), ('name', 'Nome'), ('username', 'Usuário'), ('profile', 'Perfil'), ('created_at', 'Criado em')]:
            self.users_tree.heading(col, text=title)
        self.users_tree.pack(fill='both', expand=True, padx=10, pady=10)

    def validate_int(self, value: str, field_name: str) -> int:
        try:
            return int(value)
        except ValueError:
            raise ValueError(f'O campo {field_name} deve conter apenas números inteiros.')

    def save_product(self):
        try:
            if not all([self.name_var.get().strip(), self.category_var.get().strip(), self.quantity_var.get().strip(), self.min_quantity_var.get().strip(), self.unit_var.get().strip()]):
                raise ValueError('Preencha todos os campos obrigatórios do produto.')
            quantity = self.validate_int(self.quantity_var.get(), 'Quantidade inicial')
            min_quantity = self.validate_int(self.min_quantity_var.get(), 'Quantidade mínima')
            StockService.add_product(self.name_var.get().strip(), self.category_var.get().strip(), quantity, min_quantity, self.unit_var.get().strip())
            messagebox.showinfo('Sucesso', 'Produto cadastrado com sucesso!')
            self.clear_product_form()
            self.load_products()
        except Exception as e:
            messagebox.showerror('Erro', str(e))

    def edit_product(self):
        try:
            if not self.selected_product_id:
                raise ValueError('Selecione um produto na tabela para atualizar.')
            if not all([self.name_var.get().strip(), self.category_var.get().strip(), self.min_quantity_var.get().strip(), self.unit_var.get().strip()]):
                raise ValueError('Preencha os campos obrigatórios para atualizar.')
            min_quantity = self.validate_int(self.min_quantity_var.get(), 'Quantidade mínima')
            StockService.update_product(self.selected_product_id, self.name_var.get().strip(), self.category_var.get().strip(), min_quantity, self.unit_var.get().strip())
            messagebox.showinfo('Sucesso', 'Produto atualizado com sucesso!')
            self.clear_product_form()
            self.load_products()
        except Exception as e:
            messagebox.showerror('Erro', str(e))

    def clear_product_form(self):
        self.selected_product_id = None
        self.name_var.set('')
        self.category_var.set('')
        self.quantity_var.set('')
        self.min_quantity_var.set('')
        self.unit_var.set('')

    def on_select_product(self, event):
        selection = self.products_tree.selection()
        if not selection:
            return
        item = self.products_tree.item(selection[0])['values']
        self.selected_product_id = item[0]
        self.name_var.set(item[1])
        self.category_var.set(item[2])
        self.quantity_var.set(item[3])
        self.min_quantity_var.set(item[4])
        self.unit_var.set(item[5])
        self.move_product_var.set(str(item[0]))

    def load_products(self):
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        products = ProductModel.list_products()
        for p in products:
            status = 'Abaixo do mínimo' if p['quantity'] < p['min_quantity'] else 'OK'
            tags = ('low_stock',) if status != 'OK' else ()
            self.products_tree.insert('', 'end', values=(p['id'], p['name'], p['category'], p['quantity'], p['min_quantity'], p['unit'], status), tags=tags)
        self.load_alerts()

    def search_products(self):
        for item in self.products_tree.get_children():
            self.products_tree.delete(item)
        products = ProductModel.search_products(self.search_var.get().strip())
        for p in products:
            status = 'Abaixo do mínimo' if p['quantity'] < p['min_quantity'] else 'OK'
            tags = ('low_stock',) if status != 'OK' else ()
            self.products_tree.insert('', 'end', values=(p['id'], p['name'], p['category'], p['quantity'], p['min_quantity'], p['unit'], status), tags=tags)

    def register_movement(self):
        try:
            product_id = self.validate_int(self.move_product_var.get(), 'Produto (ID)')
            quantity = self.validate_int(self.move_qty_var.get(), 'Quantidade')
            if quantity <= 0:
                raise ValueError('A quantidade deve ser maior que zero.')
            StockService.move_stock(product_id, self.move_type_var.get(), quantity, self.user['id'], self.note_var.get().strip())
            messagebox.showinfo('Sucesso', 'Movimentação registrada com sucesso!')
            self.move_qty_var.set('')
            self.note_var.set('')
            self.load_products()
            self.load_movements()
        except Exception as e:
            messagebox.showerror('Erro', str(e))

    def load_movements(self):
        for item in self.movements_tree.get_children():
            self.movements_tree.delete(item)
        for m in MovementModel.list_movements():
            self.movements_tree.insert('', 'end', values=(m['id'], m['product_name'], m['movement_type'], m['quantity'], m['username'], m['note'], m['created_at']))

    def load_alerts(self):
        for item in self.alerts_tree.get_children():
            self.alerts_tree.delete(item)
        for p in ProductModel.list_products():
            if p['quantity'] < p['min_quantity']:
                self.alerts_tree.insert('', 'end', values=(p['id'], p['name'], p['quantity'], p['min_quantity'], p['category']), tags=('alert',))

    def register_user(self):
        try:
            if self.user['profile'] != 'Administrador':
                raise ValueError('Apenas administradores podem cadastrar usuários.')
            if not all([self.user_name_var.get().strip(), self.user_username_var.get().strip(), self.user_password_var.get().strip()]):
                raise ValueError('Preencha todos os campos obrigatórios do usuário.')
            if UserModel.get_by_username(self.user_username_var.get().strip()):
                raise ValueError('Já existe um usuário com esse login.')
            UserModel.create_user(
                self.user_name_var.get().strip(),
                self.user_username_var.get().strip(),
                self.user_password_var.get().strip(),
                self.user_profile_var.get()
            )
            messagebox.showinfo('Sucesso', 'Usuário cadastrado com sucesso!')
            self.user_name_var.set('')
            self.user_username_var.set('')
            self.user_password_var.set('')
            self.user_profile_var.set('Comum')
            self.load_users()
        except Exception as e:
            messagebox.showerror('Erro', str(e))

    def load_users(self):
        for item in self.users_tree.get_children():
            self.users_tree.delete(item)
        for u in UserModel.list_users():
            self.users_tree.insert('', 'end', values=(u['id'], u['name'], u['username'], u['profile'], u['created_at']))

    def run(self):
        self.root.mainloop()
