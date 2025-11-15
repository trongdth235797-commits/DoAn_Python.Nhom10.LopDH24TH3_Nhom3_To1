# hoadon_view.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from database import fetch_all, execute_query

def show():
    win = tk.Toplevel()
    win.title("Quản lý hóa đơn")
    win.geometry("1000x650")

    frm = tk.LabelFrame(win, text="Thông tin hóa đơn", font=("Times New Roman", 12, "bold"), padx=10, pady=10)
    frm.pack(fill="x", padx=10, pady=6)

    tk.Label(frm, text="Mã HĐ:", font=("Times New Roman", 12)).grid(row=0, column=0, sticky="w")
    txt_ma = tk.Entry(frm, font=("Times New Roman", 12)); txt_ma.grid(row=0, column=1, padx=6)
    tk.Label(frm, text="Nhân viên:", font=("Times New Roman", 12)).grid(row=1, column=0, sticky="w")
    cbo_nv = ttk.Combobox(frm, state="readonly"); cbo_nv.grid(row=1, column=1, padx=6)
    tk.Label(frm, text="Khách hàng:", font=("Times New Roman", 12)).grid(row=0, column=2, sticky="w")
    cbo_kh = ttk.Combobox(frm, state="readonly"); cbo_kh.grid(row=0, column=3, padx=6)
    tk.Label(frm, text="Ngày bán:", font=("Times New Roman", 12)).grid(row=1, column=2, sticky="w")
    dt = DateEntry(frm, date_pattern="yyyy-mm-dd"); dt.grid(row=1, column=3, padx=6)

    # chi tiết
    frm2 = tk.LabelFrame(win, text="Chi tiết (thêm sản phẩm vào HĐ)", font=("Times New Roman", 12, "bold"), padx=10, pady=10)
    frm2.pack(fill="x", padx=10, pady=6)
    tk.Label(frm2, text="Sản phẩm:", font=("Times New Roman", 12)).grid(row=0, column=0, sticky="w")
    cbo_sp = ttk.Combobox(frm2, state="readonly"); cbo_sp.grid(row=0, column=1, padx=6)
    tk.Label(frm2, text="Số lượng:", font=("Times New Roman", 12)).grid(row=0, column=2, sticky="w")
    txt_sl = tk.Entry(frm2, font=("Times New Roman", 12), width=10); txt_sl.grid(row=0, column=3, padx=6)
    tk.Button(frm2, text="Thêm vào HĐ", command=lambda: them_cthd()).grid(row=0, column=4, padx=6)
    tk.Label(frm, text="Tìm HĐ:", font=("Times New Roman", 12)).grid(row=2, column=0, sticky="w", pady=4)
    txt_search = tk.Entry(frm, font=("Times New Roman", 12)); txt_search.grid(row=2, column=1, padx=6)
    tk.Button(frm, text="Tìm kiếm", command=lambda: search_hd()).grid(row=2, column=2, padx=6)



    # Treeview chi tiết
    cols = ("MaHD","MaSP","TenSP","SL","DonGia","ThanhTien")
    tree = ttk.Treeview(win, columns=cols, show="headings")
    for c in cols:
        tree.heading(c, text=c); tree.column(c, anchor="center", width=140)
    tree.pack(fill="both", expand=True, padx=10, pady=6)
    lbl_total = tk.Label(win, text="Tổng tiền: 0", font=("Times New Roman", 12, "bold"))
    lbl_total.pack(padx=10, pady=4)

    def tinh_tong():
        tong = 0
        for r in tree.get_children():
            thanhtien = tree.item(r)['values'][5]  # cột ThanhTien
            tong += float(thanhtien)
        lbl_total.config(text=f"Tổng tiền: {tong:,.0f} VNĐ")


    btnf = tk.Frame(win); btnf.pack(fill="x", padx=10, pady=6)
    tk.Button(btnf, text="Tạo hóa đơn", command=lambda: them_hd()).pack(side="left", padx=6)
    tk.Button(btnf, text="Xóa chi tiết HĐ", command=lambda: xoa_ct()).pack(side="left", padx=6)
    tk.Button(btnf, text="Tải lại", command=lambda: load()).pack(side="left", padx=6)

    def load_comboboxes():
        cbo_nv['values'] = [f"{r['MaNV']}" for r in fetch_all("SELECT MaNV, TenNV FROM nhanvien")]
        cbo_kh['values'] = [f"{r['MaKhach']}" for r in fetch_all("SELECT MaKhach, TenKhach FROM khachhang")]
        cbo_sp['values'] = [f"{r['MaSP']}" for r in fetch_all("SELECT MaSP, TenSP FROM sanpham")]

    def load():
        tree.delete(*tree.get_children())
    
    # LEFT JOIN để lấy tất cả hóa đơn, kể cả chưa có chi tiết
        rows = fetch_all("""
            SELECT h.MaHD, c.MaSP, s.TenSP, c.SL, c.DonGia, c.ThanhTien
            FROM hoadon h
            LEFT JOIN cthd c ON h.MaHD = c.MaHD
            LEFT JOIN sanpham s ON c.MaSP = s.MaSP
            ORDER BY h.MaHD
    """)
    
        for r in rows:
            masp = r['MaSP'] if r['MaSP'] else ''
            tensp = r['TenSP'] if r['TenSP'] else ''
            sl = r['SL'] if r['SL'] else 0
            dg = r['DonGia'] if r['DonGia'] else 0
            tt = r['ThanhTien'] if r['ThanhTien'] else 0
            tree.insert("", "end", values=(r['MaHD'], masp, tensp, sl, dg, tt))
    
        tinh_tong()
        txt_ma.delete(0, tk.END)
        cbo_nv.set(''); cbo_kh.set(''); dt.set_date(''); cbo_sp.set(''); txt_sl.delete(0, tk.END)


    def them_hd():
        mahd = txt_ma.get().strip()
        nv = cbo_nv.get(); kh = cbo_kh.get(); ngay = dt.get_date()
        if not (mahd and nv and kh):
            messagebox.showwarning("Thiếu","Nhập mã HĐ, NV, KH")
            return
        # Kiểm tra HĐ đã tồn tại chưa
        existing = fetch_all("SELECT * FROM hoadon WHERE MaHD=%s", (mahd,))
        if existing:
            messagebox.showwarning("Lỗi","Mã HĐ đã tồn tại")
            return
        
        if execute_query("INSERT INTO hoadon (MaHD, MaNV, MaKhach, NgayBan) VALUES (%s,%s,%s,%s)", (mahd, nv, kh, ngay)):
            messagebox.showinfo("OK","Đã tạo hóa đơn")
            txt_sl.delete(0, tk.END)
            cbo_sp.set('')
            load()
            load_comboboxes()  # cập nhật combobox

    def them_cthd():
        mahd = txt_ma.get().strip()
        if not mahd:
            messagebox.showwarning("Lỗi","Tạo hóa đơn trước khi thêm sản phẩm")
            return

        masp = cbo_sp.get().strip()
        if not masp:
            messagebox.showwarning("Lỗi","Chọn sản phẩm")
            return

        try:
            sl = int(txt_sl.get().strip())
        except:
            messagebox.showwarning("Lỗi","SL phải là số nguyên")
            return

    # lấy giá hiện tại
        rows = fetch_all("SELECT Gia FROM sanpham WHERE MaSP=%s", (masp,))
        if not rows:
            messagebox.showerror("Lỗi", "Không tìm SP")
            return

        gia = rows[0]['Gia']
        thanhtien = gia * sl
        q = "INSERT INTO cthd (MaHD, MaSP, SL, DonGia, ThanhTien) VALUES (%s,%s,%s,%s,%s)"
        if execute_query(q, (mahd, masp, sl, gia, thanhtien)):
            messagebox.showinfo("OK","Đã thêm vào chi tiết")
            load()  # load lại Treeview
            txt_sl.delete(0, tk.END)
            cbo_sp.set('')
    def xoa_ct():
        sel = tree.selection()
        if not sel: messagebox.showwarning("Chọn","Chọn 1 dòng"); return
        r = tree.item(sel[0])['values']; mahd=r[0]; masp=r[1]
        if not masp:
            messagebox.showwarning("Lỗi", "Hóa đơn này chưa có sản phẩm để xóa")
            return

        if messagebox.askyesno("Xóa", f"Xóa SP {masp} khỏi HĐ {mahd}?"):
            execute_query("DELETE FROM cthd WHERE MaHD=%s AND MaSP=%s", (mahd, masp))
            tree.delete(sel[0])
            tinh_tong()  # Cập nhật tổng tiền
    def on_select(e):
        sel = tree.selection()
        if not sel:
            return
        r = tree.item(sel[0])['values']
    # r = (MaHD, MaSP, TenSP, SL, DonGia, ThanhTien)

    # Điền vào các ô thông tin HĐ
        txt_ma.delete(0, tk.END); txt_ma.insert(0, r[0])
    
    # Chọn nhân viên và khách hàng tương ứng (giả sử chỉ lấy MaNV/MaKhach)
        cbo_sp.set(r[2])  # Hiển thị tên SP
        txt_sl.delete(0, tk.END); txt_sl.insert(0, r[3])

    tree.bind("<<TreeviewSelect>>", on_select)
    def search_hd():
        keyword = txt_search.get().strip()
        tree.delete(*tree.get_children())  # Xóa Treeview trước khi hiển thị kết quả

        if not keyword:
            messagebox.showwarning("Nhập từ khóa", "Vui lòng nhập mã HĐ, MaNV hoặc MaKhach để tìm")
            return

    # Query tìm kiếm
        q = """SELECT c.MaHD, c.MaSP, s.TenSP, c.SL, c.DonGia, c.ThanhTien
           FROM cthd c
           JOIN sanpham s ON c.MaSP = s.MaSP
           JOIN hoadon h ON c.MaHD = h.MaHD
           WHERE h.MaHD LIKE %s OR h.MaNV LIKE %s OR h.MaKhach LIKE %s"""
    
        rows = fetch_all(q, (f"%{keyword}%", f"%{keyword}%", f"%{keyword}%"))
    
        if not rows:
            messagebox.showinfo("Không tìm thấy", "Không tìm thấy hóa đơn nào phù hợp")
            return

        for r in rows:
            masp = r['MaSP'] if r['MaSP'] else ''
            tensp = r['TenSP'] if r['TenSP'] else ''
            sl = r['SL'] if r['SL'] else 0
            dg = r['DonGia'] if r['DonGia'] else 0
            tt = r['ThanhTien'] if r['ThanhTien'] else 0
            tree.insert("", "end", values=(r['MaHD'], masp, tensp, sl, dg, tt))


    load_comboboxes()
    load()