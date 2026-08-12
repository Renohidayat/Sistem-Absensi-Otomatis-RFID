# 🎓 Sistem Absensi Otomatis RFID — SMK PGRI 2 Sumedang

<p align="center">
  <strong>Sistem Absensi Siswa Berbasis RFID dan IoT</strong><br>
  <em>Real-time attendance monitoring dengan ESP8266, RFID RC522, Firebase Realtime Database, dan Web Dashboard</em>
</p>

<p align="center">
  <a href="https://absensirfid-6c124.web.app">🌐 Live Demo</a> •
  <a href="#-fitur-utama">✨ Fitur</a> •
  <a href="#-arsitektur-sistem">🏗️ Arsitektur</a> •
  <a href="#-instalasi">📦 Instalasi</a> •
  <a href="#-penggunaan">📖 Penggunaan</a>
</p>

---

## 📋 Deskripsi

Proyek ini merupakan **Sistem Absensi Otomatis** untuk **SMK PGRI 2 Sumedang** yang mengintegrasikan teknologi **RFID (Radio Frequency Identification)** dengan **Internet of Things (IoT)**. Siswa cukup menempelkan kartu RFID ke reader, dan data kehadiran langsung tercatat secara otomatis ke **Firebase Realtime Database** serta dapat dimonitor secara *real-time* melalui **Web Dashboard** yang modern dan responsif.

### 🎯 Tujuan Proyek

- Mengotomatisasi proses pencatatan kehadiran siswa (absensi masuk & pulang)
- Menyediakan dashboard admin berbasis web untuk monitoring dan pelaporan
- Memberikan portal mandiri bagi siswa untuk melihat riwayat kehadiran
- Mengelola jadwal absensi yang fleksibel per hari (Senin–Minggu)
- Menyediakan fitur statistik dan export data

---

## ✨ Fitur Utama

### 🔌 Hardware (IoT)

| Fitur | Deskripsi |
|-------|-----------|
| **Pembacaan Kartu RFID** | Membaca UID kartu RFID secara otomatis via MFRC522 |
| **Tampilan LCD 16×2** | Menampilkan nama siswa, status kehadiran, dan notifikasi |
| **Buzzer Feedback** | Suara berbeda untuk: sukses, kartu tidak dikenal, sudah absen, error sistem |
| **Sinkronisasi NTP** | Waktu presisi via `pool.ntp.org` (GMT+7 WIB) |
| **Dual-Session** | Absensi masuk (pagi) dan absensi pulang (sore) secara terpisah |
| **Jadwal Dinamis** | Membaca konfigurasi jadwal harian langsung dari Firebase |
| **Deteksi Hari Libur** | Otomatis menolak absensi di hari yang dinonaktifkan |
| **Kartu Tak Dikenal** | Mencatat UID kartu yang belum terdaftar ke database |

### 💻 Web Dashboard (Admin)

| Fitur | Deskripsi |
|-------|-----------|
| **Absensi Harian** | Tabel real-time data absensi hari ini (Jam Masuk, Jam Pulang, Status) |
| **Laporan & Export** | Filter data per rentang tanggal, export ke Excel/CSV/PDF |
| **Statistik & Grafik** | Grafik kehadiran (Chart.js): pie chart, bar chart, distribusi per kelas |
| **Manajemen Siswa** | CRUD data siswa: Nama, NISN, Kelas, Jurusan, Angkatan, UID Kartu |
| **Registrasi Siswa** | Daftarkan kartu RFID baru ke siswa |
| **Kartu Tak Dikenal** | Lihat & daftarkan kartu yang belum terdaftar |
| **Kelola Admin** | Tambah/hapus email admin yang boleh mengakses dashboard |
| **Pengaturan Jam** | Konfigurasi jadwal absensi harian per hari (buka, terlambat, tutup) |
| **Login Google** | Autentikasi admin via Google Sign-In (Firebase Auth) |
| **Responsive** | UI adaptif untuk desktop, tablet, dan mobile |

### 🎒 Portal Siswa

| Fitur | Deskripsi |
|-------|-----------|
| **Login via NISN** | Siswa login menggunakan NISN untuk melihat data pribadi |
| **Riwayat Absensi** | Tabel riwayat kehadiran per bulan (Jam Masuk, Jam Pulang, Status) |
| **Statistik Pribadi** | Jumlah Hadir, Terlambat, Tidak Hadir, dan Persentase Kehadiran |
| **Filter Bulanan** | Pilih bulan untuk menampilkan data yang diinginkan |

---

## 🏗️ Arsitektur Sistem

