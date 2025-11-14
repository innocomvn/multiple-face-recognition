# Hướng Dẫn Cài Đặt & Sử Dụng
# Face Recognition Attendance & Customer System

## Tổng Quan Hệ Thống

Hệ thống nhận diện khuôn mặt tích hợp hai tính năng chính:
1. **Chấm công nhân viên** - Tự động nhận diện và ghi nhận giờ vào
2. **Nhận ra khách hàng** - Theo dõi lượt ghé thăm và thông tin khách hàng

---

## Yêu Cầu Hệ Thống

### Phần Mềm Cần Thiết
- **Python 3.8** hoặc cao hơn
- **pip** (Python package manager)
- **Webcam** (cho chức năng chụp ảnh trực tiếp)

### Hệ Điều Hành
- Windows 10/11
- macOS 10.14+
- Linux (Ubuntu 18.04+, Debian, etc.)

---

## Cài Đặt

### Bước 1: Clone Repository

```bash
git clone <repository-url>
cd multiple-face-recognition
```

### Bước 2: Tạo Virtual Environment (Khuyến Nghị)

**Windows:**
```bash
python -m venv venv
venv\Scripts\activate
```

**macOS/Linux:**
```bash
python3 -m venv venv
source venv/bin/activate
```

### Bước 3: Cài Đặt Dependencies

```bash
pip install -r requirements.txt
```

**Lưu ý:** Quá trình cài đặt có thể mất 5-10 phút do các thư viện như `dlib` và `face-recognition` cần compile.

**Nếu gặp lỗi khi cài dlib trên Windows:**
1. Tải Visual Studio Build Tools: https://visualstudio.microsoft.com/downloads/
2. Cài CMake: `pip install cmake`
3. Thử lại: `pip install dlib`

### Bước 4: Tạo Thư Mục Cần Thiết

```bash
mkdir "Training images"
mkdir "Customer images"
```

### Bước 5: Khởi Tạo Database

Database sẽ tự động được tạo khi chạy ứng dụng lần đầu.

---

## Chạy Ứng Dụng

### Chạy Server

**Sử dụng app_improved.py (Khuyến nghị - có API đầy đủ):**
```bash
python app_improved.py
```

**Hoặc sử dụng app.py (phiên bản cũ):**
```bash
python app.py
```

Server sẽ chạy tại: `http://localhost:5000`

### Truy Cập Giao Diện Web

Mở trình duyệt và truy cập:

1. **Trang chủ:** http://localhost:5000
2. **Chấm công nhân viên:** http://localhost:5000/attendance-web
3. **Nhận diện khách hàng:** http://localhost:5000/customer-recognition
4. **Quản lý khách hàng:** http://localhost:5000/customers-web

---

## Hướng Dẫn Sử Dụng

### A. Chấm Công Nhân Viên

#### 1. Đăng Ký Nhân Viên Mới

**Qua Giao Diện Web:**
1. Truy cập http://localhost:5000/attendance-web
2. Trong phần "Đăng Ký Nhân Viên Mới":
   - Nhập tên nhân viên (ví dụ: `NGUYEN_VAN_A`)
   - Chọn ảnh khuôn mặt hoặc chụp ảnh mới
   - Click "Đăng Ký"

**Qua API:**
```python
import requests

data = {'name': 'NGUYEN_VAN_A'}
files = {'image': open('employee.jpg', 'rb')}

response = requests.post(
    'http://localhost:5000/api/employees/register',
    data=data,
    files=files
)
print(response.json())
```

#### 2. Chấm Công

**Qua Giao Diện Web:**
1. Chọn ảnh hoặc chụp ảnh mới
2. Click "Nhận Diện & Chấm Công"
3. Hệ thống sẽ tự động:
   - Nhận diện khuôn mặt
   - Ghi nhận thời gian
   - Hiển thị kết quả

**Qua API:**
```python
import requests

files = {'image': open('photo.jpg', 'rb')}
response = requests.post(
    'http://localhost:5000/api/attendance/recognize',
    files=files
)
print(response.json())
```

#### 3. Xem Danh Sách Chấm Công

**Giao diện web tự động hiển thị:**
- Danh sách chấm công hôm nay
- Tổng số nhân viên đã chấm công
- Thống kê

**Hoặc qua API:**
```python
import requests

# Hôm nay
response = requests.get('http://localhost:5000/api/attendance/today')
print(response.json())

# Tất cả
response = requests.get('http://localhost:5000/api/attendance/all')
print(response.json())
```

---

### B. Nhận Diện Khách Hàng

#### 1. Thêm Khách Hàng Mới

**Qua Giao Diện Web:**
1. Truy cập http://localhost:5000/customer-recognition
2. Trong phần "Thêm Khách Hàng Mới":
   - Nhập tên khách hàng
   - Nhập email, số điện thoại (tùy chọn)
   - Nhập ghi chú (tùy chọn)
   - Chọn ảnh khuôn mặt
   - Click "Thêm Khách Hàng"

