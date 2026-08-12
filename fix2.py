import codecs

with codecs.open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

start = html.find('loadSiswaRiwayat(dbService);')
end = html.find('function countWeekdaysUntilToday')

if start != -1 and end != -1:
    corrupted_block = html[start:end]
    replacement_block = """loadSiswaRiwayat(dbService);
        } catch (err) {
          const errText = document.getElementById('siswaLoginErrorText');
          if (errText) errText.textContent = 'Terjadi kesalahan jaringan. Coba lagi.';
          siswaLoginError.style.display = 'flex';
          document.getElementById('inputNISN').classList.add('border-red-500', 'ring-4', 'ring-red-500/20');
        }

        const btn = formSiswaLogin.querySelector('.btn-login');
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

      // """
    
    html = html.replace(corrupted_block, replacement_block)
    with codecs.open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Fully fixed index.html script block!')
else:
    print('Could not find start or end block!')
