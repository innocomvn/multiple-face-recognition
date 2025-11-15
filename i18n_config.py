#!/usr/bin/env python3
"""
Internationalization (i18n) Configuration for FRAMS

This module provides basic i18n support for multiple languages.

Supported Languages:
- en: English (default)
- vi: Vietnamese

Usage:
    from i18n_config import get_text, set_language

    # Set language
    set_language('vi')

    # Get translated text
    print(get_text('welcome'))
"""

import json
import os

# Default language
DEFAULT_LANGUAGE = 'en'
current_language = DEFAULT_LANGUAGE

# Translation dictionaries
TRANSLATIONS = {
    'en': {
        # Common
        'welcome': 'Welcome to FRAMS',
        'success': 'Success',
        'error': 'Error',
        'loading': 'Loading...',
        'save': 'Save',
        'cancel': 'Cancel',
        'delete': 'Delete',
        'edit': 'Edit',
        'add': 'Add',
        'search': 'Search',
        'filter': 'Filter',
        'export': 'Export',
        'import': 'Import',
        'back': 'Back',
        'next': 'Next',
        'previous': 'Previous',
        'confirm': 'Confirm',

        # Attendance
        'attendance': 'Attendance',
        'mark_attendance': 'Mark Attendance',
        'attendance_marked': 'Attendance marked successfully',
        'already_marked': 'Attendance already marked today',
        'employee_recognized': 'Employee recognized',
        'employee_not_found': 'Employee not found',
        'no_face_detected': 'No face detected in image',

        # Customer
        'customer': 'Customer',
        'customers': 'Customers',
        'customer_recognized': 'Customer recognized',
        'new_customer': 'New Customer',
        'customer_visit': 'Customer Visit',
        'visit_count': 'Visit Count',
        'last_visit': 'Last Visit',

        # Employee
        'employee': 'Employee',
        'employees': 'Employees',
        'register_employee': 'Register Employee',
        'employee_registered': 'Employee registered successfully',
        'employee_name': 'Employee Name',

        # System
        'system_stats': 'System Statistics',
        'health_check': 'Health Check',
        'version': 'Version',
        'api_version': 'API Version',
        'database': 'Database',
        'status': 'Status',
        'online': 'Online',
        'offline': 'Offline',

        # Messages
        'upload_image': 'Upload Image',
        'take_photo': 'Take Photo',
        'processing': 'Processing...',
        'no_results': 'No results found',
        'invalid_image': 'Invalid image file',
        'image_too_large': 'Image file too large',
        'required_field': 'This field is required',

        # Navigation
        'home': 'Home',
        'dashboard': 'Dashboard',
        'reports': 'Reports',
        'settings': 'Settings',
        'logout': 'Logout',
        'login': 'Login',

        # Date/Time
        'today': 'Today',
        'yesterday': 'Yesterday',
        'this_week': 'This Week',
        'this_month': 'This Month',
        'date': 'Date',
        'time': 'Time',

        # Actions
        'view_details': 'View Details',
        'download': 'Download',
        'upload': 'Upload',
        'refresh': 'Refresh',
        'close': 'Close',
    },

    'vi': {
        # Common
        'welcome': 'Chào mừng đến với FRAMS',
        'success': 'Thành công',
        'error': 'Lỗi',
        'loading': 'Đang tải...',
        'save': 'Lưu',
        'cancel': 'Hủy',
        'delete': 'Xóa',
        'edit': 'Sửa',
        'add': 'Thêm',
        'search': 'Tìm kiếm',
        'filter': 'Lọc',
        'export': 'Xuất',
        'import': 'Nhập',
        'back': 'Quay lại',
        'next': 'Tiếp theo',
        'previous': 'Trước',
        'confirm': 'Xác nhận',

        # Attendance
        'attendance': 'Điểm danh',
        'mark_attendance': 'Chấm công',
        'attendance_marked': 'Đã chấm công thành công',
        'already_marked': 'Đã chấm công hôm nay',
        'employee_recognized': 'Nhận diện nhân viên',
        'employee_not_found': 'Không tìm thấy nhân viên',
        'no_face_detected': 'Không phát hiện khuôn mặt trong ảnh',

        # Customer
        'customer': 'Khách hàng',
        'customers': 'Khách hàng',
        'customer_recognized': 'Nhận diện khách hàng',
        'new_customer': 'Khách hàng mới',
        'customer_visit': 'Lượt ghé thăm',
        'visit_count': 'Số lần ghé',
        'last_visit': 'Lần ghé cuối',

        # Employee
        'employee': 'Nhân viên',
        'employees': 'Nhân viên',
        'register_employee': 'Đăng ký nhân viên',
        'employee_registered': 'Đã đăng ký nhân viên thành công',
        'employee_name': 'Tên nhân viên',

        # System
        'system_stats': 'Thống kê hệ thống',
        'health_check': 'Kiểm tra sức khỏe',
        'version': 'Phiên bản',
        'api_version': 'Phiên bản API',
        'database': 'Cơ sở dữ liệu',
        'status': 'Trạng thái',
        'online': 'Trực tuyến',
        'offline': 'Ngoại tuyến',

        # Messages
        'upload_image': 'Tải ảnh lên',
        'take_photo': 'Chụp ảnh',
        'processing': 'Đang xử lý...',
        'no_results': 'Không tìm thấy kết quả',
        'invalid_image': 'File ảnh không hợp lệ',
        'image_too_large': 'File ảnh quá lớn',
        'required_field': 'Trường này là bắt buộc',

        # Navigation
        'home': 'Trang chủ',
        'dashboard': 'Bảng điều khiển',
        'reports': 'Báo cáo',
        'settings': 'Cài đặt',
        'logout': 'Đăng xuất',
        'login': 'Đăng nhập',

        # Date/Time
        'today': 'Hôm nay',
        'yesterday': 'Hôm qua',
        'this_week': 'Tuần này',
        'this_month': 'Tháng này',
        'date': 'Ngày',
        'time': 'Giờ',

        # Actions
        'view_details': 'Xem chi tiết',
        'download': 'Tải xuống',
        'upload': 'Tải lên',
        'refresh': 'Làm mới',
        'close': 'Đóng',
    }
}


