#!/usr/bin/env python3
"""
FRAMS Performance Benchmark Tool

Test and measure system performance for various operations.

Usage:
    python benchmark.py                  # Run all benchmarks
    python benchmark.py --api            # Test API endpoints only
    python benchmark.py --face           # Test face recognition only
    python benchmark.py --database       # Test database operations only
    python benchmark.py --concurrent 10  # Test with 10 concurrent requests
"""

import time
import requests
import sqlite3
import os
import cv2
import face_recognition
import numpy as np
import argparse
import statistics
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime
import json

class PerformanceBenchmark:
    """Performance testing and benchmarking tool"""

    def __init__(self, base_url='http://localhost:5000'):
        self.base_url = base_url
        self.results = {}
        self.db_path = 'information.db'

    def run_all_benchmarks(self):
        """Run all performance benchmarks"""
        print("=" * 80)
        print("FRAMS PERFORMANCE BENCHMARK")
        print("=" * 80)
        print(f"Started at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"Base URL: {self.base_url}")
        print("=" * 80)
        print()

        # Test API availability
        if not self.check_api_availability():
            print("❌ API not available. Please start the server first.")
            return

        # Run benchmarks
        self.benchmark_database_operations()
        self.benchmark_face_recognition()
        self.benchmark_api_endpoints()
        self.benchmark_concurrent_requests()

        # Generate report
        self.generate_report()

    def check_api_availability(self):
        """Check if API is running"""
        try:
            response = requests.get(f"{self.base_url}/api/health", timeout=5)
            return response.status_code == 200
        except Exception:
            return False

    # ========================================================================
    # DATABASE BENCHMARKS
    # ========================================================================

    def benchmark_database_operations(self):
        """Benchmark database read/write operations"""
        print("\n📊 DATABASE BENCHMARKS")
        print("-" * 80)

        results = {
            'insert': [],
            'select': [],
            'update': [],
            'delete': []
        }

        # Setup test database
        conn = sqlite3.connect(':memory:')  # Use in-memory for speed
        cursor = conn.cursor()

        # Create test table
        cursor.execute('''
            CREATE TABLE TestAttendance (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT,
                date TEXT,
                time TEXT,
                status TEXT
            )
        ''')

        # Benchmark INSERT
        print("Testing INSERT operations...")
        for i in range(100):
            start = time.perf_counter()
            cursor.execute(
                "INSERT INTO TestAttendance (name, date, time, status) VALUES (?, ?, ?, ?)",
                (f'EMPLOYEE_{i}', '2025-01-15', '09:00:00', 'PRESENT')
            )
            conn.commit()
            end = time.perf_counter()
            results['insert'].append((end - start) * 1000)  # Convert to ms

        # Benchmark SELECT
        print("Testing SELECT operations...")
        for _ in range(100):
            start = time.perf_counter()
            cursor.execute("SELECT * FROM TestAttendance WHERE status='PRESENT'")
            cursor.fetchall()
            end = time.perf_counter()
            results['select'].append((end - start) * 1000)

        # Benchmark UPDATE
        print("Testing UPDATE operations...")
        for i in range(100):
            start = time.perf_counter()
            cursor.execute(
                "UPDATE TestAttendance SET status='ABSENT' WHERE id=?",
                (i + 1,)
            )
            conn.commit()
            end = time.perf_counter()
            results['update'].append((end - start) * 1000)

        # Benchmark DELETE
        print("Testing DELETE operations...")
        for i in range(100):
            start = time.perf_counter()
            cursor.execute("DELETE FROM TestAttendance WHERE id=?", (i + 1,))
            conn.commit()
            end = time.perf_counter()
            results['delete'].append((end - start) * 1000)

        conn.close()

        # Print results
        for operation, times in results.items():
            avg_time = statistics.mean(times)
            min_time = min(times)
            max_time = max(times)
            print(f"  {operation.upper():8} - Avg: {avg_time:.3f}ms | Min: {min_time:.3f}ms | Max: {max_time:.3f}ms")

        self.results['database'] = results

    # ========================================================================
    # FACE RECOGNITION BENCHMARKS
    # ========================================================================

    def benchmark_face_recognition(self):
        """Benchmark face recognition operations"""
        print("\n👤 FACE RECOGNITION BENCHMARKS")
        print("-" * 80)

        # Check if training images exist
        training_dir = 'Training images'
        if not os.path.exists(training_dir) or not os.listdir(training_dir):
            print("  ⚠️  No training images found. Skipping face recognition benchmark.")
            return

        results = {
            'load_image': [],
            'detect_faces': [],
            'encode_faces': [],
            'compare_faces': []
        }

        # Get a test image
        test_image = None
        for filename in os.listdir(training_dir):
            if filename.endswith(('.jpg', '.jpeg', '.png')):
                test_image = os.path.join(training_dir, filename)
                break

        if not test_image:
            print("  ⚠️  No valid test image found.")
            return

        print(f"Using test image: {test_image}")

        # Benchmark image loading
        print("Testing image loading...")
        for _ in range(10):
            start = time.perf_counter()
            img = face_recognition.load_image_file(test_image)
            end = time.perf_counter()
            results['load_image'].append((end - start) * 1000)

        # Benchmark face detection
        print("Testing face detection...")
        img = face_recognition.load_image_file(test_image)
        for _ in range(10):
            start = time.perf_counter()
            face_locations = face_recognition.face_locations(img)
            end = time.perf_counter()
            results['detect_faces'].append((end - start) * 1000)

        # Benchmark face encoding
        print("Testing face encoding...")
        face_locations = face_recognition.face_locations(img)
        if face_locations:
            for _ in range(10):
                start = time.perf_counter()
                encodings = face_recognition.face_encodings(img, face_locations)
                end = time.perf_counter()
                results['encode_faces'].append((end - start) * 1000)

            # Benchmark face comparison
            print("Testing face comparison...")
            known_encoding = encodings[0]
            for _ in range(100):
                start = time.perf_counter()
                matches = face_recognition.compare_faces([known_encoding], known_encoding)
                end = time.perf_counter()
                results['compare_faces'].append((end - start) * 1000)

        # Print results
        for operation, times in results.items():
            if times:
                avg_time = statistics.mean(times)
                min_time = min(times)
                max_time = max(times)
                print(f"  {operation.replace('_', ' ').title():20} - Avg: {avg_time:.3f}ms | Min: {min_time:.3f}ms | Max: {max_time:.3f}ms")

        self.results['face_recognition'] = results

    # ========================================================================
    # API BENCHMARKS
    # ========================================================================

    def benchmark_api_endpoints(self):
        """Benchmark API endpoint response times"""
        print("\n🌐 API ENDPOINT BENCHMARKS")
        print("-" * 80)

        endpoints = [
            {'method': 'GET', 'path': '/api/health', 'name': 'Health Check'},
            {'method': 'GET', 'path': '/api/version', 'name': 'Version Info'},
            {'method': 'GET', 'path': '/api/stats', 'name': 'System Stats'},
            {'method': 'GET', 'path': '/api/attendance/today', 'name': 'Today Attendance'},
            {'method': 'GET', 'path': '/api/attendance/all', 'name': 'All Attendance'},
            {'method': 'GET', 'path': '/api/employees', 'name': 'List Employees'},
            {'method': 'GET', 'path': '/api/customers', 'name': 'List Customers'},
        ]

        results = {}

        for endpoint in endpoints:
            print(f"Testing {endpoint['name']}...")
            times = []

            for _ in range(10):
                start = time.perf_counter()
                try:
                    if endpoint['method'] == 'GET':
                        response = requests.get(
                            f"{self.base_url}{endpoint['path']}",
                            timeout=10
                        )
                    end = time.perf_counter()

                    if response.status_code == 200:
                        times.append((end - start) * 1000)
                except Exception as e:
                    print(f"  ⚠️  Error: {str(e)}")

            if times:
                results[endpoint['name']] = {
                    'avg': statistics.mean(times),
                    'min': min(times),
                    'max': max(times),
                    'median': statistics.median(times)
                }

                print(f"  {endpoint['name']:20} - Avg: {results[endpoint['name']]['avg']:.3f}ms | "
                      f"Min: {results[endpoint['name']]['min']:.3f}ms | "
                      f"Max: {results[endpoint['name']]['max']:.3f}ms")

        self.results['api_endpoints'] = results

    # ========================================================================
    # CONCURRENT REQUEST BENCHMARKS
    # ========================================================================

    def benchmark_concurrent_requests(self, num_workers=5):
        """Benchmark API with concurrent requests"""
        print(f"\n⚡ CONCURRENT REQUEST BENCHMARKS ({num_workers} workers)")
        print("-" * 80)

        def make_request(i):
            """Make a single request"""
            start = time.perf_counter()
            try:
                response = requests.get(f"{self.base_url}/api/health", timeout=10)
                end = time.perf_counter()
                return {
                    'success': response.status_code == 200,
                    'time': (end - start) * 1000,
                    'status_code': response.status_code
                }
            except Exception as e:
                end = time.perf_counter()
                return {
                    'success': False,
                    'time': (end - start) * 1000,
                    'error': str(e)
                }

        # Test with concurrent requests
        num_requests = 50
        print(f"Sending {num_requests} concurrent requests...")

        start_time = time.perf_counter()
        results = []

        with ThreadPoolExecutor(max_workers=num_workers) as executor:
            futures = [executor.submit(make_request, i) for i in range(num_requests)]

            for future in as_completed(futures):
                result = future.result()
                results.append(result)

        end_time = time.perf_counter()

        # Analyze results
        successful = [r for r in results if r['success']]
        failed = [r for r in results if not r['success']]

        total_time = (end_time - start_time) * 1000
        requests_per_second = num_requests / ((end_time - start_time))

        print(f"\n  Total requests: {num_requests}")
        print(f"  Successful: {len(successful)}")
        print(f"  Failed: {len(failed)}")
        print(f"  Total time: {total_time:.3f}ms")
        print(f"  Requests/second: {requests_per_second:.2f}")

        if successful:
            times = [r['time'] for r in successful]
            print(f"  Avg response time: {statistics.mean(times):.3f}ms")
            print(f"  Min response time: {min(times):.3f}ms")
            print(f"  Max response time: {max(times):.3f}ms")
            print(f"  Median response time: {statistics.median(times):.3f}ms")

        self.results['concurrent'] = {
            'num_requests': num_requests,
            'num_workers': num_workers,
            'successful': len(successful),
            'failed': len(failed),
            'total_time_ms': total_time,
            'requests_per_second': requests_per_second,
            'avg_response_time_ms': statistics.mean(times) if successful else 0
        }

    # ========================================================================
    # REPORTING
    # ========================================================================

    def generate_report(self):
        """Generate final performance report"""
        print("\n" + "=" * 80)
        print("BENCHMARK SUMMARY")
        print("=" * 80)

        # Save to JSON
        report_file = f'benchmark_report_{datetime.now().strftime("%Y%m%d_%H%M%S")}.json'
        with open(report_file, 'w') as f:
            json.dump({
                'timestamp': datetime.now().isoformat(),
                'results': self.results
            }, f, indent=2)

        print(f"\n✅ Full report saved to: {report_file}")

        # Performance ratings
        print("\n📈 PERFORMANCE RATINGS:")

        # API endpoints
        if 'api_endpoints' in self.results:
            avg_api_time = statistics.mean([
                v['avg'] for v in self.results['api_endpoints'].values()
            ])
            api_rating = self._get_rating(avg_api_time, 100, 500)
            print(f"  API Response Time: {avg_api_time:.2f}ms - {api_rating}")

        # Concurrent requests
        if 'concurrent' in self.results:
            rps = self.results['concurrent']['requests_per_second']
            rps_rating = self._get_rating(rps, 50, 10, reverse=True)
            print(f"  Requests/Second: {rps:.2f} - {rps_rating}")

        # Face recognition
        if 'face_recognition' in self.results and 'encode_faces' in self.results['face_recognition']:
            if self.results['face_recognition']['encode_faces']:
                avg_encoding = statistics.mean(self.results['face_recognition']['encode_faces'])
                encoding_rating = self._get_rating(avg_encoding, 100, 300)
                print(f"  Face Encoding: {avg_encoding:.2f}ms - {encoding_rating}")

        print("\n" + "=" * 80)
        print(f"Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print("=" * 80)

    def _get_rating(self, value, excellent_threshold, poor_threshold, reverse=False):
        """Get performance rating"""
        if reverse:
            if value >= excellent_threshold:
                return "⭐⭐⭐ Excellent"
            elif value >= poor_threshold:
                return "⭐⭐ Good"
            else:
                return "⭐ Needs Improvement"
        else:
            if value <= excellent_threshold:
                return "⭐⭐⭐ Excellent"
            elif value <= poor_threshold:
                return "⭐⭐ Good"
            else:
                return "⭐ Needs Improvement"


def main():
    """Main entry point"""
    parser = argparse.ArgumentParser(description='FRAMS Performance Benchmark Tool')
    parser.add_argument('--url', default='http://localhost:5000', help='Base URL of API')
    parser.add_argument('--api', action='store_true', help='Run API benchmarks only')
    parser.add_argument('--face', action='store_true', help='Run face recognition benchmarks only')
    parser.add_argument('--database', action='store_true', help='Run database benchmarks only')
    parser.add_argument('--concurrent', type=int, metavar='N', help='Test with N concurrent workers')

    args = parser.parse_args()

    benchmark = PerformanceBenchmark(base_url=args.url)

    # Run specific benchmarks or all
    if args.database:
        benchmark.benchmark_database_operations()
    elif args.face:
        benchmark.benchmark_face_recognition()
    elif args.api:
        if benchmark.check_api_availability():
            benchmark.benchmark_api_endpoints()
        else:
            print("❌ API not available. Please start the server first.")
    elif args.concurrent:
        if benchmark.check_api_availability():
            benchmark.benchmark_concurrent_requests(num_workers=args.concurrent)
        else:
            print("❌ API not available. Please start the server first.")
    else:
        benchmark.run_all_benchmarks()


if __name__ == '__main__':
    main()
