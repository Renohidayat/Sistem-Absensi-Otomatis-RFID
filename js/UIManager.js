/**
 * Class UIManager
 * Mengelola semua manipulasi DOM, rendering data, pembuatan grafik Chart.js,
 * serta pengikatan event listener UI.
 */
export class UIManager {
  /**
   * @param {AuthManager} authManager
   * @param {FirebaseService} firebaseService
   */
  constructor(authManager, firebaseService) {
    this.auth = authManager;
    this.dbService = firebaseService;

    // Cache Data
    this.daftarSiswaCache = {}; // uid -> {nama, kelas}
    this.siswaRowsCache = [];
    this.laporanData = [];
    this.currentAbsensiUnsub = null;
    this.currentDayTab = 'senin';
    this.cacheJadwalHarian = {
      senin: { aktif: true, masuk_buka: '06:00', terlambat: '07:00', masuk_tutup: '08:00' },
      selasa: { aktif: true, masuk_buka: '06:00', terlambat: '07:00', masuk_tutup: '08:00' },
      rabu: { aktif: true, masuk_buka: '06:00', terlambat: '07:00', masuk_tutup: '08:00' },
      kamis: { aktif: true, masuk_buka: '06:00', terlambat: '07:00', masuk_tutup: '08:00' },
      jumat: { aktif: true, masuk_buka: '06:00', terlambat: '07:00', masuk_tutup: '08:00' },
      sabtu: { aktif: false, masuk_buka: '06:00', terlambat: '07:00', masuk_tutup: '08:00' },
      minggu: { aktif: false, masuk_buka: '06:00', terlambat: '07:00', masuk_tutup: '08:00' }
    };

    // Chart instances
    this.chartAbsensiHariIni = null;
    this.chartStatistikRingkasan = null;
    this.chartStatistikHarian = null;
    this.chartDistribusiMurid = null;

    this.dom = {};
  }

  /**
   * Mengcache semua elemen DOM yang digunakan oleh aplikasi.
   */
  cacheDOM() {
    this.dom = {
      adminLabel: document.getElementById('adminLabel'),
      btnAdminToggle: document.getElementById('btnAdminToggle'),
      modalLogin: document.getElementById('modalLogin'),
      loginError: document.getElementById('loginError'),
      btnLoginCancel: document.getElementById('btnLoginCancel'),
      btnGoogleLogin: document.getElementById('btnGoogleLogin'),

      // Halaman-halaman
      pages: document.querySelectorAll('.page'),
      tabBtns: document.querySelectorAll('.tab-btn'),

      // Page Absensi
      inputTanggal: document.getElementById('tanggal'),
      tabelAbsensi: document.getElementById('tabelAbsensi'),
      statTotal: document.getElementById('statTotal'),
      statHadir: document.getElementById('statHadir'),
      statTerlambat: document.getElementById('statTerlambat'),
      statBelumHadir: document.getElementById('statBelumHadir'),
      chartAbsensiHariIni: document.getElementById('chartAbsensiHariIni'),

      // Page Laporan
      tglMulai: document.getElementById('tglMulai'),
      tglAkhir: document.getElementById('tglAkhir'),
      lapJurusan: document.getElementById('lapJurusan'),
      lapKelas: document.getElementById('lapKelas'),
      btnTampilkanLaporan: document.getElementById('btnTampilkanLaporan'),
      btnExportExcel: document.getElementById('btnExportCSV'),
      tabelLaporan: document.getElementById('tabelLaporan'),
      btnMobileMenu: document.getElementById('btnMobileMenu'),
      mobileOverlay: document.getElementById('mobileOverlay'),
      mainSidebar: document.getElementById('mainSidebar'),
      lapTotal: document.getElementById('lapTotal'),
      lapHadir: document.getElementById('lapHadir'),
      lapTerlambat: document.getElementById('lapTerlambat'),

      // Page Statistik
      statSiswaSelect: document.getElementById('statSiswa'),
      statBulanInput: document.getElementById('statBulan'),
      statJurusan: document.getElementById('statJurusan'),
      statKelas: document.getElementById('statKelas'),
      btnTampilkanStatistik: document.getElementById('btnTampilkanStatistik'),
      statistikKosong: document.getElementById('statistikKosong'),
      statistikIsi: document.getElementById('statistikIsi'),
      stHadir: document.getElementById('stHadir'),
      stTerlambat: document.getElementById('stTerlambat'),
      stTidakHadir: document.getElementById('stTidakHadir'),
      stPersenHadir: document.getElementById('stPersenHadir'),
      tabelStatistikDetail: document.getElementById('tabelStatistikDetail'),
      chartStatistikRingkasan: document.getElementById('chartStatistikRingkasan'),
      chartStatistikHarian: document.getElementById('chartStatistikHarian'),
      statTotalMurid: document.getElementById('statTotalMurid'),
      tabelKelasMurid: document.getElementById('tabelKelasMurid'),
      chartDistribusiMurid: document.getElementById('chartDistribusiMurid'),
      jmTotalMurid: document.getElementById('jmTotalMurid'),
      jmTotalKelas: document.getElementById('jmTotalKelas'),
      jmTotalAngkatan: document.getElementById('jmTotalAngkatan'),
      jmTotalJurusan: document.getElementById('jmTotalJurusan'),
      jumlahMuridContent: document.getElementById('jumlahMuridContent'),

      // Page Registrasi
      registrasiLocked: document.getElementById('registrasiLocked'),
      registrasiContent: document.getElementById('registrasiContent'),
      btnLoginsFromLocked: document.querySelectorAll('.btnLoginFromLocked'),
      alertSuccess: document.getElementById('alertSuccess'),
      alertError: document.getElementById('alertError'),
      lastScannedUID: document.getElementById('lastScannedUID'),
      btnGunakanUID: document.getElementById('btnGunakanUID'),
      formRegistrasi: document.getElementById('formRegistrasi'),
      regNama: document.getElementById('regNama'),
      regNISN: document.getElementById('regNISN'),
      regKelas: document.getElementById('regKelas'),
      regJurusan: document.getElementById('regJurusan'),
      regAngkatan: document.getElementById('regAngkatan'),
      regUID: document.getElementById('regUID'),
      searchSiswa: document.getElementById('searchSiswa'),
      tabelSiswa: document.getElementById('tabelSiswa'),

      // Modal Edit
      modalEditSiswa: document.getElementById('modalEditSiswa'),
      editError: document.getElementById('editError'),
      editUID: document.getElementById('editUID'),
      editNama: document.getElementById('editNama'),
      editNISN: document.getElementById('editNISN'),
      editKelas: document.getElementById('editKelas'),
      editJurusan: document.getElementById('editJurusan'),
      editAngkatan: document.getElementById('editAngkatan'),
      btnEditCancel: document.getElementById('btnEditCancel'),
      btnEditSubmit: document.getElementById('btnEditSubmit'),

      // Page Kartu Tidak Dikenal
      tidakDikenalLocked: document.getElementById('tidakDikenalLocked'),
      tidakDikenalContent: document.getElementById('tidakDikenalContent'),
      tabelTidakDikenal: document.getElementById('tabelTidakDikenal'),

      // Page Kelola Admin
      kelolaAdminLocked: document.getElementById('kelolaAdminLocked'),
      kelolaAdminContent: document.getElementById('kelolaAdminContent'),
      alertAdminSuccess: document.getElementById('alertAdminSuccess'),
      alertAdminError: document.getElementById('alertAdminError'),
      formTambahAdmin: document.getElementById('formTambahAdmin'),
      editAngkatan: document.getElementById('editAngkatan'),
      btnEditCancel: document.getElementById('btnEditCancel'),
      btnEditSubmit: document.getElementById('btnEditSubmit'),

      // Page Kartu Tidak Dikenal
      tidakDikenalLocked: document.getElementById('tidakDikenalLocked'),
      tidakDikenalContent: document.getElementById('tidakDikenalContent'),
      tabelTidakDikenal: document.getElementById('tabelTidakDikenal'),

      // Page Kelola Admin
      kelolaAdminLocked: document.getElementById('kelolaAdminLocked'),
      kelolaAdminContent: document.getElementById('kelolaAdminContent'),
      alertAdminSuccess: document.getElementById('alertAdminSuccess'),
      alertAdminError: document.getElementById('alertAdminError'),
      formTambahAdmin: document.getElementById('formTambahAdmin'),
      adminEmail: document.getElementById('adminEmail'),
      tabelAdmin: document.getElementById('tabelAdmin'),

      // Page Pengaturan Jam
      formPengaturanJam: document.getElementById('formPengaturanJam'),
      inputJamMasukBuka: document.getElementById('inputJamMasukBuka'),
      inputJamMasukTerlambat: document.getElementById('inputJamMasukTerlambat'),
      inputJamMasukTutup: document.getElementById('inputJamMasukTutup'),
      inputJamPulangBuka: document.getElementById('inputJamPulangBuka'),
      inputJamPulangTutup: document.getElementById('inputJamPulangTutup'),
      jadwalHariTabs: document.querySelectorAll('.jadwal-hari-tab'),
      labelHariTerpilih: document.getElementById('labelHariTerpilih'),
      descHariTerpilih: document.getElementById('descHariTerpilih'),
      hariAktifToggle: document.getElementById('hariAktifToggle'),
      labelHariAktif: document.getElementById('labelHariAktif'),
      panelWaktuHari: document.getElementById('panelWaktuHari'),
      btnSalinKeKerja: document.getElementById('btnSalinKeKerja'),
      tabelRingkasanJadwal: document.getElementById('tabelRingkasanJadwal'),
      btnSimpanPengaturan: document.getElementById('btnSimpanPengaturan'),
      btnResetPengaturan: document.getElementById('btnResetPengaturan'),
      pengaturanTerakhirUpdate: document.getElementById('pengaturanTerakhirUpdate'),
      pengaturanJamAksi: document.getElementById('pengaturanJamAksi'),
      alertPengaturanSuccess: document.getElementById('alertPengaturanSuccess'),
      alertPengaturanError: document.getElementById('alertPengaturanError'),
    };
  }

