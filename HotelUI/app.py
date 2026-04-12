from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
app.secret_key = 'hotel_management_secret_key'

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mysql1234',  # MySQL root şifrenizi buraya yazın
    'database': 'hotel_management',
    'charset': 'utf8mb4',
    'collation': 'utf8mb4_general_ci',
    'use_unicode': True
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

# ─── DASHBOARD ───
@app.route('/')
def dashboard():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT COUNT(*) AS c FROM BOOKINGS")
    bookings = cur.fetchone()['c']
    cur.execute("SELECT COUNT(*) AS c FROM GUESTS")
    guests = cur.fetchone()['c']
    cur.execute("SELECT COUNT(*) AS c FROM PROPERTIES")
    properties = cur.fetchone()['c']
    cur.execute("SELECT COALESCE(SUM(Total_Amount),0) AS c FROM PAYMENTS")
    revenue = cur.fetchone()['c']
    cur.execute("SELECT COUNT(*) AS c FROM REVIEWS")
    reviews = cur.fetchone()['c']
    cur.execute("SELECT COALESCE(AVG(Rating),0) AS c FROM REVIEWS")
    avg_rating = round(cur.fetchone()['c'], 1)
    cur.close()
    db.close()
    return render_template('dashboard.html',
        bookings=bookings, guests=guests, properties=properties,
        revenue=revenue, reviews=reviews, avg_rating=avg_rating)

# ─── QUERY 1: Guests by property & month ───
@app.route('/guests', methods=['GET'])
def guests_page():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("SELECT Property_ID, Title, City FROM PROPERTIES")
    props = cur.fetchall()

    results = None
    sel_prop = request.args.get('property_id', '')
    sel_year = request.args.get('year', '2026')
    sel_month = request.args.get('month', '')

    if sel_prop and sel_month:
        cur.execute("""
            SELECT DISTINCT u.Full_Name, u.Email, u.Phone,
                   b.Booking_ID, b.CheckIn_Date, b.CheckOut_Date
            FROM USERS u
            JOIN GUESTS g ON g.User_ID = u.User_ID
            JOIN BOOKING_DETAILS bd ON bd.Guest_ID = g.Guest_ID
            JOIN BOOKINGS b ON b.Booking_ID = bd.Booking_ID
            JOIN ROOMS r ON r.Room_ID = b.Room_ID
            WHERE r.Property_ID = %s
              AND YEAR(b.CheckIn_Date) = %s
              AND MONTH(b.CheckIn_Date) = %s
            ORDER BY b.CheckIn_Date
        """, (sel_prop, sel_year, sel_month))
        results = cur.fetchall()

    cur.close()
    db.close()
    return render_template('guests.html', properties=props, results=results,
        sel_prop=sel_prop, sel_year=sel_year, sel_month=sel_month)

# ─── QUERY 2: Properties overview ───
@app.route('/properties')
def properties_page():
    db = get_db()
    cur = db.cursor(dictionary=True)
    cur.execute("""
        SELECT p.Property_ID, p.Title, p.City, p.Address,
               u.Full_Name AS Host_Name, u.Email AS Host_Email,
               COUNT(DISTINCT b.Booking_ID) AS Total_Bookings
        FROM PROPERTIES p
        JOIN HOSTS h ON h.Host_ID = p.Host_ID
        JOIN USERS u ON u.User_ID = h.User_ID
        LEFT JOIN ROOMS r ON r.Property_ID = p.Property_ID
        LEFT JOIN BOOKINGS b ON b.Room_ID = r.Room_ID
        GROUP BY p.Property_ID, p.Title, p.City, p.Address, u.Full_Name, u.Email
        ORDER BY Total_Bookings DESC
    """)
    results = cur.fetchall()
    cur.close()
    db.close()
    return render_template('properties.html', results=results)

