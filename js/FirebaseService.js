import { ref, onValue, set, get, remove, update } from "https://www.gstatic.com/firebasejs/10.12.0/firebase-database.js";
import { db } from "./config.js";

/**
 * Class FirebaseService
 * Mengelola semua interaksi dengan Firebase Realtime Database secara OOP.
 */
export class FirebaseService {
  /**
   * Berlangganan (subscribe) real-time data absensi pada tanggal tertentu.
   * @param {string} tanggalKey - Format: "D-M-YYYY" (misal: "12-6-2026")
   * @param {function} callback - Callback function ketika data berubah.
   * @returns {function} Fungsi unsubscribe untuk membatalkan listener.
   */
  subscribeAbsensi(tanggalKey, callback) {
    const absensiRef = ref(db, `/absensi/${tanggalKey}`);
    return onValue(absensiRef, callback);
  }

  /**
   * Mengambil data absensi dari rentang tanggal tertentu secara asinkron.
   * @param {string[]} dateKeys - Kumpulan key tanggal.
   * @returns {Promise<Array>} List data absensi.
   */
  async getAbsensiRange(dateKeys) {
    const records = [];
    for (const tgl of dateKeys) {
      const snap = await get(ref(db, `/absensi/${tgl}`));
      if (snap.exists()) {
        snap.forEach((child) => {
          records.push({
            key: child.key,
            val: child.val(),
            tanggalKey: tgl
          });
        });
      }
    }
    return records;
  }

  /**
   * Berlangganan real-time daftar siswa terdaftar.
   * @param {function} callback - Callback function ketika data berubah.
   * @returns {function} Fungsi unsubscribe.
   */
  subscribeSiswa(callback) {
    const siswaRef = ref(db, '/siswa');
    return onValue(siswaRef, callback);
  }

  /**
   * Mengecek detail siswa berdasarkan UID.
   * @param {string} uid
   * @returns {Promise<any>}
   */
  async getSiswa(uid) {
    return get(ref(db, `/siswa/${uid}`));
  }

  /**
   * Menyimpan/Mendaftarkan siswa baru.
   * @param {string} uid
   * @param {object} data - { nama, kelas, uid }
   */
  async saveSiswa(uid, data) {
    return set(ref(db, `/siswa/${uid}`), data);
  }

  /**
   * Memperbarui data siswa yang sudah ada.
   * @param {string} uid
   * @param {object} data - Data baru siswa
   */
  async updateSiswa(uid, data) {
    return update(ref(db, `/siswa/${uid}`), data);
  }

  /**
   * Menghapus siswa berdasarkan UID.
   * @param {string} uid
   */
  async deleteSiswa(uid) {
    return remove(ref(db, `/siswa/${uid}`));
  }

  /**
   * Berlangganan real-time data kartu tidak dikenal.
   * @param {function} callback
   * @returns {function} Fungsi unsubscribe.
   */
  subscribeTidakDikenal(callback) {
    const tdRef = ref(db, '/tidak_dikenal');
    return onValue(tdRef, callback);
  }

  /**
   * Menghapus kartu tidak dikenal dari riwayat berdasarkan key id Firebase-nya.
   * @param {string} key
   */
  async deleteTidakDikenal(key) {
    return remove(ref(db, `/tidak_dikenal/${key}`));
  }

  /**
   * Mengecek apakah alamat email terdaftar sebagai admin.
   * Jika database admin kosong, email pertama akan otomatis terdaftar sebagai admin pertama (Bootstrapping).
   * @param {string} email
   * @returns {Promise<boolean>}
   */
  async checkAdminEmail(email) {
    const emailKey = email.toLowerCase().replace(/\./g, ',');
    const adminsRef = ref(db, '/admins');
    const snap = await get(adminsRef);
    
    // Bootstrapping: Jika database admins benar-benar kosong, daftarkan email pertama ini
    if (!snap.exists()) {
      await set(ref(db, `/admins/${emailKey}`), {
        email: email.toLowerCase(),
        addedBy: 'System (First Registration)',
        addedAt: new Date().toISOString()
      });
      return true;
    }

    const adminSnap = await get(ref(db, `/admins/${emailKey}`));
    return adminSnap.exists();
  }

  /**
   * Menambahkan email admin baru ke database.
   * @param {string} email
   * @param {string} addedBy
   */
  async addAdmin(email, addedBy) {
    const emailKey = email.toLowerCase().replace(/\./g, ',');
    return set(ref(db, `/admins/${emailKey}`), {
      email: email.toLowerCase(),
      addedBy: addedBy,
      addedAt: new Date().toISOString()
    });
  }

