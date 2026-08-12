
    document.addEventListener('DOMContentLoaded', () => {
      // ===== STUDENT PORTAL LOGIC =====
      const siswaLoginPage = document.getElementById('siswaLoginPage');
      const siswaRiwayatPage = document.getElementById('siswaRiwayatPage');
      const formSiswaLogin = document.getElementById('formSiswaLogin');
      const btnSiswaLogout = document.getElementById('btnSiswaLogout');
      const btnSiswaFilter = document.getElementById('btnSiswaFilter');
      const siswaLoginError = document.getElementById('siswaLoginError');

      let currentSiswaData = null;

      // Set default month filter
      const today = new Date();
      const monthStr = today.toISOString().slice(0, 7);
      document.getElementById('siswaFilterBulan').value = monthStr;

      btnSiswaLogout.addEventListener('click', () => {
        currentSiswaData = null;
        siswaRiwayatPage.style.display = 'none';
        siswaLoginPage.style.display = 'block';
      });

      // Direct Admin Login dari Halaman Siswa
      const btnAdminDirectLogin = document.getElementById('btnAdminDirectLogin');
      if (btnAdminDirectLogin) {
        btnAdminDirectLogin.addEventListener('click', async () => {
          btnAdminDirectLogin.innerHTML = '<span class="material-symbols-outlined" style="font-size:20px;animation:spin 1s linear infinite">progress_activity</span> Membuka Google...';
          btnAdminDirectLogin.disabled = true;
          
          try {
            // Import Firebase dan AuthManager secara dinamis
            const { FirebaseService } = await import('./js/FirebaseService.js?v=7');
            const { AuthManager } = await import('./js/AuthManager.js?v=7');
            
            const dbService = new FirebaseService();
            const authManager = new AuthManager(dbService);
            
            // Panggil popup login google
            const user = await authManager.loginWithGoogle();
            
            // Cek apakah sukses dan terdaftar
            const isUserAdmin = await dbService.checkAdminEmail(user.email);
            if (isUserAdmin) {
              btnAdminDirectLogin.innerHTML = '<span class="material-symbols-outlined" style="font-size:20px;color:#16a34a">check_circle</span> Sukses. Mengalihkan...';
              window.location.href = 'admin.html';
            } else {
              await authManager.logout();
              alert("Akses ditolak: Email Anda tidak terdaftar sebagai admin.");
              btnAdminDirectLogin.innerHTML = '<span class="material-symbols-outlined" style="font-size:20px;color:#64748b">admin_panel_settings</span> Masuk sebagai Admin (Google)';
              btnAdminDirectLogin.disabled = false;
            }
          } catch (error) {
            console.error(error);
            if (error.code !== 'auth/popup-closed-by-user') {
               alert("Terjadi kesalahan saat login Google.");
            }
            btnAdminDirectLogin.innerHTML = '<span class="material-symbols-outlined" style="font-size:20px;color:#64748b">admin_panel_settings</span> Masuk sebagai Admin (Google)';
            btnAdminDirectLogin.disabled = false;
          }
        });
      }

      formSiswaLogin.addEventListener('submit', async (e) => {
        e.preventDefault();
        const nisn = document.getElementById('inputNISN').value.trim();
        if (!nisn) return;

        siswaLoginError.style.display = 'none';
        document.getElementById('inputNISN').classList.remove('border-red-500', 'ring-4', 'ring-red-500/20');
        document.getElementById('inputNISN').classList.remove('border-red-500', 'ring-4', 'ring-red-500/20');
        const btn = formSiswaLogin.querySelector('.btn-login');
        btn.innerHTML = '<span class="material-symbols-outlined" style="font-size:20px;animation:spin 1s linear infinite">progress_activity</span> Memverifikasi...';
        btn.disabled = true;

        try {
          // Import FirebaseService dynamically
          const { FirebaseService } = await import('./js/FirebaseService.js?v=7');
          const dbService = new FirebaseService();
          const result = await dbService.getSiswaByNIS(nisn);

          if (!result) {
            const errText = document.getElementById('siswaLoginErrorText');
            if (errText) errText.textContent = 'NISN tidak ditemukan. Pastikan NISN Anda benar.';
            siswaLoginError.style.display = 'flex';
            document.getElementById('inputNISN').classList.add('border-red-500', 'ring-4', 'ring-red-500/20');
            btn.innerHTML = '<span class="material-symbols-outlined" style="font-size:20px">login</span> Masuk';
            btn.disabled = false;
            return;
          }

          currentSiswaData = result;
          const d = result.data;
          document.getElementById('siswaRiwayatNama').textContent = d.nama || result.uid;
          document.getElementById('siswaRiwayatKelas').textContent = d.kelas || '-';
          document.getElementById('siswaRiwayatJurusan').textContent = d.jurusan || '-';
          document.getElementById('siswaRiwayatAngkatan').textContent = d.angkatan || '-';
          document.getElementById('siswaRiwayatNISN').textContent = d.nisn || d.NISN || nisn;

          siswaLoginPage.style.display = 'none';
          siswaRiwayatPage.style.display = 'block';
          

          // Load initial data
          loadSiswaRiwayat(dbService);
        } catch (err) {
          const errText = document.getElementById('siswaLoginErrorText');
          if (errText) errText.textContent = 'Terjadi kesalahan jaringan. Coba lagi.';
          siswaLoginError.style.display = 'flex';
          document.getElementById('inputNISN').classList.add('border-red-500', 'ring-4', 'ring-red-500/20');
        }

        if(btn) {
            btn.innerHTML = '<span class="material-symbols-outlined" style="font-size:20px">login</span> Masuk';
            btn.disabled = false;
        }
      });

      btnSiswaFilter.addEventListener('click', async () => {
        if (!currentSiswaData) return;
        const { FirebaseService } = await import('./js/FirebaseService.js?v=7');
        const dbService = new FirebaseService();
        loadSiswaRiwayat(dbService);
      });

      async function loadSiswaRiwayat(dbService) {
        const monthInput = document.getElementById('siswaFilterBulan').value;
        if (!monthInput || !currentSiswaData) return;

        const [tahun, bulan] = monthInput.split('-').map(Number);
        const tbody = document.getElementById('tabelSiswaRiwayat');
        tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:2rem;color:var(--text-muted);">Memuat data...</td></tr>';

        try {
          const records = await dbService.getAbsensiSiswa(
            currentSiswaData.uid,
            currentSiswaData.data.nama || currentSiswaData.uid,
            bulan,
            tahun
          );

          let hadir = 0, terlambat = 0;

          const byDate = {};
          records.forEach(r => {
            const tgl = r.tanggalKey;
            if (!byDate[tgl]) byDate[tgl] = r.val;
            else byDate[tgl] = { ...byDate[tgl], ...r.val };
          });

          Object.values(byDate).forEach(val => {
            const status = (val.status || '').toUpperCase();
            if (status.includes('TERLAMBAT')) {
              terlambat++;
            } else if (status === 'HADIR' || val.jam_masuk || val.jam) {
              hadir++;
            }
          });

          const totalHadir = hadir + terlambat;
          const weekdaysElapsed = countWeekdaysUntilToday(tahun, bulan);
          const tidakHadir = Math.max(0, weekdaysElapsed - totalHadir);
          const persen = weekdaysElapsed > 0 ? Math.round((totalHadir / weekdaysElapsed) * 100) : 0;

          document.getElementById('siswaStHadir').textContent = hadir;
          document.getElementById('siswaStTerlambat').textContent = terlambat;
          document.getElementById('siswaStTidakHadir').textContent = tidakHadir;
          document.getElementById('siswaStPersen').textContent = persen + '%';

          if (records.length === 0) {
            tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:2rem;color:var(--text-muted);">Tidak ada data absensi untuk bulan ini.</td></tr>';
            return;
          }

          let htmlOutput = '';
          let no = 1;
          const sortedDates = Object.keys(byDate).sort((a, b) => {
            const [da, ma, ya] = a.split('-').map(Number);
            const [db, mb, yb] = b.split('-').map(Number);
            return new Date(ya, ma - 1, da) - new Date(yb, mb - 1, db);
          });

          sortedDates.forEach(tgl => {
            const val = byDate[tgl];
            const status = val.status || '-';
            const jamMasuk = val.jam_masuk || val.jam || '-';
            const jamPulang = val.jam_pulang || val.waktu_pulang || '-';

            let statusColor = '#2563eb';
            let statusBg = '#dbeafe';
            if (status.toUpperCase().includes('TERLAMBAT')) {
              statusColor = '#ea580c';
              statusBg = '#fff7ed';
            }

            htmlOutput += '<tr>' +
              '<td>' + (no++) + '</td>' +
              '<td>' + tgl + '</td>' +
              '<td>' + jamMasuk + '</td>' +
              '<td>' + jamPulang + '</td>' +
              '<td><span style="background:' + statusBg + ';color:' + statusColor + ';padding:0.25rem 0.75rem;border-radius:9999px;font-size:0.75rem;font-weight:600;">' + status + '</span></td>' +
            '</tr>';
          });

          tbody.innerHTML = htmlOutput;
        } catch (err) {
          console.error(err);
          tbody.innerHTML = '<tr><td colspan="5" style="text-align:center;padding:2rem;color:#dc2626;">Gagal memuat data.</td></tr>';
        }
      }

      function countWeekdaysUntilToday(year, month) {
        const today = new Date();
        const daysInMonth = new Date(year, month, 0).getDate();
        // Determine the last day to count
        let lastDay = daysInMonth;
        if (year === today.getFullYear() && month === (today.getMonth() + 1)) {
          // Current month: only count up to today
          lastDay = Math.min(today.getDate(), daysInMonth);
        } else if (new Date(year, month - 1, 1) > today) {
          // Future month: no weekdays elapsed
          return 0;
        }
        let count = 0;
        for (let d = 1; d <= lastDay; d++) {
          const day = new Date(year, month - 1, d).getDay();
          if (day !== 0 && day !== 6) count++;
        }
        return count;
      }

      function countWeekdays(year, month) {
        const daysInMonth = new Date(year, month, 0).getDate();
        let count = 0;
        for (let d = 1; d <= daysInMonth; d++) {
          const day = new Date(year, month - 1, d).getDay();
          if (day !== 0 && day !== 6) count++;
        }
        return count;
      }
    });
  