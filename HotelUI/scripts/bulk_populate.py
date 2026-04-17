# -*- coding: utf-8 -*-
"""
bulk_populate.py — Cok sayida ilan, kullanici, rezervasyon ve yorum ekler.
Mevcut 9 fotograf setini (villa/studio/loft/kapadokya/alacati/bodrum) 
farkli sehir ve isimlerde dondurek kullanir.
"""
import mysql.connector
from werkzeug.security import generate_password_hash
import random

DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'mysql1234',
    'database': 'airbnb_clone'
}

def get_db():
    return mysql.connector.connect(**DB_CONFIG)

# Photo sets (ext, int1, int2)
PHOTO_SETS = {
    'villa':     ('luxurious_villa_istanbul.png', 'villa_int_1.png',     'villa_int_2.png'),
    'studio':    ('cozy_studio_beach.png',        'studio_int_1.png',    'studio_int_2.png'),
    'loft':      ('loft_ext.png',                 'loft_int_1.png',      'loft_int_2.png'),
    'kapadokya': ('kapadokya_ext.png',            'kapadokya_int_1.png', 'kapadokya_int_2.png'),
    'alacati':   ('alacati_ext.png',              'alacati_int_1.png',   'alacati_int_2.png'),
    'bodrum':    ('bodrum_ext.png',               'bodrum_int_1.png',    'bodrum_int_2.png'),
}

# (title, description, type, room_type, city, district, price, max_guests, photo_set)
PROPERTIES_TO_ADD = [
    # --- ISTANBUL ---
    ('Sarıyer Bogazici Konak', 'Bogaz kiyisinda tarihi konak, kendi iskele, bol yesillik.',
     'Villa', 'Entire place', 'Istanbul', 'Sariyer', 1450.00, 8, 'villa'),
    ('Uskudar Kozy Apart', 'Asya yakasinin kalbinde, Bogazin karsi yakasindan sehir manzarasi.',
     'Apartment', 'Entire place', 'Istanbul', 'Uskudar', 620.00, 3, 'studio'),
    ('Moda Chic Loft', 'Bars sokagina yurume mesafesinde, endustriyel tasarimli modern daire.',
     'Apartment', 'Entire place', 'Istanbul', 'Kadikoy', 880.00, 4, 'loft'),
    ('Cihangir Sanat Evi', 'Galeriler ve kafelerle cevrilmis, 100 yillik Rum pasajinda esoerlesen daire.',
     'House', 'Private room', 'Istanbul', 'Cihangir', 550.00, 2, 'loft'),
    ('Bebek Su Ustu Residence', 'Bogazin tam kenarinda lüks rezidans, marina manzarali balkon.',
     'Apartment', 'Entire place', 'Istanbul', 'Bebek', 1900.00, 5, 'villa'),

    # --- ANTALYA ---
    ('Kas Akdeniz Konagi', 'Masmavi Akdeniz manzarali, cicek bahceli, takilme keyfi yuksek apart.',
     'House', 'Entire place', 'Antalya', 'Kas', 750.00, 4, 'alacati'),
    ('Side Antik Suit', 'Apollo Tapinaginin hemen yaninda, tarihle ic ice suit otel odasi.',
     'Apartment', 'Private room', 'Antalya', 'Side', 480.00, 2, 'studio'),
    ('Olympos Bungalov', 'Olimpos sahilinde ahsap bungalov, plaja 2 dakika, huzur dolu.',
     'House', 'Entire place', 'Antalya', 'Olympos', 420.00, 3, 'kapadokya'),

    # --- IZMIR ---
    ('Cesme Ruzgar Evi', 'Ezginin denizine 80m, ruzgar sorfuculerin goz bebegi konumda.',
     'House', 'Entire place', 'Izmir', 'Cesme', 980.00, 6, 'alacati'),
    ('Urla Zeytinlik Kosk', 'Zeytinlikler arasinda butik kosk, sarap tadim turlarina kolay erisim.',
     'Villa', 'Entire place', 'Izmir', 'Urla', 1250.00, 7, 'villa'),
    ('Karsiyaka Sahil Apart', 'Karsiyaka sahilinde tam cepheli apart, aksamustu yuruyuse cikma keyfi.',
     'Apartment', 'Entire place', 'Izmir', 'Karsiyaka', 560.00, 3, 'studio'),

    # --- MUGLA / BODRUM ---
    ('Bitez Bahce Villasi', 'Mandalinaliklarin arasinda gizlenip kalmis, havuzlu bahce villasi.',
     'Villa', 'Entire place', 'Mugla', 'Bitez', 1680.00, 6, 'bodrum'),
    ('Gokova Koyu Evi', 'Gokova korfezinin sapir sapir sularini yarip yuzebileceginiz koy evi.',
     'House', 'Entire place', 'Mugla', 'Gokova', 920.00, 5, 'kapadokya'),
    ('Datca Tas Ev', 'Datcanin kiliclari arasinda, dogayla butunlesmis geleneksel tas ev.',
     'House', 'Entire place', 'Mugla', 'Datca', 810.00, 4, 'alacati'),

    # --- NEVSEHIR / KAPADOKYA ---
    ('Goreme Balon Suiti', 'Baloncular erkenden kalkarken kahvenitze ile balonlari izleyin.',
     'Villa', 'Entire place', 'Nevsehir', 'Goreme', 850.00, 2, 'kapadokya'),
    ('Uchisar Kale Apart', 'Uchisar Kalesi eteginde, oyulmus kayalara gizlenip kalmis suit daire.',
     'Apartment', 'Entire place', 'Nevsehir', 'Uchisar', 770.00, 3, 'kapadokya'),

    # --- TRABZON / KARADENIZ ---
    ('Uzungol Dag Evi', 'Sisle ortulen dogada golet kenarinda sis ve huzur dolu dag evi.',
     'House', 'Entire place', 'Trabzon', 'Uzungol', 650.00, 6, 'loft'),
    ('Rize Cay Bahcesi Koyu', 'Cay bahceleri arasinda gizemli koy evi, Rize kahvaltisina uyanin.',
     'House', 'Entire place', 'Rize', 'Guneysu', 480.00, 4, 'kapadokya'),

    # --- BURSA ---
    ('Bursa Uludag Kayak Evi', 'Kis sezonu icin: Uludag eteginde, sapka ve eldivenleri hazirlayin.',
     'House', 'Entire place', 'Bursa', 'Uludag', 1100.00, 8, 'villa'),

    # --- ESKISEHIR ---
    ('Eskisehir Porsuk Loft', 'Porsuk nehrini izlediginiz, unlu kahvecilik kulturu yaninda sik loft.',
     'Apartment', 'Entire place', 'Eskisehir', 'Odunpazari', 520.00, 3, 'loft'),
]

