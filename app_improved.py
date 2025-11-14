from flask import Flask, render_template, request, jsonify, session
from flask_cors import CORS
import cv2
import numpy as np
import face_recognition
import os
from datetime import datetime
from datetime import date
import sqlite3
import json
import pandas as pd
import base64
from werkzeug.security import generate_password_hash, check_password_hash
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # Generate secure secret key
CORS(app)  # Enable CORS for API access

# Configuration
TRAINING_IMAGES_PATH = 'Training images'
CUSTOMER_IMAGES_PATH = 'Customer images'
ATTENDANCE_DB = 'information.db'
FACE_MATCH_THRESHOLD = 0.50

# Ensure directories exist
os.makedirs(TRAINING_IMAGES_PATH, exist_ok=True)
os.makedirs(CUSTOMER_IMAGES_PATH, exist_ok=True)

# ============================================================================
# DATABASE INITIALIZATION
# ============================================================================

def init_databases():
    """Initialize all required databases"""
    # Attendance database
    conn = sqlite3.connect(ATTENDANCE_DB)
    conn.execute('''CREATE TABLE IF NOT EXISTS Attendance
                    (NAME TEXT NOT NULL,
                     Time TEXT NOT NULL,
                     Date TEXT NOT NULL)''')

    # Customer database
    conn.execute('''CREATE TABLE IF NOT EXISTS Customers
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                     Name TEXT NOT NULL,
                     Email TEXT,
                     Phone TEXT,
                     LastVisit TEXT,
                     VisitCount INTEGER DEFAULT 0,
                     Notes TEXT)''')

    # Customer visits tracking
    conn.execute('''CREATE TABLE IF NOT EXISTS CustomerVisits
                    (ID INTEGER PRIMARY KEY AUTOINCREMENT,
                     CustomerName TEXT NOT NULL,
                     VisitTime TEXT NOT NULL,
                     VisitDate TEXT NOT NULL)''')

    conn.commit()
    conn.close()

init_databases()

# ============================================================================
# HELPER FUNCTIONS
# ============================================================================

def load_face_encodings(image_path):
    """Load and encode faces from a directory"""
    images = []
    class_names = []

    if not os.path.exists(image_path):
        return [], []

    file_list = os.listdir(image_path)

    for filename in file_list:
        if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
            img_path = os.path.join(image_path, filename)
            img = cv2.imread(img_path)
            if img is not None:
                images.append(img)
                class_names.append(os.path.splitext(filename)[0])

    encode_list = []
    for img in images:
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        encodings = face_recognition.face_encodings(img_rgb)
        if len(encodings) > 0:
            encode_list.append(encodings[0])
        else:
            print(f"Warning: No face found in image")

    return encode_list, class_names

def recognize_face_from_image(image, known_encodings, known_names):
    """Recognize faces in an image and return results"""
    # Resize for faster processing
    small_image = cv2.resize(image, (0, 0), None, 0.25, 0.25)
    rgb_image = cv2.cvtColor(small_image, cv2.COLOR_BGR2RGB)

    face_locations = face_recognition.face_locations(rgb_image)
    face_encodings = face_recognition.face_encodings(rgb_image, face_locations)

    results = []
    for face_encoding, face_location in zip(face_encodings, face_locations):
        matches = face_recognition.compare_faces(known_encodings, face_encoding)
        face_distances = face_recognition.face_distance(known_encodings, face_encoding)

        if len(face_distances) > 0:
            best_match_index = np.argmin(face_distances)

            if face_distances[best_match_index] < FACE_MATCH_THRESHOLD:
                name = known_names[best_match_index]
                confidence = 1 - face_distances[best_match_index]
            else:
                name = "Unknown"
                confidence = 0
        else:
            name = "Unknown"
            confidence = 0

        # Scale face location back to original size
        y1, x2, y2, x1 = face_location
        y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4

        results.append({
            'name': name,
            'confidence': float(confidence),
            'location': {'x1': int(x1), 'y1': int(y1), 'x2': int(x2), 'y2': int(y2)}
        })

    return results

