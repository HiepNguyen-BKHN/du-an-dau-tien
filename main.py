import flet as ft
import sqlite3
from datetime import datetime

# ==========================================
# CƠ SỞ DỮ LIỆU
# ==========================================
conn = sqlite3.connect("chitieu.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS hu_chi_tieu (ten TEXT PRIMARY KEY, so_tien INTEGER)')
cursor.execute('CREATE TABLE IF NOT EXISTS lich_su (id INTEGER PRIMARY KEY AUTOINCREMENT, loai TEXT, mo_ta TEXT, so_tien INTEGER, hu TEXT, thoi_gian TEXT)')
conn.commit()


def main(page: ft.Page):
    page.title = "Quản lý chi tiêu Pro"
    page.window.width = 450
    page.window.height = 850
    page.scroll = ft.ScrollMode.AUTO
    page.theme_mode = ft.ThemeMode.LIGHT

    # Dữ liệu
    data_hu = {}
    cursor.execute("SELECT ten, so_tien FROM hu_chi_tieu")
    rows = cursor.fetchall()
    if not rows:
        data_hu = {"Thiết yếu": 0, "Tiết kiệm": 0}
        for ten, so_tien in data_hu.items():
            cursor.execute("INSERT INTO hu_chi_tieu VALUES (?, ?)", (ten, so_tien))
        conn.commit()
    else:
        for row in rows:
            data_hu[row[0]] = row[1]

    # UI Components
    so_du_display = ft.Column()
    danh_sach_quan_ly_hu = ft.Column()
    lich_su_chi_tieu = ft.ListView(expand=True, spacing=5, height=200)
    thong_ke_6_thang = ft.Column()
    thong_ke_4_tuan = ft.Column()

    txt_ten_hu_moi = ft.TextField(label="Tên hũ mới", expand=True)
    txt_tien_nap = ft.TextField(label="Số tiền nạp", keyboard_type=ft.KeyboardType.NUMBER, expand=True)
    txt_tien_chi = ft.TextField(label="Số tiền chi", keyboard_type=ft.KeyboardType.NUMBER, expand=True)
    txt_mo_ta_chi = ft.TextField(label="Nội dung chi", expand=True)

    dropdown_nap = ft.Dropdown(label="Hũ nạp", expand=True)
    dropdown_chi = ft.Dropdown(label="Hũ chi", expand=True)
    thang_chon_6_thang = ft.Dropdown(label="Tháng kết thúc", expand=True)
    thang_chon_4_tuan = ft.Dropdown(label="Tháng xem tuần", expand=True)

    def _thanh_bieu_do(nhan: str, gia_tri: int, toi_da: int, mau):
        """Vẽ thanh ngang dạng ProgressBar thuần Flet — không cần thư viện ngoài"""
        pct = (gia_tri / toi_da) if toi_da > 0 else 0
        return ft.Column([
            ft.Row([
                ft.Text(nhan, width=70, size=12),
                ft.ProgressBar(value=pct, expand=True, color=mau, bgcolor=ft.Colors.GREY_200, height=18),
                ft.Text(f"{gia_tri:,}đ", width=90, size=11, text_align=ft.TextAlign.RIGHT),
            ]),
        ], spacing=2)

    def cap_nhat_thong_ke(e=None):
        # Lấy danh sách tháng có giao dịch
        cursor.execute("SELECT thoi_gian FROM lich_su WHERE loai='CHI'")
        danh_sach_thang = set([datetime.now().strftime("%m/%Y")])
        for row in cursor.fetchall():
            try:
                dt = datetime.strptime(row[0], "%d/%m/%Y %H:%M")
                danh_sach_thang.add(dt.strftime("%m/%Y"))
            except:
                pass

        danh_sach_thang = sorted(
            list(danh_sach_thang),
            key=lambda x: datetime.strptime(x, "%m/%Y"),
            reverse=True
        )
        options_thang = [ft.DropdownOption(t) for t in danh_sach_thang]
        thang_chon_6_thang.options = options_thang
        thang_chon_4_tuan.options = options_thang
        if not thang_chon_6_thang.value:
            thang_chon_6_thang.value = danh_sach_thang[0]
        if not thang_chon_4_tuan.value:
            thang_chon_4_tuan.value = danh_sach_thang[0]

        # --- 6 THÁNG ---
        dt_base = datetime.strptime(thang_chon_6_thang.value, "%m/%Y")
        past_6 = []
        for i in range(6):
            m, y = dt_base.month - i, dt_base.year
            if m <= 0: m += 12; y -= 1
            past_6.append(f"{m:02d}/{y}")
        past_6 = past_6[::-1]

        data_6 = {m: 0 for m in past_6}
        cursor.execute("SELECT thoi_gian, so_tien FROM lich_su WHERE loai='CHI'")
        for row in cursor.fetchall():
            try:
                tg = datetime.strptime(row[0], "%d/%m/%Y %H:%M").strftime("%m/%Y")
                if tg in data_6: data_6[tg] += row[1]
            except:
                pass

        max_6 = max(data_6.values()) if any(data_6.values()) else 1
        thong_ke_6_thang.controls.clear()
        thong_ke_6_thang.controls.append(ft.Text("📅 Chi tiêu 6 tháng gần nhất", weight="bold", size=13))
        for thang, tien in data_6.items():
            thong_ke_6_thang.controls.append(
                _thanh_bieu_do(thang, tien, max_6, ft.Colors.BLUE)
            )

        # --- 4 TUẦN ---
        data_4 = [0, 0, 0, 0]
        cursor.execute("SELECT thoi_gian, so_tien FROM lich_su WHERE loai='CHI'")
        for row in cursor.fetchall():
            try:
                dt = datetime.strptime(row[0], "%d/%m/%Y %H:%M")
                if dt.strftime("%m/%Y") == thang_chon_4_tuan.value:
                    idx = min((dt.day - 1) // 7, 3)
                    data_4[idx] += row[1]
            except:
                pass

        max_4 = max(data_4) if any(data_4) else 1
        thong_ke_4_tuan.controls.clear()
        thong_ke_4_tuan.controls.append(ft.Text("🗓 Chi tiêu 4 tuần trong tháng", weight="bold", size=13))
        for i, tien in enumerate(data_4):
            thong_ke_4_tuan.controls.append(
                _thanh_bieu_do(f"Tuần {i+1}", tien, max_4, ft.Colors.ORANGE)
            )

        page.update()

    thang_chon_6_thang.on_change = cap_nhat_thong_ke
    thang_chon_4_tuan.on_change = cap_nhat_thong_ke

    def refresh_ui():
        so_du_display.controls.clear()
        tong_tien = sum(data_hu.values())
        so_du_display.controls.append(
            ft.Container(
                content=ft.Text(f"TỔNG TIỀN: {tong_tien:,} đ", size=24, weight="bold", color=ft.Colors.GREEN),
                alignment=ft.Alignment.CENTER,
                padding=10
            )
        )
        for ten, so_tien in data_hu.items():
            so_du_display.controls.append(
                ft.ListTile(title=ft.Text(ten), trailing=ft.Text(f"{so_tien:,} đ", weight="bold"))
            )

        options = [ft.DropdownOption(ten) for ten in data_hu.keys()]
        dropdown_nap.options = options
        dropdown_chi.options = options

        danh_sach_quan_ly_hu.controls.clear()
        for ten in data_hu.keys():
            danh_sach_quan_ly_hu.controls.append(
                ft.Row([
                    ft.Text(ten, expand=True),
                    ft.IconButton(
                        icon=ft.Icons.DELETE_OUTLINE,
                        icon_color=ft.Colors.RED,
                        on_click=lambda e, t=ten: xoa_hu(t)
                    )
                ])
            )

        lich_su_chi_tieu.controls.clear()
        cursor.execute("SELECT loai, mo_ta, so_tien, hu, thoi_gian FROM lich_su ORDER BY id DESC")
        for row in cursor.fetchall():
            loai, mo_ta, tien, hu, tg = row
            mau = ft.Colors.GREEN if loai == "NẠP" else ft.Colors.RED
            lich_su_chi_tieu.controls.append(
                ft.ListTile(
                    leading=ft.Icon(ft.Icons.ADD_CIRCLE if loai == "NẠP" else ft.Icons.REMOVE_CIRCLE, color=mau),
                    title=ft.Text(mo_ta, weight="bold"),
                    subtitle=ft.Text(f"{tien:,} đ ({hu}) • {tg}", size=12)
                )
            )
        cap_nhat_thong_ke()
        page.update()

    def them_hu_moi(e):
        if txt_ten_hu_moi.value:
            ten = txt_ten_hu_moi.value.strip()
            if ten not in data_hu:
                data_hu[ten] = 0
                cursor.execute("INSERT INTO hu_chi_tieu VALUES (?, ?)", (ten, 0))
                conn.commit()
                txt_ten_hu_moi.value = ""
                refresh_ui()

    def xoa_hu(ten):
        if ten in data_hu:
            del data_hu[ten]
            cursor.execute("DELETE FROM hu_chi_tieu WHERE ten=?", (ten,))
            conn.commit()
            refresh_ui()

    def nap_tien(e):
        if txt_tien_nap.value and txt_tien_nap.value.isdigit() and dropdown_nap.value:
            val, hu = int(txt_tien_nap.value), dropdown_nap.value
            data_hu[hu] += val
            cursor.execute("UPDATE hu_chi_tieu SET so_tien=? WHERE ten=?", (data_hu[hu], hu))
            cursor.execute("INSERT INTO lich_su (loai, mo_ta, so_tien, hu, thoi_gian) VALUES (?,?,?,?,?)",
                           ("NẠP", "Nạp tiền", val, hu, datetime.now().strftime("%d/%m/%Y %H:%M")))
            conn.commit()
            txt_tien_nap.value = ""
            refresh_ui()

    def chi_tien(e):
        if txt_tien_chi.value and txt_tien_chi.value.isdigit() and dropdown_chi.value:
            val, hu = int(txt_tien_chi.value), dropdown_chi.value
            data_hu[hu] -= val
            cursor.execute("UPDATE hu_chi_tieu SET so_tien=? WHERE ten=?", (data_hu[hu], hu))
            cursor.execute("INSERT INTO lich_su (loai, mo_ta, so_tien, hu, thoi_gian) VALUES (?,?,?,?,?)",
                           ("CHI", txt_mo_ta_chi.value, val, hu, datetime.now().strftime("%d/%m/%Y %H:%M")))
            conn.commit()
            txt_tien_chi.value = ""
            txt_mo_ta_chi.value = ""
            refresh_ui()

    # ==========================================
    # GIAO DIỆN
    # ==========================================
    page.add(
        ft.ExpansionTile(
            title=ft.Text("⚙️ QUẢN LÝ DANH SÁCH HŨ", weight="bold"),
            controls=[
                ft.Row([txt_ten_hu_moi, ft.Button("Thêm", on_click=them_hu_moi)]),
                danh_sach_quan_ly_hu
            ]
        ),
        ft.Divider(),
        ft.Text("📊 TRẠNG THÁI CÁC HŨ", weight="bold", size=18),
        so_du_display,
        ft.Divider(),
        ft.Text("💰 GIAO DỊCH", weight="bold", size=18),
        ft.ExpansionTile(
            title=ft.Text("💵 Nạp tiền", weight="bold", color=ft.Colors.GREEN),
            controls=[
                ft.Row([txt_tien_nap, dropdown_nap]),
                ft.Button("Xác nhận nạp", on_click=nap_tien, width=400)
            ]
        ),
        ft.ExpansionTile(
            title=ft.Text("💸 Chi tiêu", weight="bold", color=ft.Colors.RED),
            controls=[
                dropdown_chi,
                ft.Row([txt_mo_ta_chi, txt_tien_chi]),
                ft.Button("Xác nhận chi", on_click=chi_tien, width=400)
            ]
        ),
        ft.Divider(),
        ft.Text("📈 BIỂU ĐỒ CHI TIÊU", weight="bold", size=18),
        ft.ExpansionTile(
            title=ft.Text("📅 6 tháng / 4 tuần", weight="bold", color=ft.Colors.BLUE),
            controls=[
                ft.Row([thang_chon_6_thang, thang_chon_4_tuan]),
                thong_ke_6_thang,
                ft.Divider(height=10),
                thong_ke_4_tuan,
            ]
        ),
        ft.Divider(),
        ft.Text("📜 LỊCH SỬ", weight="bold", size=18),
        lich_su_chi_tieu
    )
    refresh_ui()


ft.run(main)