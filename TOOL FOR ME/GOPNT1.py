import fitz  # Thư viện PyMuPDF
import os

def merge_multiple_pdfs(pdf_list, output_path):
    """
    Hàm gộp nhiều file PDF thành một file duy nhất.
    
    :param pdf_list: Danh sách đường dẫn các file PDF cần gộp (theo thứ tự).
    :param output_path: Đường dẫn file PDF đầu ra.
    """
    # Tạo một file PDF trống để chứa kết quả
    merged_pdf = fitz.open()

    for pdf_path in pdf_list:
        if not os.path.exists(pdf_path):
            print(f"⚠️ Cảnh báo: File không tồn tại và sẽ bị bỏ qua - {pdf_path}")
            continue
            
        try:
            # Mở file PDF gốc
            with fitz.open(pdf_path) as pdf:
                # Chèn toàn bộ nội dung của file này vào file tổng
                merged_pdf.insert_pdf(pdf)
                print(f"✅ Đã gộp thành công: {pdf_path}")
        except Exception as e:
            print(f"❌ Lỗi khi đọc file {pdf_path}: {e}")

    # Lưu file kết quả
    try:
        # Tối ưu hóa dung lượng (garbage=4, deflate=True) khi lưu
        merged_pdf.save(output_path, garbage=4, deflate=True)
        print(f"\n🎉 Tuyệt vời! File gộp đã được lưu tại:\n👉 {output_path}")
    except Exception as e:
        print(f"❌ Lỗi khi lưu file đầu ra: {e}")
    finally:
        # Luôn nhớ đóng tài nguyên
        merged_pdf.close()

# ================= CÁCH SỬ DỤNG ================= 
if __name__ == "__main__":
    # Thay đổi danh sách các đường dẫn file bạn muốn gộp ở đây
    # Các file sẽ được gộp theo đúng thứ tự từ trên xuống dưới
    danh_sach_file = [
        r"E:\2025.2\MIT\1.pdf",
        r"E:\2025.2\MIT\2.pdf",
        r"E:\2025.2\MIT\3.pdf",
        r"E:\2025.2\MIT\4.pdf",
        r"E:\2025.2\MIT\5.pdf",
        r"E:\2025.2\MIT\6.pdf",
        r"E:\2025.2\MIT\7.pdf",
        r"E:\2025.2\MIT\8.pdf",
        r"E:\2025.2\MIT\9.pdf",
        r"E:\2025.2\MIT\10.pdf"
    ]
    
    # Đường dẫn file PDF kết quả sau khi gộp
    file_ket_qua = r"C:\Users\user\Downloads\MIT.pdf"
    
    merge_multiple_pdfs(danh_sach_file, file_ket_qua)
