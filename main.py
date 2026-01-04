import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import datetime
from datetime import datetime as dt
import calendar
from tkinter import font as tkfont
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use('TkAgg')
from PIL import Image, ImageTk
import io
import base64

class FontManager:
    """Manajer font Apple-style"""
    @staticmethod
    def get_fonts():
        fonts = {}
        try:
            # Coba load font San Francisco (font Apple)
            fonts["regular"] = ("Helvetica", 11)
            fonts["bold"] = ("Helvetica", 11, "bold")
            fonts["large"] = ("Helvetica", 16)
            fonts["title"] = ("Helvetica", 20, "bold")
            fonts["small"] = ("Helvetica", 9)
        except:
            # Fallback ke font sistem
            fonts["regular"] = ("Segoe UI", 11) if os.name == 'nt' else ("Ubuntu", 11)
            fonts["bold"] = ("Segoe UI", 11, "bold") if os.name == 'nt' else ("Ubuntu", 11, "bold")
            fonts["large"] = ("Segoe UI", 16) if os.name == 'nt' else ("Ubuntu", 16)
            fonts["title"] = ("Segoe UI", 20, "bold") if os.name == 'nt' else ("Ubuntu", 20, "bold")
            fonts["small"] = ("Segoe UI", 9) if os.name == 'nt' else ("Ubuntu", 9)
        return fonts

class IconManager:
    """Manajer ikon untuk aplikasi - versi sederhana dengan emoji"""
    def __init__(self):
        self.icons = {}
        self.load_icons()
    
    def load_icons(self):
        """Load ikon sederhana atau gunakan emoji sebagai fallback"""
        try:
            # Coba buat ikon sederhana menggunakan PIL
            self.create_simple_icons()
        except:
            # Jika gagal, gunakan emoji
            self.use_emoji_icons()
    
    def create_simple_icons(self):
        """Buat ikon sederhana dengan PIL"""
        icon_size = (24, 24)
        
        # Ikon Home (kotak dengan pintu)
        home_img = Image.new('RGBA', icon_size, (0, 0, 0, 0))
        home_draw = ImageDraw.Draw(home_img)
        home_draw.rectangle([4, 4, 20, 20], outline='#007aff', width=2)
        home_draw.rectangle([8, 12, 16, 20], fill='#007aff')
        self.icons["home"] = ImageTk.PhotoImage(home_img)
        
        # Ikon Stats (grafik)
        stats_img = Image.new('RGBA', icon_size, (0, 0, 0, 0))
        stats_draw = ImageDraw.Draw(stats_img)
        # Buat grafik sederhana
        points = [(4, 20), (8, 12), (12, 16), (16, 8), (20, 4)]
        for i in range(len(points)-1):
            stats_draw.line([points[i], points[i+1]], fill='#007aff', width=2)
        self.icons["stats"] = ImageTk.PhotoImage(stats_img)
        
        # Ikon Add (plus)
        add_img = Image.new('RGBA', icon_size, (0, 0, 0, 0))
        add_draw = ImageDraw.Draw(add_img)
        add_draw.line([12, 4, 12, 20], fill='#007aff', width=2)
        add_draw.line([4, 12, 20, 12], fill='#007aff', width=2)
        self.icons["add"] = ImageTk.PhotoImage(add_img)
        
        # Ikon Export (panah keluar)
        export_img = Image.new('RGBA', icon_size, (0, 0, 0, 0))
        export_draw = ImageDraw.Draw(export_img)
        export_draw.line([4, 12, 18, 12], fill='#007aff', width=2)
        export_draw.line([18, 12, 14, 8], fill='#007aff', width=2)
        export_draw.line([18, 12, 14, 16], fill='#007aff', width=2)
        self.icons["export"] = ImageTk.PhotoImage(export_img)
        
        # Ikon Settings (roda gigi)
        settings_img = Image.new('RGBA', icon_size, (0, 0, 0, 0))
        settings_draw = ImageDraw.Draw(settings_img)
        # Lingkaran dengan gigi
        settings_draw.ellipse([4, 4, 20, 20], outline='#007aff', width=2)
        # Gigi-gigi
        for angle in [0, 45, 90, 135, 180, 225, 270, 315]:
            rad = angle * 3.14159 / 180
            x1 = 12 + 8 * math.cos(rad)
            y1 = 12 + 8 * math.sin(rad)
            x2 = 12 + 10 * math.cos(rad)
            y2 = 12 + 10 * math.sin(rad)
            settings_draw.line([x1, y1, x2, y2], fill='#007aff', width=2)
        self.icons["settings"] = ImageTk.PhotoImage(settings_img)
    
    def use_emoji_icons(self):
        """Gunakan emoji sebagai ikon"""
        self.icons = {
            "home": "🏠",
            "stats": "📊",
            "add": "➕",
            "export": "📤",
            "settings": "⚙️"
        }
    
    def get(self, name):
        return self.icons.get(name)

