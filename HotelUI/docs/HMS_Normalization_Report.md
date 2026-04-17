# Veritabanı Normalizasyon Raporu
## HMS Plus — Airbnb Tabanlı Konaklama Yönetim Sistemi

**Ders:** Veritabanı Sistemlerine Giriş  
**Proje:** Grup Projesi  
**Tarih:** Nisan 2026

---

## 1. UNF — Normalleştirilmemiş Form (Unnormalized Form)

### 1.1 Senaryo

HMS Plus, ev sahiplerinin mülklerini listeleyebildiği, misafirlerin rezervasyon yapabildiği, ödeme yapabildiği ve yorum bırakabildiği bir online konaklama platformudur. Sistem; kullanıcı yönetimi, ilan yönetimi, rezervasyon akışı, ödeme takibi ve misafir değerlendirmelerini kapsar.

### 1.2 UNF Tablosundaki Tüm Nitelikler (35 Adet)

Aşağıdaki 35 nitelik, normalizasyon öncesinde **tek bir düz tabloda** tutulduğu varsayılan ham veri kümesini temsil eder:

| # | Nitelik Adı | Açıklama |
|---|-------------|----------|
| 1 | User_ID | Kullanıcı sıra numarası |
| 2 | User_FullName | Kullanıcının tam adı |
| 3 | User_Email | Kullanıcı e-posta adresi (benzersiz) |
| 4 | User_Phone | Kullanıcı telefon numarası |
| 5 | User_Role | Kullanıcı rolü (host / guest / admin) |
| 6 | User_Status | Hesap durumu (active / inactive / suspended) |
| 7 | User_CreatedAt | Hesap oluşturma tarihi |
| 8 | Property_ID | Mülk sıra numarası |
| 9 | Property_Title | İlan başlığı |
| 10 | Property_Description | İlan açıklaması |
| 11 | Property_Type | Mülk türü (apartment / villa / house / studio) |
| 12 | Property_RoomType | Oda türü (entire place / private room) |
| 13 | Property_City | Mülkün şehri |
| 14 | Property_District | Mülkün ilçesi |
| 15 | Property_Address | Açık adres |
| 16 | Property_BasePrice | Gecelik taban fiyat (₺) |
| 17 | Property_MaxGuests | Maksimum misafir sayısı |
| 18 | Property_Status | İlan durumu (active / inactive / maintenance) |
| 19 | Property_CreatedAt | İlan oluşturma tarihi |
| 20 | Photo_URL | Fotoğraf dosya yolu |
| 21 | Photo_IsPrimary | Ana fotoğraf mı? (0/1) |
| 22 | Photo_SortOrder | Fotoğraf sıralama değeri |
| 23 | Amenity_Name | Özellik adı (WiFi, Havuz, Klima vb.) |
| 24 | Amenity_Icon | Özelliğin ikonu |
| 25 | Booking_ID | Rezervasyon sıra numarası |
| 26 | Booking_CheckIn | Giriş tarihi |
| 27 | Booking_CheckOut | Çıkış tarihi |
| 28 | Booking_GuestCount | Misafir sayısı |
| 29 | Booking_TotalPrice | Toplam rezervasyon ücreti |
| 30 | Booking_Status | Rezervasyon durumu |
| 31 | Payment_Method | Ödeme yöntemi |
| 32 | Payment_Status | Ödeme durumu |
| 33 | Payment_Date | Ödeme tarihi |
| 34 | Review_Rating | Kullanıcı puanı (1-5) |
| 35 | Review_Comment | Kullanıcı yorum metni |

---

### 1.3 UNF Örnek Veri Seti (15 Satır)

> **Not:** Aşağıdaki tablo gerçek bir senaryo üzerinden oluşturulmuş ham veri kümesidir. Tekrar eden değerler ve çok değerli gruplar (amenities, photos) kasıtlı olarak dahil edilmiştir.

