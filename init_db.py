import sqlite3
import os
from werkzeug.security import generate_password_hash

def init_db():
    if os.path.exists('/app/health.db'):
        os.remove('/app/health.db')

    conn = sqlite3.connect('/app/health.db')
    cursor = conn.cursor()

    # Create Users table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS Users (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            email TEXT NOT NULL UNIQUE,
            password TEXT NOT NULL
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
            user_id INTEGER,
            name TEXT NOT NULL,
            dosage TEXT,
            instructions TEXT,
            FOREIGN KEY (user_id) REFERENCES Users(id)
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
    hashed_pw = generate_password_hash("password123")
    cursor.execute("INSERT INTO Users (name, email, password) VALUES (?, ?, ?)",
                   ("Julian", "julian@example.com", hashed_pw))

    user_id = cursor.lastrowid

    # Check if there's data in Appointments before inserting
    cursor.execute("INSERT INTO Appointments (user_id, doctor_name, specialty, clinic, date_time, status, type) VALUES (?, 'Dr. Elena Rostova', 'Cardiology', 'Diagnostic Center A', 'Today, 14:30', 'Scheduled', 'Virtual Consultation')", (user_id,))
    cursor.execute("INSERT INTO Appointments (user_id, doctor_name, specialty, clinic, date_time, status, type) VALUES (?, 'Dr. Marcus Thorne', 'Dermatology', 'Skin Health Institute', 'OCT 12, 10:00 AM', 'Completed', 'Video Consultation')", (user_id,))

    # Add other seed data...
    cursor.execute("INSERT INTO MedicalReports (user_id, title, date, description) VALUES (?, 'Lab Results - Fasting Bloodwork', '2023-10-01', 'Normal values across all metrics.')", (user_id,))

    cursor.execute("INSERT INTO PharmacyMedications (user_id, name, dosage, instructions) VALUES (?, 'Vitamin D3', '1000 IU', 'Take with breakfast')", (user_id,))

    cursor.execute("INSERT INTO Notifications (user_id, title, message, time) VALUES (?, 'Vitamin D3', 'Take with breakfast', '8:00 AM')", (user_id,))

    conn.commit()
    conn.close()

if __name__ == '__main__':
    init_db()
    print("Database initialized successfully.")