HOSTS = [
    ('Can Ozdemir',   'can@host.com',    '05311234567', 'host'),
    ('Deniz Aktug',   'deniz@host.com',  '05422345678', 'host'),
    ('Fatma Bulut',   'fatma@host.com',  '05533456789', 'host'),
    ('Haluk Erdem',   'haluk@host.com',  '05644567890', 'host'),
    ('Ipek Sahin',    'ipek@host.com',   '05755678901', 'host'),
]

GUESTS = [
    ('Murat Celik',    'murat@guest.com',  '05311112222', 'guest'),
    ('Filiz Yildiz',   'filiz@guest.com',  '05422223333', 'guest'),
    ('Oguz Cinar',     'oguz@guest.com',   '05533334444', 'guest'),
    ('Tugce Aydın',    'tugce@guest.com',  '05644445555', 'guest'),
    ('Baran Korkmaz',  'baran@guest.com',  '05755556666', 'guest'),
    ('Nilay Duman',    'nilay@guest.com',  '05866667777', 'guest'),
]

REVIEW_COMMENTS = [
    (5, 'Hayatimdaki en guzell tatillerden! Her sey kusursuzdu, kesinlikle tekrar gelecekim.'),
    (5, 'Ev sahibi cok ilgiliydi, mekan fotolarda gozuktugunden daha guzel.'),
    (4, 'Konum mukemmel, temizlik yerindeydi. Mutfak biraz kucuk ama kabul edilebilir.'),
    (4, 'Uyku kalitesi cok iyiydi, manzara inanilmazdi. Tekrar gorisurmek uzere!'),
    (5, 'Tavsiye ederim! Butun ailecek huzur dolu bir tatil gecirdik.'),
    (3, 'Genel olarak guzel ama park sorunu yasadik. Yine de sehir icin makul.'),
    (4, 'Leziz kahvaltiyla merhaba demek harikaymis. Atmosfer tam istedigimiz gibiydi.'),
    (5, 'Romantik kacamak icin biciilmis. Her koseye ozen gosterilmis.'),
    (4, 'Check-in cok kolaydi. Konum merkeze yakin, her sey el altindaydı.'),
    (3, 'Beklentimize uygundu, fiyat performans dengesi tamam. Bir daha dusunurum.'),
]

