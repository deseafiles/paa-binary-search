import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from .database import insertDataBarang

class MarketStockApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Market Stock Application")
        self.root.geometry("900x700")
        self.root.configure(bg="#F5F2E8")
        
        # Data storage
        self.stock_items = []
        self.current_screen = "login"
        
        # Colors from the design
        self.bg_color = "#F5F2E8"
        self.orange_color = "#E8A547"
        self.green_color = "#4CAF50"
        self.white_color = "#FFFFFF"
        self.text_color = "#666666"
        
        self.show_login_screen()
    
    def clear_screen(self):
        for widget in self.root.winfo_children():
            widget.destroy()
    
    def show_login_screen(self):
        self.clear_screen()
        self.current_screen = "login"
        
        # Main container
        main_frame = tk.Frame(self.root, bg=self.bg_color)
        main_frame.pack(fill="both", expand=True)
        
        # Logo and title section
        title_frame = tk.Frame(main_frame, bg=self.bg_color)
        title_frame.pack(expand=True)
        
        # Title
        market_label = tk.Label(
            title_frame,
            text="MARKET",
            font=("Arial", 36, "bold"),
            fg=self.green_color,
            bg=self.bg_color
        )
        market_label.pack()
        
        stock_label = tk.Label(
            title_frame,
            text="STOCK",
            font=("Arial", 36, "bold"),
            fg=self.orange_color,
            bg=self.bg_color
        )
        stock_label.pack()
        
        # Cart icon placeholder (using text)
        icon_label = tk.Label(
            title_frame,
            text="🛒",
            font=("Arial", 48),
            bg=self.bg_color
        )
        icon_label.pack(pady=20)
        
        # Login form
        form_frame = tk.Frame(title_frame, bg=self.bg_color)
        form_frame.pack(pady=30)
        
        # Account field
        account_frame = tk.Frame(form_frame, bg=self.bg_color)
        account_frame.pack(pady=10)
        
        account_icon = tk.Label(
            account_frame,
            text="👤",
            font=("Monotomic Mono", 20),
            bg=self.bg_color,
            fg=self.orange_color
        )
        account_icon.pack(side="left", padx=10)
        
        self.account_entry = tk.Entry(
            account_frame,
            font=("Arial", 14),
            width=25,
            relief="flat",
            bd=2,
            highlightthickness=2,
            highlightcolor=self.orange_color,
            bg=self.white_color
        )
        self.account_entry.pack(side="left", ipady=8)
        self.account_entry.insert(0, "Account")
        self.account_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.account_entry, "Account"))
        
        # Password field
        password_frame = tk.Frame(form_frame, bg=self.bg_color)
        password_frame.pack(pady=10)
        
        password_icon = tk.Label(
            password_frame,
            text="🔒",
            font=("Arial", 20),
            bg=self.bg_color,
            fg=self.orange_color
        )
        password_icon.pack(side="left", padx=10)
        
        self.password_entry = tk.Entry(
            password_frame,
            font=("Arial", 14),
            width=25,
            relief="flat",
            bd=2,
            highlightthickness=2,
            highlightcolor=self.orange_color,
            bg=self.white_color
        )
        self.password_entry.pack(side="left", ipady=8)
        self.password_entry.insert(0, "Password")
        self.password_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.password_entry, "Password"))
        
        # # Login button
        # login_btn = tk.Button(
        #     form_frame,
        #     text="→",
        #     font=("Arial", 20, "bold"),
        #     bg=self.orange_color,
        #     fg=self.white_color,
        #     relief="flat",
        #     width=3,
        #     height=2,
        #     command=self.login,
        #     cursor="hand2"
        # )
        # login_btn.pack(side="right", padx=20)
        
        # Login button (full width)
        full_login_btn = tk.Button(
            title_frame,
            text="LOGIN",
            font=("Arial", 16, "bold"),
            bg=self.orange_color,
            fg=self.white_color,
            relief="flat",
            width=20,
            height=2,
            command=self.login,
            cursor="hand2"
        )
        full_login_btn.pack(pady=20)
    
    def clear_placeholder(self, entry, placeholder):
        if entry.get() == placeholder:
            entry.delete(0, tk.END)
    
    def login(self):
        # Simple validation - in real app, you'd check credentials
        account = self.account_entry.get()
        password = self.password_entry.get()
        
        if account and account != "Account" and password and password != "Password":
            self.show_main_menu()
        else:
            messagebox.showerror("ISI DULU GAK", "Isi account dan password nya dulu kocak!")
    
    def show_main_menu(self):
        self.clear_screen()
        self.current_screen = "main_menu"
        
        # Header with search bar
        self.create_header_with_search("Cari barang mu di Market Stock..")
        
        # Menu buttons
        menu_frame = tk.Frame(self.root, bg=self.bg_color)
        menu_frame.pack(expand=True)
        
        # Menu button 1 - Masih Banyak
        btn1 = tk.Button(
            menu_frame,
            text="MASIH BANYAK",
            font=("Arial", 16, "bold"),
            bg=self.orange_color,
            fg=self.white_color,
            relief="flat",
            width=30,
            height=2,
            command=self.show_stock_available,
            cursor="hand2"
        )
        btn1.pack(pady=15)
        
        # Menu button 2 - Hampir Habis
        btn2 = tk.Button(
            menu_frame,
            text="HAMPIR HABIS",
            font=("Arial", 16, "bold"),
            bg=self.orange_color,
            fg=self.white_color,
            relief="flat",
            width=30,
            height=2,
            command=self.show_stock_low,
            cursor="hand2"
        )
        btn2.pack(pady=15)
        
        # Bottom navigation
        self.create_bottom_nav()
    
    def create_header_with_search(self, placeholder=""):
        # Header frame
        header_frame = tk.Frame(self.root, bg=self.bg_color)
        header_frame.pack(fill="x", padx=20, pady=10)
        
        # Back button (only if not on main menu)
        if self.current_screen != "main_menu":
            back_btn = tk.Button(
                header_frame,
                text="←",
                font=("Arial", 20, "bold"),
                bg=self.orange_color,
                fg=self.white_color,
                relief="flat",
                width=3,
                height=1,
                command=self.go_back,
                cursor="hand2"
            )
            back_btn.pack(side="left", padx=(0, 10))
        
        # Search frame
        search_frame = tk.Frame(header_frame, bg=self.bg_color)
        search_frame.pack(side="left", fill="x", expand=True)
        
        # Search entry
        self.search_entry = tk.Entry(
            search_frame,
            font=("Arial", 12),
            relief="flat",
            bd=2,
            highlightthickness=2,
            highlightcolor=self.orange_color,
            bg=self.white_color
        )
        self.search_entry.pack(fill="x", ipady=8, padx=(0, 10))
        
        if placeholder:
            self.search_entry.insert(0, placeholder)
            self.search_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.search_entry, placeholder))
        
        # # Close button
        # close_btn = tk.Button(
        #     header_frame,
        #     text="✕",
        #     font=("Arial", 16, "bold"),
        #     bg=self.orange_color,
        #     fg=self.white_color,
        #     relief="flat",
        #     width=3,
        #     height=2,
        #     command=self.root.quit,
        #     cursor="hand2"
        # )
        # close_btn.pack(side="right")
    
    def create_bottom_nav(self):
        # Bottom navigation frame
        bottom_frame = tk.Frame(self.root, bg=self.bg_color)
        bottom_frame.pack(side="bottom", fill="x", padx=20, pady=20)
        
        # Remove button (-)
        remove_btn = tk.Button(
            bottom_frame,
            text="—",
            font=("Arial", 20, "bold"),
            bg=self.orange_color,
            fg=self.white_color,
            relief="flat",
            width=5,
            height=2,
            command=self.remove_item,
            cursor="hand2"
        )
        remove_btn.pack(side="left")
        
        # Add button (+)
        add_btn = tk.Button(
            bottom_frame,
            text="+",
            font=("Arial", 20, "bold"),
            bg=self.orange_color,
            fg=self.white_color,
            relief="flat",
            width=5,
            height=2,
            command=self.show_add_stock_screen,
            cursor="hand2"
        )
        add_btn.pack(side="right")
    
    def show_add_stock_screen(self):
        self.clear_screen()
        self.current_screen = "add_stock"
        
        # Header
        self.create_header_with_search()
        
        # Title
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(pady=20)
        
        title_btn = tk.Label(
            title_frame,
            text="Add On Stock",
            font=("Arial", 18, "bold"),
            bg=self.orange_color,
            fg=self.white_color,
            relief="flat",
            width=20,
            height=2
        )
        title_btn.pack()
        
        # Form frame
        form_frame = tk.Frame(self.root, bg=self.bg_color)
        form_frame.pack(expand=True, padx=50)
        
        # Nama Barang
        nama_frame = tk.Frame(form_frame, bg=self.bg_color)
        nama_frame.pack(fill="x", pady=10)
        
        nama_label = tk.Label(
            nama_frame,
            text="Nama Barang :",
            font=("Arial", 14, "bold"),
            fg=self.orange_color,
            bg=self.bg_color
        )
        nama_label.pack(anchor="w")
        
        self.nama_entry = tk.Entry(
            nama_frame,
            font=("Arial", 12),
            relief="flat",
            bd=2,
            highlightthickness=2,
            highlightcolor=self.orange_color,
            bg=self.white_color
        )
        self.nama_entry.pack(fill="x", ipady=8, pady=5)
        self.nama_entry.insert(0, "Masukan nama barang")
        self.nama_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.nama_entry, "Masukan nama barang"))
        
        # Kode Barang
        kode_frame = tk.Frame(form_frame, bg=self.bg_color)
        kode_frame.pack(fill="x", pady=10)
        
        kode_label = tk.Label(
            kode_frame,
            text="Stok :",
            font=("Arial", 14, "bold"),
            fg=self.orange_color,
            bg=self.bg_color
        )
        kode_label.pack(anchor="w")
        
        self.kode_entry = tk.Entry(
            kode_frame,
            font=("Arial", 12),
            relief="flat",
            bd=2,
            highlightthickness=2,
            highlightcolor=self.orange_color,
            bg=self.white_color
        )
        self.kode_entry.pack(fill="x", ipady=8, pady=5)
        self.kode_entry.insert(0, "Masukan kode barang")
        self.kode_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.kode_entry, "Masukan kode barang"))
        
        # Jumlah Stock
        stock_frame = tk.Frame(form_frame, bg=self.bg_color)
        stock_frame.pack(fill="x", pady=10)
        
        stock_label = tk.Label(
            stock_frame,
            text="Harga Satuan :",
            font=("Arial", 14, "bold"),
            fg=self.orange_color,
            bg=self.bg_color
        )
        stock_label.pack(anchor="w")
        
        self.stock_entry = tk.Entry(
            stock_frame,
            font=("Arial", 12),
            relief="flat",
            bd=2,
            highlightthickness=2,
            highlightcolor=self.orange_color,
            bg=self.white_color
        )
        self.stock_entry.pack(fill="x", ipady=8, pady=5)
        self.stock_entry.insert(0, "Masukan stock barang")
        self.stock_entry.bind("<FocusIn>", lambda e: self.clear_placeholder(self.stock_entry, "Masukan stock barang"))
        
        # Submit button
        submit_btn = tk.Button(
            form_frame,
            text="SUBMIT",
            font=("Arial", 16, "bold"),
            bg=self.orange_color,
            fg=self.white_color,
            relief="flat",
            width=20,
            height=2,
            command=self.add_stock_item,
            cursor="hand2"
        )
        submit_btn.pack(pady=30)
        
        # Bottom navigation
        self.create_bottom_nav()
    
    def add_stock_item(self):
        nama = self.nama_entry.get()
        stok = self.kode_entry.get()  
        harga = self.stock_entry.get()

        if nama and nama != "Masukan nama barang" and stok and stok != "Masukan stock barang" and harga and harga != 'Masukkan harga barang':
            try:
                stock_qty = int(stok)
                harga = 10000  
                insertDataBarang(nama, stock_qty, harga)
                messagebox.showinfo("Sukses", "Barang berhasil ditambahkan ke database!")
                self.show_main_menu()
            except ValueError:
                messagebox.showerror("Error", "Jumlah stock harus berupa angka!")
        else:
            messagebox.showerror("Error", "Mohon isi semua field!")
        
    def show_stock_available(self):
        self.show_stock_list("Masih Banyak", lambda x: x['stock'] > 10)
        
    def show_stock_low(self):
        self.show_stock_list("Hampir Habis", lambda x: x['stock'] <= 10)
        
    def show_stock_list(self, title, filter_func):
        self.clear_screen()
        self.current_screen = "stock_list"
        
        # Header
        self.create_header_with_search()
        
        # Title
        title_frame = tk.Frame(self.root, bg=self.bg_color)
        title_frame.pack(pady=20)
        
        title_label = tk.Label(
            title_frame,
            text=title,
            font=("Arial", 18, "bold"),
            bg=self.orange_color,
            fg=self.white_color,
            relief="flat",
            width=20,
            height=2
        )
        title_label.pack()
        
        # Stock list frame
        list_frame = tk.Frame(self.root, bg=self.bg_color)
        list_frame.pack(expand=True, fill="both", padx=50, pady=20)
        
        # Filter items
        filtered_items = [item for item in self.stock_items if filter_func(item)]
        
        # Create scrollable frame
        canvas = tk.Canvas(list_frame, bg=self.bg_color, highlightthickness=0)
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=canvas.yview)
        scrollable_frame = tk.Frame(canvas, bg=self.bg_color)
        
        scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )
        
        canvas.create_window((0, 0), window=scrollable_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)
        
        # Display items
        if filtered_items:
            for i, item in enumerate(filtered_items):
                item_frame = tk.Frame(scrollable_frame, bg=self.white_color, relief="solid", bd=1)
                item_frame.pack(fill="x", pady=5, padx=10)
                
                item_label = tk.Label(
                    item_frame,
                    text=f"{item['nama']} (Kode: {item['kode']}) - Stock: {item['stock']}",
                    font=("Arial", 12),
                    bg=self.white_color,
                    fg=self.text_color,
                    anchor="w"
                )
                item_label.pack(fill="x", padx=10, pady=10)
        else:
            no_data_label = tk.Label(
                scrollable_frame,
                text="Tidak ada data",
                font=("Arial", 14),
                bg=self.bg_color,
                fg=self.text_color
            )
            no_data_label.pack(pady=50)
        
        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")
        
        # Bottom navigation
        self.create_bottom_nav()
    
    def remove_item(self):
        if self.stock_items:
            # Simple removal - remove last item
            removed_item = self.stock_items.pop()
            messagebox.showinfo("Info", f"Item '{removed_item['nama']}' telah dihapus")
        else:
            messagebox.showinfo("Info", "Tidak ada item untuk dihapus")
    
    def go_back(self):
        if self.current_screen in ["add_stock", "stock_list"]:
            self.show_main_menu()
        else:
            self.show_login_screen()

def main():
    root = tk.Tk()
    app = MarketStockApp(root)
    
    # Center the window
    root.update_idletasks()
    width = root.winfo_width()
    height = root.winfo_height()
    x = (root.winfo_screenwidth() // 2) - (width // 2)
    y = (root.winfo_screenheight() // 2) - (height // 2)
    root.geometry(f"{width}x{height}+{x}+{y}")
    
    root.mainloop()

if __name__ == "__main__":
    main()