| User_ID | User_FullName | User_Email | User_Role | Property_ID | Property_Title | Property_City | Property_BasePrice | Amenity_Name | Photo_URL | Booking_ID | Booking_CheckIn | Booking_CheckOut | Booking_TotalPrice | Booking_Status | Payment_Status | Review_Rating | Review_Comment |
|---------|--------------|-----------|----------|-------------|---------------|--------------|-------------------|-------------|----------|------------|----------------|-----------------|-------------------|---------------|---------------|-------------|----------------|
| 2 | Ahmet Evsahibi | host@example.com | host | 1 | Boğaz Manzaralı Lüks Villa | Istanbul | 1200.00 | WiFi | luxurious_villa_istanbul.png | 1 | 2026-04-01 | 2026-04-05 | 4800.00 | completed | completed | 5 | Muhteşem manzara! |
| 2 | Ahmet Evsahibi | host@example.com | host | 1 | Boğaz Manzaralı Lüks Villa | Istanbul | 1200.00 | Havuz | luxurious_villa_istanbul.png | 1 | 2026-04-01 | 2026-04-05 | 4800.00 | completed | completed | 5 | Muhteşem manzara! |
| 2 | Ahmet Evsahibi | host@example.com | host | 1 | Boğaz Manzaralı Lüks Villa | Istanbul | 1200.00 | Klima | villa_int_1.png | 1 | 2026-04-01 | 2026-04-05 | 4800.00 | completed | completed | 5 | Muhteşem manzara! |
| 2 | Ahmet Evsahibi | host@example.com | host | 1 | Boğaz Manzaralı Lüks Villa | Istanbul | 1200.00 | Otopark | villa_int_2.png | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL |
| 3 | Mehmet Misafir | guest@example.com | guest | 2 | Alanya Sahilinde Şirin Stüdyo | Antalya | 450.00 | WiFi | cozy_studio_beach.png | 2 | 2026-04-23 | 2026-04-26 | 1350.00 | confirmed | pending | NULL | NULL |
| 3 | Mehmet Misafir | guest@example.com | guest | 2 | Alanya Sahilinde Şirin Stüdyo | Antalya | 450.00 | WiFi | studio_int_1.png | 2 | 2026-04-23 | 2026-04-26 | 1350.00 | confirmed | pending | NULL | NULL |
| 3 | Mehmet Misafir | guest@example.com | guest | 3 | Kadıköy Merkezde Modern Loft | Istanbul | 800.00 | WiFi | loft_ext.png | 3 | 2026-05-10 | 2026-05-13 | 2400.00 | pending | NULL | NULL | NULL |
| 2 | Ahmet Evsahibi | host@example.com | host | 3 | Kadıköy Merkezde Modern Loft | Istanbul | 800.00 | Mutfak | loft_int_1.png | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL |
| 2 | Ahmet Evsahibi | host@example.com | host | 2 | Alanya Sahilinde Şirin Stüdyo | Antalya | 450.00 | WiFi | studio_int_2.png | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL |
| 1 | System Admin | admin@example.com | admin | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL |
| 3 | Mehmet Misafir | guest@example.com | guest | 1 | Boğaz Manzaralı Lüks Villa | Istanbul | 1200.00 | Havuz | luxurious_villa_istanbul.png | 4 | 2026-06-01 | 2026-06-04 | 3600.00 | confirmed | completed | NULL | NULL |
| 3 | Mehmet Misafir | guest@example.com | guest | 1 | Boğaz Manzaralı Lüks Villa | Istanbul | 1200.00 | WiFi | luxurious_villa_istanbul.png | 4 | 2026-06-01 | 2026-06-04 | 3600.00 | confirmed | completed | NULL | NULL |
| 3 | Mehmet Misafir | guest@example.com | guest | 2 | Alanya Sahilinde Şirin Stüdyo | Antalya | 450.00 | WiFi | cozy_studio_beach.png | 5 | 2026-07-15 | 2026-07-20 | 2250.00 | pending | NULL | NULL | NULL |
| 2 | Ahmet Evsahibi | host@example.com | host | 1 | Boğaz Manzaralı Lüks Villa | Istanbul | 1200.00 | Otopark | villa_int_1.png | NULL | NULL | NULL | NULL | NULL | NULL | NULL | NULL |
| 3 | Mehmet Misafir | guest@example.com | guest | 3 | Kadıköy Merkezde Modern Loft | Istanbul | 800.00 | Mutfak | loft_int_2.png | 6 | 2026-08-01 | 2026-08-05 | 3200.00 | completed | refunded | 3 | Konum güzeldi ama gürültülüydü |

