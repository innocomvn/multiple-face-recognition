#!/usr/bin/env python3
"""
FRAMS Client - Python Client Library for Face Recognition API

Dễ dàng tích hợp hệ thống nhận diện khuôn mặt vào ứng dụng của bạn.

Example:
    from frams_client import FRAMSClient

    client = FRAMSClient('http://localhost:5000')

    # Chấm công
    result = client.mark_attendance('employee.jpg')
    print(f"Recognized: {result['recognized']} people")

    # Nhận diện khách hàng
    customers = client.recognize_customer('customer.jpg')
    for customer in customers:
        print(f"Welcome back {customer['name']}!")
"""

import requests
from typing import Dict, List, Optional, Union
from pathlib import Path
import json


class FRAMSClient:
    """
    Python client for FRAMS API

    Args:
        base_url (str): Base URL of FRAMS API (default: http://localhost:5000)
        timeout (int): Request timeout in seconds (default: 30)

    Example:
        >>> client = FRAMSClient()
        >>> result = client.mark_attendance('photo.jpg')
        >>> print(result['recognized'])
        2
    """

    def __init__(self, base_url: str = 'http://localhost:5000', timeout: int = 30):
        self.base_url = base_url.rstrip('/')
        self.api_url = f"{self.base_url}/api"
        self.timeout = timeout
        self.session = requests.Session()

    def _make_request(
        self,
        method: str,
        endpoint: str,
        data: Optional[Dict] = None,
        files: Optional[Dict] = None,
        json_data: Optional[Dict] = None
    ) -> Dict:
        """
        Make HTTP request to API

        Args:
            method: HTTP method (GET, POST, PUT, DELETE)
            endpoint: API endpoint
            data: Form data
            files: Files to upload
            json_data: JSON data

        Returns:
            Response JSON

        Raises:
            requests.exceptions.RequestException: On request error
        """
        url = f"{self.api_url}/{endpoint.lstrip('/')}"

        try:
            response = self.session.request(
                method=method,
                url=url,
                data=data,
                files=files,
                json=json_data,
                timeout=self.timeout
            )
            response.raise_for_status()
            return response.json()

        except requests.exceptions.RequestException as e:
            raise Exception(f"API request failed: {str(e)}")

    # ========================================================================
    # HEALTH & MONITORING
    # ========================================================================

    def health_check(self) -> Dict:
        """
        Check API health status

        Returns:
            dict: Health status information

        Example:
            >>> client.health_check()
            {'status': 'healthy', 'version': '2.0.0', ...}
        """
        return self._make_request('GET', '/health')

    def get_stats(self) -> Dict:
        """
        Get system statistics

        Returns:
            dict: System statistics

        Example:
            >>> stats = client.get_stats()
            >>> print(stats['stats']['employees']['total'])
            10
        """
        return self._make_request('GET', '/stats')

    def get_version(self) -> Dict:
        """
        Get API version information

        Returns:
            dict: Version information

        Example:
            >>> client.get_version()
            {'version': '2.0.0', 'api_version': 'v1', ...}
        """
        return self._make_request('GET', '/version')

    # ========================================================================
    # ATTENDANCE API
    # ========================================================================

    def mark_attendance(self, image_path: Union[str, Path]) -> Dict:
        """
        Recognize faces and mark attendance

        Args:
            image_path: Path to image file

        Returns:
            dict: Recognition results

        Example:
            >>> result = client.mark_attendance('team_photo.jpg')
            >>> print(f"Recognized {result['recognized']} employees")
            Recognized 3 employees
        """
        with open(image_path, 'rb') as f:
            files = {'image': f}
            return self._make_request('POST', '/attendance/recognize', files=files)

    def get_today_attendance(self) -> Dict:
        """
        Get today's attendance records

        Returns:
            dict: Today's attendance

        Example:
            >>> attendance = client.get_today_attendance()
            >>> for record in attendance['attendance']:
            ...     print(f"{record['NAME']}: {record['Time']}")
        """
        return self._make_request('GET', '/attendance/today')

    def get_all_attendance(self) -> Dict:
        """
        Get all attendance records

        Returns:
            dict: All attendance records

        Example:
            >>> all_records = client.get_all_attendance()
            >>> print(f"Total records: {all_records['count']}")
        """
        return self._make_request('GET', '/attendance/all')

    def get_employee_attendance(self, name: str) -> Dict:
        """
        Get attendance records for specific employee

        Args:
            name: Employee name

        Returns:
            dict: Employee attendance records

        Example:
            >>> records = client.get_employee_attendance('NGUYEN_VAN_A')
            >>> print(f"Attended {records['count']} days")
        """
        return self._make_request('GET', f'/attendance/employee/{name}')

    # ========================================================================
    # EMPLOYEE API
    # ========================================================================

    def register_employee(self, name: str, image_path: Union[str, Path]) -> Dict:
        """
        Register new employee

        Args:
            name: Employee name
            image_path: Path to face image

        Returns:
            dict: Registration result

        Example:
            >>> result = client.register_employee('NGUYEN_VAN_A', 'face.jpg')
            >>> print(result['message'])
            Employee NGUYEN_VAN_A registered successfully
        """
        with open(image_path, 'rb') as f:
            files = {'image': f}
            data = {'name': name}
            return self._make_request('POST', '/employees/register', data=data, files=files)

    def get_employees(self) -> Dict:
        """
        Get list of all employees

        Returns:
            dict: Employee list

        Example:
            >>> employees = client.get_employees()
            >>> print(employees['employees'])
            ['NGUYEN_VAN_A', 'TRAN_THI_B', ...]
        """
        return self._make_request('GET', '/employees')

    # ========================================================================
    # CUSTOMER API
    # ========================================================================

    def recognize_customer(self, image_path: Union[str, Path]) -> List[Dict]:
        """
        Recognize customer from image

        Args:
            image_path: Path to image file

        Returns:
            list: List of recognized customers

        Example:
            >>> customers = client.recognize_customer('customer.jpg')
            >>> for customer in customers:
            ...     print(f"Welcome {customer['name']}! Visit #{customer['visit_count']}")
        """
        with open(image_path, 'rb') as f:
            files = {'image': f}
            result = self._make_request('POST', '/customers/recognize', files=files)
            return result.get('customers', [])

    def create_customer(
        self,
        name: str,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        notes: Optional[str] = None
    ) -> int:
        """
        Create new customer

        Args:
            name: Customer name
            email: Email address (optional)
            phone: Phone number (optional)
            notes: Additional notes (optional)

        Returns:
            int: Customer ID

        Example:
            >>> customer_id = client.create_customer(
            ...     'NGUYEN_VAN_C',
            ...     email='customer@example.com',
            ...     phone='0912345678'
            ... )
            >>> print(f"Customer ID: {customer_id}")
        """
        data = {'name': name}
        if email:
            data['email'] = email
        if phone:
            data['phone'] = phone
        if notes:
            data['notes'] = notes

        result = self._make_request('POST', '/customers', json_data=data)
        return result['customer_id']

    def get_customers(self) -> List[Dict]:
        """
        Get all customers

        Returns:
            list: List of customers

        Example:
            >>> customers = client.get_customers()
            >>> for customer in customers:
            ...     print(f"{customer['Name']}: {customer['VisitCount']} visits")
        """
        result = self._make_request('GET', '/customers')
        return result.get('customers', [])

    def get_customer(self, customer_id: int) -> Dict:
        """
        Get customer details

        Args:
            customer_id: Customer ID

        Returns:
            dict: Customer information

        Example:
            >>> customer = client.get_customer(1)
            >>> print(customer['Name'])
            NGUYEN_VAN_C
        """
        result = self._make_request('GET', f'/customers/{customer_id}')
        return result['customer']

    def update_customer(
        self,
        customer_id: int,
        name: Optional[str] = None,
        email: Optional[str] = None,
        phone: Optional[str] = None,
        notes: Optional[str] = None
    ) -> Dict:
        """
        Update customer information

        Args:
            customer_id: Customer ID
            name: New name (optional)
            email: New email (optional)
            phone: New phone (optional)
            notes: New notes (optional)

        Returns:
            dict: Update result

        Example:
            >>> client.update_customer(1, email='newemail@example.com')
            {'success': True, 'message': 'Customer updated successfully'}
        """
        data = {}
        if name:
            data['name'] = name
        if email:
            data['email'] = email
        if phone:
            data['phone'] = phone
        if notes:
            data['notes'] = notes

        return self._make_request('PUT', f'/customers/{customer_id}', json_data=data)

    def delete_customer(self, customer_id: int) -> Dict:
        """
        Delete customer

        Args:
            customer_id: Customer ID

        Returns:
            dict: Deletion result

        Example:
            >>> client.delete_customer(1)
            {'success': True, 'message': 'Customer deleted successfully'}
        """
        return self._make_request('DELETE', f'/customers/{customer_id}')

    def upload_customer_photo(self, customer_id: int, image_path: Union[str, Path]) -> Dict:
        """
        Upload customer photo

        Args:
            customer_id: Customer ID
            image_path: Path to face image

        Returns:
            dict: Upload result

        Example:
            >>> client.upload_customer_photo(1, 'customer_face.jpg')
            {'success': True, 'message': 'Photo uploaded successfully'}
        """
        with open(image_path, 'rb') as f:
            files = {'image': f}
            return self._make_request(
                'POST',
                f'/customers/{customer_id}/upload-photo',
                files=files
            )

    def get_customer_visits(self, name: str) -> List[Dict]:
        """
        Get customer visit history

        Args:
            name: Customer name

        Returns:
            list: Visit history

        Example:
            >>> visits = client.get_customer_visits('NGUYEN_VAN_C')
            >>> print(f"Total visits: {len(visits)}")
        """
        result = self._make_request('GET', f'/customers/{name}/visits')
        return result.get('visits', [])

    # ========================================================================
    # HIGH-LEVEL METHODS
    # ========================================================================

    def add_customer_with_photo(
        self,
        name: str,
        image_path: Union[str, Path],
        email: Optional[str] = None,
        phone: Optional[str] = None,
        notes: Optional[str] = None
    ) -> int:
        """
        Create customer and upload photo in one call

        Args:
            name: Customer name
            image_path: Path to face image
            email: Email (optional)
            phone: Phone (optional)
            notes: Notes (optional)

        Returns:
            int: Customer ID

        Example:
            >>> customer_id = client.add_customer_with_photo(
            ...     'NGUYEN_VAN_C',
            ...     'customer.jpg',
            ...     email='test@example.com'
            ... )
        """
        # Create customer
        customer_id = self.create_customer(name, email, phone, notes)

        # Upload photo
        self.upload_customer_photo(customer_id, image_path)

        return customer_id