def populate():
    db = get_db()
    cur = db.cursor()
    pw = generate_password_hash('password123')

    # ---- 1. ADD HOSTS ----
    host_ids = []
    for full_name, email, phone, role in HOSTS:
        try:
            cur.execute(
                "INSERT INTO Users (full_name, email, phone, password_hash, role) VALUES (%s,%s,%s,%s,%s)",
                (full_name, email, phone, pw, role)
            )
            db.commit()
            host_ids.append(cur.lastrowid)
            print(f"[OK] Host: {full_name} (id={cur.lastrowid})")
        except mysql.connector.errors.IntegrityError:
            cur.execute("SELECT user_id FROM Users WHERE email=%s", (email,))
            row = cur.fetchone()
            host_ids.append(row[0])
            print(f"[SKIP] Host exists: {email}")

    # ---- 2. ADD GUESTS ----
    guest_ids = []
    for full_name, email, phone, role in GUESTS:
        try:
            cur.execute(
                "INSERT INTO Users (full_name, email, phone, password_hash, role) VALUES (%s,%s,%s,%s,%s)",
                (full_name, email, phone, pw, role)
            )
            db.commit()
            guest_ids.append(cur.lastrowid)
            print(f"[OK] Guest: {full_name} (id={cur.lastrowid})")
        except mysql.connector.errors.IntegrityError:
            cur.execute("SELECT user_id FROM Users WHERE email=%s", (email,))
            row = cur.fetchone()
            guest_ids.append(row[0])
            print(f"[SKIP] Guest exists: {email}")

    # ---- 3. GET AMENITY MAP ----
    cur.execute("SELECT amenity_id, name FROM Amenities")
    amenity_map = {row[1]: row[0] for row in cur.fetchall()}
    needed_amenities = ['WiFi', 'Havuz', 'Klima', 'Mutfak', 'Otopark', 'TV']
    for name in needed_amenities:
        if name not in amenity_map:
            cur.execute("INSERT INTO Amenities (name) VALUES (%s)", (name,))
            db.commit()
            amenity_map[name] = cur.lastrowid

    amenity_presets = {
        'villa':     ['WiFi', 'Havuz', 'Klima', 'Otopark'],
        'studio':    ['WiFi', 'Klima'],
        'loft':      ['WiFi', 'Mutfak', 'TV'],
        'kapadokya': ['WiFi', 'Klima', 'TV'],
        'alacati':   ['WiFi', 'Mutfak', 'Klima'],
        'bodrum':    ['WiFi', 'Havuz', 'Klima', 'Otopark'],
    }

    # ---- 4. ADD PROPERTIES + PHOTOS + AMENITIES ----
    new_property_ids = []
    for i, prop in enumerate(PROPERTIES_TO_ADD):
        title, desc, ptype, rtype, city, district, price, max_g, photo_set = prop
        host_id = host_ids[i % len(host_ids)]

        cur.execute("""
            INSERT INTO Properties
              (host_id, title, description, property_type, room_type, city, district, base_price, max_guests)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """, (host_id, title, desc, ptype, rtype, city, district, price, max_g))
        db.commit()
        pid = cur.lastrowid
        new_property_ids.append(pid)
        print(f"[OK] Property: {title} (id={pid})")

        # Photos
        ext, int1, int2 = PHOTO_SETS[photo_set]
        cur.execute("INSERT INTO PropertyPhotos (property_id, image_url, is_primary, sort_order) VALUES (%s,%s,%s,%s)", (pid, ext, True, 0))
        cur.execute("INSERT INTO PropertyPhotos (property_id, image_url, is_primary, sort_order) VALUES (%s,%s,%s,%s)", (pid, int1, False, 1))
        cur.execute("INSERT INTO PropertyPhotos (property_id, image_url, is_primary, sort_order) VALUES (%s,%s,%s,%s)", (pid, int2, False, 2))
        db.commit()

        # Amenities
        for amenity_name in amenity_presets.get(photo_set, ['WiFi']):
            aid = amenity_map.get(amenity_name)
            if aid:
                try:
                    cur.execute("INSERT INTO PropertyAmenities (property_id, amenity_id) VALUES (%s,%s)", (pid, aid))
                except:
                    pass
        db.commit()

    print(f"\n[OK] {len(new_property_ids)} properties added.")

    # ---- 5. ADD BOOKINGS + PAYMENTS + REVIEWS ----
    # Date pairs for completed/confirmed/pending bookings (past, near future, far future)
    date_pairs = [
        ('2026-02-10', '2026-02-13', 'completed'),
        ('2026-02-20', '2026-02-23', 'completed'),
        ('2026-03-05', '2026-03-08', 'completed'),
        ('2026-03-18', '2026-03-21', 'completed'),
        ('2026-04-01', '2026-04-04', 'completed'),
        ('2026-05-10', '2026-05-13', 'confirmed'),
        ('2026-05-20', '2026-05-24', 'confirmed'),
        ('2026-06-05', '2026-06-09', 'confirmed'),
        ('2026-07-15', '2026-07-19', 'pending'),
        ('2026-08-01', '2026-08-05', 'pending'),
    ]

    total_bookings = 0
    total_reviews  = 0

    for idx, pid in enumerate(new_property_ids):
        # Get base_price
        cur.execute("SELECT base_price FROM Properties WHERE property_id=%s", (pid,))
        base_price = float(cur.fetchone()[0])

        # Assign 2-3 bookings per property
        num_bookings = 2 if idx % 3 != 0 else 3
        used_date_indices = random.sample(range(len(date_pairs)), num_bookings)

        for di in used_date_indices:
            check_in, check_out, status = date_pairs[di]
            from datetime import datetime
            nights = (datetime.strptime(check_out, '%Y-%m-%d') - datetime.strptime(check_in, '%Y-%m-%d')).days
            total_price = round(base_price * nights, 2)
            guest_count = random.randint(1, 3)
            guest_id    = guest_ids[(idx + di) % len(guest_ids)]

            cur.execute("""
                INSERT INTO Bookings
                  (property_id, guest_id, check_in, check_out, guest_count, total_price, status)
                VALUES (%s,%s,%s,%s,%s,%s,%s)
            """, (pid, guest_id, check_in, check_out, guest_count, total_price, status))
            db.commit()
            booking_id = cur.lastrowid
            total_bookings += 1

            # Payment for confirmed/completed
            if status in ('completed', 'confirmed'):
                pay_status = 'completed' if status == 'completed' else 'pending'
                try:
                    cur.execute("""
                        INSERT INTO Payments (booking_id, amount, payment_method, payment_status)
                        VALUES (%s,%s,%s,%s)
                    """, (booking_id, total_price, 'Credit Card', pay_status))
                    db.commit()
                except:
                    pass

            # Review for completed bookings
            if status == 'completed':
                rating, comment = random.choice(REVIEW_COMMENTS)
                try:
                    cur.execute("""
                        INSERT INTO Reviews (booking_id, guest_id, property_id, rating, comment)
                        VALUES (%s,%s,%s,%s,%s)
                    """, (booking_id, guest_id, pid, rating, comment))
                    db.commit()
                    total_reviews += 1
                except:
                    pass

    cur.close()
    db.close()
    print(f"\n[DONE] Bulk population complete!")
    print(f"  Properties : {len(new_property_ids)}")
    print(f"  Hosts      : {len(HOSTS)}")
    print(f"  Guests     : {len(GUESTS)}")
    print(f"  Bookings   : {total_bookings}")
    print(f"  Reviews    : {total_reviews}")

if __name__ == '__main__':
    populate()