  /**
   * Menghapus email admin dari database.
   * @param {string} email
   */
  async deleteAdmin(email) {
    const emailKey = email.toLowerCase().replace(/\./g, ',');
    return remove(ref(db, `/admins/${emailKey}`));
  }

  /**
   * Berlangganan (subscribe) data daftar admin secara real-time.
   * @param {function} callback
   * @returns {function} Fungsi unsubscribe.
   */
  subscribeAdmins(callback) {
    const adminsRef = ref(db, '/admins');
    return onValue(adminsRef, callback);
  }

  /**
   * Berlangganan (subscribe) data pengaturan secara real-time.
   * @param {function} callback
   * @returns {function} Fungsi unsubscribe.
   */
  subscribePengaturan(callback) {
    const pengaturanRef = ref(db, '/pengaturan');
    return onValue(pengaturanRef, callback);
  }

  /**
   * Memperbarui pengaturan jadwal harian (Senin - Minggu) secara atomik.
   * @param {object} jadwalHarian - Object berisi jadwal per hari { senin, selasa, rabu, kamis, jumat, sabtu, minggu }
   * @param {string} terakhirDiperbarui - Timestamp update terakhir
   */
  async updateJadwalHarian(jadwalHarian, terakhirDiperbarui) {
    const updates = {};
    updates['/pengaturan/jadwal_harian'] = jadwalHarian;
    if (terakhirDiperbarui) {
      updates['/pengaturan/terakhir_diperbarui'] = terakhirDiperbarui;
    }
    return update(ref(db), updates);
  }

  /**
   * Memperbarui pengaturan jam masuk, pulang, dan hari operasional secara atomik (backward compatibility).
   * @param {object} masuk - Data jam masuk { jam_buka, menit_buka, jam_terlambat, menit_terlambat, jam_tutup, menit_tutup }
   * @param {object} pulang - Data jam pulang { jam_buka, menit_buka, jam_tutup, menit_tutup }
   * @param {object} hari - Data hari operasional { senin, selasa, rabu, kamis, jumat, sabtu, minggu }
   * @param {string} terakhirDiperbarui - Timestamp update terakhir
   */
  async updatePengaturanJam(masuk, pulang, hari, terakhirDiperbarui) {
    const updates = {};
    updates['/pengaturan/masuk'] = masuk;
    updates['/pengaturan/pulang'] = pulang;
    if (hari) {
      updates['/pengaturan/hari'] = hari;
    }
    if (terakhirDiperbarui) {
      updates['/pengaturan/terakhir_diperbarui'] = terakhirDiperbarui;
    }
    return update(ref(db), updates);
  }

  /**
   * Mencari siswa berdasarkan NISN dari database /siswa.
   * @param {string} nisn - NISN siswa
   * @returns {Promise<{uid: string, data: object}|null>}
   */
  async getSiswaByNIS(nisn) {
    const snap = await get(ref(db, '/siswa'));
    if (!snap.exists()) return null;
    let found = null;
    snap.forEach((child) => {
      const val = child.val();
      const valNisn = val.nisn || val.NISN || '';
      if (String(valNisn).trim() === String(nisn).trim()) {
        found = { uid: child.key, data: val };
      }
    });
    return found;
  }

  /**
   * Mengambil semua data absensi untuk siswa tertentu dalam bulan tertentu.
   * @param {string} uid - UID kartu siswa
   * @param {string} nama - Nama siswa (key identitas)
   * @param {number} bulan - Bulan (1-12)
   * @param {number} tahun - Tahun (misal: 2026)
   * @returns {Promise<Array>} List data absensi siswa
   */
  async getAbsensiSiswa(uid, nama, bulan, tahun) {
    const records = [];
    // Generate all date keys for the given month
    const daysInMonth = new Date(tahun, bulan, 0).getDate();
    for (let d = 1; d <= daysInMonth; d++) {
      const tgl = `${d}-${bulan}-${tahun}`;
      const snap = await get(ref(db, `/absensi/${tgl}`));
      if (snap.exists()) {
        snap.forEach((child) => {
          const val = child.val();
          // Match by UID or by name key
          if (child.key === uid || child.key === nama || 
              val.uid === uid || val.nama === nama) {
            records.push({
              key: child.key,
              val: val,
              tanggalKey: tgl,
              tanggalFormatted: `${d}/${bulan}/${tahun}`
            });
          }
        });
      }
    }
    return records;
  }
}

