#!/usr/bin/env python3
"""
Database Backup Script - FRAMS

Tự động backup database và training/customer images.
Hỗ trợ backup theo lịch hoặc manual.

Usage:
    python backup_database.py                    # Backup ngay
    python backup_database.py --auto-delete 7    # Xóa backup > 7 ngày
    python backup_database.py --compress         # Backup và nén
"""

import os
import shutil
import sqlite3
from datetime import datetime, timedelta
import argparse
import zipfile


class DatabaseBackup:
    """Database and files backup manager"""

    def __init__(self, backup_dir='backups'):
        self.backup_dir = backup_dir
        self.db_file = 'information.db'
        self.training_dir = 'Training images'
        self.customer_dir = 'Customer images'

        # Create backup directory
        os.makedirs(backup_dir, exist_ok=True)

    def create_backup(self, compress=False):
        """
        Create backup of database and images

        Args:
            compress (bool): Create compressed backup

        Returns:
            str: Backup path
        """
        # Create timestamp
        timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
        backup_name = f'backup_{timestamp}'
        backup_path = os.path.join(self.backup_dir, backup_name)

        print(f"🔄 Creating backup: {backup_name}")

        # Create backup directory
        os.makedirs(backup_path, exist_ok=True)

        try:
            # 1. Backup database
            if os.path.exists(self.db_file):
                print(f"   📊 Backing up database...")
                self._backup_database(backup_path)
            else:
                print(f"   ⚠️  Database not found: {self.db_file}")

            # 2. Backup training images
            if os.path.exists(self.training_dir):
                print(f"   📸 Backing up training images...")
                shutil.copytree(
                    self.training_dir,
                    os.path.join(backup_path, 'Training images')
                )
            else:
                print(f"   ⚠️  Training images not found")

            # 3. Backup customer images
            if os.path.exists(self.customer_dir):
                print(f"   📸 Backing up customer images...")
                shutil.copytree(
                    self.customer_dir,
                    os.path.join(backup_path, 'Customer images')
                )
            else:
                print(f"   ⚠️  Customer images not found")

            # 4. Create metadata file
            self._create_metadata(backup_path)

            # 5. Compress if requested
            if compress:
                print(f"   🗜️  Compressing backup...")
                zip_path = self._compress_backup(backup_path)
                shutil.rmtree(backup_path)  # Remove uncompressed
                backup_path = zip_path

            print(f"✅ Backup completed: {backup_path}")
            return backup_path

        except Exception as e:
            print(f"❌ Backup failed: {str(e)}")
            # Clean up failed backup
            if os.path.exists(backup_path):
                shutil.rmtree(backup_path)
            raise

    def _backup_database(self, backup_path):
        """Backup SQLite database properly"""
        db_backup_path = os.path.join(backup_path, 'information.db')

        # Use SQLite backup API
        source = sqlite3.connect(self.db_file)
        dest = sqlite3.connect(db_backup_path)

        source.backup(dest)

        source.close()
        dest.close()

    def _create_metadata(self, backup_path):
        """Create metadata file with backup info"""
        metadata = {
            'timestamp': datetime.now().isoformat(),
            'database': os.path.exists(self.db_file),
            'training_images': len(os.listdir(self.training_dir)) if os.path.exists(self.training_dir) else 0,
            'customer_images': len(os.listdir(self.customer_dir)) if os.path.exists(self.customer_dir) else 0
        }

        # Get database stats
        if os.path.exists(self.db_file):
            conn = sqlite3.connect(self.db_file)
            cursor = conn.execute("SELECT COUNT(*) FROM Attendance")
            metadata['attendance_records'] = cursor.fetchone()[0]

            cursor = conn.execute("SELECT COUNT(*) FROM Customers")
            metadata['customers_count'] = cursor.fetchone()[0]

            cursor = conn.execute("SELECT COUNT(*) FROM CustomerVisits")
            metadata['customer_visits'] = cursor.fetchone()[0]

            conn.close()

        metadata_path = os.path.join(backup_path, 'backup_info.txt')
        with open(metadata_path, 'w') as f:
            f.write("FRAMS Database Backup\n")
            f.write("=" * 60 + "\n\n")
            f.write(f"Timestamp: {metadata['timestamp']}\n")
            f.write(f"Database backed up: {metadata['database']}\n")
            f.write(f"Training images: {metadata['training_images']}\n")
            f.write(f"Customer images: {metadata['customer_images']}\n")

            if 'attendance_records' in metadata:
                f.write(f"\nDatabase Statistics:\n")
                f.write(f"  - Attendance records: {metadata['attendance_records']}\n")
                f.write(f"  - Customers: {metadata['customers_count']}\n")
                f.write(f"  - Customer visits: {metadata['customer_visits']}\n")

    def _compress_backup(self, backup_path):
        """Compress backup directory to ZIP"""
        zip_path = f"{backup_path}.zip"

        with zipfile.ZipFile(zip_path, 'w', zipfile.ZIP_DEFLATED) as zipf:
            for root, dirs, files in os.walk(backup_path):
                for file in files:
                    file_path = os.path.join(root, file)
                    arcname = os.path.relpath(file_path, self.backup_dir)
                    zipf.write(file_path, arcname)

        return zip_path

    def restore_backup(self, backup_path):
        """
        Restore from backup

        Args:
            backup_path (str): Path to backup directory or ZIP file

        Warning:
            This will overwrite current data!
        """
        print(f"⚠️  WARNING: This will overwrite current data!")
        confirm = input("Type 'yes' to continue: ")

        if confirm.lower() != 'yes':
            print("Restore cancelled")
            return

        print(f"🔄 Restoring from: {backup_path}")

        try:
            # Extract if ZIP
            if backup_path.endswith('.zip'):
                print("   📦 Extracting backup...")
                extract_path = backup_path.replace('.zip', '')
                with zipfile.ZipFile(backup_path, 'r') as zipf:
                    zipf.extractall(self.backup_dir)
                backup_path = extract_path

            # Restore database
            db_backup = os.path.join(backup_path, 'information.db')
            if os.path.exists(db_backup):
                print("   📊 Restoring database...")
                shutil.copy2(db_backup, self.db_file)

            # Restore training images
            training_backup = os.path.join(backup_path, 'Training images')
            if os.path.exists(training_backup):
                print("   📸 Restoring training images...")
                if os.path.exists(self.training_dir):
                    shutil.rmtree(self.training_dir)
                shutil.copytree(training_backup, self.training_dir)

            # Restore customer images
            customer_backup = os.path.join(backup_path, 'Customer images')
            if os.path.exists(customer_backup):
                print("   📸 Restoring customer images...")
                if os.path.exists(self.customer_dir):
                    shutil.rmtree(self.customer_dir)
                shutil.copytree(customer_backup, self.customer_dir)

            print("✅ Restore completed successfully!")

        except Exception as e:
            print(f"❌ Restore failed: {str(e)}")
            raise

    def list_backups(self):
        """List all available backups"""
        backups = []

        if not os.path.exists(self.backup_dir):
            return backups

        for item in os.listdir(self.backup_dir):
            item_path = os.path.join(self.backup_dir, item)

            if os.path.isdir(item_path) and item.startswith('backup_'):
                backups.append({
                    'name': item,
                    'path': item_path,
                    'type': 'directory',
                    'size': self._get_directory_size(item_path),
                    'timestamp': datetime.strptime(item.split('_')[1] + '_' + item.split('_')[2], '%Y%m%d_%H%M%S')
                })
            elif item.endswith('.zip') and item.startswith('backup_'):
                backups.append({
                    'name': item,
                    'path': item_path,
                    'type': 'zip',
                    'size': os.path.getsize(item_path),
                    'timestamp': datetime.strptime(item.split('_')[1] + '_' + item.split('_')[2].replace('.zip', ''), '%Y%m%d_%H%M%S')
                })

        return sorted(backups, key=lambda x: x['timestamp'], reverse=True)

    def _get_directory_size(self, path):
        """Calculate directory size"""
        total = 0
        for root, dirs, files in os.walk(path):
            for file in files:
                total += os.path.getsize(os.path.join(root, file))
        return total

    def cleanup_old_backups(self, days=7):
        """
        Delete backups older than specified days

        Args:
            days (int): Delete backups older than this many days
        """
        print(f"🗑️  Cleaning up backups older than {days} days...")

        cutoff_date = datetime.now() - timedelta(days=days)
        deleted_count = 0

        for backup in self.list_backups():
            if backup['timestamp'] < cutoff_date:
                print(f"   Deleting: {backup['name']}")

                if backup['type'] == 'zip':
                    os.remove(backup['path'])
                else:
                    shutil.rmtree(backup['path'])

                deleted_count += 1

        print(f"✅ Deleted {deleted_count} old backups")