---

### 1.4 UNF'deki Sorunlar

Bu ham veri tablosunda tespit edilen başlıca sorunlar:

1. **Tekrarlayan Gruplar (Repeating Groups):** `Amenity_Name` ve `Photo_URL` alanları birden fazla değere sahip olup aynı rezervasyon için satır tekrarlanmaktadır.
2. **Veri Tekrarı (Data Redundancy):** `User_FullName`, `User_Email` gibi kullanıcı bilgileri her rezervasyon satırında tekrar edilmektedir.
3. **Güncelleme Anomalisi (Update Anomaly):** Bir mülkün fiyatı değiştiğinde onlarca satırın güncellenmesi gerekir.
4. **Ekleme Anomalisi (Insertion Anomaly):** Henüz rezervasyonu olmayan bir mülk eklenemez (NULL değerler zorunlu hale gelir).
5. **Silme Anomalisi (Deletion Anomaly):** Bir rezervasyon silindiğinde ilgili kullanıcı veya mülk bilgileri de kaybedilir.

---

## 2. Fonksiyonel Bağımlılık Analizi

### 2.1 Birincil Bağımlılıklar

```
User_ID → User_FullName, User_Email, User_Phone, User_Role, User_Status, User_CreatedAt

Property_ID → Property_Title, Property_Description, Property_Type, Property_RoomType,
              Property_City, Property_District, Property_Address, Property_BasePrice,
              Property_MaxGuests, Property_Status, Property_CreatedAt, User_ID (host)

Booking_ID → Booking_CheckIn, Booking_CheckOut, Booking_GuestCount,
             Booking_TotalPrice, Booking_Status, Property_ID, User_ID (guest)

Booking_ID → Payment_Method, Payment_Status, Payment_Date

Booking_ID → Review_Rating, Review_Comment

Amenity_ID → Amenity_Name, Amenity_Icon
```

---

### 2.2 Kısmi Bağımlılıklar (Partial Dependencies) — 2NF İhlali

UNF tablosunda bileşik anahtar `{Booking_ID, Property_ID, Amenity_Name}` kullanıldığında kısmi bağımlılıklar ortaya çıkar:

| Bağımlılık | Tür | Açıklama |
|------------|-----|----------|
| `Property_ID → Property_Title` | **Kısmi** | Başlık doğrudan mülke aittir, rezervasyona değil |
| `Property_ID → Property_City` | **Kısmi** | Şehir doğrudan mülke aittir |
| `Property_ID → Property_BasePrice` | **Kısmi** | Fiyat doğrudan mülke aittir |
| `User_ID → User_FullName` | **Kısmi** | Kullanıcı adı rezervasyona değil kullanıcıya bağlıdır |
| `User_ID → User_Email` | **Kısmi** | E-posta rezervasyona değil kullanıcıya bağlıdır |
| `Amenity_Name → Amenity_Icon` | **Kısmi** | İkon bilgisi özelliğe aittir, mülk-özellik çiftine değil |

> **Sonuç:** Bu kısmi bağımlılıklar tablonun **2NF'yi ihlal ettiğini** gösterir.

---

### 2.3 Geçişli Bağımlılıklar (Transitive Dependencies) — 3NF İhlali

| Bağımlılık Zinciri | Tür | Açıklama |
|--------------------|-----|----------|
| `Booking_ID → Property_ID → Property_City` | **Geçişli** | Şehir Booking'e anahtar olmayan alan üzerinden bağlıdır |
| `Booking_ID → Property_ID → Property_BasePrice` | **Geçişli** | Taban fiyat rezervasyona dolaylı bağlıdır |
| `Booking_ID → User_ID → User_Email` | **Geçişli** | E-posta rezervasyona dolaylı bağlıdır |
| `Property_ID → User_ID → User_FullName` | **Geçişli** | Ev sahibi adı mülke dolaylı bağlıdır |
| `Booking_ID → Payment_Method, Payment_Status` | **Geçişli** | Ödeme bilgisi rezervasyonun üzerinde ayrı tutulmalıdır |
| `Booking_ID → Review_Rating, Review_Comment` | **Geçişli** | Yorum bilgisi rezervasyonun üzerinde ayrı tutulmalıdır |

