# HMS Plus — Airbnb Clone | Veritabanı Sistemleri Grup Projesi

> Airbnb'den ilham alınan, Python Flask + MySQL ile geliştirilmiş full-stack konaklama yönetim sistemi.

---

## 🚀 Özellikler

- **Rol Tabanlı Erişim:** Misafir, Ev Sahibi ve Admin panelleri
- **Tam Rezervasyon Akışı:** Listeleme → Rezervasyon → Ödeme → Yorum
- **Akıllı Takvim:** Flatpickr ile dolu tarihleri engelleme ve çakışma önleme
- **Dinamik Fiyatlandırma:** Tarih güncellemesinde otomatik tutar yeniden hesaplama
- **Admin Paneli:** Kullanıcı, ilan, rezervasyon ve rapor yönetimi

---

## 🗄️ Veritabanı Mimarisi

Proje **UNF → 1NF → 2NF → 3NF** normalizasyon sürecini eksiksiz uygular.

**10 Tablo:** `Users`, `Properties`, `Amenities`, `PropertyAmenities`, `PropertyPhotos`, `Bookings`, `Payments`, `Reviews`, `UserCards`, `BookingGuests`

📄 Detaylı normalizasyon raporu: [`docs/HMS_Normalization_Report.md`](docs/HMS_Normalization_Report.md)

---

## ⚙️ Kurulum

### 1. Bağımlılıklar
```bash
pip install flask mysql-connector-python werkzeug python-dotenv
```

### 2. Ortam Değişkenleri
`.env.example` dosyasını `.env` olarak kopyalayın ve doldurun:
```bash
cp .env.example .env
```

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password
DB_NAME=airbnb_clone
SECRET_KEY=your_secret_key
```

### 3. Veritabanını Oluştur
```bash
mysql -u root -p < database/setup_airbnb.sql
```

### 4. Örnek Verileri Yükle
```bash
python scripts/populate_data.py
python scripts/bulk_populate.py
```

### 5. Uygulamayı Başlat
```bash
python app.py
```
Uygulama `http://localhost:5000` adresinde çalışır.

---

## 👤 Demo Hesaplar

Tüm hesapların şifresi: **`password123`**

### 🔴 Admin
| İsim | E-posta |
|------|---------|
| System Admin | admin@example.com |

### 🏠 Ev Sahipleri (Host)
| İsim | E-posta | İlanları |
|------|---------|----------|
| Ahmet Evsahibi | host@example.com | Lüks Villa (İstanbul), Şirin Stüdyo (Antalya), Modern Loft (İstanbul) |
| Zeynep Hanım | zeynep@example.com | Kapadokya Mağara Evi |
| Burak Yılmaz | burak@example.com | Alaçatı Taş Butik, Bodrum Sonsuzluk Villas |
| Can Özdemir | can@host.com | Sarıyer Boğaziçi Konak, Kaş Akdeniz Konağı, Çeşme Rüzgar Evi, Bitez Bahçe Villası, Göreme Balon Suiti, Uzungöl Dağ Evi, Bursa Uludağ Kayak Evi |
| Deniz Aktug | deniz@host.com | Üsküdar Kozy Apart, Side Antik Süit, Urla Zeytinlik Köşk, Göcek Köyü Evi, Üçhisar Kale Apart, Rize Çay Bahçesi, Eskişehir Porsuk Loft |
| Fatma Bulut | fatma@host.com | Moda Chic Loft, Olympos Bungalov, Karşıyaka Sahil Apart, Datça Taş Ev |
| Haluk Erdem | haluk@host.com | Cihangir Sanat Evi |
| İpek Şahin | ipek@host.com | Bebek Su Üstü Residence |

### 🧳 Misafirler (Guest)
| İsim | E-posta |
|------|---------|
| Mehmet Misafir | guest@example.com |
| Selin Arslan | selin@example.com |
| Emre Demir | emre@example.com |
| Ayşe Kaya | ayse@example.com |
| Murat Çelik | murat@guest.com |
| Filiz Yıldız | filiz@guest.com |
| Oğuz Çınar | oguz@guest.com |
| Tuğçe Aydın | tugce@guest.com |
| Baran Korkmaz | baran@guest.com |
| Nilay Duman | nilay@guest.com |

---

## 📁 Proje Yapısı

```
HotelUI/
├── app.py                    # Flask uygulama — tüm route'lar
├── .env                      # Ortam değişkenleri (git'e eklenmez)
├── .env.example              # Şablon
├── database/
│   ├── setup_airbnb.sql      # Veritabanı şema (CREATE TABLE)
│   └── normalization_journey.sql
├── docs/
│   ├── HMS_Normalization_Report.md   # UNF→3NF normalizasyon raporu
│   ├── Final_Project_Report.md       # Final proje raporu
│   └── HMS_UNF_Data_Extended.csv     # UNF örnek veri seti
├── scripts/
│   ├── populate_data.py      # İlk 3 ilana ek veri
│   └── bulk_populate.py      # 20 ilan toplu veri
├── static/                   # CSS + fotoğraflar
└── templates/                # Jinja2 HTML şablonları
```

---

## 📊 Veri İstatistikleri

| Tablo | Kayıt Sayısı |
|-------|-------------|
| Kullanıcılar (Users) | 19 |
| İlanlar (Properties) | 26 |
| Rezervasyonlar (Bookings) | 53+ |
| Ödemeler (Payments) | 40+ |
| Yorumlar (Reviews) | 23+ |
| Özellikler (Amenities) | 6 |

---

## 🛠️ Teknoloji Yığını

| Katman | Teknoloji |
|--------|-----------|
| Backend | Python 3.12, Flask |
| Veritabanı | MySQL 8.0 |
| Frontend | HTML5, Vanilla CSS, JavaScript |
| Takvim | Flatpickr |
| İkonlar | Font Awesome 6 |
| Şifreleme | Werkzeug (PBKDF2-SHA256) |
