# API Documentation - Face Recognition System

## Tổng Quan (Overview)

Hệ thống API RESTful cho nhận diện khuôn mặt, hỗ trợ:
- **Chấm công nhân viên** (Employee Attendance)
- **Nhận diện khách hàng** (Customer Recognition)
- **Quản lý thông tin** (Data Management)

**Base URL:** `http://localhost:5000/api`

---

## 1. API Chấm Công Nhân Viên (Attendance API)

### 1.1. Nhận Diện & Chấm Công

**Endpoint:** `POST /api/attendance/recognize`

**Mô tả:** Upload ảnh để nhận diện khuôn mặt nhân viên và tự động chấm công

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body:
  - `image` (file): Ảnh chứa khuôn mặt (JPG, PNG)

**Response Success (200):**
```json
{
  "success": true,
  "total_faces": 2,
  "recognized": 1,
  "results": [
    {
      "name": "NGUYEN_VAN_A",
      "confidence": 0.87,
      "already_marked": false
    }
  ]
}
```

**Response Error (400/404/500):**
```json
{
  "error": "Error message"
}
```

**Ví dụ cURL:**
```bash
curl -X POST http://localhost:5000/api/attendance/recognize \
  -F "image=@photo.jpg"
```

**Ví dụ Python:**
```python
import requests

files = {'image': open('photo.jpg', 'rb')}
response = requests.post('http://localhost:5000/api/attendance/recognize', files=files)
print(response.json())
```

**Ví dụ JavaScript:**
```javascript
const formData = new FormData();
formData.append('image', fileInput.files[0]);

fetch('http://localhost:5000/api/attendance/recognize', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log(data));
```

---

### 1.2. Lấy Danh Sách Chấm Công Hôm Nay

**Endpoint:** `GET /api/attendance/today`

**Mô tả:** Lấy danh sách tất cả nhân viên đã chấm công hôm nay

**Response:**
```json
{
  "success": true,
  "date": "2025-11-14",
  "count": 5,
  "attendance": [
    {
      "NAME": "NGUYEN_VAN_A",
      "Time": "08:30:15",
      "Date": "2025-11-14"
    },
    {
      "NAME": "TRAN_THI_B",
      "Time": "08:45:22",
      "Date": "2025-11-14"
    }
  ]
}
```

**Ví dụ cURL:**
```bash
curl http://localhost:5000/api/attendance/today
```

---

### 1.3. Lấy Toàn Bộ Lịch Sử Chấm Công

**Endpoint:** `GET /api/attendance/all`

**Mô tả:** Lấy toàn bộ lịch sử chấm công của tất cả nhân viên

**Response:**
```json
{
  "success": true,
  "count": 150,
  "attendance": [
    {
      "NAME": "NGUYEN_VAN_A",
      "Time": "08:30:15",
      "Date": "2025-11-14"
    }
  ]
}
```

---

### 1.4. Lấy Lịch Sử Chấm Công Của Nhân Viên

**Endpoint:** `GET /api/attendance/employee/<name>`

**Mô tả:** Lấy lịch sử chấm công của một nhân viên cụ thể

**Parameters:**
- `name` (string): Tên nhân viên

**Response:**
```json
{
  "success": true,
  "employee": "NGUYEN_VAN_A",
  "count": 25,
  "attendance": [
    {
      "Time": "08:30:15",
      "Date": "2025-11-14"
    },
    {
      "Time": "08:25:10",
      "Date": "2025-11-13"
    }
  ]
}
```

**Ví dụ cURL:**
```bash
curl http://localhost:5000/api/attendance/employee/NGUYEN_VAN_A
```

---

## 2. API Nhận Diện Khách Hàng (Customer Recognition API)

### 2.1. Nhận Diện Khách Hàng

**Endpoint:** `POST /api/customers/recognize`

**Mô tả:** Upload ảnh để nhận diện khách hàng và ghi nhận lượt ghé thăm

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body:
  - `image` (file): Ảnh chứa khuôn mặt

**Response:**
```json
{
  "success": true,
  "total_faces": 1,
  "recognized": 1,
  "customers": [
    {
      "name": "NGUYEN_VAN_C",
      "confidence": 0.92,
      "email": "customer@example.com",
      "phone": "0912345678",
      "visit_count": 5,
      "last_visit": "2025-11-14",
      "notes": "Khách hàng VIP"
    }
  ]
}
```

**Ví dụ Python:**
```python
import requests

files = {'image': open('customer_photo.jpg', 'rb')}
response = requests.post('http://localhost:5000/api/customers/recognize', files=files)
data = response.json()

if data['success'] and data['recognized'] > 0:
    for customer in data['customers']:
        print(f"Khách hàng: {customer['name']}")
        print(f"Số lần ghé: {customer['visit_count']}")
```

---

### 2.2. Lấy Danh Sách Khách Hàng

**Endpoint:** `GET /api/customers`

**Mô tả:** Lấy danh sách tất cả khách hàng