> **Sonuç:** Bu geçişli bağımlılıklar **3NF'yi ihlal eder.** Her sütun yalnızca birincil anahtara bağımlı olmalıdır.

---

## 3. Normalizasyon Adımları

### 3.1 1NF — Birinci Normal Form

**Kural:**
- Her sütun atomik (bölünemez) tek bir değer içermeli
- Her satır benzersiz olmalı (birincil anahtar tanımlanmalı)
- Tekrarlayan gruplar olmamalı

**Yapılan İşlemler:**

| Sorun | Çözüm |
|-------|-------|
| `Amenity_Name` birden fazla değer içeriyordu | Her özellik ayrı satıra taşındı |
| `Photo_URL` birden fazla değer içeriyordu | Her fotoğraf ayrı satıra taşındı |
| Bileşik anahtarlar belirsizdi | Her tablo için net bir Primary Key belirlendi |
| NULL değer grupları satırları anlamsız kılıyordu | NULL'lı alanlar için ayrı tablolar oluşturuldu |

---

### 3.2 2NF — İkinci Normal Form

**Kural:**
- 1NF koşullarını sağlamalı
- Anahtar olmayan hiçbir sütun bileşik birincil anahtarın yalnızca bir kısmına bağımlı olmamalıdır

**Tespit edilen kısmi bağımlılıklar çözülerek aşağıdaki tablolar oluşturuldu:**

- ✅ `Property_ID → Title, City, Price` → **Properties** tablosuna taşındı
- ✅ `User_ID → FullName, Email` → **Users** tablosuna taşındı
- ✅ `Amenity_Name → Icon` → **Amenities** tablosuna taşındı
- ✅ `Photo_URL, IsPrimary, SortOrder` → **PropertyPhotos** tablosuna taşındı
- ✅ Mülk-Özellik N:M ilişkisi → **PropertyAmenities** ara tablosuyla çözüldü

---

### 3.3 3NF — Üçüncü Normal Form

**Kural:**
- 2NF koşullarını sağlamalı
- Anahtar olmayan hiçbir sütun başka bir anahtar olmayan sütuna geçişli bağımlı olmamalı

**Tespit edilen geçişli bağımlılıklar çözüldü:**

| Geçişli Bağımlılık | Çözüm |
|--------------------|-------|
| `Booking_ID → Property_ID → City, BasePrice` | Properties tablosu izole edildi; Booking sadece FK tutar |
| `Booking_ID → User_ID → Email, FullName` | Users tablosu izole edildi; Booking sadece FK tutar |
| `Booking_ID → Payment_Method, Payment_Status, Payment_Date` | **Payments** tablosu oluşturuldu |
| `Booking_ID → Review_Rating, Review_Comment` | **Reviews** tablosu oluşturuldu |

---

## 4. 3NF Final Şeması

### 4.1 Tablolar ve SQL Tanımları

**1. Users**
```sql
Users(
  user_id       INT PK AUTO_INCREMENT,
  full_name     VARCHAR(100) NOT NULL,
  email         VARCHAR(100) UNIQUE NOT NULL,
  phone         VARCHAR(20),
  password_hash VARCHAR(255) NOT NULL,
  role          ENUM('host','guest','admin') DEFAULT 'guest',
  account_status ENUM('active','inactive','suspended') DEFAULT 'active',
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
)
```
> Her alan yalnızca **user_id**'ye bağımlıdır. ✅

---

**2. Properties**
```sql
Properties(
  property_id   INT PK AUTO_INCREMENT,
  host_id       INT FK → Users(user_id),
  title         VARCHAR(150) NOT NULL,
  description   TEXT,
  property_type VARCHAR(50),
  room_type     VARCHAR(50),
  city          VARCHAR(50) NOT NULL,
  district      VARCHAR(50),
  address_line  TEXT,
  base_price    DECIMAL(10,2) NOT NULL,
  max_guests    INT DEFAULT 1,
  status        ENUM('active','inactive','maintenance') DEFAULT 'active',
  created_at    DATETIME DEFAULT CURRENT_TIMESTAMP
)
```
> Her alan yalnızca **property_id**'ye bağımlıdır. ✅

