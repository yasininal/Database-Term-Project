# -*- coding: utf-8 -*-
import mysql.connector
from werkzeug.security import generate_password_hash

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mysql1234',
    'database': 'airbnb_clone'
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

def populate():
    db = get_db()
    cur = db.cursor()

    pw = generate_password_hash('password123')

    # 1. NEW USERS
    new_users = [
        ('Zeynep Hanim', 'zeynep@example.com', '05321112233', 'host'),
        ('Burak Yilmaz',  'burak@example.com',  '05444556677', 'host'),
        ('Selin Arslan',  'selin@example.com',  '05559991122', 'guest'),
        ('Emre Demir',    'emre@example.com',   '05332223344', 'guest'),
        ('Ayse Kaya',     'ayse@example.com',   '05446667788', 'guest'),
    ]

    user_ids = {}
    for full_name, email, phone, role in new_users:
        try:
            cur.execute(
                "INSERT INTO Users (full_name, email, phone, password_hash, role) VALUES (%s,%s,%s,%s,%s)",
                (full_name, email, phone, pw, role)
            )
            db.commit()
            user_ids[email] = cur.lastrowid
            print(f"[OK] User added: {full_name} (id={cur.lastrowid})")
        except mysql.connector.errors.IntegrityError:
            cur.execute("SELECT user_id FROM Users WHERE email=%s", (email,))
            row = cur.fetchone()
            user_ids[email] = row[0]
            print(f"[SKIP] User exists: {email} (id={row[0]})")

    zeynep_id = user_ids['zeynep@example.com']
    burak_id  = user_ids['burak@example.com']
    selin_id  = user_ids['selin@example.com']
    emre_id   = user_ids['emre@example.com']
    ayse_id   = user_ids['ayse@example.com']

    # 2. NEW PROPERTIES
    new_properties = [
        (zeynep_id, 'Kapadokya Magara Evi',
         'Urgup\'un kalbinde, sicak tas duvarlar ve balon manzarasiyla tarihin icinde bir konaklama deneyimi.',
         'Villa', 'Entire place', 'Nevsehir', 'Urgup', 950.00, 4),
        (burak_id, 'Alacati Tas Butik',
         'Alacati\'nin cicekli sokaklari arasinda, ruzgar surfune adim atma mesafesinde geleneksel tas ev.',
         'House', 'Entire place', 'Izmir', 'Alacati', 1100.00, 6),
        (burak_id, 'Bodrum Sonsuzluk Villas',
         'Ege\'nin mavisine acilan sonsuzluk havuzlu, modern ve luks Bodrum villasi. Yat cevresi, gun batimi manzarasi.',
         'Villa', 'Entire place', 'Mugla', 'Bodrum', 2200.00, 8),
    ]

    prop_ids = {}
    for prop in new_properties:
        cur.execute("""
            INSERT INTO Properties
              (host_id, title, description, property_type, room_type, city, district, base_price, max_guests)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, prop)
        db.commit()
        pid = cur.lastrowid
        prop_ids[prop[1]] = pid
        print(f"[OK] Property added: {prop[1]} (id={pid})")

    kapadokya_id = prop_ids['Kapadokya Magara Evi']
    alacati_id   = prop_ids['Alacati Tas Butik']
    bodrum_id    = prop_ids['Bodrum Sonsuzluk Villas']

    # 3. PHOTOS
    photos = [
        (kapadokya_id, 'kapadokya_ext.png',  True,  0),
        (kapadokya_id, 'kapadokya_int_1.png', False, 1),
        (kapadokya_id, 'kapadokya_int_2.png', False, 2),
        (alacati_id,   'alacati_ext.png',     True,  0),
        (alacati_id,   'alacati_int_1.png',   False, 1),
        (alacati_id,   'alacati_int_2.png',   False, 2),
        (bodrum_id,    'bodrum_ext.png',       True,  0),
        (bodrum_id,    'bodrum_int_1.png',     False, 1),
        (bodrum_id,    'bodrum_int_2.png',     False, 2),
    ]
    for p_id, url, primary, order in photos:
        cur.execute(
            "INSERT INTO PropertyPhotos (property_id, image_url, is_primary, sort_order) VALUES (%s,%s,%s,%s)",
            (p_id, url, primary, order)
        )
    db.commit()
    print("[OK] Photos added")

    # 4. AMENITIES
    cur.execute("SELECT amenity_id, name FROM Amenities")
    amenity_map = {row[1]: row[0] for row in cur.fetchall()}
    needed = ['WiFi', 'Havuz', 'Klima', 'Mutfak', 'Otopark', 'TV']
    for name in needed:
        if name not in amenity_map:
            cur.execute("INSERT INTO Amenities (name) VALUES (%s)", (name,))
            db.commit()
            amenity_map[name] = cur.lastrowid

    prop_amenities = [
        (kapadokya_id, amenity_map['WiFi']),
        (kapadokya_id, amenity_map['Klima']),
        (kapadokya_id, amenity_map['TV']),
        (alacati_id,   amenity_map['WiFi']),
        (alacati_id,   amenity_map['Mutfak']),
        (alacati_id,   amenity_map['Klima']),
        (bodrum_id,    amenity_map['WiFi']),
        (bodrum_id,    amenity_map['Havuz']),
        (bodrum_id,    amenity_map['Klima']),
        (bodrum_id,    amenity_map['Otopark']),
    ]
    for pid, aid in prop_amenities:
        try:
            cur.execute("INSERT INTO PropertyAmenities (property_id, amenity_id) VALUES (%s,%s)", (pid, aid))
        except:
            pass
    db.commit()
    print("[OK] Amenities added")

    # 5. BOOKINGS
    cur.execute("SELECT user_id FROM Users WHERE email='guest@example.com'")
    mehmet_id = cur.fetchone()[0]

    bookings = [
        (kapadokya_id, mehmet_id, '2026-03-10', '2026-03-13', 2,  2850.00,  'completed'),
        (kapadokya_id, selin_id,  '2026-05-20', '2026-05-23', 2,  2850.00,  'confirmed'),
        (alacati_id,   emre_id,   '2026-05-01', '2026-05-05', 3,  4400.00,  'confirmed'),
        (alacati_id,   ayse_id,   '2026-03-15', '2026-03-18', 4,  3300.00,  'completed'),
        (bodrum_id,    mehmet_id, '2026-07-01', '2026-07-07', 5, 13200.00,  'confirmed'),
        (bodrum_id,    selin_id,  '2026-08-10', '2026-08-14', 2,  8800.00,  'pending'),
    ]

    booking_ids = []
    for b in bookings:
        cur.execute("""
            INSERT INTO Bookings
              (property_id, guest_id, check_in, check_out, guest_count, total_price, status)
            VALUES (%s,%s,%s,%s,%s,%s,%s)
        """, b)
        db.commit()
        booking_ids.append(cur.lastrowid)
        print(f"[OK] Booking added: id={cur.lastrowid}")

    # 6. PAYMENTS
    payments = [
        (booking_ids[0], 2850.00,  'Credit Card',  'completed'),
        (booking_ids[2], 4400.00,  'Credit Card',  'completed'),
        (booking_ids[3], 3300.00,  'Bank Transfer', 'completed'),
        (booking_ids[4], 13200.00, 'Credit Card',  'completed'),
    ]
    for b_id, amount, method, status in payments:
        cur.execute(
            "INSERT INTO Payments (booking_id, amount, payment_method, payment_status) VALUES (%s,%s,%s,%s)",
            (b_id, amount, method, status)
        )
    db.commit()
    print("[OK] Payments added")

    # 7. REVIEWS
    reviews = [
        (booking_ids[0], mehmet_id, kapadokya_id, 5, 'Inanilmaz bir deneyim! Magara odasi, balon manzarasi, her sey mukemmeldi.'),
        (booking_ids[3], ayse_id,   alacati_id,   4, 'Alacati\'nin ruhunu yansitan sirin bir yer. Kahvalti harika, sadece otopark zor.'),
    ]
    for b_id, g_id, p_id, rating, comment in reviews:
        try:
            cur.execute(
                "INSERT INTO Reviews (booking_id, guest_id, property_id, rating, comment) VALUES (%s,%s,%s,%s,%s)",
                (b_id, g_id, p_id, rating, comment)
            )
        except Exception as e:
            print(f"[WARN] Review skip: {e}")
    db.commit()
    print("[OK] Reviews added")

    cur.close()
    db.close()
    print("\n[DONE] All data inserted successfully!")
    print("       +5 users, +3 properties, +9 photos, +6 bookings, +4 payments, +2 reviews")

if __name__ == '__main__':
    populate()
