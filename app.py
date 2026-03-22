import os
from flask import Flask, render_template, request, redirect, url_for, session, flash
from werkzeug.utils import secure_filename
from werkzeug.security import generate_password_hash, check_password_hash
from functools import wraps
import sqlite3
import datetime

app = Flask(__name__)
app.secret_key = 'super_secret_health_key_for_development'

def get_db_connection():
    conn = sqlite3.connect('/app/health.db')
    conn.row_factory = sqlite3.Row
    return conn

def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/signup', methods=('GET', 'POST'))
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM Users WHERE email = ?', (email,)).fetchone()

        if user:
            flash('Email address already exists', 'error')
            conn.close()
            return redirect(url_for('signup'))

        hashed_password = generate_password_hash(password)
        conn.execute('INSERT INTO Users (name, email, password) VALUES (?, ?, ?)',
                     (name, email, hashed_password))
        conn.commit()
        conn.close()

        flash('Account created successfully. Please log in.', 'success')
        return redirect(url_for('login'))

    return render_template('signup.html')

@app.route('/login', methods=('GET', 'POST'))
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = get_db_connection()
        user = conn.execute('SELECT * FROM Users WHERE email = ?', (email,)).fetchone()
        conn.close()

        if user and check_password_hash(user['password'], password):
            session.clear()
            session['user_id'] = user['id']
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid email or password', 'error')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def dashboard():
    user_id = session['user_id']
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM Users WHERE id = ?', (user_id,)).fetchone()
    appointments = conn.execute('SELECT * FROM Appointments WHERE user_id = ? ORDER BY id DESC LIMIT 2', (user_id,)).fetchall()
    notifications = conn.execute('SELECT * FROM Notifications WHERE user_id = ? ORDER BY id DESC LIMIT 2', (user_id,)).fetchall()
    conn.close()
    return render_template('dashboard.html', user=user, appointments=appointments, notifications=notifications)