# ============================================================================
# EXAMPLE USAGE
# ============================================================================

if __name__ == '__main__':
    print("FRAMS Client - Example Usage")
    print("=" * 60)

    # Initialize client
    client = FRAMSClient()

    try:
        # Health check
        print("\n1. Health Check:")
        health = client.health_check()
        print(f"   Status: {health['status']}")
        print(f"   Version: {health['version']}")

        # Get stats
        print("\n2. System Statistics:")
        stats = client.get_stats()
        print(f"   Employees: {stats['stats']['employees']['total']}")
        print(f"   Customers: {stats['stats']['customers']['total']}")
        print(f"   Today's Attendance: {stats['stats']['attendance']['today']}")

        # Get employees
        print("\n3. Employee List:")
        employees = client.get_employees()
        print(f"   Total: {employees['count']}")
        if employees['employees']:
            for emp in employees['employees'][:3]:
                print(f"   - {emp}")

        # Get customers
        print("\n4. Customer List:")
        customers = client.get_customers()
        print(f"   Total: {len(customers)}")
        if customers:
            for customer in customers[:3]:
                print(f"   - {customer['Name']}: {customer['VisitCount']} visits")

        print("\n" + "=" * 60)
        print("✅ All tests passed!")

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\nMake sure the server is running:")
        print("  python app_improved.py")
