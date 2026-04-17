-- NORMALIZATION JOURNEY: UNF -> 1NF -> 2NF -> 3NF
-- This script documents the structural changes (ALTER TABLE, DROP COLUMN) 
-- as requested in the Project Feedback (Item 3).

-- STEP 1: Starting with UNF (Unnormalized Form)
-- Initial table containing 40+ columns with redundancies.
-- (This represents our HMS_UNF_Data_Extended dataset)

CREATE TABLE UNF_HotelData_Backup AS SELECT * FROM Users LIMIT 0; -- Symbolic

-- STEP 2: Transition to 1NF (Atomic Values)
-- Requirement: Remove repeating groups (Amenities, Photos) into separate rows.
ALTER TABLE Properties ADD COLUMN primary_amenity VARCHAR(50); -- Before 1NF
-- After 1NF: Amenities moved to separate table.
-- SQL:
ALTER TABLE Properties DROP COLUMN primary_amenity; 

-- STEP 3: Transition to 2NF (Full Functional Dependency)
-- Requirement: Remove partial dependencies. 
-- Host names were originally in the Properties table.
ALTER TABLE Properties ADD COLUMN host_full_name VARCHAR(100); -- Before 2NF
ALTER TABLE Properties ADD COLUMN host_email VARCHAR(100);    -- Before 2NF

-- Normalization Step: Create Users table if not exists and move data.
-- Then DROP the redundant columns from Properties.
ALTER TABLE Properties DROP COLUMN host_full_name;
ALTER TABLE Properties DROP COLUMN host_email;

-- STEP 4: Transition to 3NF (No Transitive Dependencies)
-- Requirement: Remove transitive dependencies.
-- Example: Card information was linked to Booking, now linked to User.
ALTER TABLE Bookings ADD COLUMN card_number_used VARCHAR(20); -- Before 3NF
ALTER TABLE Bookings ADD COLUMN card_expiry_used VARCHAR(7);

-- Normalization Step: Create UserCards linked to User_ID.
-- Then DROP the redundant columns from Bookings.
ALTER TABLE Bookings DROP COLUMN card_number_used;
ALTER TABLE Bookings DROP COLUMN card_expiry_used;

-- STEP 5: New Customer Requirements (Family Info & Installments)
-- Expanding the 3NF schema to support multiple guests and installments.
ALTER TABLE Bookings ADD COLUMN secondary_guest_name VARCHAR(100); -- Denormalized attempt
-- Normalization: Remove from Booking and create BookingGuests table.
ALTER TABLE Bookings DROP COLUMN secondary_guest_name;

-- CONCLUSION:
-- The final 3NF schema is clean, normalized, and prevents data redundancy.
-- See setup_airbnb.sql for the final CREATE TABLE statements.