  /**
   * Menginisialisasi UI: setup default inputs, bind listeners, load awal.
   */
  init() {
    this.cacheDOM();
    console.log("UIManager init: btnAdminToggle =", this.dom.btnAdminToggle);
    const today = new Date();

    // Set default value tanggal
    if (this.dom.inputTanggal) {
      this.dom.inputTanggal.value = this.formatTanggalInput(today);
    }
    if (this.dom.tglMulai) {
      this.dom.tglMulai.value = this.formatTanggalInput(today);
    }
    if (this.dom.tglAkhir) {
      this.dom.tglAkhir.value = this.formatTanggalInput(today);
    }
    if (this.dom.statBulanInput) {
      this.dom.statBulanInput.value = this.formatTanggalInput(today).slice(0, 7); // YYYY-MM
    }

    this.bindEvents();

    // Jalankan observer status autentikasi Firebase
    this.auth.observeAuthState((user, isAdmin, errorMessage) => {
      if (errorMessage) {
        this.dom.loginError.textContent = errorMessage;
        this.dom.loginError.style.display = 'block';
        this.openLoginModal();
      }
      this.renderAdminState();
    });

    // Jalankan listener Firebase awal
    this.setupFirebaseListeners();
  }

  /**
   * Mengatur listener database real-time.
   */
  setupFirebaseListeners() {
    // 1. Load Siswa Terdaftar (selalu aktif untuk cache)
    this.dbService.subscribeSiswa((snapshot) => {
      this.daftarSiswaCache = {};
      this.siswaRowsCache = [];

      if (snapshot.exists()) {
        snapshot.forEach((child) => {
          const d = child.val();
          const uid = child.key;
          this.daftarSiswaCache[uid] = d;
          this.siswaRowsCache.push({ uid, d });
        });

        // urutkan berdasarkan nama
        this.siswaRowsCache.sort((a, b) => (a.d.nama || '').localeCompare(b.d.nama || ''));
      }

      this.renderTabelSiswa(this.dom.searchSiswa.value);
      this.refreshStatFilters();
      this.renderStatistikMuridDanKelas();
      this.renderJumlahMurid();

      // Trigger reload absensi hari ini setelah siswa di-cache agar angka "Belum Hadir" akurat
      const tanggalKey = this.formatTanggalFirebase(new Date(this.dom.inputTanggal.value));
      this.loadAbsensi(tanggalKey);
    });

    // 2. Load Kartu Tidak Dikenal
    this.dbService.subscribeTidakDikenal((snapshot) => {
      this.renderTabelTidakDikenal(snapshot);
      this.renderLastScannedUID(snapshot);
    });

    // 3. Load Daftar Admin
    this.dbService.subscribeAdmins((snapshot) => {
      this.renderTabelAdmin(snapshot);
    });

    // 4. Load Pengaturan Jam Kerja & Jadwal Per Hari
    this.dbService.subscribePengaturan((snapshot) => {
      if (snapshot.exists()) {
        const val = snapshot.val();
        if (val.jadwal_harian) {
          this.cacheJadwalHarian = { ...this.cacheJadwalHarian, ...val.jadwal_harian };
        }
        this.cachePengaturan = val;
      }

      this.renderCurrentDayForm();
      this.renderDayBadges();
      this.renderRingkasanJadwal();

      if (this.cachePengaturan && this.cachePengaturan.terakhir_diperbarui && this.dom.pengaturanTerakhirUpdate) {
        const date = new Date(this.cachePengaturan.terakhir_diperbarui);
        const formattedDate = date.toLocaleDateString('id-ID', { day: '2-digit', month: 'short', year: 'numeric' });
        const formattedTime = date.toLocaleTimeString('id-ID', { hour: '2-digit', minute: '2-digit' });
        this.dom.pengaturanTerakhirUpdate.textContent = `Terakhir diperbarui: ${formattedDate}, ${formattedTime}`;
      }
    });
  }

