# 🎯 FRAMS - Face Recognition Attendance & Customer Management System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-1.1.2-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Hệ thống nhận diện khuôn mặt tích hợp AI, cung cấp giải pháp toàn diện cho **chấm công nhân viên** và **quản lý khách hàng**.

![Face Recognition](https://img.shields.io/badge/AI-Face_Recognition-ff69b4)
![OpenCV](https://img.shields.io/badge/OpenCV-4.4.0-green)
![REST API](https://img.shields.io/badge/API-RESTful-orange)

---

## ✨ Tính Năng Chính

### 🏢 Chấm Công Nhân Viên
- ✅ Nhận diện khuôn mặt tự động
- ✅ Ghi nhận thời gian chấm công
- ✅ Xem lịch sử chấm công theo ngày/tháng
- ✅ Hỗ trợ nhiều khuôn mặt trong 1 ảnh
- ✅ API đầy đủ cho tích hợp

### 👥 Nhận Diện Khách Hàng
- ✅ Theo dõi lượt ghé thăm
- ✅ Lưu trữ thông tin khách hàng (email, SĐT, ghi chú)
- ✅ Xem lịch sử ghé thăm
- ✅ Quản lý CRUD đầy đủ
- ✅ Thống kê và báo cáo

### 🔌 RESTful API
- ✅ Endpoints đầy đủ cho attendance & customers
- ✅ Hỗ trợ CORS
- ✅ JSON response format
- ✅ Error handling chuẩn

### 🎨 Giao Diện Web
- ✅ Responsive design (Bootstrap 4)
- ✅ Giao diện đẹp, hiện đại
- ✅ Hỗ trợ upload ảnh và chụp trực tiếp
- ✅ Real-time statistics

---

## 🚀 Cài Đặt Nhanh

### 1. Clone Repository
```bash
git clone <repository-url>
cd multiple-face-recognition
```

### 2. Cài Đặt Dependencies
```bash
pip install -r requirements.txt
```

### 3. Chạy Application
```bash
python app_improved.py
```

### 4. Truy Cập
Mở trình duyệt: **http://localhost:5000**

---

## 📋 Yêu Cầu Hệ Thống

- **Python:** 3.8 hoặc cao hơn
- **Webcam:** Cho chức năng chụp ảnh trực tiếp (tùy chọn)
- **RAM:** Tối thiểu 4GB
- **OS:** Windows, macOS, hoặc Linux

---

## 📖 Hướng Dẫn Sử Dụng

### Chấm Công Nhân Viên

#### Bước 1: Đăng ký nhân viên
```python
import requests

data = {'name': 'NGUYEN_VAN_A'}
files = {'image': open('employee.jpg', 'rb')}

response = requests.post(
    'http://localhost:5000/api/employees/register',
    data=data,
    files=files
)
```

#### Bước 2: Chấm công
```python
files = {'image': open('photo.jpg', 'rb')}
response = requests.post(
    'http://localhost:5000/api/attendance/recognize',
    files=files
)
print(response.json())
```

### Nhận Diện Khách Hàng

#### Bước 1: Thêm khách hàng
```python
import requests

# Tạo khách hàng
customer_data = {
    "name": "NGUYEN_VAN_C",
    "email": "customer@example.com",
    "phone": "0912345678",
    "notes": "Khách hàng VIP"
}
response = requests.post('http://localhost:5000/api/customers', json=customer_data)
customer_id = response.json()['customer_id']

# Upload ảnh
files = {'image': open('customer.jpg', 'rb')}
requests.post(f'http://localhost:5000/api/customers/{customer_id}/upload-photo', files=files)
```

#### Bước 2: Nhận diện
```python
files = {'image': open('customer_photo.jpg', 'rb')}
response = requests.post('http://localhost:5000/api/customers/recognize', files=files)

data = response.json()
if data['recognized'] > 0:
    for customer in data['customers']:
        print(f"Khách hàng: {customer['name']}")
        print(f"Số lần ghé: {customer['visit_count']}")
```

---

## 🌐 API Endpoints

### Attendance API

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/attendance/recognize` | Nhận diện & chấm công |
| GET | `/api/attendance/today` | Danh sách chấm công hôm nay |
| GET | `/api/attendance/all` | Toàn bộ lịch sử chấm công |
| GET | `/api/attendance/employee/<name>` | Lịch sử của 1 nhân viên |

### Customer API

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/customers/recognize` | Nhận diện khách hàng |
| GET | `/api/customers` | Danh sách khách hàng |
| POST | `/api/customers` | Tạo khách hàng mới |
| GET | `/api/customers/<id>` | Chi tiết khách hàng |
| PUT | `/api/customers/<id>` | Cập nhật khách hàng |
| DELETE | `/api/customers/<id>` | Xóa khách hàng |
| POST | `/api/customers/<id>/upload-photo` | Upload ảnh |
| GET | `/api/customers/<name>/visits` | Lịch sử ghé thăm |

### Employee API

| Method | Endpoint | Mô tả |
|--------|----------|-------|
| POST | `/api/employees/register` | Đăng ký nhân viên |
| GET | `/api/employees` | Danh sách nhân viên |

📚 **Xem tài liệu đầy đủ:** [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

## 🖥️ Giao Diện Web

### Trang Chủ
**URL:** http://localhost:5000

![Main Page](https://via.placeholder.com/800x400/667eea/ffffff?text=Main+Dashboard)

### Chấm Công
**URL:** http://localhost:5000/attendance-web
- Upload ảnh hoặc chụp trực tiếp
- Xem danh sách chấm công hôm nay
- Đăng ký nhân viên mới
- Thống kê real-time

### Nhận Diện Khách Hàng
**URL:** http://localhost:5000/customer-recognition
- Nhận diện khách hàng
- Thêm khách hàng mới
- Xem thông tin chi tiết
- Theo dõi lượt ghé thăm

### Quản Lý Khách Hàng
**URL:** http://localhost:5000/customers-web
- Bảng quản lý với DataTables
- CRUD operations
- Tìm kiếm và filter
- Export data

---

## 📁 Cấu Trúc Dự Án

```
multiple-face-recognition/
│
├── app.py                          # Ứng dụng gốc
├── app_improved.py                 # ⭐ Ứng dụng mới (khuyến nghị)
├── requirements.txt                # Python dependencies
│
├── API_DOCUMENTATION.md            # 📖 Tài liệu API đầy đủ
├── SETUP_GUIDE.md                  # 🛠️ Hướng dẫn cài đặt chi tiết
├── README_NEW.md                   # 📄 File này
│
├── information.db                  # SQLite database
│
├── Training images/                # 📸 Ảnh nhân viên
├── Customer images/                # 📸 Ảnh khách hàng
│
└── templates/                      # HTML templates
    ├── main_improved.html          # Trang chủ mới
    ├── attendance_tracking.html    # Chấm công
    ├── customer_recognition.html   # Nhận diện khách hàng
    ├── customers.html              # Quản lý khách hàng
    └── ...                         # Templates khác
```

---

## 🔧 Công Nghệ Sử Dụng

### Backend
- **Python 3.8+**
- **Flask** - Web framework
- **face_recognition** - Face detection & recognition
- **OpenCV** - Computer vision
- **SQLite** - Database
- **Flask-CORS** - API CORS support

### Frontend
- **HTML5/CSS3**
- **Bootstrap 4** - UI framework
- **jQuery** - AJAX & DOM manipulation
- **Font Awesome** - Icons
- **DataTables** - Data grid

### AI/ML
- **dlib** - Deep learning library
- **face_recognition** - Face encoding
- **numpy** - Numerical computing

---

## 📊 Database Schema

### Attendance Table
```sql
CREATE TABLE Attendance (
    NAME TEXT NOT NULL,
    Time TEXT NOT NULL,
    Date TEXT NOT NULL
)
```

### Customers Table
```sql
CREATE TABLE Customers (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    Name TEXT NOT NULL,
    Email TEXT,
    Phone TEXT,
    LastVisit TEXT,
    VisitCount INTEGER DEFAULT 0,
    Notes TEXT
)
```

### CustomerVisits Table
```sql
CREATE TABLE CustomerVisits (
    ID INTEGER PRIMARY KEY AUTOINCREMENT,
    CustomerName TEXT NOT NULL,
    VisitTime TEXT NOT NULL,
    VisitDate TEXT NOT NULL
)
```

---

## ⚙️ Configuration

### Thay đổi ngưỡng nhận diện
Trong `app_improved.py`:
```python
FACE_MATCH_THRESHOLD = 0.50  # Mặc định: 0.50
```
- **Tăng (0.60-0.70):** Chính xác hơn, khó nhận diện hơn
- **Giảm (0.30-0.40):** Dễ nhận diện, có thể kém chính xác

### Thay đổi port
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)  # Đổi port
```

---

## 🐛 Xử Lý Sự Cố

### Lỗi cài đặt dlib (Windows)
```bash
# Cài Visual Studio Build Tools
# Sau đó:
pip install cmake
pip install dlib
```

### Webcam không hoạt động
- Kiểm tra quyền truy cập camera
- Thử camera USB khác
- Kiểm tra camera đang được sử dụng bởi app khác

### Không nhận diện được
- Đảm bảo ảnh có ánh sáng tốt
- Khuôn mặt chiếm ít nhất 30% ảnh
- Nhìn thẳng vào camera

📚 **Xem chi tiết:** [SETUP_GUIDE.md](SETUP_GUIDE.md)

---

## 🚀 Deployment

### Heroku
```bash
heroku create your-app-name
git push heroku main
```

### Docker
```dockerfile
FROM python:3.8
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app_improved.py"]
```

### Gunicorn
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app_improved:app
```

---

## 📝 To-Do List

- [ ] Thêm authentication/authorization
- [ ] Export báo cáo Excel/PDF
- [ ] Email notifications
- [ ] Mobile app (React Native/Flutter)
- [ ] Dashboard analytics nâng cao
- [ ] Multi-language support
- [ ] Dark mode

---

## 🤝 Đóng Góp

Contributions are welcome! Please feel free to submit a Pull Request.

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👥 Authors

- **Original FRAMS** - Initial work
- **Enhanced Version** - API & Customer Recognition features

---

## 🙏 Acknowledgments

- [face_recognition](https://github.com/ageitgey/face_recognition) by Adam Geitgey
- [OpenCV](https://opencv.org/)
- [Flask](https://flask.palletsprojects.com/)
- Bootstrap & jQuery communities

---

## 📞 Liên Hệ & Hỗ Trợ

- **Issues:** [GitHub Issues](https://github.com/your-repo/issues)
- **Email:** support@example.com
- **Documentation:** [API Docs](API_DOCUMENTATION.md) | [Setup Guide](SETUP_GUIDE.md)

---

<p align="center">
  Made with ❤️ using Python & AI
</p>

<p align="center">
  <strong>⭐ Nếu thấy hữu ích, hãy cho dự án 1 star! ⭐</strong>
</p>