---

**3. Amenities**
```sql
Amenities(
  amenity_id INT PK AUTO_INCREMENT,
  name       VARCHAR(50) NOT NULL,
  icon       VARCHAR(50)
)
```
> Her alan yalnızca **amenity_id**'ye bağımlıdır. ✅

---

**4. PropertyAmenities** *(N:M çözüm tablosu)*
```sql
PropertyAmenities(
  property_id INT FK → Properties(property_id),
  amenity_id  INT FK → Amenities(amenity_id),
  PK(property_id, amenity_id)
)
```
> Türetilmiş bilgi içermez. ✅

---

**5. PropertyPhotos**
```sql
PropertyPhotos(
  photo_id    INT PK AUTO_INCREMENT,
  property_id INT FK → Properties(property_id),
  image_url   TEXT NOT NULL,
  is_primary  BOOLEAN DEFAULT FALSE,
  sort_order  INT DEFAULT 0
)
```
> Her alan yalnızca **photo_id**'ye bağımlıdır. ✅

---

**6. Bookings**
```sql
Bookings(
  booking_id  INT PK AUTO_INCREMENT,
  property_id INT FK → Properties(property_id),
  guest_id    INT FK → Users(user_id),
  check_in    DATE NOT NULL,
  check_out   DATE NOT NULL,
  guest_count INT DEFAULT 1,
  total_price DECIMAL(10,2) NOT NULL,
  status      ENUM('pending','confirmed','cancelled','completed') DEFAULT 'pending',
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
)
```
> Her alan yalnızca **booking_id**'ye bağımlıdır. Mülk/kullanıcı bilgileri FK üzerinden erişilir. ✅

---

**7. Payments** *(Geçişli bağımlılık çözümü)*
```sql
Payments(
  payment_id      INT PK AUTO_INCREMENT,
  booking_id      INT UNIQUE FK → Bookings(booking_id),
  amount          DECIMAL(10,2) NOT NULL,
  payment_method  VARCHAR(50),
  payment_status  ENUM('pending','completed','refunded','failed') DEFAULT 'pending',
  transaction_ref VARCHAR(100),
  payment_date    DATETIME DEFAULT CURRENT_TIMESTAMP
)
```
> `Booking_ID → Payment_Status` geçişli bağımlılığı bu tabloyla çözüldü. ✅

---

**8. Reviews** *(Geçişli bağımlılık çözümü)*
```sql
Reviews(
  review_id   INT PK AUTO_INCREMENT,
  booking_id  INT UNIQUE FK → Bookings(booking_id),
  guest_id    INT FK → Users(user_id),
  property_id INT FK → Properties(property_id),
  rating      TINYINT CHECK(rating BETWEEN 1 AND 5),
  comment     TEXT,
  created_at  DATETIME DEFAULT CURRENT_TIMESTAMP
)
```
> `Booking_ID → Review_Rating` geçişli bağımlılığı bu tabloyla çözüldü. ✅

---

**9. UserCards**
```sql
UserCards(
  card_id           INT PK AUTO_INCREMENT,
  user_id           INT FK → Users(user_id),
  card_holder       VARCHAR(100) NOT NULL,
  card_number_masked VARCHAR(20) NOT NULL,
  expiry_date       VARCHAR(7) NOT NULL
)
```
> Her alan yalnızca **card_id**'ye bağımlıdır. ✅

---

**10. BookingGuests** *(Ek misafir bilgileri)*
```sql
BookingGuests(
  guest_info_id INT PK AUTO_INCREMENT,
  booking_id    INT FK → Bookings(booking_id),
  full_name     VARCHAR(100) NOT NULL,
  relationship  VARCHAR(50),
  age           INT
)
```
> Her alan yalnızca **guest_info_id**'ye bağımlıdır. ✅

---

### 4.2 Varlık-İlişki Diyagramı (ERD)