def set_language(lang_code):
    """
    Set the current language

    Args:
        lang_code (str): Language code ('en', 'vi', etc.)
    """
    global current_language
    if lang_code in TRANSLATIONS:
        current_language = lang_code
    else:
        current_language = DEFAULT_LANGUAGE


def get_language():
    """Get current language code"""
    return current_language


def get_text(key, lang=None):
    """
    Get translated text for a key

    Args:
        key (str): Translation key
        lang (str, optional): Language code. Uses current language if not specified.

    Returns:
        str: Translated text, or the key itself if translation not found

    Example:
        >>> get_text('welcome')
        'Welcome to FRAMS'
        >>> get_text('welcome', 'vi')
        'Chào mừng đến với FRAMS'
    """
    lang_code = lang or current_language

    if lang_code in TRANSLATIONS and key in TRANSLATIONS[lang_code]:
        return TRANSLATIONS[lang_code][key]
    elif key in TRANSLATIONS[DEFAULT_LANGUAGE]:
        return TRANSLATIONS[DEFAULT_LANGUAGE][key]
    else:
        return key


def get_all_translations(lang=None):
    """
    Get all translations for a language

    Args:
        lang (str, optional): Language code. Uses current language if not specified.

    Returns:
        dict: All translations for the language
    """
    lang_code = lang or current_language
    return TRANSLATIONS.get(lang_code, TRANSLATIONS[DEFAULT_LANGUAGE])


def get_supported_languages():
    """
    Get list of supported language codes

    Returns:
        list: List of language codes
    """
    return list(TRANSLATIONS.keys())


# Flask integration helper
def init_i18n(app):
    """
    Initialize i18n for Flask app

    Args:
        app: Flask application instance

    Example:
        from flask import Flask
        from i18n_config import init_i18n

        app = Flask(__name__)
        init_i18n(app)
    """
    from flask import request, session

    @app.before_request
    def before_request():
        """Set language based on request or session"""
        # Check session
        if 'language' in session:
            set_language(session['language'])
        # Check Accept-Language header
        elif request.accept_languages:
            best_match = request.accept_languages.best_match(get_supported_languages())
            if best_match:
                set_language(best_match)

    # Add translation function to Jinja2
    app.jinja_env.globals.update(
        _=get_text,
        get_text=get_text,
        current_language=get_language
    )


# Example usage
if __name__ == '__main__':
    print("=== FRAMS i18n Demo ===\n")

    # English
    print("English:")
    set_language('en')
    print(f"  {get_text('welcome')}")
    print(f"  {get_text('mark_attendance')}")
    print(f"  {get_text('customer_recognized')}")

    # Vietnamese
    print("\nVietnamese:")
    set_language('vi')
    print(f"  {get_text('welcome')}")
    print(f"  {get_text('mark_attendance')}")
    print(f"  {get_text('customer_recognized')}")

    print(f"\nSupported languages: {get_supported_languages()}")
