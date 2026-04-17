import fitz  # Tên module của thư viện PyMuPDF

def merge_4_pages_to_1(input_path: str, output_path: str):
    """
    Hàm gộp 4 trang PDF thành 1 trang.
    Bố cục:
      [Trang 1] [Trang 2]
      [Trang 3] [Trang 4]
    """
    # Mở file PDF đầu vào
    try:
        src_pdf = fitz.open(input_path)
    except Exception as e:
        print(f"Lỗi khi mở file: {e}")
        return
        
    if len(src_pdf) == 0:
        print("File PDF đầu vào trống!")
        return
        
    # Tạo file PDF mới để chứa kết quả đầu ra
    dest_pdf = fitz.open()

    # Lấy kích thước của trang đầu tiên làm chuẩn cho file đích.
    # Chiều rộng (W) và chiều cao (H) của trang đích sẽ bằng trang gốc.
    first_page = src_pdf[0]
    W = first_page.rect.width
    H = first_page.rect.height

    # Khai báo tọa độ 4 khung hình chữ nhật trên trang đích để chứa 4 trang gốc
    # Tọa độ fitz.Rect(x0, y0, x1, y1)
    rects = [
        fitz.Rect(0, 0, W/2, H/2),         # Góc trên - bên trái (Trang 1)
        fitz.Rect(W/2, 0, W, H/2),         # Góc trên - bên phải (Trang 2)
        fitz.Rect(0, H/2, W/2, H),         # Góc dưới - bên trái (Trang 3)
        fitz.Rect(W/2, H/2, W, H)          # Góc dưới - bên phải (Trang 4)
    ]

    total_pages = len(src_pdf)

    # Duyệt vòng lặp mỗi bước nhảy là 4 trang
    for i in range(0, total_pages, 4):
        # Tạo 1 trang trống mới trên file đích
        new_page = dest_pdf.new_page(width=W, height=H)
        
        # Đặt tối đa 4 trang tiếp theo vào các vùng đã khai báo
        for j in range(4):
            current_page_index = i + j
            if current_page_index < total_pages:
                # show_pdf_page tự động thu nhỏ/phóng to trang gốc cho vừa vào ô rects[j]
                new_page.show_pdf_page(rects[j], src_pdf, current_page_index)

    # Lưu kết quả ra file mới
    dest_pdf.save(output_path)
    
    # Đóng các tài nguyên
    src_pdf.close()
    dest_pdf.close()
    print(f"Tuyệt vời! File đã được gộp thành công và lưu tại: {output_path}")

# ================= CÁCH SỬ DỤNG ================= 
if __name__ == "__main__":
    # Thay đổi đường dẫn tới file của bạn ở đây
    input_file = r"C:\Users\user\Downloads\VHNMD.pdf" 
    output_file = r"\LANGUAGE\NMD.pdf"
    
    merge_4_pages_to_1(input_file, output_file)