def mark_attendance(name):
    """Mark attendance for an employee"""
    now = datetime.now()
    time_str = now.strftime('%H:%M:%S')
    today = date.today()

    conn = sqlite3.connect(ATTENDANCE_DB)

    # Check if already marked today
    cursor = conn.execute(
        "SELECT * FROM Attendance WHERE NAME=? AND Date=?",
        (name, str(today))
    )

    if cursor.fetchone() is None:
        conn.execute(
            "INSERT INTO Attendance (NAME, Time, Date) VALUES (?, ?, ?)",
            (name, time_str, str(today))
        )
        conn.commit()
        conn.close()
        return True

    conn.close()
    return False

def mark_customer_visit(name):
    """Mark customer visit and update customer record"""
    now = datetime.now()
    time_str = now.strftime('%H:%M:%S')
    today = date.today()

    conn = sqlite3.connect(ATTENDANCE_DB)

    # Record visit
    conn.execute(
        "INSERT INTO CustomerVisits (CustomerName, VisitTime, VisitDate) VALUES (?, ?, ?)",
        (name, time_str, str(today))
    )

    # Update customer record
    cursor = conn.execute("SELECT * FROM Customers WHERE Name=?", (name,))
    customer = cursor.fetchone()

    if customer:
        visit_count = customer[5] + 1
        conn.execute(
            "UPDATE Customers SET LastVisit=?, VisitCount=? WHERE Name=?",
            (str(today), visit_count, name)
        )

    conn.commit()
    conn.close()

# ============================================================================
# API ENDPOINTS - ATTENDANCE SYSTEM
# ============================================================================

