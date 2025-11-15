# ⚡ Quick Start Guide - 3 Phút Bắt Đầu!

## 🚀 Khởi động nhanh

### Linux/macOS:
```bash
./start.sh
```

### Windows:
```batch
start.bat
```

**Hoặc chạy thủ công:**
```bash
# 1. Cài dependencies
pip install -r requirements.txt

# 2. Chạy app
python app_improved.py
```

## 🌐 Truy cập ứng dụng

Mở trình duyệt: **http://localhost:5000**

## 📱 Các trang chính

| URL | Chức năng |
|-----|-----------|
| http://localhost:5000 | Trang chủ |
| http://localhost:5000/attendance-web | Chấm công nhân viên |
| http://localhost:5000/customer-recognition | Nhận diện khách hàng |
| http://localhost:5000/customers-web | Quản lý khách hàng |

## 🧪 Test API

```bash
# Đảm bảo server đang chạy
python test_api.py
```

## 📖 Hướng dẫn đầy đủ

- **Setup chi tiết:** [SETUP_GUIDE.md](SETUP_GUIDE.md)
- **API Documentation:** [API_DOCUMENTATION.md](API_DOCUMENTATION.md)
- **Full README:** [README_NEW.md](README_NEW.md)

## 🎯 Sử dụng cơ bản

### 1. Đăng ký nhân viên
1. Vào http://localhost:5000/attendance-web
2. Cuộn xuống "Đăng Ký Nhân Viên Mới"
3. Nhập tên (ví dụ: NGUYEN_VAN_A)
4. Chọn/chụp ảnh
5. Click "Đăng Ký"

### 2. Chấm công
1. Ở cùng trang
2. Chọn/chụp ảnh
3. Click "Nhận Diện & Chấm Công"
4. Xem kết quả

### 3. Thêm khách hàng
1. Vào http://localhost:5000/customer-recognition
2. Điền thông tin (tên, email, SĐT, ghi chú)
3. Chọn ảnh khuôn mặt
4. Click "Thêm Khách Hàng"

### 4. Nhận diện khách hàng
1. Ở cùng trang
2. Chọn/chụp ảnh
3. Click "Nhận Diện Khách Hàng"
4. Xem thông tin chi tiết

## 🔧 Troubleshooting

### Server không khởi động
```bash
# Kiểm tra port 5000 có đang sử dụng không
lsof -i :5000  # Linux/macOS
netstat -ano | findstr :5000  # Windows

# Nếu có, kill process hoặc đổi port trong app_improved.py
```

### Lỗi cài đặt
```bash
# Cài lại dependencies
pip install --upgrade pip
pip install -r requirements.txt --no-cache-dir
```

### Không nhận diện được
- Đảm bảo ảnh rõ ràng, ánh sáng tốt
- Khuôn mặt chiếm ít nhất 30% ảnh
- Nhìn thẳng vào camera

## 📞 Hỗ trợ

- **Issues:** GitHub Issues
- **Docs:** Xem các file .md trong thư mục
- **Email:** support@example.com

---

**Chúc bạn sử dụng thành công! 🎉**