**Response:**
```json
{
  "success": true,
  "count": 50,
  "customers": [
    {
      "ID": 1,
      "Name": "NGUYEN_VAN_C",
      "Email": "customer@example.com",
      "Phone": "0912345678",
      "LastVisit": "2025-11-14",
      "VisitCount": 5,
      "Notes": "Khách hàng VIP"
    }
  ]
}
```

---

### 2.3. Thêm Khách Hàng Mới

**Endpoint:** `POST /api/customers`

**Mô tả:** Tạo mới một khách hàng

**Request:**
- Method: `POST`
- Content-Type: `application/json`
- Body:
```json
{
  "name": "NGUYEN_VAN_C",
  "email": "customer@example.com",
  "phone": "0912345678",
  "notes": "Khách hàng VIP"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Customer created successfully",
  "customer_id": 10
}
```

**Ví dụ Python:**
```python
import requests

data = {
    "name": "NGUYEN_VAN_C",
    "email": "customer@example.com",
    "phone": "0912345678",
    "notes": "Khách hàng thân thiết"
}

response = requests.post(
    'http://localhost:5000/api/customers',
    json=data
)
print(response.json())
```

---

### 2.4. Lấy Thông Tin Khách Hàng

**Endpoint:** `GET /api/customers/<customer_id>`

**Mô tả:** Lấy thông tin chi tiết của một khách hàng

**Response:**
```json
{
  "success": true,
  "customer": {
    "ID": 1,
    "Name": "NGUYEN_VAN_C",
    "Email": "customer@example.com",
    "Phone": "0912345678",
    "LastVisit": "2025-11-14",
    "VisitCount": 5,
    "Notes": "Khách hàng VIP"
  }
}
```

---

### 2.5. Cập Nhật Thông Tin Khách Hàng

**Endpoint:** `PUT /api/customers/<customer_id>`

**Mô tả:** Cập nhật thông tin khách hàng

**Request:**
```json
{
  "name": "NGUYEN_VAN_C",
  "email": "new_email@example.com",
  "phone": "0987654321",
  "notes": "Updated notes"
}
```

**Response:**
```json
{
  "success": true,
  "message": "Customer updated successfully"
}
```

---

### 2.6. Xóa Khách Hàng

**Endpoint:** `DELETE /api/customers/<customer_id>`

**Mô tả:** Xóa khách hàng khỏi hệ thống

**Response:**
```json
{
  "success": true,
  "message": "Customer deleted successfully"
}
```

**Ví dụ Python:**
```python
import requests

customer_id = 10
response = requests.delete(f'http://localhost:5000/api/customers/{customer_id}')
print(response.json())
```

---

### 2.7. Upload Ảnh Khách Hàng

**Endpoint:** `POST /api/customers/<customer_id>/upload-photo`

**Mô tả:** Upload ảnh khuôn mặt cho khách hàng

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body:
  - `image` (file): Ảnh khuôn mặt

**Response:**
```json
{
  "success": true,
  "message": "Photo uploaded successfully"
}
```

**Ví dụ Python:**
```python
import requests

customer_id = 10
files = {'image': open('customer_face.jpg', 'rb')}
response = requests.post(
    f'http://localhost:5000/api/customers/{customer_id}/upload-photo',
    files=files
)
print(response.json())
```

---

### 2.8. Lấy Lịch Sử Ghé Thăm

**Endpoint:** `GET /api/customers/<name>/visits`

**Mô tả:** Lấy lịch sử ghé thăm của khách hàng

**Response:**
```json
{
  "success": true,
  "customer": "NGUYEN_VAN_C",
  "count": 5,
  "visits": [
    {
      "ID": 1,
      "CustomerName": "NGUYEN_VAN_C",
      "VisitTime": "14:30:00",
      "VisitDate": "2025-11-14"
    }
  ]
}
```

---

## 3. API Quản Lý Nhân Viên (Employee Management API)

### 3.1. Đăng Ký Nhân Viên Mới

**Endpoint:** `POST /api/employees/register`

**Mô tả:** Đăng ký nhân viên mới với ảnh khuôn mặt

**Request:**
- Method: `POST`
- Content-Type: `multipart/form-data`
- Body:
  - `name` (string): Tên nhân viên
  - `image` (file): Ảnh khuôn mặt

**Response:**
```json
{
  "success": true,
  "message": "Employee NGUYEN_VAN_A registered successfully"
}
```

**Ví dụ Python:**
```python
import requests

data = {'name': 'NGUYEN_VAN_A'}
files = {'image': open('employee_face.jpg', 'rb')}

response = requests.post(
    'http://localhost:5000/api/employees/register',
    data=data,
    files=files
)
print(response.json())
```

**Ví dụ cURL:**
```bash
curl -X POST http://localhost:5000/api/employees/register \
  -F "name=NGUYEN_VAN_A" \
  -F "image=@employee_face.jpg"
```

---

### 3.2. Lấy Danh Sách Nhân Viên

**Endpoint:** `GET /api/employees`

**Mô tả:** Lấy danh sách tất cả nhân viên đã đăng ký