**Qua API:**
```python
import requests

# Tạo khách hàng
data = {
    "name": "NGUYEN_VAN_C",
    "email": "customer@example.com",
    "phone": "0912345678",
    "notes": "Khách hàng VIP"
}
response = requests.post('http://localhost:5000/api/customers', json=data)
customer_id = response.json()['customer_id']

# Upload ảnh
files = {'image': open('customer.jpg', 'rb')}
requests.post(
    f'http://localhost:5000/api/customers/{customer_id}/upload-photo',
    files=files
)
```

#### 2. Nhận Diện Khách Hàng

**Qua Giao Diện Web:**
1. Chọn ảnh hoặc chụp ảnh
2. Click "Nhận Diện Khách Hàng"
3. Hệ thống hiển thị:
   - Tên khách hàng
   - Thông tin liên hệ
   - Số lần ghé thăm
   - Ghi chú

**Qua API:**
```python
import requests

files = {'image': open('customer_photo.jpg', 'rb')}
response = requests.post(
    'http://localhost:5000/api/customers/recognize',
    files=files
)

data = response.json()
if data['recognized'] > 0:
    for customer in data['customers']:
        print(f"Tên: {customer['name']}")
        print(f"Số lần ghé: {customer['visit_count']}")
```

#### 3. Quản Lý Khách Hàng

Truy cập http://localhost:5000/customers-web để:
- Xem danh sách tất cả khách hàng
- Chỉnh sửa thông tin
- Xóa khách hàng
- Xem lịch sử ghé thăm

---

## Cấu Trúc Thư Mục

```
multiple-face-recognition/
├── app.py                          # Ứng dụng gốc
├── app_improved.py                 # Ứng dụng mới với API đầy đủ
├── requirements.txt                # Dependencies
├── API_DOCUMENTATION.md            # Tài liệu API
├── SETUP_GUIDE.md                  # Hướng dẫn này
├── information.db                  # SQLite database
│
├── Training images/                # Ảnh nhân viên
│   ├── NGUYEN_VAN_A.png
│   └── TRAN_THI_B.png
│
├── Customer images/                # Ảnh khách hàng
│   ├── NGUYEN_VAN_C.png
│   └── LE_THI_D.png
│
└── templates/                      # HTML templates
    ├── main.html                   # Trang chủ
    ├── attendance_tracking.html    # Chấm công
    ├── customer_recognition.html   # Nhận diện khách hàng
    └── customers.html              # Quản lý khách hàng
```

---

## Sử Dụng API

### Ví Dụ Python Script Hoàn Chỉnh

```python
import requests
from pathlib import Path

class FaceRecognitionSystem:
    def __init__(self, base_url='http://localhost:5000/api'):
        self.base_url = base_url

    # === NHÂN VIÊN ===

    def register_employee(self, name, image_path):
        """Đăng ký nhân viên mới"""
        data = {'name': name}
        files = {'image': open(image_path, 'rb')}
        response = requests.post(f'{self.base_url}/employees/register',
                                data=data, files=files)
        return response.json()

    def mark_attendance(self, image_path):
        """Chấm công"""
        files = {'image': open(image_path, 'rb')}
        response = requests.post(f'{self.base_url}/attendance/recognize',
                                files=files)
        return response.json()

    def get_today_attendance(self):
        """Danh sách chấm công hôm nay"""
        response = requests.get(f'{self.base_url}/attendance/today')
        return response.json()

    # === KHÁCH HÀNG ===

    def add_customer(self, name, email=None, phone=None, notes=None, image_path=None):
        """Thêm khách hàng mới"""
        # Tạo bản ghi
        data = {"name": name, "email": email, "phone": phone, "notes": notes}
        response = requests.post(f'{self.base_url}/customers', json=data)
        customer_id = response.json()['customer_id']

        # Upload ảnh nếu có
        if image_path:
            files = {'image': open(image_path, 'rb')}
            requests.post(f'{self.base_url}/customers/{customer_id}/upload-photo',
                         files=files)

        return customer_id

    def recognize_customer(self, image_path):
        """Nhận diện khách hàng"""
        files = {'image': open(image_path, 'rb')}
        response = requests.post(f'{self.base_url}/customers/recognize',
                                files=files)
        return response.json()

    def get_all_customers(self):
        """Danh sách tất cả khách hàng"""
        response = requests.get(f'{self.base_url}/customers')
        return response.json()


# === SỬ DỤNG ===

system = FaceRecognitionSystem()

# Đăng ký nhân viên
print("Đăng ký nhân viên...")
result = system.register_employee('NGUYEN_VAN_A', 'employee.jpg')
print(result)

# Chấm công
print("\nChấm công...")
result = system.mark_attendance('capture.jpg')
print(f"Nhận diện được: {result['recognized']} người")

# Thêm khách hàng
print("\nThêm khách hàng...")
customer_id = system.add_customer(
    name='NGUYEN_VAN_C',
    email='customer@example.com',
    phone='0912345678',
    notes='Khách VIP',
    image_path='customer.jpg'
)
print(f"Customer ID: {customer_id}")

# Nhận diện khách hàng
print("\nNhận diện khách hàng...")
result = system.recognize_customer('customer_photo.jpg')
if result['recognized'] > 0:
    for customer in result['customers']:
        print(f"- {customer['name']}: {customer['visit_count']} lượt ghé")
```

