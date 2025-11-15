#!/usr/bin/env python3
"""
Test script cho Face Recognition API
Kiểm tra tất cả endpoints có hoạt động không
"""

import requests
import json
from datetime import date

# Configuration
API_BASE = 'http://localhost:5000/api'

def print_section(title):
    """Print section header"""
    print("\n" + "="*60)
    print(f"  {title}")
    print("="*60)

def test_employees_list():
    """Test GET /api/employees"""
    print_section("TEST: Get Employees List")

    try:
        response = requests.get(f'{API_BASE}/employees')
        data = response.json()

        if response.status_code == 200 and data.get('success'):
            print(f"✅ Success: Found {data['count']} employees")
            if data['employees']:
                print(f"   Employees: {', '.join(data['employees'])}")
            else:
                print("   No employees registered yet")
        else:
            print(f"❌ Failed: {data.get('error', 'Unknown error')}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_attendance_today():
    """Test GET /api/attendance/today"""
    print_section("TEST: Today's Attendance")

    try:
        response = requests.get(f'{API_BASE}/attendance/today')
        data = response.json()

        if response.status_code == 200 and data.get('success'):
            print(f"✅ Success: {data['count']} people marked attendance today")
            print(f"   Date: {data['date']}")

            if data['attendance']:
                print("\n   Attendance List:")
                for record in data['attendance'][:5]:  # Show first 5
                    print(f"   - {record['NAME']}: {record['Time']}")

                if data['count'] > 5:
                    print(f"   ... and {data['count'] - 5} more")
        else:
            print(f"❌ Failed: {data.get('error', 'Unknown error')}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_customers_list():
    """Test GET /api/customers"""
    print_section("TEST: Get Customers List")

    try:
        response = requests.get(f'{API_BASE}/customers')
        data = response.json()

        if response.status_code == 200 and data.get('success'):
            print(f"✅ Success: Found {data['count']} customers")

            if data['customers']:
                print("\n   Customer List:")
                for customer in data['customers'][:5]:  # Show first 5
                    print(f"   - {customer['Name']}: {customer['Email'] or 'No email'} ({customer['VisitCount']} visits)")

                if data['count'] > 5:
                    print(f"   ... and {data['count'] - 5} more")
            else:
                print("   No customers registered yet")
        else:
            print(f"❌ Failed: {data.get('error', 'Unknown error')}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_create_customer():
    """Test POST /api/customers"""
    print_section("TEST: Create Customer (without image)")

    try:
        customer_data = {
            "name": "TEST_CUSTOMER",
            "email": "test@example.com",
            "phone": "0123456789",
            "notes": "This is a test customer created by test script"
        }

        response = requests.post(f'{API_BASE}/customers', json=customer_data)
        data = response.json()

        if response.status_code == 201 and data.get('success'):
            print(f"✅ Success: Customer created with ID {data['customer_id']}")
            print(f"   Name: {customer_data['name']}")
            print(f"   Email: {customer_data['email']}")
            return data['customer_id']
        else:
            print(f"❌ Failed: {data.get('error', 'Unknown error')}")
            return None

    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return None

def test_get_customer(customer_id):
    """Test GET /api/customers/<id>"""
    print_section(f"TEST: Get Customer Details (ID: {customer_id})")

    try:
        response = requests.get(f'{API_BASE}/customers/{customer_id}')
        data = response.json()

        if response.status_code == 200 and data.get('success'):
            customer = data['customer']
            print(f"✅ Success: Retrieved customer details")
            print(f"   ID: {customer['ID']}")
            print(f"   Name: {customer['Name']}")
            print(f"   Email: {customer['Email']}")
            print(f"   Phone: {customer['Phone']}")
            print(f"   Visit Count: {customer['VisitCount']}")
        else:
            print(f"❌ Failed: {data.get('error', 'Unknown error')}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_update_customer(customer_id):
    """Test PUT /api/customers/<id>"""
    print_section(f"TEST: Update Customer (ID: {customer_id})")

    try:
        update_data = {
            "name": "TEST_CUSTOMER_UPDATED",
            "email": "updated@example.com",
            "phone": "0987654321",
            "notes": "Updated by test script"
        }

        response = requests.put(f'{API_BASE}/customers/{customer_id}', json=update_data)
        data = response.json()

        if response.status_code == 200 and data.get('success'):
            print(f"✅ Success: Customer updated")
            print(f"   New email: {update_data['email']}")
            print(f"   New phone: {update_data['phone']}")
        else:
            print(f"❌ Failed: {data.get('error', 'Unknown error')}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_delete_customer(customer_id):
    """Test DELETE /api/customers/<id>"""
    print_section(f"TEST: Delete Customer (ID: {customer_id})")

    try:
        response = requests.delete(f'{API_BASE}/customers/{customer_id}')
        data = response.json()

        if response.status_code == 200 and data.get('success'):
            print(f"✅ Success: Customer deleted")
        else:
            print(f"❌ Failed: {data.get('error', 'Unknown error')}")

    except Exception as e:
        print(f"❌ Error: {str(e)}")

def test_server_connection():
    """Test if server is running"""
    print_section("TEST: Server Connection")

    try:
        response = requests.get('http://localhost:5000/', timeout=3)
        if response.status_code == 200:
            print("✅ Server is running at http://localhost:5000")
            return True
        else:
            print(f"⚠️  Server responded but with status {response.status_code}")
            return False
    except requests.exceptions.ConnectionError:
        print("❌ Cannot connect to server!")
        print("   Make sure the server is running:")
        print("   python app_improved.py")
        return False
    except Exception as e:
        print(f"❌ Error: {str(e)}")
        return False

def main():
    """Run all tests"""
    print("\n" + "🧪 "*30)
    print("  FACE RECOGNITION API - TEST SUITE")
    print("🧪 "*30)

    # Check server connection first
    if not test_server_connection():
        print("\n⚠️  Please start the server first and try again!")
        return

    # Run tests
    test_employees_list()
    test_attendance_today()
    test_customers_list()

    # CRUD tests
    customer_id = test_create_customer()
    if customer_id:
        test_get_customer(customer_id)
        test_update_customer(customer_id)
        test_delete_customer(customer_id)

    # Summary
    print_section("TEST SUMMARY")
    print("✅ All basic endpoint tests completed")
    print("\n📝 NOTE:")
    print("   - Image upload tests skipped (requires actual image files)")
    print("   - Face recognition tests skipped (requires face images)")
    print("\n💡 To test full functionality:")
    print("   1. Add employee images to 'Training images/' folder")
    print("   2. Use the web interface at http://localhost:5000")
    print("   3. Or upload images via API using files parameter")

    print("\n" + "="*60)

if __name__ == '__main__':
    main()