def format_size(size_bytes):
    """Format bytes to human readable"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"


def main():
    parser = argparse.ArgumentParser(description='FRAMS Database Backup Tool')
    parser.add_argument('--compress', action='store_true', help='Create compressed backup')
    parser.add_argument('--restore', metavar='PATH', help='Restore from backup')
    parser.add_argument('--list', action='store_true', help='List all backups')
    parser.add_argument('--auto-delete', type=int, metavar='DAYS', help='Delete backups older than N days')

    args = parser.parse_args()

    backup_manager = DatabaseBackup()

    try:
        # List backups
        if args.list:
            print("\n📋 Available Backups:")
            print("=" * 80)

            backups = backup_manager.list_backups()
            if not backups:
                print("No backups found")
            else:
                for backup in backups:
                    print(f"\n  Name: {backup['name']}")
                    print(f"  Type: {backup['type']}")
                    print(f"  Size: {format_size(backup['size'])}")
                    print(f"  Date: {backup['timestamp'].strftime('%Y-%m-%d %H:%M:%S')}")

            print("\n" + "=" * 80)

        # Restore
        elif args.restore:
            backup_manager.restore_backup(args.restore)

        # Auto-delete
        elif args.auto_delete:
            backup_manager.cleanup_old_backups(args.auto_delete)

        # Create backup
        else:
            backup_path = backup_manager.create_backup(compress=args.compress)

            # Auto-delete if enabled
            if args.auto_delete:
                backup_manager.cleanup_old_backups(args.auto_delete)

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return 1

    return 0


if __name__ == '__main__':
    exit(main())