@app.route('/appointments', methods=('GET', 'POST'))
@login_required
def appointments():
    user_id = session['user_id']
    conn = get_db_connection()
    if request.method == 'POST':
        import random
        doctor_name = request.form['doctor_name']
        specialty = request.form['specialty']
        clinic = request.form['clinic']
        date_time = request.form['date_time']
        appt_type = request.form['type']

        # Simulate wait time calculation based on date/time logic
        wait_time = random.randint(5, 45) # Random wait time between 5 and 45 minutes

        conn.execute('INSERT INTO Appointments (user_id, doctor_name, specialty, clinic, date_time, status, type, wait_time) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                     (user_id, doctor_name, specialty, clinic, date_time, 'Scheduled', appt_type, wait_time))

        # Add a notification
        conn.execute('INSERT INTO Notifications (user_id, title, message, time) VALUES (?, ?, ?, ?)',
                     (user_id, 'Upcoming Appointment', f"Appointment scheduled with {doctor_name} on {date_time}", 'Just now'))
        conn.commit()
        return redirect(url_for('appointments'))

    user = conn.execute('SELECT * FROM Users WHERE id = ?', (user_id,)).fetchone()
    next_appointment = conn.execute('SELECT * FROM Appointments WHERE user_id = ? AND status = ? ORDER BY id ASC LIMIT 1', (user_id, 'Scheduled')).fetchone()
    appointments = conn.execute('SELECT * FROM Appointments WHERE user_id = ? ORDER BY id DESC', (user_id,)).fetchall()
    conn.close()
    return render_template('appointments.html', user=user, next_appointment=next_appointment, appointments=appointments)

UPLOAD_FOLDER = os.path.join(app.root_path, 'static', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

import datetime

@app.template_filter('format_datetime')
def format_datetime(value):
    try:
        # datetime-local format: 2026-10-24T14:30
        dt = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M')
        return dt.strftime('%b %d, %I:%M %p').upper()
    except:
        return value

@app.template_filter('format_month')
def format_month(value):
    try:
        dt = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M')
        return dt.strftime('%b').upper()
    except:
        return value[:3]

@app.template_filter('format_day')
def format_day(value):
    try:
        dt = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M')
        return dt.strftime('%d')
    except:
        return value[4:6]

@app.template_filter('format_time')
def format_time(value):
    try:
        dt = datetime.datetime.strptime(value, '%Y-%m-%dT%H:%M')
        return dt.strftime('%I:%M %p')
    except:
        return value.split(',')[1] if ',' in value else value



@app.route('/reports', methods=('GET', 'POST'))
@login_required
def reports():
    user_id = session['user_id']
    conn = get_db_connection()
    if request.method == 'POST':
        title = request.form['title']
        description = request.form['description']
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        file = request.files.get('file')
        file_path = None
        if file and file.filename != '':
            filename = secure_filename(file.filename)
            # Make filename unique per user to prevent overrides
            unique_filename = f"u{user_id}_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}_{filename}"
            save_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
            file.save(save_path)
            file_path = f"uploads/{unique_filename}"

        conn.execute('INSERT INTO MedicalReports (user_id, title, date, description, file_path) VALUES (?, ?, ?, ?, ?)',
                     (user_id, title, date, description, file_path))
        conn.commit()
        return redirect(url_for('reports'))

    user = conn.execute('SELECT * FROM Users WHERE id = ?', (user_id,)).fetchone()
    reports = conn.execute('SELECT * FROM MedicalReports WHERE user_id = ? ORDER BY date DESC', (user_id,)).fetchall()
    conn.close()
    return render_template('reports.html', user=user, reports=reports)

@app.route('/pharmacy', methods=('GET', 'POST'))
@login_required
def pharmacy():
    user_id = session['user_id']
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name']
        dosage = request.form['dosage']
        instructions = request.form['instructions']
        frequency = request.form.get('frequency', 'Daily')
        reminder_time = request.form.get('reminder_time', '')

        conn.execute('INSERT INTO PharmacyMedications (user_id, name, dosage, instructions, frequency, reminder_time) VALUES (?, ?, ?, ?, ?, ?)',
                     (user_id, name, dosage, instructions, frequency, reminder_time))

        # Add a notification
        conn.execute('INSERT INTO Notifications (user_id, title, message, time) VALUES (?, ?, ?, ?)',
                     (user_id, 'Medicine Reminder Created', f"Reminder set for {name} ({dosage}) {frequency} at {reminder_time}", 'Just now'))
        conn.commit()
        return redirect(url_for('pharmacy'))

    user = conn.execute('SELECT * FROM Users WHERE id = ?', (user_id,)).fetchone()
    medications = conn.execute('SELECT * FROM PharmacyMedications WHERE user_id = ?', (user_id,)).fetchall()
    conn.close()
    return render_template('pharmacy.html', user=user, medications=medications)

@app.route('/reviews')
@login_required
def reviews():
    user_id = session['user_id']
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM Users WHERE id = ?', (user_id,)).fetchone()
    reviews = conn.execute('SELECT * FROM DoctorReviews WHERE user_id = ? ORDER BY id DESC', (user_id,)).fetchall()
    conn.close()
    return render_template('reviews.html', user=user, reviews=reviews)

@app.route('/profile', methods=('GET', 'POST'))
@login_required
def profile():
    user_id = session['user_id']
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']

        # Optionally allow password update here, but omitted for simplicity

        conn.execute('UPDATE Users SET name = ?, email = ? WHERE id = ?', (name, email, user_id))
        conn.commit()
        return redirect(url_for('profile'))

    user = conn.execute('SELECT * FROM Users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return render_template('profile.html', user=user)

@app.route('/settings')
@login_required
def settings():
    user_id = session['user_id']
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM Users WHERE id = ?', (user_id,)).fetchone()
    conn.close()
    return render_template('settings.html', user=user)

@app.route('/notifications')
@login_required
def notifications():
    user_id = session['user_id']
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM Users WHERE id = ?', (user_id,)).fetchone()
    notifications = conn.execute('SELECT * FROM Notifications WHERE user_id = ? ORDER BY id DESC', (user_id,)).fetchall()
    conn.close()
    return render_template('notifications.html', user=user, notifications=notifications)

@app.route('/ordering', methods=('GET', 'POST'))
@login_required
def ordering():
    user_id = session['user_id']
    conn = get_db_connection()
    if request.method == 'POST':
        medication_name = request.form['medication_name']
        quantity = request.form['quantity']
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        conn.execute('INSERT INTO MedicineOrders (user_id, medication_name, quantity, status, date) VALUES (?, ?, ?, ?, ?)',
                     (user_id, medication_name, quantity, 'Pending', date))
        conn.commit()
        return redirect(url_for('ordering'))

    user = conn.execute('SELECT * FROM Users WHERE id = ?', (user_id,)).fetchone()
    orders = conn.execute('SELECT * FROM MedicineOrders WHERE user_id = ? ORDER BY id DESC', (user_id,)).fetchall()
    conn.close()
    return render_template('ordering.html', user=user, orders=orders)

@app.route('/support', methods=('GET', 'POST'))
@login_required
def support():
    user_id = session['user_id']
    conn = get_db_connection()
    if request.method == 'POST':
        subject = request.form['subject']
        message = request.form['message']
        conn.execute('INSERT INTO HelpSupport (user_id, subject, message, status) VALUES (?, ?, ?, ?)',
                     (user_id, subject, message, 'Open'))
        conn.commit()
        return redirect(url_for('support'))

    user = conn.execute('SELECT * FROM Users WHERE id = ?', (user_id,)).fetchone()
    tickets = conn.execute('SELECT * FROM HelpSupport WHERE user_id = ? ORDER BY id DESC', (user_id,)).fetchall()
    conn.close()
    return render_template('support.html', user=user, tickets=tickets)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