```
┌─────────────────────────────────────────────────────────────────────┐
│                        ARSITEKTUR SISTEM                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                     │
│   ┌──────────────┐        WiFi        ┌──────────────────────┐     │
│   │  ESP8266      │ ◄──────────────► │  Firebase Realtime   │     │
│   │  + RFID RC522 │     HTTP/REST     │  Database            │     │
│   │  + LCD I2C    │                   │  (Cloud)             │     │
│   │  + Buzzer     │                   └──────────┬───────────┘     │
│   └──────────────┘                               │                  │
│         ▲                                        │ Real-time Sync   │
│         │ Tap Kartu                              ▼                  │
│   ┌──────────┐                          ┌──────────────────┐       │
│   │  Siswa   │                          │  Web Dashboard   │       │
│   │  (Kartu  │                          │  (admin.html)    │       │
│   │   RFID)  │                          │  + Portal Siswa  │       │
│   └──────────┘                          │  (index.html)    │       │
│                                         └──────────────────┘       │
└─────────────────────────────────────────────────────────────────────┘
```

### Alur Kerja Sistem

```
Siswa Tap Kartu ──► RFID Reader ──► ESP8266 ──► Cek Jadwal Firebase
                                                       │
                                        ┌──────────────┼──────────────┐
                                        ▼              ▼              ▼
                                   Hari Libur?    Sesi Masuk?     Sesi Pulang?
                                   (Tolak)        (Catat)         (Catat)
                                                       │              │
                                                       ▼              ▼
                                                  Status:         Jam Pulang
                                                  HADIR /         dicatat
                                                  TERLAMBAT
                                                       │
                                                       ▼
                                              Firebase Database
                                                       │
                                                       ▼
                                              Dashboard Admin
                                              (Real-time Update)
```

---

## 🛠️ Teknologi yang Digunakan

### Hardware

| Komponen | Keterangan |
|----------|------------|
| **ESP8266 (NodeMCU)** | Mikrokontroler utama dengan WiFi built-in |
| **MFRC522 (RC522)** | Modul RFID reader 13.56 MHz |
| **LCD 16×2 I2C** | Display karakter via protokol I2C (alamat 0x27) |
| **Buzzer Aktif** | Feedback audio untuk setiap status absensi |
| **Kartu RFID** | Kartu/Tag Mifare 13.56 MHz |

### Wiring (Pin Mapping)

| Komponen | Pin ESP8266 |
|----------|-------------|
| RFID SS (SDA) | D8 |
| RFID RST | D3 |
| RFID MOSI | D7 |
| RFID MISO | D6 |
| RFID SCK | D5 |
| LCD SDA | D2 |
| LCD SCL | D1 |
| Buzzer | D0 |

### Software & Framework

| Teknologi | Fungsi |
|-----------|--------|
| **Arduino IDE** | Pengembangan firmware ESP8266 |
| **FirebaseESP8266** | Library Firebase untuk ESP8266 |
| **NTPClient** | Sinkronisasi waktu via internet |
| **Firebase Realtime Database** | Backend database real-time |
| **Firebase Authentication** | Autentikasi admin via Google Sign-In |
| **Firebase Hosting** | Hosting web dashboard |
| **HTML5 / CSS3 / JavaScript (ES6+)** | Frontend web dashboard |
| **Tailwind CSS** | Styling utility-first (admin dashboard) |
| **Chart.js** | Library grafik statistik interaktif |
| **Google Material Symbols** | Ikon UI modern |
| **Google Fonts (Inter)** | Tipografi premium |

---

## 📁 Struktur Proyek

```
Visualisasi_Dasboard_iot/
│
├── 📄 index.html                  # Portal Siswa (login NISN + riwayat absensi)
├── 📄 admin.html                  # Dashboard Admin (absensi, laporan, statistik, dll.)
├── 📄 migrate_jam_pulang.html     # Tool migrasi data jam pulang ke Firebase
│
├── 📂 js/                         # JavaScript Modules
│   ├── config.js                  # Konfigurasi Firebase (API Key, DB URL)
│   ├── app.js                     # Entry point aplikasi admin
│   ├── AuthManager.js             # Manajemen autentikasi (Google Sign-In)
│   ├── FirebaseService.js         # Service layer untuk Firebase RTDB
│   └── UIManager.js               # Controller DOM & rendering UI (1900+ baris)
│
├── 📂 css/
│   └── style.css                  # Custom stylesheet (11 KB)
│
├── 📂 assets/
│   └── logo.png                   # Logo SMK PGRI 2 Sumedang
│
├── 📂 .firebase/
│   └── kode iot/
│       └── sketch_jun10a/
│           └── sketch_jun10a.ino  # Firmware ESP8266 (537 baris)
│
├── 📄 firebase.json               # Konfigurasi Firebase Hosting
├── 📄 .firebaserc                 # Project binding Firebase
├── 📄 .gitignore                  # Git ignore rules
└── 📄 DESIGN.md                   # Dokumentasi desain UI/UX
```

