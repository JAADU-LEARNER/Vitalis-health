import sqlite3
import os

def init_db():
    conn = sqlite3.connect('/app/health.db')
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE
        )
    ''')

    # Create Appointments table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Appointments (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            doctor_name TEXT NOT NULL,
            specialty TEXT,
            clinic TEXT,
            date_time TEXT NOT NULL,
            status TEXT,
            type TEXT,
            FOREIGN KEY (user_id) REFERENCES Users(id)
        )
    ''')

    # Create MedicalReports table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MedicalReports (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            description TEXT,
            file_path TEXT,
            FOREIGN KEY (user_id) REFERENCES Users(id)
        )
    ''')

    # Create PharmacyMedications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS PharmacyMedications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            dosage TEXT,
            instructions TEXT
        )
    ''')

    # Create DoctorReviews table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS DoctorReviews (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            doctor_name TEXT NOT NULL,
            rating INTEGER NOT NULL,
            review TEXT,
            FOREIGN KEY (user_id) REFERENCES Users(id)
        )
    ''')

    # Create Notifications table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Notifications (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            title TEXT NOT NULL,
            message TEXT,
            time TEXT,
            FOREIGN KEY (user_id) REFERENCES Users(id)
        )
    ''')

    # Create MedicineOrders table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS MedicineOrders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            medication_name TEXT NOT NULL,
            quantity INTEGER,
            status TEXT,
            date TEXT,
            FOREIGN KEY (user_id) REFERENCES Users(id)
        )
    ''')

    # Create HelpSupport table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS HelpSupport (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            subject TEXT NOT NULL,
            message TEXT NOT NULL,
            status TEXT,
            FOREIGN KEY (user_id) REFERENCES Users(id)
        )
    ''')

    # Insert sample seed data
    cursor.execute("INSERT OR IGNORE INTO Users (id, name, email) VALUES (1, 'Julian', 'julian@example.com')")

    # Check if there's data in Appointments before inserting
    cursor.execute("SELECT COUNT(*) FROM Appointments")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO Appointments (user_id, doctor_name, specialty, clinic, date_time, status, type) VALUES (1, 'Dr. Elena Rostova', 'Cardiology', 'Diagnostic Center A', 'Today, 14:30', 'Scheduled', 'Virtual Consultation')")
        cursor.execute("INSERT INTO Appointments (user_id, doctor_name, specialty, clinic, date_time, status, type) VALUES (1, 'Dr. Marcus Thorne', 'Dermatology', 'Skin Health Institute', 'OCT 12, 10:00 AM', 'Completed', 'Video Consultation')")

    # Add other seed data...
    cursor.execute("SELECT COUNT(*) FROM MedicalReports")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO MedicalReports (user_id, title, date, description) VALUES (1, 'Lab Results - Fasting Bloodwork', '2023-10-01', 'Normal values across all metrics.')")

    cursor.execute("SELECT COUNT(*) FROM PharmacyMedications")
    if cursor.fetchone()[0] == 0:
         cursor.execute("INSERT INTO PharmacyMedications (name, dosage, instructions) VALUES ('Vitamin D3', '1000 IU', 'Take with breakfast')")

    cursor.execute("SELECT COUNT(*) FROM Notifications")
    if cursor.fetchone()[0] == 0:
        cursor.execute("INSERT INTO Notifications (user_id, title, message, time) VALUES (1, 'Vitamin D3', 'Take with breakfast', '8:00 AM')")

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
