# khachhang_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from database import fetch_all, execute_query

def show():
    win = tk.Toplevel()
    win.title("Quản lý khách hàng")
    win.geometry("800x500")

    frm = tk.LabelFrame(win, text="Thông tin khách hàng", font=("Times New Roman", 12, "bold"), padx=10, pady=10)
    frm.pack(fill="x", padx=10, pady=8)

    tk.Label(frm, text="Mã KH:", font=("Times New Roman", 12)).grid(row=0, column=0, sticky="w", pady=4)
    txt_id = tk.Entry(frm, font=("Times New Roman", 12)); txt_id.grid(row=0, column=1, padx=6)
    tk.Label(frm, text="Tên KH:", font=("Times New Roman", 12)).grid(row=1, column=0, sticky="w", pady=4)
    txt_name = tk.Entry(frm, font=("Times New Roman", 12)); txt_name.grid(row=1, column=1, padx=6)
    tk.Label(frm, text="Địa chỉ:", font=("Times New Roman", 12)).grid(row=0, column=2, sticky="w", pady=4)
    txt_addr = tk.Entry(frm, font=("Times New Roman", 12), width=40); txt_addr.grid(row=0, column=3, padx=6)
    tk.Label(frm, text="Điện thoại:", font=("Times New Roman", 12)).grid(row=1, column=2, sticky="w", pady=4)
    txt_phone = tk.Entry(frm, font=("Times New Roman", 12)); txt_phone.grid(row=1, column=3, padx=6)
    frm_search = tk.Frame(win)
    frm_search.pack(fill="x", padx=10, pady=4)

    tk.Label(frm_search, text="Tìm KH:", font=("Times New Roman", 12)).pack(side="left")
    txt_search = tk.Entry(frm_search, font=("Times New Roman", 12))
    txt_search.pack(side="left", padx=6)
    tk.Button(frm_search, text="Tìm kiếm", command=lambda: search_kh()).pack(side="left", padx=6)
    tk.Button(frm_search, text="Tải lại", command=lambda: load()).pack(side="left", padx=6)

    btnf = tk.Frame(win); btnf.pack(fill="x", padx=10, pady=6)
    tk.Button(btnf, text="Thêm", width=10, command=lambda: them()).pack(side="left", padx=6)
    tk.Button(btnf, text="Sửa", width=10, command=lambda: sua()).pack(side="left", padx=6)
    tk.Button(btnf, text="Xóa", width=10, command=lambda: xoa()).pack(side="left", padx=6)
    tk.Button(btnf, text="Tải lại", width=10, command=lambda: load()).pack(side="left", padx=6)

    cols = ("MaKhach","TenKhach","DiaChi","DienThoai")
    tree = ttk.Treeview(win, columns=cols, show="headings")
    for c in cols:
        tree.heading(c, text=c); tree.column(c, width=160, anchor="center")
    tree.pack(fill="both", expand=True, padx=10, pady=6)

    def load():
        tree.delete(*tree.get_children())
        for r in fetch_all("SELECT MaKhach, TenKhach, DiaChi, DienThoai FROM khachhang"):
            tree.insert("", "end", values=(r['MaKhach'], r['TenKhach'], r['DiaChi'], r['DienThoai']))
            txt_id.delete(0, tk.END)
        txt_name.delete(0, tk.END)
        txt_addr.delete(0, tk.END)
        txt_phone.delete(0, tk.END)

    def them():
        ma = txt_id.get().strip(); ten = txt_name.get().strip()
        dia = txt_addr.get().strip(); dt = txt_phone.get().strip()
        if not (ma and ten): messagebox.showwarning("Thiếu","Nhập mã và tên"); return
        if execute_query("INSERT INTO khachhang (MaKhach, TenKhach, DiaChi, DienThoai) VALUES (%s,%s,%s,%s)", (ma,ten,dia,dt)):
            messagebox.showinfo("OK","Đã thêm"); load()

    def sua():
        sel = tree.selection(); 
        if not sel: messagebox.showwarning("Chọn","Chọn khách hàng"); return
        ma = txt_id.get().strip(); ten = txt_name.get().strip(); dia = txt_addr.get().strip(); dt=txt_phone.get().strip()
        if execute_query("UPDATE khachhang SET TenKhach=%s, DiaChi=%s, DienThoai=%s WHERE MaKhach=%s", (ten,dia,dt,ma)):
            messagebox.showinfo("OK","Đã sửa"); load()

    def xoa():
        sel = tree.selection(); 
        if not sel: messagebox.showwarning("Chọn","Chọn dòng"); return
        ma = tree.item(sel[0])['values'][0]
        if messagebox.askyesno("Xóa", f"Xóa khách {ma}?"):
            execute_query("DELETE FROM khachhang WHERE MaKhach=%s", (ma,)); load()

    def on_select(e):
        sel = tree.selection(); 
        if not sel: return
        r = tree.item(sel[0])['values']
        txt_id.delete(0, tk.END); txt_id.insert(0, r[0])
        txt_name.delete(0, tk.END); txt_name.insert(0, r[1])
        txt_addr.delete(0, tk.END); txt_addr.insert(0, r[2])
        txt_phone.delete(0, tk.END); txt_phone.insert(0, r[3])
    def search_kh():
        keyword = txt_search.get().strip()
        tree.delete(*tree.get_children())
        if not keyword:
            messagebox.showwarning("Nhập từ khóa", "Nhập mã hoặc tên khách hàng để tìm")
            return
        q = "SELECT MaKhach, TenKhach, DiaChi, DienThoai FROM khachhang WHERE MaKhach LIKE %s OR TenKhach LIKE %s"
        rows = fetch_all(q, (f"%{keyword}%", f"%{keyword}%"))
        if not rows:
            messagebox.showinfo("Không tìm thấy", "Không tìm thấy khách hàng nào")
            return
        for r in rows:
            tree.insert("", "end", values=(r['MaKhach'], r['TenKhach'], r['DiaChi'], r['DienThoai']))

    tree.bind("<ButtonRelease-1>", on_select)
    load()