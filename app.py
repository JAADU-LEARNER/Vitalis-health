from flask import Flask, render_template, request, redirect, url_for
import sqlite3
import datetime

app = Flask(__name__)

def get_db_connection():
    conn = sqlite3.connect('/app/health.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def dashboard():
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM Users WHERE id = ?', (1,)).fetchone()
    appointments = conn.execute('SELECT * FROM Appointments WHERE user_id = ? ORDER BY id DESC LIMIT 2', (1,)).fetchall()
    notifications = conn.execute('SELECT * FROM Notifications WHERE user_id = ? ORDER BY id DESC LIMIT 2', (1,)).fetchall()
    conn.close()
    return render_template('dashboard.html', user=user, appointments=appointments, notifications=notifications)

@app.route('/appointments')
def appointments():
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM Users WHERE id = ?', (1,)).fetchone()
    next_appointment = conn.execute('SELECT * FROM Appointments WHERE user_id = ? AND status = ? ORDER BY id ASC LIMIT 1', (1, 'Scheduled')).fetchone()
    appointments = conn.execute('SELECT * FROM Appointments WHERE user_id = ? ORDER BY id DESC', (1,)).fetchall()
    conn.close()
    return render_template('appointments.html', user=user, next_appointment=next_appointment, appointments=appointments)

@app.route('/reports')
def reports():
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM Users WHERE id = ?', (1,)).fetchone()
    reports = conn.execute('SELECT * FROM MedicalReports WHERE user_id = ? ORDER BY date DESC', (1,)).fetchall()
    conn.close()
    return render_template('reports.html', user=user, reports=reports)

@app.route('/pharmacy')
def pharmacy():
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM Users WHERE id = ?', (1,)).fetchone()
    medications = conn.execute('SELECT * FROM PharmacyMedications').fetchall()
    conn.close()
    return render_template('pharmacy.html', user=user, medications=medications)

@app.route('/reviews')
def reviews():
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM Users WHERE id = ?', (1,)).fetchone()
    reviews = conn.execute('SELECT * FROM DoctorReviews WHERE user_id = ? ORDER BY id DESC', (1,)).fetchall()
    conn.close()
    return render_template('reviews.html', user=user, reviews=reviews)

@app.route('/profile', methods=('GET', 'POST'))
def profile():
    conn = get_db_connection()
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        conn.execute('UPDATE Users SET name = ?, email = ? WHERE id = ?', (name, email, 1))
        conn.commit()
        return redirect(url_for('profile'))

    user = conn.execute('SELECT * FROM Users WHERE id = ?', (1,)).fetchone()
    conn.close()
    return render_template('profile.html', user=user)

@app.route('/settings')
def settings():
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM Users WHERE id = ?', (1,)).fetchone()
    conn.close()
    return render_template('settings.html', user=user)

@app.route('/notifications')
def notifications():
    conn = get_db_connection()
    user = conn.execute('SELECT * FROM Users WHERE id = ?', (1,)).fetchone()
    notifications = conn.execute('SELECT * FROM Notifications WHERE user_id = ? ORDER BY id DESC', (1,)).fetchall()
    conn.close()
    return render_template('notifications.html', user=user, notifications=notifications)

@app.route('/ordering', methods=('GET', 'POST'))
def ordering():
    conn = get_db_connection()
    if request.method == 'POST':
        medication_name = request.form['medication_name']
        quantity = request.form['quantity']
        date = datetime.datetime.now().strftime("%Y-%m-%d")
        conn.execute('INSERT INTO MedicineOrders (user_id, medication_name, quantity, status, date) VALUES (?, ?, ?, ?, ?)',
                     (1, medication_name, quantity, 'Pending', date))
        conn.commit()
        return redirect(url_for('ordering'))

    user = conn.execute('SELECT * FROM Users WHERE id = ?', (1,)).fetchone()
    orders = conn.execute('SELECT * FROM MedicineOrders WHERE user_id = ? ORDER BY id DESC', (1,)).fetchall()
    conn.close()
    return render_template('ordering.html', user=user, orders=orders)

@app.route('/support', methods=('GET', 'POST'))
def support():
    conn = get_db_connection()
    if request.method == 'POST':
        subject = request.form['subject']
        message = request.form['message']
        conn.execute('INSERT INTO HelpSupport (user_id, subject, message, status) VALUES (?, ?, ?, ?)',
                     (1, subject, message, 'Open'))
        conn.commit()
        return redirect(url_for('support'))

    user = conn.execute('SELECT * FROM Users WHERE id = ?', (1,)).fetchone()
    tickets = conn.execute('SELECT * FROM HelpSupport WHERE user_id = ? ORDER BY id DESC', (1,)).fetchall()
    conn.close()
    return render_template('support.html', user=user, tickets=tickets)

if __name__ == '__main__':
    app.run(debug=True, port=5000)
