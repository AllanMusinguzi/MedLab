# utils/database.py
import sqlite3
from datetime import datetime, timedelta
import random

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('healthcare.db')
        self.create_tables()
        self.populate_sample_data()

    def create_tables(self):
        cursor = self.conn.cursor()
        
        # Create necessary tables
        cursor.executescript('''
            CREATE TABLE IF NOT EXISTS patients (
                id INTEGER PRIMARY KEY,
                name TEXT,
                age INTEGER,
                contact TEXT,
                status TEXT
            );

            CREATE TABLE IF NOT EXISTS tests (
                id INTEGER PRIMARY KEY,
                patient_id INTEGER,
                type TEXT,
                date TEXT,
                status TEXT,
                FOREIGN KEY (patient_id) REFERENCES patients (id)
            );

            CREATE TABLE IF NOT EXISTS results (
                id INTEGER PRIMARY KEY,
                test_id INTEGER,
                result TEXT,
                date TEXT,
                FOREIGN KEY (test_id) REFERENCES tests (id)
            );

            CREATE TABLE IF NOT EXISTS activities (
                id INTEGER PRIMARY KEY,
                timestamp TEXT,
                description TEXT
            );
        ''')
        
        self.conn.commit()

    def populate_sample_data(self):
        cursor = self.conn.cursor()
        
        # Only populate if tables are empty
        if cursor.execute("SELECT COUNT(*) FROM patients").fetchone()[0] == 0:
            # Add sample patients
            patients = [
                ('John Doe', 45, '555-0101', 'Active'),
                ('Jane Smith', 32, '555-0102', 'Active'),
                ('Bob Johnson', 58, '555-0103', 'Inactive')
            ]
            cursor.executemany(
                "INSERT INTO patients (name, age, contact, status) VALUES (?, ?, ?, ?)",
                patients
            )

            # Add sample tests and results
            # Add sample activities
            self.conn.commit()

    def get_dashboard_stats(self):
        cursor = self.conn.cursor()
        
        return {
            'total_patients': cursor.execute("SELECT COUNT(*) FROM patients").fetchone()[0],
            'pending_tests': cursor.execute("SELECT COUNT(*) FROM tests WHERE status='Pending'").fetchone()[0],
            'completed_tests': cursor.execute("SELECT COUNT(*) FROM tests WHERE status='Completed'").fetchone()[0],
            'critical_cases': cursor.execute("SELECT COUNT(*) FROM results WHERE result='Critical'").fetchone()[0]
        }

    def get_monthly_patients_data(self):
        # Simulate monthly data for the past 6 months
        months = []
        data = []
        current_date = datetime.now()
        
        for i in range(6):
            date = current_date - timedelta(days=30*i)
            months.append(date.strftime('%B'))
            data.append(random.randint(50, 200))
            
        return list(zip(reversed(months), reversed(data)))

    def get_test_results_distribution(self):
        cursor = self.conn.cursor()
        results = cursor.execute(
            "SELECT result, COUNT(*) FROM results GROUP BY result"
        ).fetchall()
        return results or [('Normal', 65), ('Abnormal', 25), ('Critical', 10)]

    def get_recent_activities(self, limit=5):
        cursor = self.conn.cursor()
        activities = cursor.execute(
            "SELECT timestamp, description FROM activities ORDER BY timestamp DESC LIMIT ?",
            (limit,)
        ).fetchall()
        
        # Return sample data if no activities exist
        if not activities:
            return [
                {
                    'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M'),
                    'description': 'New patient registered: John Doe'
                },
                {
                    'timestamp': (datetime.now() - timedelta(hours=2)).strftime('%Y-%m-%d %H:%M'),
                    'description': 'Test results updated for patient ID: 1001'
                }
            ]
        
        return [{'timestamp': a[0], 'description': a[1]} for a in activities]