# ─── QUERY 3: Change booking date ───
@app.route('/manage-booking', methods=['GET', 'POST'])
def manage_booking():
    db = get_db()
    cur = db.cursor(dictionary=True)

    if request.method == 'POST':
        action = request.form.get('action')
        booking_id = request.form.get('booking_id')

        if action == 'update_date':
            checkin = request.form.get('checkin')
            checkout = request.form.get('checkout')
            cur.execute("""
                UPDATE BOOKINGS SET CheckIn_Date=%s, CheckOut_Date=%s
                WHERE Booking_ID=%s
            """, (checkin, checkout, booking_id))
            db.commit()
            flash(f'Booking #{booking_id} dates updated successfully.', 'success')

        elif action == 'delete':
            cur.execute("DELETE FROM BOOKINGS WHERE Booking_ID=%s", (booking_id,))
            db.commit()
            flash(f'Booking #{booking_id} removed successfully.', 'success')

        cur.close()
        db.close()
        return redirect(url_for('manage_booking'))

    cur.execute("""
        SELECT b.Booking_ID, b.CheckIn_Date, b.CheckOut_Date, b.Status,
               p.Title AS Property, r.Room_Type,
               u.Full_Name AS Guest_Name
        FROM BOOKINGS b
        JOIN ROOMS r ON r.Room_ID = b.Room_ID
        JOIN PROPERTIES p ON p.Property_ID = r.Property_ID
        JOIN BOOKING_DETAILS bd ON bd.Booking_ID = b.Booking_ID AND bd.Is_Primary = TRUE
        JOIN GUESTS g ON g.Guest_ID = bd.Guest_ID
        JOIN USERS u ON u.User_ID = g.User_ID
        ORDER BY b.CheckIn_Date DESC
    """)
    bookings = cur.fetchall()
    cur.close()
    db.close()
    return render_template('manage_booking.html', bookings=bookings)

# ─── QUERY 4: Make a payment ───
@app.route('/payments', methods=['GET', 'POST'])
def payments_page():
    db = get_db()
    cur = db.cursor(dictionary=True)

    if request.method == 'POST':
        booking_id = request.form.get('booking_id')
        method_id = request.form.get('method_id')
        amount = request.form.get('amount')
        inst_count = int(request.form.get('installments', 1))

        cur.execute("""
            INSERT INTO PAYMENTS (Booking_ID, Method_ID, Total_Amount, Payment_Date)
            VALUES (%s, %s, %s, CURDATE())
        """, (booking_id, method_id, amount))
        payment_id = cur.lastrowid

        inst_amount = round(float(amount) / inst_count, 2)
        for i in range(inst_count):
            cur.execute("""
                INSERT INTO INSTALLMENTS (Payment_ID, Due_Date, Amount, Status)
                VALUES (%s, DATE_ADD(CURDATE(), INTERVAL %s MONTH), %s, 'Pending')
            """, (payment_id, i + 1, inst_amount))

        db.commit()
        flash(f'Payment of ${amount} recorded with {inst_count} installment(s).', 'success')
        cur.close()
        db.close()
        return redirect(url_for('payments_page'))

    cur.execute("""
        SELECT b.Booking_ID, p.Title AS Property, r.Room_Type,
               u.Full_Name AS Guest_Name
        FROM BOOKINGS b
        JOIN ROOMS r ON r.Room_ID = b.Room_ID
        JOIN PROPERTIES p ON p.Property_ID = r.Property_ID
        JOIN BOOKING_DETAILS bd ON bd.Booking_ID = b.Booking_ID AND bd.Is_Primary = TRUE
        JOIN GUESTS g ON g.Guest_ID = bd.Guest_ID
        JOIN USERS u ON u.User_ID = g.User_ID
        ORDER BY b.Booking_ID
    """)
    bookings = cur.fetchall()

    cur.execute("""
        SELECT pm.Method_ID, u.Full_Name, pm.Card_Type, pm.Card_Last4
        FROM PAYMENT_METHODS pm
        JOIN GUESTS g ON g.Guest_ID = pm.Guest_ID
        JOIN USERS u ON u.User_ID = g.User_ID
    """)
    methods = cur.fetchall()

    cur.execute("""
        SELECT p.Payment_ID, p.Total_Amount, p.Payment_Date,
               b.Booking_ID, pr.Title AS Property,
               u.Full_Name AS Guest_Name, pm.Card_Type, pm.Card_Last4
        FROM PAYMENTS p
        JOIN BOOKINGS b ON b.Booking_ID = p.Booking_ID
        JOIN ROOMS r ON r.Room_ID = b.Room_ID
        JOIN PROPERTIES pr ON pr.Property_ID = r.Property_ID
        JOIN BOOKING_DETAILS bd ON bd.Booking_ID = b.Booking_ID AND bd.Is_Primary = TRUE
        JOIN GUESTS g ON g.Guest_ID = bd.Guest_ID
        JOIN USERS u ON u.User_ID = g.User_ID
        LEFT JOIN PAYMENT_METHODS pm ON pm.Method_ID = p.Method_ID
        ORDER BY p.Payment_Date DESC
    """)
    payments = cur.fetchall()

    cur.close()
    db.close()
    return render_template('payments.html', bookings=bookings, methods=methods, payments=payments)

# ─── QUERY 5: Remove booking (handled in manage_booking POST) ───

if __name__ == '__main__':
    app.run(debug=True, port=5000)