---

## 📦 Instalasi

### Prasyarat

- **Arduino IDE** v1.8+ atau v2.x dengan Board Manager ESP8266
- **Node.js** v16+ (untuk Firebase CLI)
- **Firebase CLI** (`npm install -g firebase-tools`)
- **Akun Google** untuk Firebase project
- **Browser modern** (Chrome, Firefox, Edge)

### 1️⃣ Setup Firebase

```bash
# Login ke Firebase
firebase login

# Inisialisasi proyek (jika belum)
firebase init hosting
```

**Konfigurasi Firebase Console:**

1. Buat project baru di [Firebase Console](https://console.firebase.google.com/)
2. Aktifkan **Realtime Database** (region: `asia-southeast1`)
3. Aktifkan **Authentication** → Provider **Google**
4. Aktifkan **Hosting**
5. Salin konfigurasi Firebase ke `js/config.js`:

```javascript
const firebaseConfig = {
  apiKey: "YOUR_API_KEY",
  authDomain: "YOUR_PROJECT.firebaseapp.com",
  databaseURL: "https://YOUR_PROJECT-default-rtdb.asia-southeast1.firebasedatabase.app",
  projectId: "YOUR_PROJECT_ID",
  storageBucket: "YOUR_PROJECT.firebasestorage.app",
  messagingSenderId: "YOUR_SENDER_ID",
  appId: "YOUR_APP_ID"
};
```

**Aturan Database (Realtime Database Rules):**

```json
{
  "rules": {
    ".read": true,
    ".write": true
  }
}
```

> ⚠️ **Peringatan:** Rules di atas bersifat terbuka (development). Untuk produksi, batasi akses tulis hanya untuk pengguna terautentikasi.

### 2️⃣ Setup Hardware (ESP8266)

1. **Install Board Manager ESP8266** di Arduino IDE:
   - `File` → `Preferences` → `Additional Board Manager URLs`:
     ```
     http://arduino.esp8266.com/stable/package_esp8266com_index.json
     ```
   - `Tools` → `Board Manager` → Cari **esp8266** → Install

2. **Install Library** via Library Manager:
   - `MFRC522` by GithubCommunity
   - `LiquidCrystal_I2C` by Frank de Brabander
   - `Firebase ESP8266 Client` by Mobizt
   - `NTPClient` by Fabrice Weinberg

3. **Konfigurasi WiFi** di `.firebase/kode iot/sketch_jun10a/sketch_jun10a.ino`:
   ```cpp
   #define WIFI_SSID "NAMA_WIFI_ANDA"
   #define WIFI_PASSWORD "PASSWORD_WIFI_ANDA"
   ```

4. **Upload ke ESP8266:**
   - Board: `NodeMCU 1.0 (ESP-12E Module)`
   - Upload Speed: `115200`
   - Flash Size: `4MB (FS:2MB, OTA:~1019KB)`

### 3️⃣ Deploy Web Dashboard

```bash
# Deploy ke Firebase Hosting
firebase deploy

# Atau deploy hosting saja
firebase deploy --only hosting
```

Dashboard dapat diakses di: `https://YOUR_PROJECT.web.app`

---

## 📖 Penggunaan

### 🔐 Login Admin

1. Buka `admin.html` atau klik tombol **"Masuk sebagai Admin (Google)"** di portal siswa
2. Klik **Login Admin** di sidebar
3. Masuk menggunakan **akun Google** yang sudah terdaftar sebagai admin
4. Email pertama yang login akan otomatis terdaftar sebagai admin (bootstrapping)

### 📝 Registrasi Siswa

1. Login sebagai Admin
2. Buka menu **Registrasi Siswa**
3. Isi data: **Nama**, **NISN**, **Kelas**, **Jurusan**, **Angkatan**, **UID Kartu RFID**
4. UID Kartu bisa didapat dari:
   - **Tab Kartu Tak Dikenal** (tap kartu baru → salin UID)
   - **Serial Monitor** Arduino IDE (baca output UID saat tap)

### 🕐 Pengaturan Jadwal

1. Buka menu **Pengaturan Jam**
2. Konfigurasi per hari (Senin–Minggu):
   - **Aktif/Nonaktif** — Aktifkan atau nonaktifkan absensi di hari tersebut
   - **Jam Buka Masuk** — Waktu mulai menerima absensi masuk
   - **Jam Terlambat** — Batas jam untuk status HADIR vs TERLAMBAT
   - **Jam Tutup Masuk** — Batas akhir absensi masuk
   - **Jam Buka Pulang** — Waktu mulai menerima absensi pulang
   - **Jam Tutup Pulang** — Batas akhir absensi pulang

### 📊 Melihat Statistik

1. Buka menu **Statistik**
2. Pilih rentang tanggal (Minggu Ini, Bulan Ini, atau Custom)
3. Lihat:
   - **Ringkasan kehadiran** (Hadir, Terlambat, Tidak Hadir)
   - **Grafik harian** (bar chart)
   - **Distribusi per kelas** (pie chart)

### 📤 Export Data

1. Buka menu **Laporan & Export**
2. Pilih rentang tanggal
3. Klik tombol export:
   - **📗 Excel** (`.xlsx`)
   - **📄 CSV** (`.csv`)
   - **📕 PDF** (`.pdf`)

### 🎒 Portal Siswa

1. Buka `index.html` (halaman utama)
2. Masukkan **NISN** siswa
3. Klik **Masuk**
4. Lihat riwayat kehadiran per bulan dengan statistik otomatis

---

## 🗄️ Struktur Database Firebase

```
absensirfid-6c124-default-rtdb/
│
├── 📂 siswa/                          # Data Siswa Terdaftar
│   └── {UID_KARTU}/
│       ├── nama: "ANDI_SOPIAN"
│       ├── nisn: "0118614277"
│       ├── kelas: "X"
│       ├── jurusan: "TSM"
│       ├── angkatan: "2026"
│       └── uid: "61430618"
│
├── 📂 absensi/                        # Data Absensi Harian
│   └── {tanggal}/                     # Format: "D-M-YYYY" (misal: "12-8-2026")
│       └── {UID_KARTU}/
│           ├── nama: "ANDI_SOPIAN"
│           ├── nisn: "0118614277"
│           ├── kelas: "X"
│           ├── uid: "61430618"
│           ├── status: "HADIR"        # HADIR / TERLAMBAT
│           ├── tanggal: "12-8-2026"
│           ├── jam: "07:00:15"        # Backward compat
│           ├── jam_masuk: "07:00:15"
│           └── jam_pulang: "15:30:22"
│
├── 📂 rekap/                          # Rekap Statistik Per Siswa
│   └── {NAMA_SISWA}/
│       ├── total: 15
│       └── terlambat: 2
│
├── 📂 tidak_dikenal/                  # Log Kartu Tidak Terdaftar
│   └── {push_id}/
│       ├── uid: "AA11BB22"
│       ├── tanggal: "12-8-2026"
│       └── jam: "07:15:30"
│
├── 📂 admins/                         # Daftar Email Admin
│   └── {email_key}/                   # Email dengan "." diganti ","
│       ├── email: "admin@gmail.com"
│       ├── addedBy: "System"
│       └── addedAt: "2026-08-12T10:00:00Z"
│
└── 📂 pengaturan/                     # Konfigurasi Sistem
    ├── terakhir_diperbarui: "..."
    └── 📂 jadwal_harian/
        ├── 📂 senin/
        │   ├── aktif: true
        │   ├── masuk_buka: "06:00"
        │   ├── terlambat: "07:00"
        │   ├── masuk_tutup: "08:00"
        │   ├── pulang_buka: "15:00"
        │   └── pulang_tutup: "17:00"
        ├── 📂 selasa/ ...
        ├── 📂 rabu/ ...
        ├── 📂 kamis/ ...
        ├── 📂 jumat/ ...
        ├── 📂 sabtu/
        │   └── aktif: false
        └── 📂 minggu/
            └── aktif: false
```

---

## 🔊 Kode Buzzer

Sistem menggunakan pola suara buzzer yang berbeda untuk setiap status:

| Pola Buzzer | Status | Deskripsi |
|-------------|--------|-----------|
| 🔔 **Beep pendek 1×** (150ms) | ✅ Sukses | Absensi masuk/pulang berhasil tercatat |
| 🔔🔔 **Beep 2× cepat** (150ms × 2) | ⚠️ Sudah Absen | Siswa sudah melakukan absensi hari ini |
| 🔔 **Beep panjang 1×** (1000ms) | ❌ Tidak Terdaftar | Kartu RFID belum didaftarkan ke sistem |
| 🔔🔔🔔 **Beep 3× sangat cepat** (100ms × 3) | 🚫 Error Sistem | Kesalahan koneksi atau di luar jadwal |

---

## 📱 Tampilan Dashboard

### Halaman Admin

| Menu | Ikon | Deskripsi |
|------|------|-----------|
| Absensi | `fingerprint` | Data absensi real-time hari ini |
| Laporan & Export | `description` | Filter & export data absensi |
| Statistik | `bar_chart` | Grafik & analisis kehadiran |
| Jumlah Siswa | `groups` | Pengelompokan siswa (kelas, jurusan, angkatan) |
| Registrasi Siswa | `person_add` | Daftarkan siswa baru |
| Kartu Tak Dikenal | `router` | Log kartu yang belum terdaftar |
| Kelola Admin | `manage_accounts` | Manajemen email admin |
| Pengaturan Jam | `schedule` | Konfigurasi jadwal absensi per hari |
| Portal Siswa | `school` | Link ke halaman siswa |

---

## 🔒 Keamanan

- **Autentikasi Admin**: Login via Google Sign-In (Firebase Authentication)
- **Whitelist Email**: Hanya email yang terdaftar di node `/admins` yang dapat mengakses dashboard
- **Bootstrapping**: Email pertama yang login otomatis terdaftar sebagai admin
- **Bypass Admin**: Email `yogicahyaa@gmail.com` memiliki akses bypass (hardcoded di `AuthManager.js`)
- **Auto-Logout**: Jika email tidak terdaftar, sistem otomatis logout dan menampilkan pesan error

> ⚠️ **Catatan Keamanan**: Untuk produksi, sebaiknya:
> - Perbarui Firebase Database Rules agar tidak terbuka (`".read": true, ".write": true`)
> - Hapus bypass email hardcoded di `AuthManager.js`
> - Gunakan Firebase Security Rules berbasis auth

---

## 🚀 Deployment

### Firebase Hosting

```bash
# Login Firebase CLI
firebase login

# Deploy semua
firebase deploy

# Deploy hosting saja
firebase deploy --only hosting
```

**URL Produksi**: [https://absensirfid-6c124.web.app](https://absensirfid-6c124.web.app)

### Local Development

```bash
# Jalankan server lokal
python -m http.server 8000

# Atau gunakan Firebase Emulator
firebase emulators:start
```

Buka browser: `http://localhost:8000`

---

## 🧪 Troubleshooting

| Masalah | Solusi |
|---------|--------|
| Kartu RFID tidak terbaca | Periksa wiring SPI (pin D5–D8), pastikan kartu Mifare 13.56 MHz |
| LCD tidak menyala | Cek alamat I2C (default 0x27), periksa koneksi D1 (SCL) & D2 (SDA) |
| WiFi gagal konek | Pastikan SSID & password benar, jangkauan WiFi cukup |
| Firebase error | Periksa API Key dan Database URL di `config.js` dan `.ino` |
| Login admin gagal | Pastikan email terdaftar di node `/admins` di Firebase |
| NISN siswa tidak ditemukan | Pastikan NISN sudah diinput saat registrasi siswa |
| Data absensi tidak muncul | Periksa format tanggal (`D-M-YYYY`), cek koneksi internet ESP |
| Dashboard tidak update | Hard refresh browser (Ctrl+F5), periksa versi cache JS |

---

## 📄 Lisensi

Proyek ini dikembangkan untuk keperluan pendidikan dan tugas akhir di **SMK PGRI 2 Sumedang**.

---

## 👨‍💻 Pengembang

| Peran | Nama |
|-------|------|
| **Developer** | Yogi Cahya |
| **Institusi** | SMK PGRI 2 Sumedang |
| **Tahun** | 2026 |

---

## 🙏 Ucapan Terima Kasih

- **SMK PGRI 2 Sumedang** — Dukungan institusi
- **Firebase by Google** — Backend-as-a-Service
- **Arduino & ESP8266 Community** — Open-source hardware platform
- **Chart.js** — Library visualisasi data
- **Tailwind CSS** — Utility-first CSS framework
- **Google Fonts & Material Symbols** — Tipografi dan ikonografi

---

<p align="center">
  <strong>🏫 SMK PGRI 2 Sumedang — Sistem Absensi Otomatis RFID & IoT</strong><br>
  <em>Dibangun dengan ❤️ untuk pendidikan Indonesia</em>
</p>