@app.route('/api/attendance/recognize', methods=['POST'])
def api_recognize_attendance():
    """API endpoint to recognize face and mark attendance from uploaded image"""
    try:
        # Get image from request
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        file = request.files['image']

        # Read image
        image_bytes = file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            return jsonify({'error': 'Invalid image'}), 400

        # Load known faces
        known_encodings, known_names = load_face_encodings(TRAINING_IMAGES_PATH)

        if len(known_encodings) == 0:
            return jsonify({'error': 'No registered employees found'}), 404

        # Recognize faces
        results = recognize_face_from_image(image, known_encodings, known_names)

        # Mark attendance for recognized faces
        attendance_marked = []
        for result in results:
            if result['name'] != "Unknown":
                is_new = mark_attendance(result['name'])
                attendance_marked.append({
                    'name': result['name'],
                    'confidence': result['confidence'],
                    'already_marked': not is_new
                })

        return jsonify({
            'success': True,
            'total_faces': len(results),
            'recognized': len(attendance_marked),
            'results': attendance_marked
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/attendance/today', methods=['GET'])
def api_get_today_attendance():
    """Get today's attendance records"""
    try:
        today = date.today()
        conn = sqlite3.connect(ATTENDANCE_DB)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            "SELECT DISTINCT NAME, Time, Date FROM Attendance WHERE Date=? ORDER BY Time",
            (str(today),)
        )
        rows = cursor.fetchall()
        conn.close()

        attendance_list = [dict(row) for row in rows]

        return jsonify({
            'success': True,
            'date': str(today),
            'count': len(attendance_list),
            'attendance': attendance_list
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/attendance/all', methods=['GET'])
def api_get_all_attendance():
    """Get all attendance records"""
    try:
        conn = sqlite3.connect(ATTENDANCE_DB)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            "SELECT DISTINCT NAME, Time, Date FROM Attendance ORDER BY Date DESC, Time DESC"
        )
        rows = cursor.fetchall()
        conn.close()

        attendance_list = [dict(row) for row in rows]

        return jsonify({
            'success': True,
            'count': len(attendance_list),
            'attendance': attendance_list
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/attendance/employee/<name>', methods=['GET'])
def api_get_employee_attendance(name):
    """Get attendance records for a specific employee"""
    try:
        conn = sqlite3.connect(ATTENDANCE_DB)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            "SELECT Time, Date FROM Attendance WHERE NAME=? ORDER BY Date DESC",
            (name,)
        )
        rows = cursor.fetchall()
        conn.close()

        attendance_list = [dict(row) for row in rows]

        return jsonify({
            'success': True,
            'employee': name,
            'count': len(attendance_list),
            'attendance': attendance_list
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# API ENDPOINTS - CUSTOMER RECOGNITION
# ============================================================================

@app.route('/api/customers/recognize', methods=['POST'])
def api_recognize_customer():
    """API endpoint to recognize customer from uploaded image"""
    try:
        # Get image from request
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        file = request.files['image']

        # Read image
        image_bytes = file.read()
        nparr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

        if image is None:
            return jsonify({'error': 'Invalid image'}), 400

        # Load known customers
        known_encodings, known_names = load_face_encodings(CUSTOMER_IMAGES_PATH)

        if len(known_encodings) == 0:
            return jsonify({'error': 'No registered customers found'}), 404

        # Recognize faces
        results = recognize_face_from_image(image, known_encodings, known_names)

        # Mark customer visits
        recognized_customers = []
        for result in results:
            if result['name'] != "Unknown":
                mark_customer_visit(result['name'])

                # Get customer details
                conn = sqlite3.connect(ATTENDANCE_DB)
                conn.row_factory = sqlite3.Row
                cursor = conn.execute("SELECT * FROM Customers WHERE Name=?", (result['name'],))
                customer = cursor.fetchone()
                conn.close()

                if customer:
                    recognized_customers.append({
                        'name': result['name'],
                        'confidence': result['confidence'],
                        'email': customer['Email'],
                        'phone': customer['Phone'],
                        'visit_count': customer['VisitCount'] + 1,
                        'last_visit': str(date.today()),
                        'notes': customer['Notes']
                    })

        return jsonify({
            'success': True,
            'total_faces': len(results),
            'recognized': len(recognized_customers),
            'customers': recognized_customers
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers', methods=['GET', 'POST'])
def api_customers():
    """Get all customers or create new customer"""
    try:
        if request.method == 'GET':
            conn = sqlite3.connect(ATTENDANCE_DB)
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM Customers ORDER BY Name")
            rows = cursor.fetchall()
            conn.close()

            customers_list = [dict(row) for row in rows]

            return jsonify({
                'success': True,
                'count': len(customers_list),
                'customers': customers_list
            })

        elif request.method == 'POST':
            data = request.get_json()

            if not data or 'name' not in data:
                return jsonify({'error': 'Name is required'}), 400

            name = data['name']
            email = data.get('email', '')
            phone = data.get('phone', '')
            notes = data.get('notes', '')

            conn = sqlite3.connect(ATTENDANCE_DB)
            conn.execute(
                "INSERT INTO Customers (Name, Email, Phone, LastVisit, VisitCount, Notes) VALUES (?, ?, ?, ?, ?, ?)",
                (name, email, phone, str(date.today()), 0, notes)
            )
            conn.commit()
            customer_id = conn.execute("SELECT last_insert_rowid()").fetchone()[0]
            conn.close()

            return jsonify({
                'success': True,
                'message': 'Customer created successfully',
                'customer_id': customer_id
            }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers/<int:customer_id>', methods=['GET', 'PUT', 'DELETE'])
def api_customer_detail(customer_id):
    """Get, update or delete a specific customer"""
    try:
        conn = sqlite3.connect(ATTENDANCE_DB)

        if request.method == 'GET':
            conn.row_factory = sqlite3.Row
            cursor = conn.execute("SELECT * FROM Customers WHERE ID=?", (customer_id,))
            customer = cursor.fetchone()
            conn.close()

            if customer:
                return jsonify({
                    'success': True,
                    'customer': dict(customer)
                })
            else:
                return jsonify({'error': 'Customer not found'}), 404

        elif request.method == 'PUT':
            data = request.get_json()

            cursor = conn.execute("SELECT * FROM Customers WHERE ID=?", (customer_id,))
            if cursor.fetchone() is None:
                conn.close()
                return jsonify({'error': 'Customer not found'}), 404

            name = data.get('name')
            email = data.get('email')
            phone = data.get('phone')
            notes = data.get('notes')

            conn.execute(
                "UPDATE Customers SET Name=?, Email=?, Phone=?, Notes=? WHERE ID=?",
                (name, email, phone, notes, customer_id)
            )
            conn.commit()
            conn.close()

            return jsonify({
                'success': True,
                'message': 'Customer updated successfully'
            })

        elif request.method == 'DELETE':
            cursor = conn.execute("SELECT Name FROM Customers WHERE ID=?", (customer_id,))
            customer = cursor.fetchone()

            if customer is None:
                conn.close()
                return jsonify({'error': 'Customer not found'}), 404

            customer_name = customer[0]

            # Delete customer record
            conn.execute("DELETE FROM Customers WHERE ID=?", (customer_id,))
            conn.commit()
            conn.close()

            # Delete customer image if exists
            for ext in ['.png', '.jpg', '.jpeg']:
                img_path = os.path.join(CUSTOMER_IMAGES_PATH, f"{customer_name}{ext}")
                if os.path.exists(img_path):
                    os.remove(img_path)

            return jsonify({
                'success': True,
                'message': 'Customer deleted successfully'
            })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers/<int:customer_id>/upload-photo', methods=['POST'])
def api_upload_customer_photo(customer_id):
    """Upload photo for a customer"""
    try:
        if 'image' not in request.files:
            return jsonify({'error': 'No image provided'}), 400

        file = request.files['image']

        # Get customer name
        conn = sqlite3.connect(ATTENDANCE_DB)
        cursor = conn.execute("SELECT Name FROM Customers WHERE ID=?", (customer_id,))
        customer = cursor.fetchone()
        conn.close()

        if customer is None:
            return jsonify({'error': 'Customer not found'}), 404

        customer_name = customer[0]

        # Save image
        img_path = os.path.join(CUSTOMER_IMAGES_PATH, f"{customer_name}.png")
        file.save(img_path)

        return jsonify({
            'success': True,
            'message': 'Photo uploaded successfully'
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/customers/<name>/visits', methods=['GET'])
def api_get_customer_visits(name):
    """Get visit history for a specific customer"""
    try:
        conn = sqlite3.connect(ATTENDANCE_DB)
        conn.row_factory = sqlite3.Row
        cursor = conn.execute(
            "SELECT * FROM CustomerVisits WHERE CustomerName=? ORDER BY VisitDate DESC, VisitTime DESC",
            (name,)
        )
        rows = cursor.fetchall()
        conn.close()

        visits_list = [dict(row) for row in rows]

        return jsonify({
            'success': True,
            'customer': name,
            'count': len(visits_list),
            'visits': visits_list
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# API ENDPOINTS - EMPLOYEE MANAGEMENT
# ============================================================================

@app.route('/api/employees/register', methods=['POST'])
def api_register_employee():
    """Register a new employee with photo"""
    try:
        if 'image' not in request.files or 'name' not in request.form:
            return jsonify({'error': 'Image and name are required'}), 400

        file = request.files['image']
        name = request.form['name']

        # Save image
        img_path = os.path.join(TRAINING_IMAGES_PATH, f"{name}.png")
        file.save(img_path)

        return jsonify({
            'success': True,
            'message': f'Employee {name} registered successfully'
        }), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/employees', methods=['GET'])
def api_get_employees():
    """Get list of all registered employees"""
    try:
        employees = []

        if os.path.exists(TRAINING_IMAGES_PATH):
            for filename in os.listdir(TRAINING_IMAGES_PATH):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    name = os.path.splitext(filename)[0]
                    employees.append(name)

        return jsonify({
            'success': True,
            'count': len(employees),
            'employees': employees
        })

    except Exception as e:
        return jsonify({'error': str(e)}), 500

# ============================================================================
# WEB ROUTES - ORIGINAL FUNCTIONALITY
# ============================================================================

@app.route('/new', methods=['GET', 'POST'])
def new():
    if request.method == "POST":
        return render_template('index.html')
    else:
        return "Everything is okay!"

@app.route('/name', methods=['GET', 'POST'])
def name():
    if request.method == "POST":
        name1 = request.form['name1']

        cam = cv2.VideoCapture(0)

        while True:
            ret, frame = cam.read()
            if not ret:
                print("failed to grab frame")
                break
            cv2.imshow("Press Space to capture image", frame)

            k = cv2.waitKey(1)
            if k % 256 == 27:
                # ESC pressed
                print("Escape hit, closing...")
                break
            elif k % 256 == 32:
                # SPACE pressed
                img_name = name1 + ".png"
                cv2.imwrite(os.path.join(TRAINING_IMAGES_PATH, img_name), frame)
                print("{} written!".format(img_name))
                break

        cam.release()
        cv2.destroyAllWindows()
        return render_template('image.html')
    else:
        return 'All is not well'

@app.route("/", methods=["GET"])
def home():
    """Main landing page"""
    return render_template('main_improved.html')

@app.route("/recognize-webcam", methods=["GET", "POST"])
def recognize():
    """Original webcam-based recognition (legacy)"""
    if request.method == "POST":
        # Load known faces
        known_encodings, known_names = load_face_encodings(TRAINING_IMAGES_PATH)

        if len(known_encodings) == 0:
            return "No training images found. Please register employees first."

        print('Encoding Complete')

        cap = cv2.VideoCapture(0)

        while True:
            success, img = cap.read()
            if not success:
                break

            imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
            imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

            facesCurFrame = face_recognition.face_locations(imgS)
            encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

            for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
                matches = face_recognition.compare_faces(known_encodings, encodeFace)
                faceDis = face_recognition.face_distance(known_encodings, encodeFace)

                matchIndex = np.argmin(faceDis)

                if faceDis[matchIndex] < FACE_MATCH_THRESHOLD:
                    name = known_names[matchIndex].upper()
                    mark_attendance(name)
                else:
                    name = 'Unknown'

                y1, x2, y2, x1 = faceLoc
                y1, x2, y2, x1 = y1*4, x2*4, y2*4, x1*4
                cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
                cv2.rectangle(img, (x1, y2-35), (x2, y2), (0, 255, 0), cv2.FILLED)
                cv2.putText(img, name, (x1+6, y2-6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

            cv2.imshow('Punch your Attendance', img)
            c = cv2.waitKey(1)
            if c == 27:
                break

        cap.release()
        cv2.destroyAllWindows()

        return render_template('first.html')
    else:
        return render_template('main.html')

@app.route('/how', methods=["GET", "POST"])
def how():
    return render_template('form.html')

@app.route('/data', methods=["GET", "POST"])
def data():
    if request.method == "POST":
        today = date.today()
        conn = sqlite3.connect(ATTENDANCE_DB)
        conn.row_factory = sqlite3.Row
        cur = conn.cursor()
        cursor = cur.execute("SELECT DISTINCT NAME, Time, Date FROM Attendance WHERE Date=?", (str(today),))
        rows = cur.fetchall()
        conn.close()

        return render_template('form2.html', rows=rows)
    else:
        return render_template('form1.html')

@app.route('/whole', methods=["GET", "POST"])
def whole():
    conn = sqlite3.connect(ATTENDANCE_DB)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()
    cursor = cur.execute("SELECT DISTINCT NAME, Time, Date FROM Attendance")
    rows = cur.fetchall()
    conn.close()
    return render_template('form3.html', rows=rows)

@app.route('/dashboard', methods=["GET", "POST"])
def dashboard():
    return render_template('dashboard.html')

# ============================================================================
# NEW WEB PAGES - CUSTOMER MANAGEMENT
# ============================================================================

@app.route('/customers-web')
def customers_web():
    """Web page to display all customers"""
    return render_template('customers.html')

@app.route('/customer-recognition')
def customer_recognition_page():
    """Web page for customer recognition"""
    return render_template('customer_recognition.html')

@app.route('/attendance-web')
def attendance_web():
    """Web page for attendance tracking"""
    return render_template('attendance_tracking.html')

# ============================================================================
# RUN APPLICATION
# ============================================================================

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
