# nhanvien_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from database import fetch_all, execute_query

def show():
    win = tk.Toplevel()
    win.title("Quản lý nhân viên")
    win.geometry("900x600")

    frm = tk.LabelFrame(win, text="Thông tin nhân viên", font=("Times New Roman", 12, "bold"), padx=10, pady=10)
    frm.pack(fill="x", padx=10, pady=8)

    tk.Label(frm, text="Mã NV:", font=("Times New Roman", 12)).grid(row=0, column=0, sticky="w", pady=4)
    txt_id = tk.Entry(frm, font=("Times New Roman", 12)); txt_id.grid(row=0, column=1, padx=6)
    tk.Label(frm, text="Tên NV:", font=("Times New Roman", 12)).grid(row=1, column=0, sticky="w", pady=4)
    txt_name = tk.Entry(frm, font=("Times New Roman", 12)); txt_name.grid(row=1, column=1, padx=6)
    tk.Label(frm, text="Giới tính:", font=("Times New Roman", 12)).grid(row=0, column=2, sticky="w", pady=4)
    cbo_gt = ttk.Combobox(frm, values=["Nam","Nữ"], state="readonly"); cbo_gt.grid(row=0, column=3, padx=6)
    tk.Label(frm, text="Địa chỉ:", font=("Times New Roman", 12)).grid(row=1, column=2, sticky="w", pady=4)
    txt_addr = tk.Entry(frm, font=("Times New Roman", 12)); txt_addr.grid(row=1, column=3, padx=7)
    tk.Label(frm, text="Điện thoại:", font=("Times New Roman", 12)).grid(row=2, column=0, sticky="w", pady=4)
    txt_phone = tk.Entry(frm, font=("Times New Roman", 12)); txt_phone.grid(row=2, column=1, padx=6)
    tk.Label(frm, text="Ngày sinh:", font=("Times New Roman", 12)).grid(row=2, column=2, sticky="w", pady=4)
    dt = DateEntry(frm, date_pattern="yyyy-mm-dd"); dt.grid(row=2, column=3, padx=6)
    tk.Label(frm, text="Tài khoản:", font=("Times New Roman", 12)).grid(row=3, column=0, sticky="w", pady=4)
    txt_user = tk.Entry(frm, font=("Times New Roman", 12)); txt_user.grid(row=3, column=1, padx=6)
    tk.Label(frm, text="Mật khẩu:", font=("Times New Roman", 12)).grid(row=3, column=2, sticky="w", pady=4)
    txt_pass = tk.Entry(frm, font=("Times New Roman", 12)); txt_pass.grid(row=3, column=3, padx=6)
    tk.Label(frm, text="Vai trò:", font=("Times New Roman", 12)).grid(row=4, column=0, sticky="w", pady=4)
    cbo_role = ttk.Combobox(frm, values=["Quan Ly","Nhân viên"], state="readonly"); cbo_role.grid(row=4, column=1, padx=6)
    frm_search = tk.Frame(win)
    frm_search.pack(fill="x", padx=10, pady=4)

    tk.Label(frm_search, text="Tìm NV:", font=("Times New Roman", 12)).pack(side="left")
    txt_search = tk.Entry(frm_search, font=("Times New Roman", 12))
    txt_search.pack(side="left", padx=6)
    tk.Button(frm_search, text="Tìm kiếm", command=lambda: search_nv()).pack(side="left", padx=6)
    tk.Button(frm_search, text="Tải lại", command=lambda: load()).pack(side="left", padx=6)

    btnf = tk.Frame(win); btnf.pack(fill="x", padx=10, pady=6)
    tk.Button(btnf, text="Thêm", width=10, command=lambda: them()).pack(side="left", padx=6)
    tk.Button(btnf, text="Sửa", width=10, command=lambda: sua()).pack(side="left", padx=6)
    tk.Button(btnf, text="Xóa", width=10, command=lambda: xoa()).pack(side="left", padx=6)
    tk.Button(btnf, text="Tải lại", width=10, command=lambda: reset_form()).pack(side="left", padx=6)

    cols = ("Mã NV","Tên NV","Giới tính","Địa chỉ","Điện thoại","Ngày sinh","Tên đăng nhập","Mật khẩu","Vai trò")
    tree = ttk.Treeview(win, columns=cols, show="headings")
    for c in cols:
        tree.heading(c, text=c); tree.column(c, anchor="center", width=120)
    tree.pack(fill="both", expand=True, padx=10, pady=6)

    def load():
        tree.delete(*tree.get_children())
        for r in fetch_all("SELECT MaNV, TenNV, GioiTinh, DiaChi, DienThoai, NgaySinh, TenDangNhap, MatKhau, VaiTro FROM nhanvien"):
            tree.insert("", "end", values=(r['MaNV'], r['TenNV'], r['GioiTinh'], r['DiaChi'], r['DienThoai'], r['NgaySinh'].strftime("%Y-%m-%d") if r['NgaySinh'] else "", r['TenDangNhap'], r['MatKhau'], r['VaiTro']))

    def them():
        ma = txt_id.get().strip(); ten = txt_name.get().strip(); gt = cbo_gt.get().strip()
        dc = txt_addr.get().strip(); dtv = txt_phone.get().strip(); ns = dt.get_date()
        user = txt_user.get().strip(); pwd = txt_pass.get().strip(); role = cbo_role.get().strip()
        if not (ma and ten and user and pwd):
            messagebox.showwarning("Thiếu","Nhập mã, tên, tài khoản và mật khẩu"); return
        q = "INSERT INTO nhanvien (MaNV, TenNV, GioiTinh, DiaChi, DienThoai, NgaySinh, TenDangNhap, MatKhau, VaiTro) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)"
        if execute_query(q, (ma,ten,gt,dc,dtv,ns,user,pwd,role)):
            messagebox.showinfo("OK","Đã thêm"); load()

    def sua():
        sel = tree.selection(); 
        if not sel: messagebox.showwarning("Chọn","Chọn 1 nhân viên"); return
        ma = txt_id.get().strip(); ten = txt_name.get().strip(); gt = cbo_gt.get(); 
        dc = txt_addr.get(); dtv=txt_phone.get(); ns = dt.get_date()
        user = txt_user.get().strip(); pwd = txt_pass.get().strip(); role = cbo_role.get()
        
        q = "UPDATE nhanvien SET TenNV=%s, GioiTinh=%s, DiaChi=%s, DienThoai=%s, NgaySinh=%s," 
        " TenDangNhap=%s, MatKhau=%s, VaiTro=%s WHERE MaNV=%s"
        if execute_query(q, (ten,gt,dc,dtv,ns,user,pwd,role,ma)):
            messagebox.showinfo("OK","Đã sửa"); load()

    def xoa():
        sel = tree.selection(); 
        if not sel: messagebox.showwarning("Chọn","Chọn 1 nhân viên"); return
        ma = tree.item(sel[0])['values'][0]
        if messagebox.askyesno("Xóa", f"Xóa nhân viên {ma}?"):
            execute_query("DELETE FROM nhanvien WHERE MaNV=%s", (ma,)); load()

    def reset_form():
        txt_id.delete(0, tk.END)
        txt_name.delete(0, tk.END)
        txt_addr.delete(0, tk.END)
        txt_pass.delete(0, tk.END)
        txt_phone.delete(0, tk.END)
        txt_user.delete(0, tk.END)
        cbo_gt.set('')       # Xóa giá trị Combobox
        cbo_role.set('')
        dt.set_date('')      # Xóa ngày
    def search_nv():
        keyword = txt_search.get().strip()
        tree.delete(*tree.get_children())
        if not keyword:
            messagebox.showwarning("Nhập từ khóa", "Nhập mã hoặc tên nhân viên để tìm")
            return
        q = "SELECT MaNV, TenNV, GioiTinh, DiaChi, DienThoai, NgaySinh, TenDangNhap," \
        " MatKhau, VaiTro FROM nhanvien WHERE MaNV LIKE %s OR TenNV LIKE %s"
        rows = fetch_all(q, (f"%{keyword}%", f"%{keyword}%"))
        if not rows:
            messagebox.showinfo("Không tìm thấy", "Không tìm thấy nhân viên nào")
            return
        for r in rows:
            tree.insert("", "end", values=(r['MaNV'], r['TenNV'], r['GioiTinh'], r['DiaChi'],
            r['DienThoai'], r['NgaySinh'], r['TenDangNhap'], r['MatKhau'], r['VaiTro']))

 
        
    def on_select(e):
        sel = tree.selection(); 
        if not sel: return
        r = tree.item(sel[0])['values']
        txt_id.delete(0, tk.END); txt_id.insert(0, r[0])
        txt_name.delete(0, tk.END); txt_name.insert(0, r[1])
        cbo_gt.set(r[2])
        txt_addr.delete(0, tk.END); txt_addr.insert(0, r[3])
        txt_phone.delete(0, tk.END); txt_phone.insert(0, r[4])
        try:
            dt.set_date(r[5])
        except:
            
            pass
        txt_user.delete(0, tk.END); txt_user.insert(0, r[6])
        cbo_role.set(r[7])
    

    tree.bind("<ButtonRelease-1>", on_select)
    load()