  /**
   * Menghubungkan semua event listener DOM.
   */
  bindEvents() {
    console.log("bindEvents dijalankan");

    // Mobile Sidebar Toggle
    if (this.dom.btnMobileMenu && this.dom.mainSidebar && this.dom.mobileOverlay) {
      const toggleSidebar = () => {
        this.dom.mainSidebar.classList.toggle('mobile-open');
        this.dom.mobileOverlay.classList.toggle('active');
      };
      
      this.dom.btnMobileMenu.addEventListener('click', toggleSidebar);
      this.dom.mobileOverlay.addEventListener('click', toggleSidebar);
      
      // Tutup menu otomatis jika user mengklik salah satu menu
      this.dom.tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
          if (window.innerWidth <= 768 && this.dom.mainSidebar.classList.contains('mobile-open')) {
            toggleSidebar();
          }
        });
      });
    }


    if (this.dom.btnAdminToggle) {
      this.dom.btnAdminToggle.addEventListener('click', async () => {
        console.log("Tombol Login Admin diklik");

        if (this.auth.isAdmin()) {
          await this.auth.logout();
          this.renderAdminState();
        } else {
          this.openLoginModal();
        }
      });
    }

    // Modal Login
    if (this.dom.btnLoginCancel) {
      this.dom.btnLoginCancel.addEventListener('click', () => this.closeLoginModal());
    }
    this.dom.btnGoogleLogin.addEventListener('click', () => this.handleGoogleLogin());

    // Tombol Login dari Halaman Terkunci
    this.dom.btnLoginsFromLocked.forEach(btn => {
      btn.addEventListener('click', () => this.openLoginModal());
    });


    // Page Absensi - Tanggal berubah
    this.dom.inputTanggal.addEventListener('change', (e) => {
      const selected = new Date(e.target.value);
      this.loadAbsensi(this.formatTanggalFirebase(selected));
    });

    // Page Laporan - Tampilkan
    
    // Update Laporan Filters cascading
    if (this.dom.lapJurusan && this.dom.lapKelas) {
      this.dom.lapJurusan.addEventListener('change', () => {
        const jur = this.dom.lapJurusan.value;
        const curKelas = this.dom.lapKelas.value;
        this.dom.lapKelas.innerHTML = '<option value="">Semua Kelas</option>';
        const kSet = new Set();
        Object.values(this.daftarSiswaCache).forEach(d => {
          if (!jur || (d.jurusan || 'Lainnya') === jur) {
            kSet.add(d.kelas || 'Lainnya');
          }
        });
        [...kSet].sort().forEach(k => {
          this.dom.lapKelas.innerHTML += `<option value="${k}">${k}</option>`;
        });
      });
    }

    this.dom.btnTampilkanLaporan.addEventListener('click', () => this.handleTampilkanLaporan());

    // Page Laporan - Export CSV
    this.dom.btnExportExcel.addEventListener('click', () => this.handleExportExcel());

    // Page Statistik - Tampilkan
    this.dom.btnTampilkanStatistik.addEventListener('click', () => this.handleTampilkanStatistik());

    // Page Registrasi - Pencarian Siswa
    this.dom.searchSiswa.addEventListener('input', (e) => {
      this.renderTabelSiswa(e.target.value);
    });

    // Page Registrasi - Gunakan UID dari Tap Terakhir
    this.dom.btnGunakanUID.addEventListener('click', () => {
      const uid = this.dom.lastScannedUID.textContent;
      if (uid && uid !== '-') {
        this.dom.regUID.value = uid;
      } else {
        this.showAlert('error', 'Belum ada UID yang terbaca hari ini.');
      }
    });

    // Page Registrasi - Submit Form Registrasi
    this.dom.formRegistrasi.addEventListener('submit', (e) => this.handleRegistrasiSubmit(e));

    // Page Kelola Admin - Submit Form Tambah Admin
    this.dom.formTambahAdmin.addEventListener('submit', (e) => this.handleTambahAdminSubmit(e));

    // Modal Edit - Cancel
    this.dom.btnEditCancel.addEventListener('click', () => this.closeEditModal());

    // Modal Edit - Submit
    this.dom.btnEditSubmit.addEventListener('click', () => this.handleEditSiswaSubmit());

    // Page Jumlah Murid - Grouping toggle buttons
    const groupBtns = document.querySelectorAll('#page-jumlah-murid .group-btn');
    groupBtns.forEach(btn => {
      btn.addEventListener('click', () => {
        // Remove active class styling from all buttons
        groupBtns.forEach(b => {
          b.classList.remove('active', 'text-[#1e293b]', 'bg-[#f8fafc]', 'border', 'border-[#e2e8f0]');
          b.classList.add('text-[#64748b]');
        });
        
        // Add active class styling to clicked button
        btn.classList.add('active', 'text-[#1e293b]', 'bg-[#f8fafc]', 'border', 'border-[#e2e8f0]');
        btn.classList.remove('text-[#64748b]');
        
        this.currentGroupMode = btn.dataset.groupMode;
        this.renderJumlahMurid();
      });
    });

    // Page Pengaturan Jam - Tab Hari Switching
    if (this.dom.jadwalHariTabs) {
      this.dom.jadwalHariTabs.forEach(btn => {
        btn.addEventListener('click', () => {
          this.switchJadwalHariTab(btn.dataset.hari);
        });
      });
    }

    // Page Pengaturan Jam - Toggle Status Aktif Hari
    if (this.dom.hariAktifToggle) {
      this.dom.hariAktifToggle.addEventListener('change', (e) => {
        const isChecked = e.target.checked;
        if (this.cacheJadwalHarian[this.currentDayTab]) {
          this.cacheJadwalHarian[this.currentDayTab].aktif = isChecked;
        }
        this.dom.panelWaktuHari.style.opacity = isChecked ? '1' : '0.4';
        this.dom.labelHariAktif.textContent = isChecked ? 'Hari Sekolah (Absensi Aktif)' : 'Hari Libur (Absensi Tutup)';
        this.renderDayBadges();
        this.renderRingkasanJadwal();
      });
    }

    // Page Pengaturan Jam - Salin ke Senin-Jumat
    if (this.dom.btnSalinKeKerja) {
      this.dom.btnSalinKeKerja.addEventListener('click', () => {
        this.saveCurrentInputsToCache();
        const currentData = { ...this.cacheJadwalHarian[this.currentDayTab] };
        ['senin', 'selasa', 'rabu', 'kamis', 'jumat'].forEach(hari => {
          this.cacheJadwalHarian[hari] = { ...currentData, aktif: true };
        });
        this.renderDayBadges();
        this.renderRingkasanJadwal();
        this.showPengaturanAlert('success', `Jadwal hari ${this.currentDayTab.toUpperCase()} berhasil disalin ke semua hari kerja (Senin–Jumat).`);
      });
    }

    // Page Pengaturan Jam - Submit & Reset Form Pengaturan
    if (this.dom.formPengaturanJam) {
      this.dom.formPengaturanJam.addEventListener('submit', (e) => this.handlePengaturanJamSubmit(e));
    }
    if (this.dom.btnResetPengaturan) {
      this.dom.btnResetPengaturan.addEventListener('click', () => {
        this.renderCurrentDayForm();
        this.showPengaturanAlert('success', 'Form pengaturan hari ini di-reset.');
      });
    }

    // Page Pengaturan Jam - Masking Input Jam (HH:MM)
    const timeInputs = [
      this.dom.inputJamMasukBuka,
      this.dom.inputJamMasukTerlambat,
      this.dom.inputJamMasukTutup,
      this.dom.inputJamPulangBuka,
      this.dom.inputJamPulangTutup
    ];
    timeInputs.forEach(input => {
      if (input) {
        input.addEventListener('input', (e) => {
          let val = e.target.value.replace(/[^0-9:]/g, '');
          
          // Tambahkan titik dua otomatis
          if (val.length === 2 && !val.includes(':') && e.inputType !== 'deleteContentBackward') {
            val = val + ':';
          }
          
          // Batasi jam (00-23) dan menit (00-59)
          const parts = val.split(':');
          if (parts[0] && parts[0].length <= 2) {
            const h = Number(parts[0]);
            if (h > 23) parts[0] = '23';
          }
          if (parts[1] && parts[1].length <= 2) {
            const m = Number(parts[1]);
            if (m > 59) parts[1] = '59';
          }
          val = parts.join(':');
          
          e.target.value = val.slice(0, 5);
        });
      }
    });
  }

  /**
   * Mengupdate UI berdasarkan status login Admin (Terkunci vs Terbuka).
   */
  renderAdminState() {
    const admin = this.auth.isAdmin();
    const currentUser = this.auth.getCurrentUser();

    // Pilih elemen tab-btn secara dinamis untuk menghindari issue sinkronisasi DOM
    const tabBtns = document.querySelectorAll('.tab-btn');
    tabBtns.forEach(btn => {
      const lockIcon = btn.querySelector('.lock-icon');
      if (lockIcon) {
        lockIcon.style.display = admin ? 'none' : 'inline';
      }
    });

    if (admin && currentUser) {
      this.dom.adminLabel.textContent = `Mode: Admin (${currentUser.email})`;
      this.dom.btnAdminToggle.textContent = 'Logout';

      this.dom.registrasiContent.style.display = 'block';
      this.dom.registrasiLocked.style.display = 'none';
      this.dom.tidakDikenalContent.style.display = 'block';
      this.dom.tidakDikenalLocked.style.display = 'none';
      this.dom.kelolaAdminContent.style.display = 'block';
      this.dom.kelolaAdminLocked.style.display = 'none';
    } else {
      this.dom.adminLabel.textContent = 'Mode: Pengunjung';
      this.dom.btnAdminToggle.textContent = 'Login Admin';

      this.dom.registrasiContent.style.display = 'none';
      this.dom.registrasiLocked.style.display = 'block';
      this.dom.tidakDikenalContent.style.display = 'none';
      this.dom.tidakDikenalLocked.style.display = 'block';
      this.dom.kelolaAdminContent.style.display = 'none';
      this.dom.kelolaAdminLocked.style.display = 'block';

      // Kembali ke halaman Absensi jika sedang di halaman terproteksi saat logout
      const activePage = document.querySelector('.page.active');
      if (activePage && (activePage.id === 'page-registrasi' || activePage.id === 'page-tidak-dikenal' || activePage.id === 'page-kelola-admin')) {
        this.switchTab('absensi');
      }
    }

    // Mengatur hak akses input & tombol aksi halaman Pengaturan Jam
    const inputs = [
      this.dom.inputJamMasukBuka,
      this.dom.inputJamMasukTerlambat,
      this.dom.inputJamMasukTutup,
      this.dom.inputJamPulangBuka,
      this.dom.inputJamPulangTutup,
      this.dom.hariAktifToggle,
      this.dom.btnSalinKeKerja
    ];

    inputs.forEach(input => {
      if (input) {
        input.disabled = !admin;
      }
    });

    if (this.dom.pengaturanJamAksi) {
      this.dom.pengaturanJamAksi.style.display = admin ? 'flex' : 'none';
    }
  }

  // ====== MODAL LOGIN ======
  openLoginModal() {
    this.dom.loginError.style.display = 'none';
    this.dom.modalLogin.style.display = 'flex';
  }

  closeLoginModal() {
    this.dom.modalLogin.style.display = 'none';
  }

  // Sesudah:
  async handleGoogleLogin() {
    this.dom.loginError.style.display = 'none';
    try {
      await this.auth.loginWithGoogle();
      this.closeLoginModal();
      this.renderAdminState();
    } catch (err) {
      this.dom.loginError.textContent = err.message || 'Gagal login.';
      this.dom.loginError.style.display = 'block';
    }
  }

  // ====== TAB NAVIGATION ======
  switchTab(pageName) {
    if (typeof window.navigateToPage === 'function') {
      window.navigateToPage(pageName);
    } else {
      const tabBtns = document.querySelectorAll('.tab-btn');
      tabBtns.forEach(b => {
        b.classList.toggle('active', b.dataset.page === pageName);
      });
      const pages = document.querySelectorAll('.page');
      pages.forEach(p => p.classList.remove('active'));
      const targetPage = document.getElementById('page-' + pageName);
      if (targetPage) {
        targetPage.classList.add('active');
      }
    }
  }

  // ====== PAGE 1: ABSENSI ======
  loadAbsensi(tanggalKey) {
    if (this.currentAbsensiUnsub) this.currentAbsensiUnsub();

    this.dom.tabelAbsensi.innerHTML = `<tr><td colspan="7" class="empty">Memuat data...</td></tr>`;

    this.currentAbsensiUnsub = this.dbService.subscribeAbsensi(tanggalKey, (snapshot) => {
      this.dom.tabelAbsensi.innerHTML = '';
      let totalHadir = 0, totalTerlambat = 0;
      const hadirUIDs = new Set();

      if (snapshot.exists()) {
        let no = 1;
        const rows = [];
        snapshot.forEach((child) => {
          const d = child.val();
          const status = (d.status || '').toUpperCase();
          let statusClass = 'status-default';

          if (status === 'HADIR') {
            statusClass = 'status-hadir';
            totalHadir++;
          } else if (status === 'TERLAMBAT') {
            statusClass = 'status-terlambat';
            totalTerlambat++;
          }

          if (d.uid) hadirUIDs.add(d.uid);

          const jamMasuk = d.jam_masuk || d.jam || d.waktu_masuk || d.waktu || '-';
          const jamPulang = d.jam_pulang || d.waktu_pulang || '-';
          rows.push(`
            <tr>
              <td>${no++}</td>
              <td>${d.nama ? d.nama.replace(/_/g, ' ') : '-'}</td>
              <td>${d.nisn || '-'}</td>
              <td>${d.uid || '-'}</td>
              <td>${jamMasuk}</td>
              <td>${jamPulang}</td>
              <td><span class="status ${statusClass}">${d.status || '-'}</span></td>
            </tr>
          `);
        });
        this.dom.tabelAbsensi.innerHTML = rows.join('');
        this.dom.statTotal.textContent = no - 1;
      } else {
        this.dom.tabelAbsensi.innerHTML = `<tr><td colspan="7" class="empty">Tidak ada data absensi untuk tanggal ini</td></tr>`;
        this.dom.statTotal.textContent = '0';
      }

      this.dom.statHadir.textContent = totalHadir;
      this.dom.statTerlambat.textContent = totalTerlambat;

      const totalSiswa = Object.keys(this.daftarSiswaCache).length;
      const belumHadir = Math.max(totalSiswa - hadirUIDs.size, 0);
      this.dom.statBelumHadir.textContent = belumHadir;

      this.renderChartAbsensiHariIni(totalHadir, totalTerlambat, belumHadir);
    });
  }

  renderChartAbsensiHariIni(hadir, terlambat, belumHadir) {
    const data = {
      labels: ['Hadir', 'Terlambat', 'Belum Hadir'],
      datasets: [{
        data: [hadir, terlambat, belumHadir],
        backgroundColor: ['#27a35a', '#e0922a', '#c3c8cf']
      }]
    };

    if (this.chartAbsensiHariIni) {
      this.chartAbsensiHariIni.data = data;
      this.chartAbsensiHariIni.update();
    } else {
      this.chartAbsensiHariIni = new Chart(this.dom.chartAbsensiHariIni, {
        type: 'doughnut',
        data: data,
        options: {
          responsive: true,
          plugins: {
            legend: { position: 'bottom', labels: { font: { size: 12 } } }
          }
        }
      });
    }
  }

  // ====== PAGE 2: LAPORAN ======
  async handleTampilkanLaporan() {
    this.dom.tabelLaporan.innerHTML = `<tr><td colspan="9" class="empty">Memuat data...</td></tr>`;

    const start = this.dom.tglMulai.value;
    const end = this.dom.tglAkhir.value;
    const dateKeys = this.getDateRange(start, end);

    this.laporanData = [];
    let totalHadir = 0, totalTerlambat = 0;

    const rawRecords = await this.dbService.getAbsensiRange(dateKeys);

    rawRecords.forEach(record => {
      const uid = record.key;
      const d = record.val;
      const siswaData = this.daftarSiswaCache[uid] || {};
      
      const status = (d.status || '').toUpperCase();
      if (status === 'HADIR') totalHadir++;
      else if (status === 'TERLAMBAT') totalTerlambat++;

      const jamMasuk = d.jam_masuk || d.jam || d.waktu_masuk || d.waktu || '-';
      let jamPulang = d.jam_pulang || d.waktu_pulang;
      
      if (!jamPulang && (status === 'HADIR' || status === 'TERLAMBAT')) {
        jamPulang = '16:00 (Auto)';
      } else if (!jamPulang) {
        jamPulang = '-';
      }
      
      const jurusan = d.jurusan || siswaData.jurusan || '-';
      const angkatan = d.angkatan || siswaData.angkatan || '-';
      
      this.laporanData.push({
        tanggal: d.tanggal || record.tanggalKey,
        nama: d.nama || siswaData.nama || '-',
        nisn: d.nisn || siswaData.nisn || '-',
        kelas: d.kelas || siswaData.kelas || '-',
        jurusan: jurusan,
        angkatan: angkatan,
        status: d.status || '-',
        jam_masuk: jamMasuk,
        jam_pulang: jamPulang
      });
    });

    this.dom.lapTotal.textContent = this.laporanData.length;
    this.dom.lapHadir.textContent = totalHadir;
    this.dom.lapTerlambat.textContent = totalTerlambat;

    if (this.laporanData.length === 0) {
      this.dom.tabelLaporan.innerHTML = `<tr><td colspan="9" class="empty">Tidak ada data pada rentang tanggal ini</td></tr>`;
      return;
    }

    this.dom.tabelLaporan.innerHTML = this.laporanData.map((d, i) => {
      const status = (d.status || '').toUpperCase();
      let statusClass = 'status-default';
      if (status === 'HADIR') statusClass = 'status-hadir';
      else if (status === 'TERLAMBAT') statusClass = 'status-terlambat';

      return `
        <tr>
          <td>${d.tanggal}</td>
          <td>${d.nama ? d.nama.replace(/_/g, ' ') : '-'}</td>
          <td>${d.nisn || '-'}</td>
          <td>${d.kelas || '-'}</td>
          <td>${d.jurusan || '-'}</td>
          <td>${d.angkatan || '-'}</td>
          <td><span class="status ${statusClass}">${d.status}</span></td>
          <td>${d.jam_masuk}</td>
          <td>${d.jam_pulang}</td>
        </tr>
      `;
    }).join('');
  }

  handleExportExcel() {
    if (this.laporanData.length === 0) {
      alert('Tidak ada data untuk diexport. Klik "Tampilkan" dulu.');
      return;
    }
    
    // Siapkan data array-of-arrays untuk SheetJS
    const rows = [
      ['Tanggal', 'Nama Siswa', 'NISN', 'Kelas', 'Jurusan', 'Angkatan', 'Status', 'Jam Masuk', 'Jam Pulang']
    ];
    
    this.laporanData.forEach(d => {
      rows.push([
        d.tanggal,
        d.nama ? d.nama.replace(/_/g, ' ') : '-',
        d.nisn || '-',
        d.kelas || '-',
        d.jurusan || '-',
        d.angkatan || '-',
        d.status,
        d.jam_masuk,
        d.jam_pulang
      ]);
    });

    if (typeof XLSX === 'undefined') {
      alert('Library SheetJS belum termuat. Silakan muat ulang halaman.');
      return;
    }

    const ws = XLSX.utils.aoa_to_sheet(rows);
    
    // Set column widths
    const wscols = [
      {wch: 12}, // Tanggal
      {wch: 25}, // Nama
      {wch: 15}, // NISN
      {wch: 10}, // Kelas
      {wch: 15}, // Jurusan
      {wch: 12}, // Angkatan
      {wch: 15}, // Status
      {wch: 12}, // Jam Masuk
      {wch: 12}  // Jam Pulang
    ];
    ws['!cols'] = wscols;

    const wb = XLSX.utils.book_new();
    XLSX.utils.book_append_sheet(wb, ws, "Laporan Absensi");
    XLSX.writeFile(wb, `laporan_absensi_${this.dom.tglMulai.value}_sd_${this.dom.tglAkhir.value}.xlsx`);
  }
  // ====== PAGE 3: STATISTIK PER SISWA ======
  
  refreshStatFilters() {
    if (!this.dom.statJurusan || !this.dom.statKelas || !this.dom.statSiswaSelect) return;

    // Cache the mapping logic
    const mapKelas = {}; // mapKelas[jurusan] = Set of kelas
    const mapSiswa = {}; // mapSiswa[kelas] = Array of siswa

    Object.values(this.daftarSiswaCache).forEach(d => {
      const jur = (d.jurusan || 'Lainnya').trim();
      const kel = (d.kelas || 'Lainnya').trim();
      
      if (!mapKelas[jur]) mapKelas[jur] = new Set();
      mapKelas[jur].add(kel);

      if (!mapSiswa[kel]) mapSiswa[kel] = [];
      mapSiswa[kel].push(d);
    });

    const updateKelas = () => {
      const jur = this.dom.statJurusan.value;
      const curKelas = this.dom.statKelas.value;
      this.dom.statKelas.innerHTML = '<option value="">-- Semua Kelas --</option>';
      if (jur && mapKelas[jur]) {
        [...mapKelas[jur]].sort().forEach(k => {
          this.dom.statKelas.innerHTML += `<option value="${k}">${k}</option>`;
        });
      } else if (!jur) {
        // Jika tidak ada jurusan dipilih, tampilkan semua kelas
        const allKelas = new Set();
        Object.values(mapKelas).forEach(setK => setK.forEach(k => allKelas.add(k)));
        [...allKelas].sort().forEach(k => {
          this.dom.statKelas.innerHTML += `<option value="${k}">${k}</option>`;
        });
      }
      this.dom.statKelas.value = curKelas || '';
      updateSiswa();
    };

    const updateSiswa = () => {
      const kel = this.dom.statKelas.value;
      const jur = this.dom.statJurusan.value;
      const curSiswa = this.dom.statSiswaSelect.value;
      this.dom.statSiswaSelect.innerHTML = '<option value="">-- Semua Siswa (Rekap) --</option>';
      
      let siswasToShow = [];
      if (kel && mapSiswa[kel]) {
        siswasToShow = mapSiswa[kel];
      } else {
        // Gabungkan semua yang cocok dengan jurusan
        Object.values(this.daftarSiswaCache).forEach(d => {
          if (!jur || (d.jurusan || 'Lainnya') === jur) {
            siswasToShow.push(d);
          }
        });
      }

      siswasToShow.sort((a,b) => (a.nama || '').localeCompare(b.nama || ''));
      siswasToShow.forEach(d => {
        this.dom.statSiswaSelect.innerHTML += `<option value="${(d.nama || '').replace(/"/g, '')}">${(d.nama || '-').replace(/_/g, ' ')} (${d.kelas || '-'})</option>`;
      });

      if ([...this.dom.statSiswaSelect.options].some(o => o.value === curSiswa)) {
        this.dom.statSiswaSelect.value = curSiswa;
      }
    };

    // Remove old listeners to avoid duplicates if called multiple times
    const newJurusan = this.dom.statJurusan.cloneNode(true);
    this.dom.statJurusan.parentNode.replaceChild(newJurusan, this.dom.statJurusan);
    this.dom.statJurusan = newJurusan;

    const newKelas = this.dom.statKelas.cloneNode(true);
    this.dom.statKelas.parentNode.replaceChild(newKelas, this.dom.statKelas);
    this.dom.statKelas = newKelas;

    this.dom.statJurusan.addEventListener('change', updateKelas);
    this.dom.statKelas.addEventListener('change', updateSiswa);

    // Initial populate
    updateKelas();
  }
  async handleTampilkanStatistik() {
    const namaSiswa = this.dom.statSiswaSelect.value;
    const kelasSiswa = this.dom.statKelas.value;
    const jurusanSiswa = this.dom.statJurusan.value;
    const bulanVal = this.dom.statBulanInput.value; // format YYYY-MM

    if (!bulanVal) {
      alert('Pilih bulan terlebih dahulu.');
      return;
    }
    if (!namaSiswa && !kelasSiswa && !jurusanSiswa) {
      alert('Silakan pilih minimal Jurusan atau Kelas atau Siswa.');
      return;
    }

    const [yearStr, monthStr] = bulanVal.split('-');
    const year = parseInt(yearStr, 10);
    const month = parseInt(monthStr, 10);
    const jumlahHari = new Date(year, month, 0).getDate();

    this.dom.statistikKosong.textContent = 'Memuat data...';
    this.dom.statistikKosong.style.display = 'block';
    this.dom.statistikIsi.style.display = 'none';

    // Ambil data absensi sebulan (bisa berat jika 1 bulan penuh, tapi ini cara tercepat)
    const dateKeys = [];
    for (let tgl = 1; tgl <= jumlahHari; tgl++) {
      dateKeys.push(`${tgl}-${month}-${year}`);
    }
    const rawRecords = await this.dbService.getAbsensiRange(dateKeys);

    const today = new Date();
    const isBulanIni = (year === today.getFullYear()) && (month === (today.getMonth() + 1));
    const maxHari = isBulanIni ? today.getDate() : jumlahHari;
    
    // Hanya hitung Senin - Jumat (Hari Efektif)
    let totalHariDihitung = 0;
    for (let d = 1; d <= maxHari; d++) {
      const currentDay = new Date(year, month - 1, d).getDay();
      if (currentDay !== 0 && currentDay !== 6) { // 0: Minggu, 6: Sabtu
        totalHariDihitung++;
      }
    }

    if (namaSiswa) {
      // MODE: 1 SISWA DETAIL
      let totalHadir = 0, totalTerlambat = 0;
      const detailRows = [];
      const harianHadir = Array(jumlahHari).fill(0);
      const labelHarian = Array.from({length: jumlahHari}, (_, i) => String(i + 1));

      rawRecords.forEach(record => {
        const d = record.val;
        if ((d.nama || '') === namaSiswa) {
          const tglStr = d.tanggal || record.tanggalKey;
          const [tglPart] = tglStr.split('-');
          const hariIdx = parseInt(tglPart, 10) - 1;
          harianHadir[hariIdx] = 1;

          const status = (d.status || '').toUpperCase();
          if (status === 'HADIR') totalHadir++;
          else if (status === 'TERLAMBAT') totalTerlambat++;

          detailRows.push({
            tanggal: tglStr,
            jam: d.jam_masuk || d.jam || '-',
            jam_pulang: d.jam_pulang || '-',
            status: d.status || '-'
          });
        }
      });

      const totalTercatat = totalHadir + totalTerlambat;
      const totalTidakHadir = Math.max(totalHariDihitung - totalTercatat, 0);
      const persenHadir = totalHariDihitung > 0 ? Math.round((totalTercatat / totalHariDihitung) * 100) : 0;

      this.dom.stHadir.textContent = totalHadir;
      this.dom.stTerlambat.textContent = totalTerlambat;
      this.dom.stTidakHadir.textContent = totalTidakHadir;
      this.dom.stPersenHadir.textContent = persenHadir + '%';

      // Restore table header for 1 siswa if it was previously in recap mode
      this.dom.tabelStatistikDetail.parentElement.innerHTML = `
        <table>
          <thead>
            <tr>
              <th>No</th>
              <th>Tanggal</th>
              <th>Jam Masuk</th>
              <th>Jam Pulang</th>
              <th>Status</th>
            </tr>
          </thead>
          <tbody id="tabelStatistikDetail"></tbody>
        </table>
      `;
      this.dom.tabelStatistikDetail = document.getElementById('tabelStatistikDetail');

      if (detailRows.length === 0) {
        this.dom.tabelStatistikDetail.innerHTML = `<tr><td colspan="4" class="empty">Tidak ada data kehadiran pada bulan ini</td></tr>`;
      } else {
        // Sort based on tanggal asc
        detailRows.sort((a,b) => parseInt(a.tanggal.split('-')[0]) - parseInt(b.tanggal.split('-')[0]));
        this.dom.tabelStatistikDetail.innerHTML = detailRows.map((d, i) => {
          const status = (d.status || '').toUpperCase();
          let statusClass = 'status-default';
          if (status === 'HADIR') statusClass = 'status-hadir';
          else if (status === 'TERLAMBAT') statusClass = 'status-terlambat';
          return `
            <tr>
              <td>${i + 1}</td>
              <td>${d.tanggal}</td>
              <td>${d.jam}</td>
              <td>${d.jam_pulang}</td>
              <td><span class="status ${statusClass}">${d.status}</span></td>
            </tr>
          `;
        }).join('');
      }

      this.renderChartStatistikRingkasan(totalHadir, totalTerlambat, totalTidakHadir);
      this.renderChartStatistikHarian(labelHarian.slice(0, totalHariDihitung), harianHadir.slice(0, totalHariDihitung));

    } else {
      // MODE: REKAP KELAS / JURUSAN (Semua Siswa)
      // Kumpulkan siswa yg relevan
      const siswasRelevan = [];
      Object.values(this.daftarSiswaCache).forEach(d => {
        const jur = d.jurusan || 'Lainnya';
        const kel = d.kelas || 'Lainnya';
        let match = true;
        if (jurusanSiswa && jur !== jurusanSiswa) match = false;
        if (kelasSiswa && kel !== kelasSiswa) match = false;
        if (match) siswasRelevan.push(d);
      });

      if (siswasRelevan.length === 0) {
        this.dom.tabelStatistikDetail.innerHTML = `<tr><td colspan="4" class="empty">Tidak ada siswa terdaftar di filter ini</td></tr>`;
        this.dom.stHadir.textContent = 0;
        this.dom.stTerlambat.textContent = 0;
        this.dom.stTidakHadir.textContent = 0;
        this.dom.stPersenHadir.textContent = '0%';
        this.renderChartStatistikRingkasan(0, 0, 0);
        this.renderChartStatistikHarian([], []);
        this.dom.statistikKosong.style.display = 'none';
        this.dom.statistikIsi.style.display = 'block';
        return;
      }

      const rekap = {};
      siswasRelevan.forEach(s => {
        rekap[s.nama] = { hadir: 0, terlambat: 0, kelas: s.kelas };
      });

      let globHadir = 0, globTerlambat = 0, globTercatat = 0;
      
      rawRecords.forEach(record => {
        const d = record.val;
        const n = d.nama || '';
        if (rekap[n]) {
          const status = (d.status || '').toUpperCase();
          if (status === 'HADIR') { rekap[n].hadir++; globHadir++; globTercatat++; }
          else if (status === 'TERLAMBAT') { rekap[n].terlambat++; globTerlambat++; globTercatat++; }
        }
      });

      const totalExpected = siswasRelevan.length * totalHariDihitung;
      const globTidakHadir = Math.max(totalExpected - globTercatat, 0);
      const globPersen = totalExpected > 0 ? Math.round((globTercatat / totalExpected) * 100) : 0;

      this.dom.stHadir.textContent = globHadir;
      this.dom.stTerlambat.textContent = globTerlambat;
      this.dom.stTidakHadir.textContent = globTidakHadir;
      this.dom.stPersenHadir.textContent = globPersen + '%';

      this.dom.tabelStatistikDetail.parentElement.innerHTML = `
        <table class="w-full text-left text-xs border-collapse">
          <thead>
            <tr class="border-b border-slate-200 text-slate-500">
              <th class="py-2">No</th>
              <th class="py-2">Nama Siswa</th>
              <th class="py-2">Kelas</th>
              <th class="py-2">Hadir</th>
              <th class="py-2">Terlambat</th>
              <th class="py-2">Tidak Hadir</th>
              <th class="py-2">Persentase</th>
            </tr>
          </thead>
          <tbody id="tabelStatistikDetail">
            ${siswasRelevan.sort((a,b)=>a.nama.localeCompare(b.nama)).map((s, i) => {
              const r = rekap[s.nama];
              const t = r.hadir + r.terlambat;
              const x = Math.max(totalHariDihitung - t, 0);
              const p = totalHariDihitung > 0 ? Math.round((t / totalHariDihitung) * 100) : 0;
              return `
                <tr class="border-b border-slate-200 hover:bg-slate-50">
                  <td class="py-2">${i+1}</td>
                  <td class="py-2 font-medium">${s.nama.replace(/_/g, ' ')}</td>
                  <td class="py-2">${r.kelas || '-'}</td>
                  <td class="py-2 text-emerald-600 font-bold">${r.hadir}</td>
                  <td class="py-2 text-orange-500 font-bold">${r.terlambat}</td>
                  <td class="py-2 text-red-500 font-bold">${x}</td>
                  <td class="py-2">${p}%</td>
                </tr>
              `;
            }).join('')}
          </tbody>
        </table>
      `;
      // Restore the DOM reference!
      this.dom.tabelStatistikDetail = document.getElementById('tabelStatistikDetail');

      this.renderChartStatistikRingkasan(globHadir, globTerlambat, globTidakHadir);
      // Disable harian chart for class overview because it's too complex
      this.renderChartStatistikHarian([], []);
    }

    this.dom.statistikKosong.style.display = 'none';
    this.dom.statistikIsi.style.display = 'block';
  }
  renderChartStatistikRingkasan(hadir, terlambat, tidakHadir) {
    const data = {
      labels: ['Hadir', 'Terlambat', 'Tidak Hadir'],
      datasets: [{
        data: [hadir, terlambat, tidakHadir],
        backgroundColor: ['#27a35a', '#e0922a', '#c3504f']
      }]
    };

    if (this.chartStatistikRingkasan) {
      this.chartStatistikRingkasan.data = data;
      this.chartStatistikRingkasan.update();
    } else {
      this.chartStatistikRingkasan = new Chart(this.dom.chartStatistikRingkasan, {
        type: 'doughnut',
        data: data,
        options: {
          responsive: true,
          plugins: { legend: { position: 'bottom', labels: { font: { size: 12 } } } }
        }
      });
    }
  }

  renderChartStatistikHarian(labels, dataHarian) {
    const data = {
      labels: labels,
      datasets: [{
        label: 'Kehadiran',
        data: dataHarian,
        backgroundColor: '#2c3e50'
      }]
    };

    if (this.chartStatistikHarian) {
      this.chartStatistikHarian.data = data;
      this.chartStatistikHarian.update();
    } else {
      this.chartStatistikHarian = new Chart(this.dom.chartStatistikHarian, {
        type: 'bar',
        data: data,
        options: {
          responsive: true,
          scales: {
            y: {
              min: 0,
              max: 1,
              ticks: {
                stepSize: 1,
                callback: (val) => val === 1 ? 'Hadir' : (val === 0 ? 'Tidak' : '')
              }
            },
            x: {
              title: { display: true, text: 'Tanggal' }
            }
          },
          plugins: {
            legend: { display: false },
            title: { display: true, text: 'Rekap Harian dalam Bulan' }
          }
        }
      });
    }
  }

  renderStatistikMuridDanKelas() {
    const totalMurid = this.siswaRowsCache.length;
    if (this.dom.statTotalMurid) {
      this.dom.statTotalMurid.textContent = totalMurid;
    }

    // Hitung jumlah murid per kelas dan jurusan unik
    const kelasCounts = {};
    const jurusanUnik = new Set();
    
    this.siswaRowsCache.forEach(({ d }) => {
      const kelas = (d.kelas || 'TIDAK ADA KELAS').trim().toUpperCase();
      const jurusan = (d.jurusan || 'Lainnya').trim().toUpperCase();
      
      kelasCounts[kelas] = (kelasCounts[kelas] || 0) + 1;
      if(d.jurusan && d.jurusan.trim() !== '') {
         jurusanUnik.add(jurusan);
      }
    });

    const statTotalKelas = document.getElementById('statTotalKelas');
    const statTotalJurusan = document.getElementById('statTotalJurusan');
    
    // Urutkan kelas secara alfabetis
    const sortedKelas = Object.keys(kelasCounts).sort();
    
    if (statTotalKelas) statTotalKelas.textContent = sortedKelas.length;
    if (statTotalJurusan) statTotalJurusan.textContent = jurusanUnik.size;

    // Render tabel pemetaan kelas
    if (this.dom.tabelKelasMurid) {
      if (sortedKelas.length === 0) {
        this.dom.tabelKelasMurid.innerHTML = `
          <tr>
            <td colspan="2" class="text-center py-8 text-xs text-slate-400">Belum ada data siswa</td>
          </tr>
        `;
      } else {
        this.dom.tabelKelasMurid.innerHTML = sortedKelas.map((kelas, idx) => `
          <tr class="${idx !== sortedKelas.length - 1 ? 'border-b border-slate-100' : ''} hover:bg-slate-50 transition-colors">
            <td class="py-3 text-xs font-semibold text-slate-700">
              <div class="flex items-center gap-2">
                <span class="w-2 h-2 rounded-full bg-blue-500"></span>
                ${kelas}
              </div>
            </td>
            <td class="py-3 text-xs font-bold text-right text-slate-700">
              <span class="bg-blue-100 text-blue-700 py-1 px-2 rounded-md">${kelasCounts[kelas]}</span>
            </td>
          </tr>
        `).join('');
      }
    }

    // Render Chart.js diagram batang distribusi kelas
    if (this.dom.chartDistribusiMurid) {
      const counts = sortedKelas.map(kelas => kelasCounts[kelas]);
      const data = {
        labels: sortedKelas,
        datasets: [{
          label: 'Jumlah Siswa',
          data: counts,
          backgroundColor: '#3b82f6',
          hoverBackgroundColor: '#2563eb',
          borderRadius: 6,
          borderSkipped: false
        }]
      };

      if (this.chartDistribusiMurid) {
        this.chartDistribusiMurid.data = data;
        this.chartDistribusiMurid.update();
      } else {
        this.chartDistribusiMurid = new Chart(this.dom.chartDistribusiMurid, {
          type: 'bar',
          data: data,
          options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: {
              legend: { display: false },
              tooltip: {
                backgroundColor: 'rgba(15, 23, 42, 0.9)',
                titleFont: { size: 13 },
                bodyFont: { size: 13 },
                padding: 10,
                cornerRadius: 8,
                displayColors: false
              }
            },
            scales: {
              y: { 
                beginAtZero: true, 
                ticks: { precision: 0, color: '#64748b' },
                grid: { color: '#f1f5f9', drawBorder: false }
              },
              x: {
                ticks: { color: '#64748b', font: { size: 11 } },
                grid: { display: false, drawBorder: false }
              }
            }
          }
        });
      }
    }
  }

  renderJumlahMurid() {
    const totalMurid = this.siswaRowsCache.length;
    if (this.dom.jmTotalMurid) this.dom.jmTotalMurid.textContent = totalMurid;

    // Hitung total kelas
    const kelasCounts = {};
    this.siswaRowsCache.forEach(({ d }) => {
      const kelas = (d.kelas || 'TIDAK ADA KELAS').trim().toUpperCase();
      kelasCounts[kelas] = (kelasCounts[kelas] || 0) + 1;
    });
    const totalKelas = Object.keys(kelasCounts).length;
    if (this.dom.jmTotalKelas) this.dom.jmTotalKelas.textContent = totalKelas;

    // Hitung total angkatan
    const angkatanCounts = {};
    this.siswaRowsCache.forEach(({ d }) => {
      const angkatan = d.angkatan || 'Lainnya';
      angkatanCounts[angkatan] = (angkatanCounts[angkatan] || 0) + 1;
    });
    const totalAngkatan = Object.keys(angkatanCounts).length;
    if (this.dom.jmTotalAngkatan) this.dom.jmTotalAngkatan.textContent = totalAngkatan;

    // Hitung total jurusan
    const jurusanCounts = {};
    this.siswaRowsCache.forEach(({ d }) => {
      const jur = (d.jurusan || 'Lainnya').trim().toUpperCase();
      jurusanCounts[jur] = (jurusanCounts[jur] || 0) + 1;
    });
    const totalJurusan = Object.keys(jurusanCounts).length;
    if (this.dom.jmTotalJurusan) this.dom.jmTotalJurusan.textContent = totalJurusan;

    if (!this.dom.jumlahMuridContent) return;

    if (this.currentGroupMode === 'semua') {
      // Tampilkan semua murid dalam tabel
      if (totalMurid === 0) {
        this.dom.jumlahMuridContent.innerHTML = `<div class="text-center py-8 text-xs text-[#64748b]">Belum ada data siswa terdaftar.</div>`;
        return;
      }
      this.dom.jumlahMuridContent.innerHTML = `
        <div class="overflow-x-auto border border-[#e2e8f0] rounded-lg p-2 bg-[#ffffff]">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="border-b border-[#e2e8f0]">
                <th class="py-2 px-2 text-[10px] text-[#64748b] uppercase">No</th>
                <th class="py-2 px-2 text-[10px] text-[#64748b] uppercase">Nama</th>
                <th class="py-2 px-2 text-[10px] text-[#64748b] uppercase">NISN</th>
                <th class="py-2 px-2 text-[10px] text-[#64748b] uppercase">Kelas</th>
                <th class="py-2 px-2 text-[10px] text-[#64748b] uppercase font-mono">UID</th>
              </tr>
            </thead>
            <tbody>
              ${this.siswaRowsCache.map(({ uid, d }, i) => `
                <tr class="hover:bg-[#f1f5f9] transition-colors border-b border-[#e2e8f0] last:border-none">
                  <td class="py-3 px-2 text-xs font-semibold text-[#1e293b]">${i + 1}</td>
                  <td class="py-3 px-2 text-xs text-[#1e293b]">${(d.nama || '-').replace(/_/g, ' ')}</td>
                  <td class="py-3 px-2 text-xs text-[#1e293b]">${d.nisn || '-'}</td>
                  <td class="py-3 px-2 text-xs text-[#1e293b]">${d.kelas || '-'}</td>
                  <td class="py-3 px-2 text-xs font-mono text-[#64748b]">${uid}</td>
                </tr>
              `).join('')}
            </tbody>
          </table>
        </div>
      `;
    } else if (this.currentGroupMode === 'kelas' || this.currentGroupMode === 'angkatan' || this.currentGroupMode === 'jurusan') {
      let groupingKeys = [];
      let getDataFn = null;
      let icon = '';
      let colorClass = '';

      if (this.currentGroupMode === 'kelas') {
        groupingKeys = Object.keys(kelasCounts).sort();
        getDataFn = (d) => (d.kelas || '').trim().toUpperCase();
        icon = 'meeting_room'; colorClass = 'text-[#2563eb]';
      } else if (this.currentGroupMode === 'angkatan') {
        groupingKeys = Object.keys(angkatanCounts).sort();
        getDataFn = (d) => d.angkatan || 'Lainnya';
        icon = 'calendar_today'; colorClass = 'text-orange-400';
      } else if (this.currentGroupMode === 'jurusan') {
        groupingKeys = Object.keys(jurusanCounts).sort();
        getDataFn = (d) => (d.jurusan || 'Lainnya').trim().toUpperCase();
        icon = 'category'; colorClass = 'text-purple-500';
      }

      if (groupingKeys.length === 0) {
        this.dom.jumlahMuridContent.innerHTML = `<div class="text-center py-8 text-xs text-[#64748b]">Belum ada data siswa terdaftar.</div>`;
        return;
      }

      this.dom.jumlahMuridContent.innerHTML = groupingKeys.map((groupName, index) => {
        const studentsInGroup = this.siswaRowsCache.filter(({ d }) => getDataFn(d) === groupName);
        return `
          <div class="border border-[#e2e8f0] rounded-lg mb-3 overflow-hidden bg-[#ffffff]">
            <div class="flex items-center justify-between p-3.5 hover:bg-[#f8fafc] cursor-pointer transition-colors accordion-header" data-target="group-${index}">
              <div class="flex items-center gap-2">
                <span class="material-symbols-outlined text-[20px] ${colorClass}">${icon}</span>
                <span class="text-xs font-bold text-[#1e293b] uppercase">${groupName}</span>
              </div>
              <div class="flex items-center gap-2">
                <span class="text-[10px] font-semibold text-[#64748b] bg-[#f8fafc] border border-[#e2e8f0] px-2.5 py-0.5 rounded-full">${studentsInGroup.length} Siswa</span>
                <span class="material-symbols-outlined text-[18px] text-[#64748b] transition-transform duration-300 transform" id="icon-group-${index}">expand_more</span>
              </div>
            </div>
            <div class="max-h-0 overflow-hidden transition-all duration-300 ease-in-out bg-[#ffffff]" id="content-group-${index}">
              <div class="p-3 border-t border-[#e2e8f0]">
                <table class="w-full text-left border-collapse">
                  <thead>
                    <tr class="border-b border-[#e2e8f0]">
                      <th class="py-1.5 px-2 text-[10px] text-[#64748b] uppercase">No</th>
                      <th class="py-1.5 px-2 text-[10px] text-[#64748b] uppercase">Nama</th>
                      <th class="py-1.5 px-2 text-[10px] text-[#64748b] uppercase">Kelas</th>
                      <th class="py-1.5 px-2 text-[10px] text-[#64748b] uppercase font-mono">UID</th>
                    </tr>
                  </thead>
                  <tbody>
                    ${studentsInGroup.map(({ uid, d }, i) => `
                      <tr class="border-b border-[#e2e8f0] last:border-none hover:bg-[#f1f5f9] transition-colors">
                        <td class="py-2 px-2 text-xs text-[#1e293b]">${i + 1}</td>
                        <td class="py-2 px-2 text-xs text-[#1e293b]">${(d.nama || '-').replace(/_/g, ' ')}</td>
                        <td class="py-2 px-2 text-xs text-[#1e293b]">${d.kelas || '-'}</td>
                        <td class="py-2 px-2 text-xs font-mono text-[#64748b]">${uid}</td>
                      </tr>
                    `).join('')}
                  </tbody>
                </table>
              </div>
            </div>
          </div>
        `;
      }).join('');

      this.bindAccordionEvents();
    }
  }


  // ====== PAGE 4: REGISTRASI ======
  showAlert(type, msg) {
    const el = type === 'success' ? this.dom.alertSuccess : this.dom.alertError;
    const other = type === 'success' ? this.dom.alertError : this.dom.alertSuccess;
    other.style.display = 'none';
    el.textContent = msg;
    el.style.display = 'block';
    setTimeout(() => { el.style.display = 'none'; }, 4000);
  }

  renderTabelSiswa(filterText = '') {
    const filtered = this.siswaRowsCache.filter(({ uid, d }) => {
      const text = `${d.nama || ''} ${d.nisn || ''} ${d.kelas || ''} ${d.jurusan || ''} ${d.angkatan || ''} ${uid}`.toLowerCase();
      return text.includes(filterText.toLowerCase());
    });

    if (filtered.length === 0) {
      this.dom.tabelSiswa.innerHTML = `<tr><td colspan="7" class="empty">${this.siswaRowsCache.length === 0 ? 'Belum ada siswa terdaftar' : 'Tidak ada siswa yang cocok dengan pencarian'}</td></tr>`;
      return;
    }

    this.dom.tabelSiswa.innerHTML = filtered.map(({ uid, d }, i) => `
      <tr>
        <td>${i + 1}</td>
        <td>${(d.nama || '-').replace(/_/g, ' ')}</td>
        <td>${d.nisn || '-'}</td>
        <td>${d.kelas || '-'}</td>
        <td style="font-family:monospace">${uid}</td>
        <td>
          <button class="bg-[#2563eb] hover:bg-[#1d4ed8] text-white text-[11px] px-2.5 py-1 rounded transition-colors mr-2 cursor-pointer font-medium" data-uid="${uid}" data-action="edit">Edit</button>
          <button class="bg-red-600/10 hover:bg-red-600/20 border border-red-500/20 hover:border-red-500/40 text-red-400 text-[11px] px-2.5 py-1 rounded transition-colors cursor-pointer font-medium" data-uid="${uid}" data-action="hapus">Hapus</button>
        </td>
      </tr>
    `).join('');

    // Bind Event Hapus & Edit
    this.dom.tabelSiswa.querySelectorAll('[data-action="hapus"]').forEach(el => {
      el.addEventListener('click', async () => {
        if (confirm(`Hapus siswa dengan UID ${el.dataset.uid}?`)) {
          await this.dbService.deleteSiswa(el.dataset.uid);
          this.showAlert('success', 'Data siswa dihapus.');
        }
      });
    });

    this.dom.tabelSiswa.querySelectorAll('[data-action="edit"]').forEach(el => {
      el.addEventListener('click', () => {
        this.openEditModal(el.dataset.uid);
      });
    });
  }

  async handleRegistrasiSubmit(e) {
    e.preventDefault();
    const nama = this.dom.regNama.value.trim().toUpperCase().replace(/\s+/g, '_');
    const nisn = this.dom.regNISN ? this.dom.regNISN.value.trim() : '';
    const kelas = this.dom.regKelas.value.trim();
    const jurusan = this.dom.regJurusan.value;
    const angkatan = this.dom.regAngkatan.value;
    const uid = this.dom.regUID.value.trim().toUpperCase();

    if (!nama || !nisn || !kelas || !uid || !jurusan || !angkatan) {
      this.showAlert('error', 'Semua field harus diisi.');
      return;
    }

    try {
      const existing = await this.dbService.getSiswa(uid);
      if (existing.exists()) {
        this.showAlert('error', `UID ${uid} sudah terdaftar atas nama ${existing.val().nama}.`);
        return;
      }

      await this.dbService.saveSiswa(uid, { nama, nisn, kelas, jurusan, angkatan, uid });

      // Cek dan hapus dari kartu tidak terdaftar jika ada
      this.dbService.subscribeTidakDikenal((snapshot) => {
        if (snapshot.exists()) {
          snapshot.forEach((child) => {
            if (child.val().uid === uid) {
              this.dbService.deleteTidakDikenal(child.key);
            }
          });
        }
      });

      this.showAlert('success', `Siswa ${nama.replace(/_/g, ' ')} berhasil didaftarkan dengan NISN ${nisn} & UID ${uid}.`);
      this.dom.formRegistrasi.reset();
    } catch (err) {
      this.showAlert('error', 'Gagal menyimpan: ' + err.message);
    }
  }

  // ====== EDIT MODAL ======
  openEditModal(uid) {
    const data = this.daftarSiswaCache[uid] || {};
    this.dom.editUID.value = uid;
    this.dom.editNama.value = data.nama || '';
    if (this.dom.editNISN) this.dom.editNISN.value = data.nisn || '';
    this.dom.editKelas.value = data.kelas || '';
    this.dom.editJurusan.value = data.jurusan || '';
    this.dom.editAngkatan.value = data.angkatan || '';
    this.dom.editError.style.display = 'none';
    this.dom.modalEditSiswa.classList.remove('hidden');
  }

  closeEditModal() {
    this.dom.modalEditSiswa.classList.add('hidden');
  }

  async handleEditSiswaSubmit() {
    const uid = this.dom.editUID.value;
    const nama = this.dom.editNama.value.trim().toUpperCase().replace(/\s+/g, '_');
    const nisn = this.dom.editNISN ? this.dom.editNISN.value.trim() : '';
    const kelas = this.dom.editKelas.value.trim();
    const jurusan = this.dom.editJurusan.value;
    const angkatan = this.dom.editAngkatan.value;

    if (!nama || !kelas || !jurusan || !angkatan) {
      this.showAlert('error', 'Lengkapi semua field.');
      return;
    }

    try {
      await this.dbService.updateSiswa(uid, {
        nama,
        nisn,
        kelas,
        jurusan,
        angkatan,
        terakhir_diperbarui: new Date().toISOString()
      });
      this.closeEditModal();
      this.showAlert('success', 'Data siswa berhasil diperbarui!');
    } catch (err) {
      this.showAlert('error', 'Gagal update: ' + err.message);
    }
  }

  // ====== PAGE 5: PENGATURAN JAM ======
  renderCurrentDayForm() {
    if (!this.currentDayTab || !this.dom.hariAktifToggle) return;
    
    const data = this.cacheJadwalHarian[this.currentDayTab] || {};
    
    // Set status hari
    const isAktif = data.aktif !== false;
    this.dom.hariAktifToggle.checked = isAktif;
    this.dom.panelWaktuHari.style.opacity = isAktif ? '1' : '0.4';
    this.dom.labelHariAktif.textContent = isAktif ? 'Hari Sekolah (Absensi Aktif)' : 'Hari Libur (Absensi Tutup)';
    
    // Set nilai input jam
    if (this.dom.inputJamMasukBuka) this.dom.inputJamMasukBuka.value = data.masuk_buka || '06:00';
    if (this.dom.inputJamMasukTerlambat) this.dom.inputJamMasukTerlambat.value = data.terlambat || '07:00';
    if (this.dom.inputJamMasukTutup) this.dom.inputJamMasukTutup.value = data.masuk_tutup || '08:00';
    if (this.dom.inputJamPulangBuka) this.dom.inputJamPulangBuka.value = data.pulang_buka || '15:00';
    if (this.dom.inputJamPulangTutup) this.dom.inputJamPulangTutup.value = data.pulang_tutup || '17:00';
  }

  renderDayBadges() {
    const listHari = ['senin', 'selasa', 'rabu', 'kamis', 'jumat', 'sabtu', 'minggu'];
    listHari.forEach(hari => {
      const badge = document.getElementById(`badge-${hari}`);
      if (badge) {
        const item = this.cacheJadwalHarian[hari];
        const isAktif = item && item.aktif !== false;
        badge.className = `w-2 h-2 rounded-full ${isAktif ? 'bg-emerald-400' : 'bg-zinc-600'}`;
      }
    });
  }

  renderRingkasanJadwal() {
    if (!this.dom.tabelRingkasanJadwal) return;

    const listHari = ['senin', 'selasa', 'rabu', 'kamis', 'jumat', 'sabtu', 'minggu'];
    const rows = listHari.map(hari => {
      const d = this.cacheJadwalHarian[hari] || {};
      const isAktif = d.aktif !== false;
      const statusBadge = isAktif
        ? `<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">SEKOLAH</span>`
        : `<span class="px-2 py-0.5 rounded-full text-[10px] font-bold bg-zinc-800 text-zinc-400 border border-zinc-700">LIBUR</span>`;

      return `
        <tr class="border-b border-[#e2e8f0] last:border-none hover:bg-[#ffffff] transition-colors">
          <td class="py-2.5 font-bold uppercase text-black">${hari}</td>
          <td class="py-2.5">${statusBadge}</td>
          <td class="py-2.5 text-[#64748b]">${isAktif ? (d.masuk_buka || '-') : '-'}</td>
          <td class="py-2.5 text-orange-400 font-semibold">${isAktif ? (d.terlambat || '-') : '-'}</td>
          <td class="py-2.5 text-[#64748b]">${isAktif ? (d.masuk_tutup || '-') : '-'}</td>
                            </tr>
      `;
    });

    this.dom.tabelRingkasanJadwal.innerHTML = rows.join('');
  }

  timeToMinutes(timeStr) {
    if (!timeStr) return 0;
    const [h, m] = timeStr.split(':').map(Number);
    return h * 60 + m;
  }

  parseTime(timeStr) {
    if (!timeStr) return { jam: 0, menit: 0 };
    const [h, m] = timeStr.split(':').map(Number);
    return { jam: h, menit: m };
  }

  async handlePengaturanJamSubmit(e) {
    e.preventDefault();

    if (!this.auth.isAdmin()) {
      this.showPengaturanAlert('error', 'Hanya Admin yang diizinkan untuk mengedit dan menyimpan pengaturan jam.');
      this.openLoginModal();
      return;
    }
    
    // 1. Simpan input saat ini ke cache
    this.saveCurrentInputsToCache();

    // 2. Validasi urutan jam pada hari-hari yang aktif
    const listHari = ['senin', 'selasa', 'rabu', 'kamis', 'jumat', 'sabtu', 'minggu'];
    for (const hari of listHari) {
      const d = this.cacheJadwalHarian[hari];
      if (d && d.aktif) {
        const t1 = this.timeToMinutes(d.masuk_buka);
        const t2 = this.timeToMinutes(d.terlambat);
        const t3 = this.timeToMinutes(d.masuk_tutup);
        const t4 = this.timeToMinutes(d.pulang_buka);
        const t5 = this.timeToMinutes(d.pulang_tutup);

        if (!(t1 < t2 && t2 < t3 && t3 < t4 && t4 < t5)) {
          this.showPengaturanAlert('error', `Urutan jam absensi untuk hari ${hari.toUpperCase()} tidak valid.`);
          this.switchJadwalHariTab(hari);
          return;
        }
      }
    }

    // 3. Dialog konfirmasi sebelum menyimpan
    if (!confirm("Apakah Anda yakin ingin menyimpan seluruh konfigurasi jadwal harian?")) {
      return;
    }

    const btnSimpan = this.dom.btnSimpanPengaturan;
    const btnReset = this.dom.btnResetPengaturan;

    if (btnSimpan) {
      btnSimpan.disabled = true;
      btnSimpan.innerHTML = `<span class="material-symbols-outlined text-[18px] animate-spin mr-2">sync</span> Menyimpan...`;
    }
    if (btnReset) btnReset.disabled = true;

    try {
      const timestamp = new Date().toISOString();

      // Update /pengaturan/jadwal_harian
      await this.dbService.updateJadwalHarian(this.cacheJadwalHarian, timestamp);
      this.renderDayBadges();
      this.renderRingkasanJadwal();
      this.showPengaturanAlert('success', 'Jadwal absensi harian berhasil disimpan ke database!');
    } catch (err) {
      this.showPengaturanAlert('error', 'Gagal menyimpan pengaturan: ' + err.message);
    } finally {
      if (btnSimpan) {
        btnSimpan.disabled = false;
        btnSimpan.innerHTML = `<span class="material-symbols-outlined text-[18px]">save</span> Simpan Semua Jadwal`;
      }
      if (btnReset) btnReset.disabled = false;
    }
  }

  showPengaturanAlert(type, msg) {
    const el = type === 'success' ? this.dom.alertPengaturanSuccess : this.dom.alertPengaturanError;
    const other = type === 'success' ? this.dom.alertPengaturanError : this.dom.alertPengaturanSuccess;
    other.style.display = 'none';
    el.textContent = msg;
    el.style.display = 'block';
    setTimeout(() => { el.style.display = 'none'; }, 4000);
  }

  // ====== RECONSTRUCTED MISSING METHODS ======

  formatTanggalInput(date) {
    const y = date.getFullYear();
    const m = String(date.getMonth() + 1).padStart(2, '0');
    const d = String(date.getDate()).padStart(2, '0');
    return `${y}-${m}-${d}`;
  }

  formatTanggalFirebase(date) {
    const y = date.getFullYear();
    const m = date.getMonth() + 1;
    const d = date.getDate();
    return `${d}-${m}-${y}`;
  }

  getDateRange(startStr, endStr) {
    const start = new Date(startStr);
    const end = new Date(endStr);
    const dateArray = [];
    let currentDate = new Date(start);
    while (currentDate <= end) {
      dateArray.push(this.formatTanggalFirebase(currentDate));
      currentDate.setDate(currentDate.getDate() + 1);
    }
    return dateArray;
  }

  bindAccordionEvents() {
    const headers = document.querySelectorAll('.accordion-header');
    headers.forEach(header => {
      // Hapus listener lama dengan cara clone node agar tidak terjadi double-trigger saat render ulang
      const newHeader = header.cloneNode(true);
      if (header.parentNode) {
        header.parentNode.replaceChild(newHeader, header);
      }
      
      newHeader.addEventListener('click', () => {
        const content = newHeader.nextElementSibling;
        const targetId = newHeader.getAttribute('data-target');
        const icon = document.getElementById('icon-' + targetId);
        
        // Cek apakah konten sedang terbuka atau tertutup
        if (content.style.maxHeight && content.style.maxHeight !== '0px') {
          // Sedang terbuka, maka kita tutup
          content.style.maxHeight = '0px';
          if(icon) icon.style.transform = 'rotate(0deg)';
          
          // Setelah transisi selesai, kembalikan class max-h-0 agar konsisten
          setTimeout(() => {
            if (content.style.maxHeight === '0px') {
               content.classList.add('max-h-0');
            }
          }, 300);
        } else {
          // Sedang tertutup, maka kita buka
          content.classList.remove('max-h-0');
          content.style.maxHeight = content.scrollHeight + 'px';
          if(icon) icon.style.transform = 'rotate(180deg)';
        }
      });
    });
  }

  async handleTambahAdminSubmit(e) {
    e.preventDefault();
    if (!this.auth.isAdmin()) return;
    
    const email = this.dom.adminEmail.value.trim().toLowerCase();
    if (!email) return;

    const btn = this.dom.formTambahAdmin.querySelector('button[type="submit"]');
    if (btn) btn.disabled = true;

    try {
      const currentUser = this.auth.getCurrentUser();
      await this.dbService.addAdmin(email, currentUser.email);
      if(this.dom.alertAdminSuccess) {
        this.dom.alertAdminSuccess.textContent = `Admin ${email} berhasil ditambahkan!`;
        this.dom.alertAdminSuccess.style.display = 'block';
        setTimeout(() => { this.dom.alertAdminSuccess.style.display = 'none'; }, 3000);
      }
      this.dom.formTambahAdmin.reset();
    } catch (err) {
      if(this.dom.alertAdminError) {
        this.dom.alertAdminError.textContent = err.message;
        this.dom.alertAdminError.style.display = 'block';
        setTimeout(() => { this.dom.alertAdminError.style.display = 'none'; }, 3000);
      }
    } finally {
      if (btn) btn.disabled = false;
    }
  }

  renderTabelAdmin(snapshot) {
    if (!this.dom.tabelAdmin) return;
    let html = '';
    let no = 1;
    if (snapshot.exists()) {
      snapshot.forEach(child => {
        const data = child.val();
        html += `
          <tr class="border-b border-[#e2e8f0] hover:bg-gray-50">
            <td class="py-3 px-4 text-center">${no++}</td>
            <td class="py-3 px-4 font-semibold">${data.email}</td>
            <td class="py-3 px-4">${data.addedBy || '-'}</td>
            <td class="py-3 px-4">${new Date(data.addedAt).toLocaleString('id-ID')}</td>
            <td class="py-3 px-4 text-center">
              <button class="text-red-500 hover:text-red-700 font-bold" onclick="window.hapusAdmin('${child.key}')">Hapus</button>
            </td>
          </tr>
        `;
      });
    }
    this.dom.tabelAdmin.innerHTML = html || `<tr><td colspan="5" class="text-center py-4">Belum ada admin</td></tr>`;
  }

  renderLastScannedUID(snapshot) {
    // We just ignore this or implement a minimal version if missing from UI.
  }

  renderTabelTidakDikenal(snapshot) {
    if (!this.dom.tabelTidakDikenal) return;
    let html = '';
    let no = 1;
    if (snapshot.exists()) {
      snapshot.forEach(child => {
        const data = child.val();
        html += `
          <tr class="border-b border-[#e2e8f0] hover:bg-gray-50">
            <td class="py-3 px-4 text-center">${no++}</td>
            <td class="py-3 px-4 font-bold text-red-500">${data.uid}</td>
            <td class="py-3 px-4">${data.waktu}</td>
            <td class="py-3 px-4 text-center">
              <button class="bg-blue-500 text-white px-3 py-1 rounded text-xs" onclick="window.daftarkanUID('${data.uid}')">Daftarkan</button>
            </td>
          </tr>
        `;
      });
    }
    this.dom.tabelTidakDikenal.innerHTML = html || `<tr><td colspan="4" class="text-center py-4">Tidak ada kartu tak dikenal</td></tr>`;
  }

  switchJadwalHariTab(hari) {
    if (!this.dom.jadwalHariTabs) return;
    
    // Save current before switching
    if (this.currentDayTab) this.saveCurrentInputsToCache();
    
    this.currentDayTab = hari;
    
    this.dom.jadwalHariTabs.forEach(tab => {
      if (tab.dataset.hari === hari) {
        tab.classList.add('active');
        tab.classList.remove('bg-[#f8fafc]', 'text-[#64748b]');
        tab.classList.add('bg-[#2563eb]', 'text-white');
      } else {
        tab.classList.remove('active', 'bg-[#2563eb]', 'text-white');
        tab.classList.add('bg-[#f8fafc]', 'text-[#64748b]');
      }
    });

    const namaHari = hari.charAt(0).toUpperCase() + hari.slice(1);
    if (this.dom.labelHariTerpilih) this.dom.labelHariTerpilih.textContent = `Pengaturan Hari ${namaHari}`;
    if (this.dom.descHariTerpilih) this.dom.descHariTerpilih.textContent = `Tentukan jam buka dan tutup absensi untuk hari ${namaHari}.`;
    
    this.renderCurrentDayForm();
  }

  saveCurrentInputsToCache() {
    if (!this.currentDayTab) return;
    if (!this.cacheJadwalHarian[this.currentDayTab]) {
      this.cacheJadwalHarian[this.currentDayTab] = { aktif: true };
    }
    const data = this.cacheJadwalHarian[this.currentDayTab];
    if (this.dom.inputJamMasukBuka) data.masuk_buka = this.dom.inputJamMasukBuka.value;
    if (this.dom.inputJamMasukTerlambat) data.terlambat = this.dom.inputJamMasukTerlambat.value;
    if (this.dom.inputJamMasukTutup) data.masuk_tutup = this.dom.inputJamMasukTutup.value;
    if (this.dom.inputJamPulangBuka) data.pulang_buka = this.dom.inputJamPulangBuka.value;
    if (this.dom.inputJamPulangTutup) data.pulang_tutup = this.dom.inputJamPulangTutup.value;
  }

}