### Chạy Script

```bash
python your_script.py
```

---

## Xử Lý Sự Cố

### 1. Lỗi "No module named 'face_recognition'"

**Giải pháp:**
```bash
pip install face-recognition
```

### 2. Lỗi "dlib installation failed"

**Windows:**
1. Cài Visual Studio Build Tools
2. Cài CMake: `pip install cmake`
3. Thử lại: `pip install dlib`

**macOS:**
```bash
brew install cmake
pip install dlib
```

**Linux:**
```bash
sudo apt-get install cmake
sudo apt-get install libopenblas-dev liblapack-dev
pip install dlib
```

### 3. Webcam không hoạt động

- Kiểm tra quyền truy cập camera
- Đảm bảo không có ứng dụng khác đang sử dụng camera
- Thử với camera khác (camera USB)

### 4. Không nhận diện được khuôn mặt

**Nguyên nhân:**
- Ảnh quá tối/sáng
- Góc chụp không rõ khuôn mặt
- Khuôn mặt quá nhỏ trong ảnh

**Giải pháp:**
- Chụp ảnh với ánh sáng tốt
- Đảm bảo khuôn mặt chiếm ít nhất 30% ảnh
- Nhìn thẳng vào camera

### 5. Server không khởi động

**Kiểm tra:**
```bash
# Port 5000 có đang được sử dụng?
# Windows
netstat -ano | findstr :5000

# macOS/Linux
lsof -i :5000
```

**Giải pháp:** Thay đổi port trong file app:
```python
if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=8000)  # Đổi port
```

### 6. Database bị lỗi

**Reset database:**
```bash
# Backup database cũ
mv information.db information.db.backup

# Chạy lại app để tạo database mới
python app_improved.py
```

---

## Tính Năng Nâng Cao

### 1. Thay Đổi Ngưỡng Nhận Diện

Trong `app_improved.py`, tìm dòng:
```python
FACE_MATCH_THRESHOLD = 0.50
```

Điều chỉnh:
- Tăng (0.60, 0.70): Chính xác hơn nhưng khó nhận diện
- Giảm (0.40, 0.30): Dễ nhận diện nhưng kém chính xác

### 2. Deploy lên Server

**Sử dụng Gunicorn:**
```bash
gunicorn -w 4 -b 0.0.0.0:5000 app_improved:app
```

**Sử dụng Docker:**
```dockerfile
FROM python:3.8
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app_improved.py"]
```

### 3. Tích Hợp HTTPS

Sử dụng nginx hoặc Apache làm reverse proxy với SSL certificate.

---

## Best Practices

### 1. Tên File Ảnh
- Dùng tên có ý nghĩa: `NGUYEN_VAN_A.png`
- Tránh ký tự đặc biệt: `@`, `#`, `%`
- Dùng CHỮ HOA và gạch dưới

### 2. Chất Lượng Ảnh
- Độ phân giải tối thiểu: 640x480
- Format: JPG, PNG
- Kích thước file: < 5MB

### 3. Database Backup
```bash
# Backup hàng ngày
cp information.db backups/information_$(date +%Y%m%d).db
```

### 4. Security
- Không expose database trực tiếp
- Sử dụng HTTPS trong production
- Giới hạn upload file size
- Validate input data

---

## Câu Hỏi Thường Gặp (FAQ)

**Q: Có thể nhận diện nhiều người cùng lúc không?**
A: Có, hệ thống hỗ trợ nhận diện nhiều khuôn mặt trong cùng một ảnh.

**Q: Dữ liệu được lưu ở đâu?**
A: Tất cả dữ liệu được lưu trong file `information.db` (SQLite database).

**Q: Có thể export dữ liệu không?**
A: Có, bạn có thể sử dụng SQLite browser hoặc code Python để export sang CSV/Excel.

**Q: Hệ thống có hoạt động offline không?**
A: Có, hoàn toàn hoạt động offline sau khi cài đặt xong.

**Q: Cần bao nhiêu ảnh để đăng ký một người?**
A: Chỉ cần 1 ảnh rõ ràng. Tuy nhiên, 2-3 ảnh ở các góc độ khác nhau sẽ tốt hơn.

---

## Liên Hệ & Hỗ Trợ

- **Documentation:** Xem file `API_DOCUMENTATION.md`
- **Issues:** Báo lỗi qua GitHub Issues
- **Email:** support@example.com

---

**Chúc bạn sử dụng hệ thống thành công! 🎉**