**Response:**
```json
{
  "success": true,
  "count": 10,
  "employees": [
    "NGUYEN_VAN_A",
    "TRAN_THI_B",
    "LE_VAN_C"
  ]
}
```

---

## 4. Ví Dụ Tích Hợp (Integration Examples)

### 4.1. Python - Quy Trình Hoàn Chỉnh Chấm Công

```python
import requests
from datetime import date

class AttendanceSystem:
    def __init__(self, base_url='http://localhost:5000/api'):
        self.base_url = base_url

    def register_employee(self, name, image_path):
        """Đăng ký nhân viên mới"""
        data = {'name': name}
        files = {'image': open(image_path, 'rb')}

        response = requests.post(
            f'{self.base_url}/employees/register',
            data=data,
            files=files
        )
        return response.json()

    def mark_attendance(self, image_path):
        """Chấm công bằng ảnh"""
        files = {'image': open(image_path, 'rb')}

        response = requests.post(
            f'{self.base_url}/attendance/recognize',
            files=files
        )
        return response.json()

    def get_today_attendance(self):
        """Lấy danh sách chấm công hôm nay"""
        response = requests.get(f'{self.base_url}/attendance/today')
        return response.json()

# Sử dụng
system = AttendanceSystem()

# Đăng ký nhân viên
result = system.register_employee('NGUYEN_VAN_A', 'employee.jpg')
print(result)

# Chấm công
result = system.mark_attendance('capture.jpg')
print(f"Đã nhận diện: {result['recognized']} người")

# Xem danh sách hôm nay
attendance = system.get_today_attendance()
print(f"Hôm nay có {attendance['count']} người đã chấm công")
```

### 4.2. JavaScript/Node.js - Quản Lý Khách Hàng

```javascript
const axios = require('axios');
const FormData = require('form-data');
const fs = require('fs');

const API_BASE = 'http://localhost:5000/api';

// Thêm khách hàng mới
async function addCustomer(customerData, imagePath) {
  // Tạo khách hàng
  const response = await axios.post(`${API_BASE}/customers`, customerData);
  const customerId = response.data.customer_id;

  // Upload ảnh
  const formData = new FormData();
  formData.append('image', fs.createReadStream(imagePath));

  await axios.post(
    `${API_BASE}/customers/${customerId}/upload-photo`,
    formData,
    { headers: formData.getHeaders() }
  );

  return customerId;
}

// Nhận diện khách hàng
async function recognizeCustomer(imagePath) {
  const formData = new FormData();
  formData.append('image', fs.createReadStream(imagePath));

  const response = await axios.post(
    `${API_BASE}/customers/recognize`,
    formData,
    { headers: formData.getHeaders() }
  );

  return response.data;
}

// Sử dụng
(async () => {
  // Thêm khách hàng
  const customerId = await addCustomer({
    name: 'NGUYEN_VAN_C',
    email: 'customer@example.com',
    phone: '0912345678',
    notes: 'Khách hàng VIP'
  }, 'customer_face.jpg');

  console.log(`Customer ID: ${customerId}`);

  // Nhận diện
  const result = await recognizeCustomer('camera_capture.jpg');
  if (result.recognized > 0) {
    result.customers.forEach(customer => {
      console.log(`Khách hàng: ${customer.name}`);
      console.log(`Số lần ghé: ${customer.visit_count}`);
    });
  }
})();
```

---

## 5. Mã Lỗi (Error Codes)

| HTTP Code | Ý nghĩa |
|-----------|---------|
| 200 | Success - Thành công |
| 201 | Created - Tạo mới thành công |
| 400 | Bad Request - Thiếu thông tin hoặc sai format |
| 404 | Not Found - Không tìm thấy dữ liệu |
| 500 | Internal Server Error - Lỗi server |

---

## 6. Lưu Ý Quan Trọng

### 6.1. Định Dạng Ảnh
- Hỗ trợ: JPG, JPEG, PNG
- Kích thước tối đa: 10MB
- Nên có khuôn mặt rõ ràng, ánh sáng tốt

### 6.2. Tên (Name)
- Nên dùng CHỮ HOA và dấu gạch dưới
- Ví dụ: `NGUYEN_VAN_A`, `TRAN_THI_B`
- Tránh ký tự đặc biệt

### 6.3. Ngưỡng Nhận Diện
- Ngưỡng mặc định: 0.50
- Độ tin cậy < 0.50: Không nhận diện được
- Độ tin cậy >= 0.50: Nhận diện thành công

### 6.4. Chấm Công
- Mỗi nhân viên chỉ được chấm công 1 lần/ngày
- Tự động ghi nhận thời gian chấm công

### 6.5. CORS
- API hỗ trợ CORS cho frontend
- Có thể gọi từ bất kỳ domain nào

---

## 7. Hỗ Trợ & Liên Hệ

Nếu gặp vấn đề, vui lòng kiểm tra:
1. Server đang chạy tại `http://localhost:5000`
2. Database đã được khởi tạo
3. Thư mục `Training images` và `Customer images` tồn tại
4. Dependencies đã được cài đặt đầy đủ

---

**Version:** 1.0
**Last Updated:** 2025-11-14