```
┌──────────┐         ┌────────────┐         ┌──────────────────┐
│  Users   │ 1 ──▶ N │ Properties │ 1 ──▶ N │  PropertyPhotos  │
│(user_id) │         │(property_id│         │  (photo_id)      │
└──────────┘         │ host_id FK)│         └──────────────────┘
     │               └────────────┘
     │                    │ N : M
     │               ┌────▼──────────────┐
     │               │ PropertyAmenities │ N ──▶ 1 ┌──────────┐
     │               └───────────────────┘         │Amenities │
     │                                             └──────────┘
     │ 1 ──▶ N
     │         ┌──────────┐  1 ──▶ 1  ┌──────────┐
     └────────▶│ Bookings │──────────▶│ Payments │
               │(booking  │           └──────────┘
               │  _id,    │  1 ──▶ 1  ┌──────────┐
               │guest_id, │──────────▶│ Reviews  │
               │prop_id   │           └──────────┘
               │  FKs)    │  1 ──▶ N  ┌───────────────┐
               └──────────┘──────────▶│ BookingGuests │
                                      └───────────────┘
```

### 4.3 İlişki Tablosu

| Tablo 1 | Kardinalite | Tablo 2 | Açıklama |
|---------|-------------|---------|----------|
| Users | 1 : N | Properties | Bir ev sahibi birden fazla mülk listeleyebilir |
| Users | 1 : N | Bookings | Bir misafir birden fazla rezervasyon yapabilir |
| Properties | 1 : N | PropertyPhotos | Bir mülkün birden fazla fotoğrafı olabilir |
| Properties | N : M | Amenities | Bir özellik birden fazla mülkte, bir mülkün birden fazla özelliği |
| Bookings | 1 : 1 | Payments | Her rezervasyonun en fazla bir ödemesi olabilir |
| Bookings | 1 : 1 | Reviews | Her rezervasyonun en fazla bir yorumu olabilir |
| Bookings | 1 : N | BookingGuests | Bir rezervasyona birden fazla ek misafir eklenebilir |
| Users | 1 : N | UserCards | Bir kullanıcının birden fazla kayıtlı kartı olabilir |

---

## 5. Özet Karşılaştırma Tablosu

| Kriter | UNF | 1NF | 2NF | 3NF |
|--------|-----|-----|-----|-----|
| Tekrarlayan Gruplar | ❌ Var | ✅ Yok | ✅ Yok | ✅ Yok |
| Atomik Değerler | ❌ Hayır | ✅ Evet | ✅ Evet | ✅ Evet |
| Tanımlı Birincil Anahtar | ❌ Belirsiz | ✅ Tanımlı | ✅ Tanımlı | ✅ Tanımlı |
| Kısmi Bağımlılık | ❌ Var | ❌ Var | ✅ Yok | ✅ Yok |
| Geçişli Bağımlılık | ❌ Var | ❌ Var | ❌ Var | ✅ Yok |
| Tablo Sayısı | 1 | 1 | 5 | 10 |
| Veri Tekrarı | ❌ Yüksek | ❌ Yüksek | ⚠️ Orta | ✅ Minimum |
| Güncelleme Anomalisi | ❌ Var | ❌ Var | ⚠️ Kısmen | ✅ Yok |
| Referans Bütünlüğü | ❌ Yok | ❌ Yok | ⚠️ Kısmen | ✅ ON DELETE CASCADE |

---

## 6. Sonuç

Bu normalizasyon süreci sonucunda:

- **35 nitelikli ham UNF tablosu**, 3NF kurallarına uygun **10 ayrı tabloya** ayrıştırılmıştır.
- Mülk ve kullanıcı bilgilerindeki **kısmi bağımlılıklar** 2NF'ye geçişle giderilmiştir.
- Ödeme ve yorum bilgilerinin rezervasyona dolaylı bağlı olduğu **geçişli bağımlılıklar** 3NF'ye geçişle çözülmüştür.
- `ON DELETE CASCADE` kısıtı ile veritabanı **referans bütünlüğü (Referential Integrity)** güvence altına alınmıştır.
- Mülk–Özellik N:M ilişkisi `PropertyAmenities` ara tablosuyla çözülmüştür.
- Veri tekrarı büyük ölçüde azaltılmış, sistemin ölçeklenebilirliği ve bakım kolaylığı artırılmıştır.
