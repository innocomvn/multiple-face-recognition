# Changelog

All notable changes to this project will be documented in this file.

## [2.0.0] - 2025-11-15

### Added ✨
- **RESTful API** với đầy đủ endpoints cho attendance và customer management
- **Customer Recognition System** - Nhận diện và quản lý khách hàng
- **Modern Frontend Pages:**
  - `attendance_tracking.html` - Giao diện chấm công
  - `customer_recognition.html` - Giao diện nhận diện khách hàng
  - `customers.html` - Quản lý khách hàng với DataTables
  - `main_improved.html` - Trang chủ mới với statistics
- **Database Tables:**
  - `Customers` - Lưu thông tin khách hàng
  - `CustomerVisits` - Theo dõi lượt ghé thăm
- **API Endpoints:**
  - `/api/attendance/*` - Attendance operations
  - `/api/customers/*` - Customer CRUD operations
  - `/api/employees/*` - Employee management
- **Documentation:**
  - `API_DOCUMENTATION.md` - Tài liệu API đầy đủ
  - `SETUP_GUIDE.md` - Hướng dẫn cài đặt chi tiết
  - `QUICKSTART.md` - Quick start guide
  - `README_NEW.md` - README toàn diện
- **Development Tools:**
  - `test_api.py` - Script test API
  - `start.sh` - Quick start script (Linux/macOS)
  - `start.bat` - Quick start script (Windows)
  - `Dockerfile` - Docker support
  - `docker-compose.yml` - Docker Compose config
  - `.gitignore` - Git ignore rules
  - `.env.example` - Environment variables template

### Changed 🔧
- Tách route `/` thành landing page riêng
- Di chuyển webcam recognition sang `/recognize-webcam`
- Cải thiện error handling toàn bộ API
- Thêm CORS support với Flask-CORS
- Cập nhật `requirements.txt` với dependencies mới

### Fixed 🐛
- Fix missing imports (`json`, `pandas`, `session`)
- Fix hardcoded Windows path trong training images
- Thêm secure secret key generation
- Fix database initialization timing
- Sửa lỗi không tạo thư mục tự động

### Security 🔒
- Sử dụng `secrets.token_hex()` cho secret key
- Thêm `.gitignore` để bảo vệ credentials
- Environment variables support
- Session configuration improvements

### Performance ⚡
- Optimize face encoding loading
- Giảm memory usage với lazy loading
- Cải thiện response time

## [1.0.0] - Initial Release

### Features
- Basic face recognition with webcam
- Employee attendance tracking
- SQLite database storage
- Simple web interface
- CSV export

---

## Upcoming Features 🔮

### [2.1.0] - Planned
- [ ] Authentication & Authorization
- [ ] Role-based access control (Admin/User)
- [ ] Email notifications
- [ ] Advanced analytics dashboard
- [ ] Export to Excel/PDF
- [ ] Multi-language support
- [ ] Dark mode UI
- [ ] Mobile app (React Native/Flutter)
- [ ] Real-time notifications (WebSocket)
- [ ] Bulk import employees
- [ ] Face mask detection
- [ ] Temperature screening integration

### [3.0.0] - Future
- [ ] Cloud deployment templates (AWS, GCP, Azure)
- [ ] Kubernetes support
- [ ] Redis caching
- [ ] PostgreSQL support
- [ ] GraphQL API
- [ ] Machine learning model updates
- [ ] Face anti-spoofing
- [ ] Multi-camera support
- [ ] Integration với payroll systems

---

**Note:** Dự án tuân theo [Semantic Versioning](https://semver.org/).
