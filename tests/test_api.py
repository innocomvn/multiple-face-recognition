#!/usr/bin/env python3
"""
Unit Tests for FRAMS API

Run with:
    python -m pytest tests/
    python -m pytest tests/test_api.py -v
"""

import unittest
import json
import os
import sys

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


class TestHealthEndpoints(unittest.TestCase):
    """Test health check and monitoring endpoints"""

    def setUp(self):
        """Setup test client"""
        from app_improved import app
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_health_check(self):
        """Test /api/health endpoint"""
        response = self.client.get('/api/health')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertIn('status', data)
        self.assertIn('version', data)
        self.assertEqual(data['version'], '2.0.0')

    def test_stats_endpoint(self):
        """Test /api/stats endpoint"""
        response = self.client.get('/api/stats')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('stats', data)
        self.assertIn('attendance', data['stats'])
        self.assertIn('employees', data['stats'])
        self.assertIn('customers', data['stats'])

    def test_version_endpoint(self):
        """Test /api/version endpoint"""
        response = self.client.get('/api/version')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertEqual(data['version'], '2.0.0')
        self.assertEqual(data['api_version'], 'v1')
        self.assertIn('endpoints', data)


class TestAttendanceAPI(unittest.TestCase):
    """Test attendance API endpoints"""

    def setUp(self):
        """Setup test client"""
        from app_improved import app
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_get_today_attendance(self):
        """Test /api/attendance/today endpoint"""
        response = self.client.get('/api/attendance/today')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('attendance', data)
        self.assertIn('count', data)
        self.assertIn('date', data)

    def test_get_all_attendance(self):
        """Test /api/attendance/all endpoint"""
        response = self.client.get('/api/attendance/all')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('attendance', data)
        self.assertIn('count', data)


class TestEmployeeAPI(unittest.TestCase):
    """Test employee API endpoints"""

    def setUp(self):
        """Setup test client"""
        from app_improved import app
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_get_employees(self):
        """Test /api/employees endpoint"""
        response = self.client.get('/api/employees')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('employees', data)
        self.assertIn('count', data)


class TestCustomerAPI(unittest.TestCase):
    """Test customer API endpoints"""

    def setUp(self):
        """Setup test client"""
        from app_improved import app
        app.config['TESTING'] = True
        self.client = app.test_client()

    def test_get_customers(self):
        """Test /api/customers GET endpoint"""
        response = self.client.get('/api/customers')
        self.assertEqual(response.status_code, 200)

        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('customers', data)
        self.assertIn('count', data)

    def test_create_customer(self):
        """Test /api/customers POST endpoint"""
        customer_data = {
            'name': 'TEST_CUSTOMER',
            'email': 'test@example.com',
            'phone': '0123456789',
            'notes': 'Test customer'
        }

        response = self.client.post(
            '/api/customers',
            data=json.dumps(customer_data),
            content_type='application/json'
        )

        self.assertIn(response.status_code, [200, 201])

        data = json.loads(response.data)
        self.assertTrue(data['success'])
        self.assertIn('customer_id', data)

        # Cleanup: delete test customer
        customer_id = data['customer_id']
        self.client.delete(f'/api/customers/{customer_id}')


if __name__ == '__main__':
    unittest.main()
