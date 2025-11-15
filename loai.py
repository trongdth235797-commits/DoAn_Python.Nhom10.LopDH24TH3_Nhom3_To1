# loai.py
import tkinter as tk
from tkinter import ttk, messagebox
from database import fetch_all, execute_query

def show():
    win = tk.Toplevel()
    win.title("Quản lý loại sản phẩm")
    win.geometry("600x450")

    frm = tk.LabelFrame(win, text="Thông tin loại", font=("Times New Roman", 12, "bold"), padx=10, pady=10)
    frm.pack(fill="x", padx=10, pady=8)

    tk.Label(frm, text="Mã loại:", font=("Times New Roman", 12)).grid(row=0, column=0, sticky="w", pady=4)
    txt_m = tk.Entry(frm, font=("Times New Roman", 12)); txt_m.grid(row=0, column=1, padx=6)
    tk.Label(frm, text="Tên loại:", font=("Times New Roman", 12)).grid(row=1, column=0, sticky="w", pady=4)
    txt_t = tk.Entry(frm, font=("Times New Roman", 12)); txt_t.grid(row=1, column=1, padx=6)
    tk.Label(frm, text="Hãng SX:", font=("Times New Roman", 12)).grid(row=2, column=0, sticky="w", pady=4)
    txt_h = tk.Entry(frm, font=("Times New Roman", 12)); txt_h.grid(row=2, column=1, padx=6)
    tk.Label(frm, text="Tìm Loại:", font=("Times New Roman", 12)).grid(row=3, column=0, sticky="w", pady=4)
    txt_search = tk.Entry(frm, font=("Times New Roman", 12)); txt_search.grid(row=3, column=1, padx=6)
    tk.Button(frm, text="Tìm kiếm", command=lambda: search_loai()).grid(row=3, column=2, padx=6)



    btnf = tk.Frame(win); btnf.pack(fill="x", padx=10, pady=6)
    tk.Button(btnf, text="Thêm", width=10, command=lambda: them()).pack(side="left", padx=6)
    tk.Button(btnf, text="Sửa", width=10, command=lambda: sua()).pack(side="left", padx=6)
    tk.Button(btnf, text="Xóa", width=10, command=lambda: xoa()).pack(side="left", padx=6)
    tk.Button(btnf, text="Tải lại", width=10, command=lambda: reset_form()).pack(side="left", padx=6)

    cols = ("Mã Loại","Tên Loại","Hãng sản xuất")
    tree = ttk.Treeview(win, columns=cols, show="headings")
    for c in cols:
        tree.heading(c, text=c); tree.column(c, anchor="center", width=150)
    tree.pack(fill="both", expand=True, padx=10, pady=6)

    def load_data():
        tree.delete(*tree.get_children())
        for r in fetch_all("SELECT MaLoai, TenLoai, Hangsx FROM loai"):
            tree.insert("", "end", values=(r['MaLoai'], r['TenLoai'], r['Hangsx']))

    def them():
        ma = txt_m.get().strip(); ten = txt_t.get().strip(); hang = txt_h.get().strip()
        if not (ma and ten and hang): messagebox.showwarning("Thiếu","Nhập đủ"); return
        if execute_query("INSERT INTO loai (MaLoai, TenLoai, Hangsx) VALUES (%s,%s,%s)", (ma,ten,hang)):
            messagebox.showinfo("OK","Đã thêm"); load_data()

    def sua():
        sel = tree.selection(); 
        if not sel: messagebox.showwarning("Chọn","Chọn dòng"); return
        ma = txt_m.get().strip(); ten = txt_t.get().strip(); hang = txt_h.get().strip()
        if execute_query("UPDATE loai SET TenLoai=%s, Hangsx=%s WHERE MaLoai=%s", (ten,hang,ma)):
            messagebox.showinfo("OK","Đã sửa"); load_data()

    def xoa():
        sel = tree.selection(); 
        if not sel: messagebox.showwarning("Chọn","Chọn dòng"); return
        ma = tree.item(sel[0])['values'][0]
        if messagebox.askyesno("Xóa", f"Xóa loại {ma}?"):
            execute_query("DELETE FROM loai WHERE MaLoai=%s", (ma,)); load_data()
    def reset_form():
        txt_m.delete(0, tk.END)
        txt_t.delete(0, tk.END)
        txt_h.delete(0, tk.END)
        tree.delete(*tree.get_children())
        for r in fetch_all("SELECT MaLoai, TenLoai, Hangsx FROM loai"):
            tree.insert("", "end", values=(r['MaLoai'], r['TenLoai'], r['Hangsx']))

    def search_loai():
        keyword = txt_search.get().strip()
        tree.delete(*tree.get_children())
        if not keyword:
            messagebox.showwarning("Nhập từ khóa", "Nhập mã hoặc tên loại để tìm")
            return
        q = "SELECT MaLoai, TenLoai, Hangsx FROM loai WHERE MaLoai LIKE %s OR TenLoai LIKE %s"
        rows = fetch_all(q, (f"%{keyword}%", f"%{keyword}%"))
        if not rows:
            messagebox.showinfo("Không tìm thấy", "Không tìm thấy loại nào")
            return
        for r in rows:
            tree.insert("", "end", values=(r['MaLoai'], r['TenLoai'], r['Hangsx']))





    def on_select(e):
        sel = tree.selection(); 
        if not sel: return
        r = tree.item(sel[0])['values']
        txt_m.delete(0, tk.END); txt_m.insert(0, r[0])
        txt_t.delete(0, tk.END); txt_t.insert(0, r[1])
        txt_h.delete(0, tk.END); txt_h.insert(0, r[2])

    tree.bind("<ButtonRelease-1>", on_select)
    load_data()