DROP DATABASE IF EXISTS airbnb_clone;
CREATE DATABASE airbnb_clone DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE airbnb_clone;

-- 1. Users table
CREATE TABLE Users (
    user_id INT PRIMARY KEY AUTO_INCREMENT,
    full_name VARCHAR(100) NOT NULL,
    email VARCHAR(100) UNIQUE NOT NULL,
    phone VARCHAR(20),
    password_hash VARCHAR(255) NOT NULL,
    role ENUM('host', 'guest', 'admin') DEFAULT 'guest',
    account_status ENUM('active', 'inactive', 'suspended') DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- 2. Properties
CREATE TABLE Properties (
    property_id INT PRIMARY KEY AUTO_INCREMENT,
    host_id INT NOT NULL,
    title VARCHAR(150) NOT NULL,
    description TEXT,
    property_type VARCHAR(50), 
    room_type VARCHAR(50),     
    city VARCHAR(50) NOT NULL,
    district VARCHAR(50),
    address_line TEXT,
    base_price DECIMAL(10,2) NOT NULL,
    cleaning_fee DECIMAL(10,2) DEFAULT 0.00,
    max_guests INT DEFAULT 1,
    bedroom_count INT DEFAULT 1,
    bathroom_count INT DEFAULT 1,
    status ENUM('active', 'inactive', 'maintenance') DEFAULT 'active',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (host_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- 3. PropertyPhotos
CREATE TABLE PropertyPhotos (
    photo_id INT PRIMARY KEY AUTO_INCREMENT,
    property_id INT NOT NULL,
    image_url TEXT NOT NULL,
    is_primary BOOLEAN DEFAULT FALSE,
    sort_order INT DEFAULT 0,
    FOREIGN KEY (property_id) REFERENCES Properties(property_id) ON DELETE CASCADE
);

-- 4. Amenities
CREATE TABLE Amenities (
    amenity_id INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(50) NOT NULL,
    icon VARCHAR(50) 
);

-- 5. PropertyAmenities
CREATE TABLE PropertyAmenities (
    property_id INT NOT NULL,
    amenity_id INT NOT NULL,
    PRIMARY KEY (property_id, amenity_id),
    FOREIGN KEY (property_id) REFERENCES Properties(property_id) ON DELETE CASCADE,
    FOREIGN KEY (amenity_id) REFERENCES Amenities(amenity_id) ON DELETE CASCADE
);

-- 6. Bookings
CREATE TABLE Bookings (
    booking_id INT PRIMARY KEY AUTO_INCREMENT,
    property_id INT NOT NULL,
    guest_id INT NOT NULL,
    check_in DATE NOT NULL,
    check_out DATE NOT NULL,
    guest_count INT DEFAULT 1,
    total_price DECIMAL(10,2) NOT NULL,
    status ENUM('pending', 'confirmed', 'cancelled', 'completed') DEFAULT 'pending',
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (property_id) REFERENCES Properties(property_id) ON DELETE CASCADE,
    FOREIGN KEY (guest_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- 7. Reviews
CREATE TABLE Reviews (
    review_id INT PRIMARY KEY AUTO_INCREMENT,
    booking_id INT UNIQUE NOT NULL, -- One review per booking
    guest_id INT NOT NULL,
    property_id INT NOT NULL,
    rating TINYINT CHECK (rating BETWEEN 1 AND 5),
    comment TEXT,
    created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id) ON DELETE CASCADE,
    FOREIGN KEY (guest_id) REFERENCES Users(user_id) ON DELETE CASCADE,
    FOREIGN KEY (property_id) REFERENCES Properties(property_id) ON DELETE CASCADE
);

-- 8. Payments
CREATE TABLE Payments (
    payment_id INT PRIMARY KEY AUTO_INCREMENT,
    booking_id INT UNIQUE NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    payment_method VARCHAR(50),
    payment_status ENUM('pending', 'completed', 'refunded', 'failed') DEFAULT 'pending',
    transaction_ref VARCHAR(100),
    payment_date DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id) ON DELETE CASCADE
);

-- 9. UserCards (Saved cards for checkout)
CREATE TABLE UserCards (
    card_id INT PRIMARY KEY AUTO_INCREMENT,
    user_id INT NOT NULL,
    card_holder VARCHAR(100) NOT NULL,
    card_number_masked VARCHAR(20) NOT NULL,
    expiry_date VARCHAR(7) NOT NULL, -- MM/YYYY
    FOREIGN KEY (user_id) REFERENCES Users(user_id) ON DELETE CASCADE
);

-- 10. BookingGuests (Multiple guests on one booking - Requirement: Family Information)
CREATE TABLE BookingGuests (
    guest_info_id INT PRIMARY KEY AUTO_INCREMENT,
    booking_id INT NOT NULL,
    full_name VARCHAR(100) NOT NULL,
    relationship VARCHAR(50), -- e.g., Family, Friend, Spouse
    age INT,
    FOREIGN KEY (booking_id) REFERENCES Bookings(booking_id) ON DELETE CASCADE
);

-- 11. Installments (Requirement: Pay in installments)
CREATE TABLE Installments (
    installment_id INT PRIMARY KEY AUTO_INCREMENT,
    payment_id INT NOT NULL,
    installment_number INT NOT NULL,
    amount DECIMAL(10,2) NOT NULL,
    due_date DATE NOT NULL,
    status ENUM('pending', 'paid', 'overdue') DEFAULT 'pending',
    FOREIGN KEY (payment_id) REFERENCES Payments(payment_id) ON DELETE CASCADE
);

-- 10. Sample Data

-- Users (Hashed for 'password123')
INSERT INTO Users (full_name, email, password_hash, role) VALUES 
('System Admin', 'admin@example.com', 'scrypt:32768:8:1$1bBhvQ2iJf2WUhfA$7327e5a2ef8a40102bc7c2f8d5c2ec532399bc96fd681b1623aa04212417511a6e1dbe79330e406b689e9ad2e5d9adeb040fb7a90d92ac06784408c258bfe328', 'admin'),
('Ahmet Evsahibi', 'host@example.com', 'scrypt:32768:8:1$1bBhvQ2iJf2WUhfA$7327e5a2ef8a40102bc7c2f8d5c2ec532399bc96fd681b1623aa04212417511a6e1dbe79330e406b689e9ad2e5d9adeb040fb7a90d92ac06784408c258bfe328', 'host'),
('Mehmet Misafir', 'guest@example.com', 'scrypt:32768:8:1$1bBhvQ2iJf2WUhfA$7327e5a2ef8a40102bc7c2f8d5c2ec532399bc96fd681b1623aa04212417511a6e1dbe79330e406b689e9ad2e5d9adeb040fb7a90d92ac06784408c258bfe328', 'guest');

-- Amenities
INSERT INTO Amenities (name, icon) VALUES 
('WiFi', 'fa-wifi'), ('Havuz', 'fa-swimming-pool'), ('Klima', 'fa-snowflake'), 
('Mutfak', 'fa-utensils'), ('Otopark', 'fa-car'), ('TV', 'fa-tv');

-- Properties
INSERT INTO Properties (host_id, title, description, property_type, room_type, city, district, base_price, max_guests) VALUES 
(2, 'Boğaz Manzaralı Lüks Villa', 'İstanbul boğazının eşsiz manzarasında unutulmaz bir tatil.', 'Villa', 'Entire place', 'Istanbul', 'Beşiktaş', 1200.00, 6),
(2, 'Alanya Sahilinde Şirin Stüdyo', 'Denize sıfır, huzurlu ve ekonomik bir konaklama deneyimi.', 'Apartment', 'Entire place', 'Antalya', 'Alanya', 450.00, 2),
(2, 'Kadıköy Merkezde Modern Loft', 'Endüstriyel tarzda tasarlanmış, barlar sokağına çok yakın lüks loft.', 'Apartment', 'Entire place', 'Istanbul', 'Kadıköy', 800.00, 4);

-- PropertyPhotos (3 photos per property for a better gallery)
INSERT INTO PropertyPhotos (property_id, image_url, is_primary, sort_order) VALUES 
(1, 'luxurious_villa_istanbul.png', TRUE, 0),
(1, 'villa_int_1.png', FALSE, 1),
(1, 'villa_int_2.png', FALSE, 2),
(2, 'cozy_studio_beach.png', TRUE, 0),
(2, 'studio_int_1.png', FALSE, 1),
(2, 'studio_int_2.png', FALSE, 2),
(3, 'loft_ext.png', TRUE, 0),
(3, 'loft_int_1.png', FALSE, 1),
(3, 'loft_int_2.png', FALSE, 2);

-- PropertyAmenities
INSERT INTO PropertyAmenities (property_id, amenity_id) VALUES 
(1,1), (1,2), (1,3), (1,5), (2,1), (3,1), (3,4);

-- Bookings (Completed one for review testing)
INSERT INTO Bookings (property_id, guest_id, check_in, check_out, total_price, status) VALUES 
(1, 3, '2026-04-01', '2026-04-05', 4800.00, 'completed');

-- Payments (For that completed booking)
INSERT INTO Payments (booking_id, amount, payment_method, payment_status) VALUES 
(1, 4800.00, 'Credit Card', 'completed');

-- ==========================================================
-- 11. ADVANCED VIEWS (Academically Required Queries)
-- ==========================================================

-- Q1: Detailed Reservation Confirmation (Multi-table JOIN)
CREATE OR REPLACE VIEW HMS_DetailedReservations AS
SELECT 
    b.booking_id,
    u.full_name AS guest_name,
    p.title AS property_title,
    p.city,
    b.check_in,
    b.check_out,
    b.total_price,
    b.status AS booking_status,
    pay.payment_status,
    pay.amount AS paid_amount
FROM Bookings b
JOIN Users u ON b.guest_id = u.user_id
JOIN Properties p ON b.property_id = p.property_id
LEFT JOIN Payments pay ON b.booking_id = pay.booking_id;

-- Q2: Property Analytics (Aggregates & AVG)
CREATE OR REPLACE VIEW HMS_PropertyAnalytics AS
SELECT 
    p.property_id,
    p.title,
    p.city,
    COUNT(r.review_id) AS review_count,
    ROUND(AVG(r.rating), 1) AS average_rating,
    (SELECT COUNT(*) FROM Bookings b WHERE b.property_id = p.property_id AND b.status = 'completed') AS total_stays
FROM Properties p
LEFT JOIN Reviews r ON p.property_id = r.property_id
GROUP BY p.property_id, p.title, p.city;

-- Q3: City-based Statistics (Aggregation + Having)
CREATE OR REPLACE VIEW HMS_CityStatistics AS
SELECT 
    city,
    COUNT(property_id) AS total_properties,
    MIN(base_price) AS min_price,
    MAX(base_price) AS max_price,
    AVG(base_price) AS avg_price
FROM Properties
GROUP BY city
HAVING COUNT(property_id) > 0;

-- Q4: Successful Hosts (Subquery in WHERE)
CREATE OR REPLACE VIEW HMS_SuccessfulHosts AS
SELECT u.full_name, u.email, COUNT(p.property_id) as listing_count
FROM Users u
JOIN Properties p ON u.user_id = p.host_id
WHERE u.user_id IN (
    SELECT host_id FROM Properties WHERE property_id IN (
        SELECT property_id FROM Reviews WHERE rating = 5
    )
)
GROUP BY u.user_id;

-- Q5: Property/Host Booking Summary (Requirement: List properties, hosts and booking counts)
CREATE OR REPLACE VIEW HMS_PropertyBookingSummary AS
SELECT 
    p.property_id,
    p.title AS property_title,
    u.full_name AS host_name,
    COUNT(b.booking_id) AS total_bookings
FROM Properties p
JOIN Users u ON p.host_id = u.user_id
LEFT JOIN Bookings b ON p.property_id = b.property_id
GROUP BY p.property_id, p.title, u.full_name;

-- Q6: Monthly Guest Tracker (Requirement: List all guests who stayed at a particular property in a given month)
-- Note: This view prepares the data - filtering by month/property is done in the query.
CREATE OR REPLACE VIEW HMS_MonthlyGuestTracker AS
SELECT 
    p.property_id,
    p.title AS property_title,
    u.full_name AS primary_guest_name,
    bg.full_name AS additional_guest_name,
    bg.relationship,
    b.check_in,
    MONTH(b.check_in) as stay_month,
    YEAR(b.check_in) as stay_year
FROM Bookings b
JOIN Properties p ON b.property_id = p.property_id
JOIN Users u ON b.guest_id = u.user_id
LEFT JOIN BookingGuests bg ON b.booking_id = bg.booking_id;