# Import tambahan untuk membuat ikon
from PIL import ImageDraw
import math

class Transaction:
    """Class untuk mewakili satu transaksi"""
    def __init__(self, date, category, amount, type_, description=""):
        self.date = date
        self.category = category
        self.amount = float(amount)
        self.type = type_  # "income" atau "expense"
        self.description = description
    
    def to_dict(self):
        return {
            "date": self.date,
            "category": self.category,
            "amount": self.amount,
            "type": self.type,
            "description": self.description
        }

class FinanceApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Finance Manager • Apple Style")
        self.root.geometry("1200x700")
        
        # Setup styling Apple-like
        self.setup_styles()
        
        # Inisialisasi komponen
        self.fonts = FontManager.get_fonts()
        self.icons = IconManager()
        self.transactions = []
        self.categories = {
            "income": ["Gaji", "Investasi", "Bonus", "Freelance", "Lainnya"],
            "expense": ["Makanan", "Transportasi", "Hiburan", "Belanja", "Kesehatan", "Pendidikan", "Tagihan", "Lainnya"]
        }
        
        # Data bulanan
        self.current_month = datetime.datetime.now().month
        self.current_year = datetime.datetime.now().year
        
        # Load data jika ada
        self.load_data()
        
        # Setup UI
        self.setup_ui()
        
        # Update tampilan
        self.update_display()
    
    def setup_styles(self):
        """Setup warna dan styling Apple-like"""
        style = ttk.Style()
        
        # Warna Apple modern
        self.colors = {
            "bg": "#f5f5f7",
            "card_bg": "#ffffff",
            "sidebar_bg": "#f8f9fa",
            "primary": "#007aff",
            "primary_dark": "#0056b3",
            "success": "#34c759",
            "danger": "#ff3b30",
            "warning": "#ff9500",
            "text": "#1d1d1f",
            "text_light": "#86868b",
            "border": "#d2d2d7"
        }
        
        # Konfigurasi style
        self.root.configure(bg=self.colors["bg"])
        style.theme_use('clam')
        
        # Configure ttk styles
        style.configure("Card.TFrame", background=self.colors["card_bg"])
        style.configure("Sidebar.TFrame", background=self.colors["sidebar_bg"])
        style.configure("Primary.TButton", 
                       background=self.colors["primary"],
                       foreground="white",
                       borderwidth=0,
                       focuscolor="none")
        style.map("Primary.TButton",
                 background=[('active', self.colors["primary_dark"])])
    
    def setup_ui(self):
        """Setup antarmuka pengguna"""
        # Main container
        main_container = ttk.Frame(self.root, style="Card.TFrame")
        main_container.pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
        
        # Sidebar
        self.setup_sidebar(main_container)
        
        # Main content area
        content_frame = ttk.Frame(main_container, style="Card.TFrame")
        content_frame.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(20, 0))
        
        # Header
        self.setup_header(content_frame)
        
        # Stats cards
        self.setup_stats(content_frame)
        
        # Transaction table
        self.setup_transaction_table(content_frame)
        
        # Add transaction form (hidden by default)
        self.setup_transaction_form(content_frame)
    
    def setup_sidebar(self, parent):
        """Setup sidebar navigasi"""
        sidebar = ttk.Frame(parent, style="Sidebar.TFrame", width=200)
        sidebar.pack(side=tk.LEFT, fill=tk.Y, padx=(0, 20))
        sidebar.pack_propagate(False)
        
        # Logo/Title
        title_label = tk.Label(sidebar, text="💰", font=("Helvetica", 32), 
                             bg=self.colors["sidebar_bg"], fg=self.colors["primary"])
        title_label.pack(pady=(20, 30))
        
        # Navigation buttons
        nav_items = [
            ("Dashboard", "home"),
            ("Statistik", "stats"),
            ("Tambah Transaksi", "add"),
            ("Ekspor Data", "export"),
            ("Pengaturan", "settings")
        ]
        
        for text, icon_name in nav_items:
            icon = self.icons.get(icon_name)
            if isinstance(icon, str):  # Jika ikon adalah emoji
                btn_text = f"{icon}  {text}"
                btn = ttk.Button(sidebar, text=btn_text,
                               style="TButton",
                               command=lambda t=text: self.navigate(t))
            else:  # Jika ikon adalah PhotoImage
                btn = ttk.Button(sidebar, text=f"    {text}", 
                               image=icon,
                               compound=tk.LEFT,
                               style="TButton",
                               command=lambda t=text: self.navigate(t))
            btn.pack(fill=tk.X, padx=10, pady=5)
    
    def setup_header(self, parent):
        """Setup header dengan month navigator"""
        header_frame = ttk.Frame(parent, style="Card.TFrame")
        header_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Title
        title = tk.Label(header_frame, text="Keuangan Saya", 
                        font=self.fonts["title"],
                        bg=self.colors["card_bg"],
                        fg=self.colors["text"])
        title.pack(side=tk.LEFT)
        
        # Month navigator
        nav_frame = ttk.Frame(header_frame, style="Card.TFrame")
        nav_frame.pack(side=tk.RIGHT)
        
        self.prev_btn = ttk.Button(nav_frame, text="◀", width=3,
                                  command=self.prev_month)
        self.prev_btn.pack(side=tk.LEFT, padx=2)
        
        self.month_label = tk.Label(nav_frame, text="", 
                                   font=self.fonts["bold"],
                                   bg=self.colors["card_bg"],
                                   fg=self.colors["text"])
        self.month_label.pack(side=tk.LEFT, padx=10)
        
        self.next_btn = ttk.Button(nav_frame, text="▶", width=3,
                                  command=self.next_month)
        self.next_btn.pack(side=tk.LEFT, padx=2)
        
        # Update month label
        self.update_month_label()
    
    def setup_stats(self, parent):
        """Setup statistik cards"""
        stats_frame = ttk.Frame(parent, style="Card.TFrame")
        stats_frame.pack(fill=tk.X, pady=(0, 20))
        
        # Income card
        self.income_card = self.create_stat_card(stats_frame, "Pemasukan", "0", 
                                                self.colors["success"])
        self.income_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(0, 10))
        
        # Expense card
        self.expense_card = self.create_stat_card(stats_frame, "Pengeluaran", "0", 
                                                 self.colors["danger"])
        self.expense_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=10)
        
        # Balance card
        self.balance_card = self.create_stat_card(stats_frame, "Saldo", "0", 
                                                 self.colors["primary"])
        self.balance_card.pack(side=tk.LEFT, fill=tk.BOTH, expand=True, padx=(10, 0))
    
    def create_stat_card(self, parent, title, value, color):
        """Membuat card untuk statistik"""
        card = ttk.Frame(parent, style="Card.TFrame", relief=tk.RAISED, borderwidth=1)
        
        # Title
        title_label = tk.Label(card, text=title, font=self.fonts["small"],
                             bg=self.colors["card_bg"], fg=self.colors["text_light"])
        title_label.pack(anchor=tk.W, padx=15, pady=(15, 5))
        
        # Value
        value_label = tk.Label(card, text=f"Rp{value}", font=self.fonts["large"],
                             bg=self.colors["card_bg"], fg=color)
        value_label.pack(anchor=tk.W, padx=15, pady=(0, 15))
        
        return card
    
    def setup_transaction_table(self, parent):
        """Setup tabel transaksi"""
        table_frame = ttk.Frame(parent, style="Card.TFrame")
        table_frame.pack(fill=tk.BOTH, expand=True)
        
        # Table header
        headers = ["Tanggal", "Kategori", "Deskripsi", "Jumlah", "Tipe", "Aksi"]
        for i, header in enumerate(headers):
            label = tk.Label(table_frame, text=header, font=self.fonts["bold"],
                           bg=self.colors["card_bg"], fg=self.colors["text"])
            label.grid(row=0, column=i, padx=5, pady=10, sticky="w")
        
        # Scrollable area for transactions
        self.table_canvas = tk.Canvas(table_frame, bg=self.colors["card_bg"],
                                     highlightthickness=0)
        self.table_canvas.grid(row=1, column=0, columnspan=6, 
                              sticky="nsew", padx=5, pady=5)
        
        table_frame.grid_rowconfigure(1, weight=1)
        table_frame.grid_columnconfigure(0, weight=1)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", 
                                 command=self.table_canvas.yview)
        scrollbar.grid(row=1, column=6, sticky="ns")
        self.table_canvas.configure(yscrollcommand=scrollbar.set)
        
        # Transaction container
        self.transaction_container = ttk.Frame(self.table_canvas, style="Card.TFrame")
        self.table_canvas.create_window((0, 0), window=self.transaction_container, 
                                       anchor="nw", width=self.table_canvas.winfo_reqwidth())
    
    def setup_transaction_form(self, parent):
        """Setup form untuk menambah transaksi"""
        self.form_frame = ttk.Frame(parent, style="Card.TFrame")
        self.form_frame.pack_forget()  # Sembunyikan awalnya
        
        form_title = tk.Label(self.form_frame, text="Tambah Transaksi Baru",
                            font=self.fonts["title"], bg=self.colors["card_bg"])
        form_title.pack(pady=(0, 20))
        
        # Form fields
        fields = [
            ("Tanggal (DD/MM/YYYY):", "date"),
            ("Kategori:", "category"),
            ("Jumlah:", "amount"),
            ("Tipe:", "type"),
            ("Deskripsi:", "description")
        ]
        
        self.form_vars = {}
        
        for label_text, field_name in fields:
            frame = ttk.Frame(self.form_frame, style="Card.TFrame")
            frame.pack(fill=tk.X, pady=5)
            
            label = tk.Label(frame, text=label_text, font=self.fonts["regular"],
                           bg=self.colors["card_bg"], width=20, anchor="w")
            label.pack(side=tk.LEFT)
            
            if field_name == "type":
                var = tk.StringVar(value="expense")
                income_btn = ttk.Radiobutton(frame, text="Pemasukan", variable=var,
                                           value="income", 
                                           command=self.update_category_options)
                expense_btn = ttk.Radiobutton(frame, text="Pengeluaran", variable=var,
                                            value="expense",
                                            command=self.update_category_options)
                income_btn.pack(side=tk.LEFT, padx=5)
                expense_btn.pack(side=tk.LEFT, padx=5)
                self.form_vars[field_name] = var
                
            elif field_name == "category":
                var = tk.StringVar()
                self.category_combo = ttk.Combobox(frame, textvariable=var,
                                                  values=self.categories["expense"],
                                                  state="readonly")
                self.category_combo.pack(side=tk.LEFT, fill=tk.X, expand=True)
                self.form_vars[field_name] = var
                
            else:
                var = tk.StringVar()
                entry = ttk.Entry(frame, textvariable=var)
                entry.pack(side=tk.LEFT, fill=tk.X, expand=True)
                self.form_vars[field_name] = var
        
        # Buttons
        button_frame = ttk.Frame(self.form_frame, style="Card.TFrame")
        button_frame.pack(pady=20)
        
        ttk.Button(button_frame, text="Simpan", 
                  command=self.save_transaction,
                  style="Primary.TButton").pack(side=tk.LEFT, padx=5)
        
        ttk.Button(button_frame, text="Batal", 
                  command=self.hide_form).pack(side=tk.LEFT, padx=5)
    
    def navigate(self, page):
        """Navigasi antar halaman"""
        if page == "Tambah Transaksi":
            self.show_form()
        elif page == "Ekspor Data":
            self.export_data()
        elif page == "Statistik":
            self.show_stats()
    
    def show_form(self):
        """Tampilkan form tambah transaksi"""
        self.form_frame.pack(fill=tk.BOTH, expand=True, pady=(20, 0))
        self.update_category_options()
    
    def hide_form(self):
        """Sembunyikan form"""
        self.form_frame.pack_forget()
    
    def update_category_options(self):
        """Update opsi kategori berdasarkan tipe transaksi"""
        trans_type = self.form_vars["type"].get()
        self.category_combo['values'] = self.categories[trans_type]
        if self.categories[trans_type]:
            self.category_combo.set(self.categories[trans_type][0])
    
    def save_transaction(self):
        """Simpan transaksi baru"""
        try:
            # Validasi input
            date_str = self.form_vars["date"].get()
            category = self.form_vars["category"].get()
            amount = float(self.form_vars["amount"].get())
            trans_type = self.form_vars["type"].get()
            description = self.form_vars["description"].get()
            
            # Parse tanggal
            try:
                date_obj = datetime.datetime.strptime(date_str, "%d/%m/%Y")
            except:
                date_obj = datetime.datetime.now()
            
            # Buat transaksi
            transaction = Transaction(
                date_obj.strftime("%d/%m/%Y"),
                category,
                amount,
                trans_type,
                description
            )
            
            # Tambahkan ke daftar
            self.transactions.append(transaction)
            
            # Reset form
            for var in self.form_vars.values():
                if isinstance(var, tk.StringVar):
                    var.set("")
            self.form_vars["type"].set("expense")
            self.update_category_options()
            
            # Update tampilan
            self.update_display()
            self.hide_form()
            
            # Simpan data
            self.save_data()
            
            messagebox.showinfo("Sukses", "Transaksi berhasil disimpan!")
            
        except ValueError as e:
            messagebox.showerror("Error", f"Input tidak valid: {str(e)}")
    
    def update_display(self):
        """Update semua tampilan"""
        self.update_stats()
        self.update_transaction_table()
        self.update_month_label()
    
    def update_stats(self):
        """Update statistik cards"""
        monthly_transactions = self.get_monthly_transactions()
        
        total_income = sum(t.amount for t in monthly_transactions if t.type == "income")
        total_expense = sum(t.amount for t in monthly_transactions if t.type == "expense")
        balance = total_income - total_expense
        
        # Update card values
        income_label = self.income_card.winfo_children()[1]
        expense_label = self.expense_card.winfo_children()[1]
        balance_label = self.balance_card.winfo_children()[1]
        
        income_label.config(text=f"Rp{total_income:,.0f}")
        expense_label.config(text=f"Rp{total_expense:,.0f}")
        balance_label.config(text=f"Rp{balance:,.0f}")
    
    def update_transaction_table(self):
        """Update tabel transaksi"""
        # Hapus widget lama
        for widget in self.transaction_container.winfo_children():
            widget.destroy()
        
        # Dapatkan transaksi bulan ini
        transactions = self.get_monthly_transactions()
        
        # Tampilkan transaksi
        for i, transaction in enumerate(transactions):
            row_color = "#f0f8ff" if i % 2 == 0 else self.colors["card_bg"]
            
            # Buat frame untuk setiap baris
            row_frame = ttk.Frame(self.transaction_container, style="Card.TFrame")
            row_frame.pack(fill=tk.X, pady=2)
            
            # Data kolom
            columns = [
                transaction.date,
                transaction.category,
                transaction.description[:30] + "..." if len(transaction.description) > 30 else transaction.description,
                f"Rp{transaction.amount:,.0f}",
                "Pemasukan" if transaction.type == "income" else "Pengeluaran"
            ]
            
            # Tampilkan data
            for j, value in enumerate(columns):
                color = self.colors["success"] if transaction.type == "income" else self.colors["danger"]
                label_bg = row_color
                
                if j == 3:  # Kolom jumlah
                    label = tk.Label(row_frame, text=value, font=self.fonts["regular"],
                                   bg=label_bg, fg=color)
                else:
                    label = tk.Label(row_frame, text=value, font=self.fonts["regular"],
                                   bg=label_bg, fg=self.colors["text"])
                label.grid(row=0, column=j, padx=5, pady=5, sticky="w")
                label.configure(bg=label_bg)
            
            # Tombol hapus
            delete_btn = ttk.Button(row_frame, text="Hapus", 
                                   command=lambda t=transaction: self.delete_transaction(t))
            delete_btn.grid(row=0, column=5, padx=5, pady=5)
            
            # Atur warna background frame
            row_frame.configure(style="Card.TFrame")
        
        # Update scroll region
        self.transaction_container.update_idletasks()
        self.table_canvas.configure(scrollregion=self.table_canvas.bbox("all"))
    
    def delete_transaction(self, transaction):
        """Hapus transaksi"""
        if messagebox.askyesno("Konfirmasi", "Hapus transaksi ini?"):
            self.transactions.remove(transaction)
            self.update_display()
            self.save_data()
    
    def get_monthly_transactions(self):
        """Dapatkan transaksi untuk bulan yang dipilih"""
        return [t for t in self.transactions 
                if self.is_transaction_in_month(t, self.current_month, self.current_year)]
    
    def is_transaction_in_month(self, transaction, month, year):
        """Cek apakah transaksi terjadi di bulan dan tahun tertentu"""
        try:
            trans_date = datetime.datetime.strptime(transaction.date, "%d/%m/%Y")
            return trans_date.month == month and trans_date.year == year
        except:
            return False
    
    def update_month_label(self):
        """Update label bulan"""
        month_names = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
                      "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
        self.month_label.config(text=f"{month_names[self.current_month-1]} {self.current_year}")
    
    def prev_month(self):
        """Navigasi ke bulan sebelumnya"""
        if self.current_month == 1:
            self.current_month = 12
            self.current_year -= 1
        else:
            self.current_month -= 1
        self.update_display()
    
    def next_month(self):
        """Navigasi ke bulan berikutnya"""
        if self.current_month == 12:
            self.current_month = 1
            self.current_year += 1
        else:
            self.current_month += 1
        self.update_display()
    
    def show_stats(self):
        """Tampilkan grafik statistik"""
        # Buat window baru untuk statistik
        stats_window = tk.Toplevel(self.root)
        stats_window.title("Statistik Keuangan")
        stats_window.geometry("800x600")
        stats_window.configure(bg=self.colors["bg"])
        
        # Dapatkan data
        monthly_data = {}
        for transaction in self.transactions:
            try:
                date = datetime.datetime.strptime(transaction.date, "%d/%m/%Y")
                month_year = f"{date.month}/{date.year}"
                if month_year not in monthly_data:
                    monthly_data[month_year] = {"income": 0, "expense": 0}
                
                if transaction.type == "income":
                    monthly_data[month_year]["income"] += transaction.amount
                else:
                    monthly_data[month_year]["expense"] += transaction.amount
            except:
                continue
        
        if not monthly_data:
            # Jika tidak ada data, tampilkan pesan
            no_data_label = tk.Label(stats_window, text="Tidak ada data transaksi",
                                   font=self.fonts["title"], bg=self.colors["bg"])
            no_data_label.pack(expand=True)
            return
        
        # Buat grafik
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(10, 8))
        
        # Grafik line chart
        months = list(monthly_data.keys())
        incomes = [monthly_data[m]["income"] for m in months]
        expenses = [monthly_data[m]["expense"] for m in months]
        
        ax1.plot(months, incomes, marker='o', label='Pemasukan', color=self.colors["success"])
        ax1.plot(months, expenses, marker='s', label='Pengeluaran', color=self.colors["danger"])
        ax1.set_title('Trend Bulanan')
        ax1.set_ylabel('Jumlah (Rp)')
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Grafik pie chart untuk kategori
        current_transactions = self.get_monthly_transactions()
        categories = {}
        for t in current_transactions:
            if t.type == "expense":
                if t.category not in categories:
                    categories[t.category] = 0
                categories[t.category] += t.amount
        
        if categories:
            ax2.pie(categories.values(), labels=categories.keys(), autopct='%1.1f%%')
            ax2.set_title('Distribusi Pengeluaran Bulan Ini')
        else:
            ax2.text(0.5, 0.5, 'Tidak ada data pengeluaran', 
                    ha='center', va='center', transform=ax2.transAxes)
        
        plt.tight_layout()
        
        # Tampilkan di Tkinter
        canvas = FigureCanvasTkAgg(fig, master=stats_window)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True, padx=20, pady=20)
    
    def export_data(self):
        """Ekspor data ke file JSON"""
        filename = f"finance_data_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
        data = {
            "transactions": [t.to_dict() for t in self.transactions],
            "export_date": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        
        with open(filename, 'w') as f:
            json.dump(data, f, indent=2)
        
        messagebox.showinfo("Sukses", f"Data berhasil diekspor ke {filename}")
    
    def save_data(self):
        """Simpan data ke file"""
        data = {
            "transactions": [t.to_dict() for t in self.transactions],
            "last_save": datetime.datetime.now().strftime("%d/%m/%Y %H:%M:%S")
        }
        
        with open("finance_data.json", 'w') as f:
            json.dump(data, f, indent=2)
    
    def load_data(self):
        """Load data dari file"""
        try:
            with open("finance_data.json", 'r') as f:
                data = json.load(f)
                
            for t_data in data.get("transactions", []):
                transaction = Transaction(
                    t_data["date"],
                    t_data["category"],
                    t_data["amount"],
                    t_data["type"],
                    t_data.get("description", "")
                )
                self.transactions.append(transaction)
                
        except FileNotFoundError:
            # File tidak ditemukan, buat data contoh
            self.create_sample_data()
    
    def create_sample_data(self):
        """Buat data contoh untuk pertama kali"""
        sample_transactions = [
            Transaction("01/01/2024", "Gaji", 5000000, "income", "Gaji bulanan"),
            Transaction("05/01/2024", "Makanan", 150000, "expense", "Makan di restoran"),
            Transaction("10/01/2024", "Transportasi", 200000, "expense", "Bensin dan parkir"),
            Transaction("15/01/2024", "Investasi", 1000000, "income", "Dividen saham"),
            Transaction("20/01/2024", "Belanja", 300000, "expense", "Belanja bulanan"),
            Transaction("25/01/2024", "Hiburan", 150000, "expense", "Nonton bioskop"),
        ]
        
        self.transactions.extend(sample_transactions)

def main():
    root = tk.Tk()
    app = FinanceApp(root)
    root.mainloop()

if __name__ == "__main__":
    main()