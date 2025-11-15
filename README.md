# 🎯 FRAMS 2.0 - Face Recognition Attendance & Customer Management System

[![Python](https://img.shields.io/badge/Python-3.8+-blue.svg)](https://www.python.org/)
[![Flask](https://img.shields.io/badge/Flask-1.1.2-green.svg)](https://flask.palletsprojects.com/)
[![License](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![AI](https://img.shields.io/badge/AI-Face_Recognition-ff69b4)](https://github.com/ageitgey/face_recognition)

> **Hệ thống nhận diện khuôn mặt AI toàn diện** - Giải pháp chấm công thông minh và quản lý khách hàng tự động

![Version](https://img.shields.io/badge/Version-2.0.0-brightgreen)
![Status](https://img.shields.io/badge/Status-Production_Ready-success)

---

## ✨ What's New in Version 2.0

🎉 **Major Update** - Hệ thống được nâng cấp hoàn toàn với nhiều tính năng mới!

- ✅ **RESTful API** - 15+ endpoints cho tích hợp
- ✅ **Customer Recognition** - Quản lý khách hàng thông minh
- ✅ **Modern UI** - Giao diện mới hiện đại
- ✅ **Docker Support** - Deploy dễ dàng
- ✅ **Comprehensive Docs** - Tài liệu đầy đủ

---

## 🚀 Quick Start - 3 Phút!

### **Linux/macOS:**
```bash
./start.sh
```

### **Windows:**
```batch
start.bat
```

### **Docker:**
```bash
docker-compose up -d
```

**Truy cập:** http://localhost:5000

📘 **Chi tiết:** [QUICKSTART.md](QUICKSTART.md)

---

## ✨ Features

### 🏢 Chấm Công Nhân Viên
- ✅ Nhận diện khuôn mặt tự động (99%+ accuracy)
- ✅ Ghi nhận thời gian chính xác
- ✅ Hỗ trợ nhiều khuôn mặt cùng lúc
- ✅ Xem lịch sử theo ngày/tháng/nhân viên
- ✅ Export CSV & dashboard

### 👥 Quản Lý Khách Hàng (NEW!)
- ✅ Nhận diện khách hàng returning
- ✅ Theo dõi lượt ghé thăm
- ✅ Lưu thông tin (email, phone, notes)
- ✅ CRUD operations đầy đủ
- ✅ Lịch sử chi tiết

### 🔌 RESTful API (NEW!)
- ✅ 15+ endpoints
- ✅ CORS enabled
- ✅ JSON responses
- ✅ File upload support
- ✅ Comprehensive error handling

### 🎨 Modern Web Interface
- ✅ Responsive design (Bootstrap 4)
- ✅ Real-time statistics
- ✅ Upload + Camera capture
- ✅ Beautiful UI/UX
- ✅ 4 specialized pages

---

## 📖 Documentation

| Document | Description |
|----------|-------------|
| [QUICKSTART.md](QUICKSTART.md) | Bắt đầu trong 3 phút |
| [SETUP_GUIDE.md](SETUP_GUIDE.md) | Hướng dẫn cài đặt chi tiết |
| [API_DOCUMENTATION.md](API_DOCUMENTATION.md) | API reference đầy đủ |
| [CHANGELOG.md](CHANGELOG.md) | Lịch sử thay đổi |

---

## 🌐 Pages

| URL | Feature |
|-----|---------|
| `/` | 🏠 Landing page |
| `/attendance-web` | 👨‍💼 Chấm công |
| `/customer-recognition` | 👥 Nhận diện khách hàng |
| `/customers-web` | 📊 Quản lý |

---

## 🔌 API Examples

### Chấm công
```python
import requests

files = {'image': open('photo.jpg', 'rb')}
response = requests.post('http://localhost:5000/api/attendance/recognize', files=files)

print(response.json())
# Output: {"success": true, "recognized": 2, "results": [...]}
```

### Thêm khách hàng
```python
data = {"name": "CUSTOMER_A", "email": "test@example.com"}
response = requests.post('http://localhost:5000/api/customers', json=data)
customer_id = response.json()['customer_id']

# Upload photo
files = {'image': open('customer.jpg', 'rb')}
requests.post(f'http://localhost:5000/api/customers/{customer_id}/upload-photo', files=files)
```

📚 **Full API Docs:** [API_DOCUMENTATION.md](API_DOCUMENTATION.md)

---

## 🛠️ Tech Stack

- **Backend:** Python 3.8+, Flask, face_recognition, OpenCV, SQLite
- **Frontend:** HTML5, CSS3, Bootstrap 4, jQuery
- **AI/ML:** dlib, face_recognition, numpy
- **DevOps:** Docker, Docker Compose

---

## 📂 Project Structure

```
├── app_improved.py              # Main app (v2.0)
├── templates/                   # HTML templates
│   ├── main_improved.html       # Landing
│   ├── attendance_tracking.html # Attendance
│   ├── customer_recognition.html# Customer
│   └── customers.html           # Management
├── API_DOCUMENTATION.md         # API docs
├── SETUP_GUIDE.md              # Setup guide
├── QUICKSTART.md               # Quick start
├── start.sh / start.bat        # Launchers
├── test_api.py                 # API tests
├── Dockerfile                  # Docker
└── docker-compose.yml          # Compose
```

---

## 🧪 Testing

```bash
# Test all API endpoints
python test_api.py

# Test specific endpoint
curl http://localhost:5000/api/health
```

---

## 🐳 Docker

```bash
# Build and run
docker-compose up -d

# View logs
docker-compose logs -f

# Stop
docker-compose down
```

---

## 📋 Requirements

- Python 3.8+
- 4GB RAM minimum
- Webcam (optional)
- Windows/macOS/Linux

---

## 🔧 Installation

### Method 1: Auto Install
```bash
./start.sh  # or start.bat on Windows
```

### Method 2: Manual
```bash
pip install -r requirements.txt
python app_improved.py
```

### Method 3: Docker
```bash
docker-compose up -d
```

📘 **Detailed guide:** [SETUP_GUIDE.md](SETUP_GUIDE.md)

---

## 🎓 Use Cases

- ✅ **Doanh nghiệp:** Chấm công nhân viên
- ✅ **Retail:** Nhận diện khách VIP
- ✅ **Events:** Check-in tự động
- ✅ **Hospitality:** Personalized service

---

## 🐛 Troubleshooting

**dlib installation error (Windows):**
```bash
# Install Visual Studio Build Tools first
pip install cmake
pip install dlib
```

**Port already in use:**
```bash
# Change port in app_improved.py
app.run(port=8000)  # Line ~750
```

📚 **More solutions:** [SETUP_GUIDE.md#troubleshooting](SETUP_GUIDE.md)

---

## 🔮 Roadmap

### v2.1 (Next)
- [ ] Authentication & Authorization
- [ ] Email notifications
- [ ] Advanced analytics
- [ ] Excel/PDF export

### v3.0 (Future)
- [ ] Mobile app
- [ ] Real-time WebSocket
- [ ] Face mask detection
- [ ] Cloud deployment

---

## 🤝 Contributing

1. Fork the project
2. Create feature branch (`git checkout -b feature/Amazing`)
3. Commit changes (`git commit -m 'Add Amazing'`)
4. Push to branch (`git push origin feature/Amazing`)
5. Open Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 👨‍💻 Authors

- **Original FRAMS** - v1.0
- **Enhanced v2.0** - API & Customer features

---

## 🙏 Acknowledgments

- [face_recognition](https://github.com/ageitgey/face_recognition) - Adam Geitgey
- [OpenCV](https://opencv.org/)
- [Flask](https://flask.palletsprojects.com/)
- [Bootstrap](https://getbootstrap.com/)

---

## 📞 Support

- 📖 **Docs:** [Documentation](docs/)
- 🐛 **Issues:** [GitHub Issues](issues/)
- 📧 **Email:** support@example.com

---

## ⭐ Star This Repo!

If you find this useful, please give it a star! ⭐

---

<p align="center">
  <strong>Made with ❤️ using Python & AI</strong>
</p>

<p align="center">
  <a href="QUICKSTART.md">Get Started</a> •
  <a href="API_DOCUMENTATION.md">API Docs</a> •
  <a href="SETUP_GUIDE.md">Setup Guide</a>
</p>
