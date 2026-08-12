import codecs
import re

with codecs.open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Replace Login Page
old_login = '''  <div id="siswaLoginPage" class="siswa-login-container" style="display:flex;">
    <div class="siswa-login-card">
      <div class="logo-wrapper">
        <img alt="SMK PGRI 2" src="assets/logo.png">
      </div>
      <h2>Portal Siswa</h2>
      <p>Masukkan NISN Anda untuk melihat riwayat absensi</p>
      <div class="siswa-login-error" id="siswaLoginError"></div>
      <form id="formSiswaLogin">
        <div class="input-group">
          <span class="material-symbols-outlined input-icon">badge</span>
          <input id="inputNISN" type="text" placeholder="Masukkan NISN (10 digit)" maxlength="10" pattern="[0-9]{10}" required>
        </div>
        <button type="submit" class="btn-login">
          <span class="material-symbols-outlined" style="font-size:20px">login</span>
          Masuk
        </button>
      </form>
            <div style="margin-top:1.5rem; padding-top:1.25rem; border-top:1px solid #e2e8f0; text-align:center;">
        <a href="admin.html" style="background:none;border:none;color:#64748b;font-size:0.8125rem;font-weight:600;text-decoration:none;display:inline-flex;align-items:center;gap:0.375rem;">
          <span class="material-symbols-outlined" style="font-size:16px">admin_panel_settings</span>
          Masuk sebagai Admin
        </a>
      </div>
    </div>
  </div>'''

new_login = '''  <div id="siswaLoginPage" class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4 relative overflow-hidden" style="display:flex;">
    <!-- Abstract background shapes -->
    <div class="absolute top-0 left-0 w-full h-full overflow-hidden z-0 pointer-events-none">
      <div class="absolute -top-[10%] -left-[10%] w-[40%] h-[40%] rounded-full bg-blue-200/50 blur-3xl"></div>
      <div class="absolute top-[60%] -right-[10%] w-[30%] h-[30%] rounded-full bg-indigo-200/50 blur-3xl"></div>
    </div>
    
    <div class="bg-white/90 backdrop-blur-xl border border-white shadow-2xl rounded-3xl p-8 md:p-10 max-w-md w-full relative z-10 text-center">
      <div class="w-20 h-20 mx-auto mb-6 rounded-2xl overflow-hidden shadow-md border border-slate-100 bg-white">
        <img alt="SMK PGRI 2" src="assets/logo.png" class="w-full h-full object-cover">
      </div>
      <h2 class="text-2xl font-bold text-slate-800 tracking-tight mb-2">Portal Siswa</h2>
      <p class="text-sm text-slate-500 mb-8">Masukkan NISN Anda untuk melihat riwayat absensi</p>
      
      <div class="hidden bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-xl text-sm mb-6 font-medium" id="siswaLoginError"></div>
      
      <form id="formSiswaLogin" class="text-left">
        <div class="relative mb-6 group">
          <div class="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none text-slate-400 group-focus-within:text-blue-600 transition-colors">
            <span class="material-symbols-outlined text-xl">badge</span>
          </div>
          <input id="inputNISN" type="text" placeholder="Masukkan NISN (10 digit)" maxlength="10" pattern="[0-9]{10}" required class="w-full pl-11 pr-4 py-3.5 bg-white border border-slate-200 text-slate-800 rounded-xl focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all text-sm font-medium shadow-sm">
        </div>
        <button type="submit" class="w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold py-3.5 px-4 rounded-xl shadow-lg shadow-blue-500/30 flex items-center justify-center gap-2 transition-all active:scale-[0.98]">
          <span class="material-symbols-outlined text-[20px]">login</span>
          Masuk
        </button>
      </form>
      
      <div class="mt-8 pt-6 border-t border-slate-200/60">
        <a href="admin.html" class="inline-flex items-center gap-2 text-sm font-bold text-slate-500 hover:text-slate-800 transition-colors">
          <span class="material-symbols-outlined text-[18px]">admin_panel_settings</span>
          Masuk sebagai Admin
        </a>
      </div>
    </div>
  </div>'''

# Replace Riwayat Page
old_riwayat = '''  <div id="siswaRiwayatPage" style="display:none; background:var(--canvas-bg); min-height:100vh; padding:1.5rem;">
    <div style="max-width:900px; margin:0 auto;">
      <!-- Profile Card -->
      <div class="siswa-profile-card">
        <div class="profile-info">
          <h3 id="siswaRiwayatNama">-</h3>
          <p><span id="siswaRiwayatKelas">-</span>  <span id="siswaRiwayatJurusan">-</span>  Angkatan: <span id="siswaRiwayatAngkatan">-</span>  NISN: <span id="siswaRiwayatNISN">-</span></p>
        </div>
        <button class="btn-logout" id="btnSiswaLogout">
          <span class="material-symbols-outlined" style="font-size:16px">logout</span>
          Keluar
        </button>
      </div>

      <!-- Filter Bulan -->
      <div class="card" style="margin-bottom:1.5rem;">
        <div style="display:flex;align-items:center;gap:1rem;flex-wrap:wrap;">
          <label style="font-size:0.8125rem;font-weight:600;color:var(--text-muted);">Filter Bulan:</label>
          <input type="month" id="siswaFilterBulan" style="flex:1;min-width:180px;">
          <button class="btn btn-primary" id="btnSiswaFilter" style="display:flex;align-items:center;gap:0.375rem;">
            <span class="material-symbols-outlined" style="font-size:16px">search</span>
            Tampilkan
          </button>
        </div>
      </div>

      <!-- Stat Cards -->
      <div class="siswa-stat-grid">
        <div class="siswa-stat-item">
          <div class="stat-value" style="color:#2563eb;" id="siswaStHadir">0</div>
          <div class="stat-desc">Hadir</div>
        </div>
        <div class="siswa-stat-item">
          <div class="stat-value" style="color:#ea580c;" id="siswaStTerlambat">0</div>
          <div class="stat-desc">Terlambat</div>
        </div>
        <div class="siswa-stat-item">
          <div class="stat-value" style="color:#dc2626;" id="siswaStTidakHadir">0</div>
          <div class="stat-desc">Tidak Hadir</div>
        </div>
        <div class="siswa-stat-item">
          <div class="stat-value" style="color:#16a34a;" id="siswaStPersen">0%</div>
          <div class="stat-desc">Kehadiran</div>
        </div>
      </div>

      <!-- Riwayat Table -->
      <div class="card">
        <div style="font-size:1rem;font-weight:700;margin-bottom:1rem;color:var(--text-main);">Riwayat Absensi</div>
        <div style="overflow-x:auto;">
          <table>
            <thead>
              <tr>
                <th>No</th>
                <th>Tanggal</th>
                <th>Jam Masuk</th>

                <th>Status</th>
              </tr>
            </thead>
            <tbody id="tabelSiswaRiwayat">
              <tr>
                <td colspan="5" style="text-align:center;padding:2rem;color:var(--text-muted);">Pilih bulan lalu klik Tampilkan</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  </div>'''

new_riwayat = '''  <div id="siswaRiwayatPage" class="hidden bg-slate-50 min-h-screen py-8 px-4 sm:px-6">
    <div class="max-w-5xl mx-auto space-y-6">
      
      <!-- Profile Card -->
      <div class="bg-gradient-to-r from-blue-600 to-indigo-700 rounded-2xl p-6 sm:p-8 text-white shadow-lg flex flex-col sm:flex-row sm:items-center justify-between gap-6 relative overflow-hidden">
        <div class="absolute right-0 top-0 opacity-10 pointer-events-none translate-x-1/4 -translate-y-1/4">
          <span class="material-symbols-outlined text-[200px]">account_circle</span>
        </div>
        <div class="relative z-10">
          <h3 id="siswaRiwayatNama" class="text-2xl font-bold tracking-tight mb-4">Memuat...</h3>
          <div class="flex flex-wrap items-center gap-2 sm:gap-3 text-xs sm:text-sm font-semibold">
            <span class="bg-white/20 backdrop-blur-md px-3 py-1.5 rounded-lg border border-white/10 flex items-center gap-1.5 shadow-sm"><span class="material-symbols-outlined text-[16px] opacity-80">class</span> <span id="siswaRiwayatKelas">-</span></span>
            <span class="bg-white/20 backdrop-blur-md px-3 py-1.5 rounded-lg border border-white/10 flex items-center gap-1.5 shadow-sm"><span class="material-symbols-outlined text-[16px] opacity-80">school</span> <span id="siswaRiwayatJurusan">-</span></span>
            <span class="bg-white/20 backdrop-blur-md px-3 py-1.5 rounded-lg border border-white/10 flex items-center gap-1.5 shadow-sm"><span class="material-symbols-outlined text-[16px] opacity-80">calendar_month</span> Angkatan: <span id="siswaRiwayatAngkatan">-</span></span>
            <span class="bg-white/20 backdrop-blur-md px-3 py-1.5 rounded-lg border border-white/10 flex items-center gap-1.5 shadow-sm"><span class="material-symbols-outlined text-[16px] opacity-80">badge</span> NISN: <span id="siswaRiwayatNISN">-</span></span>
          </div>
        </div>
        <button id="btnSiswaLogout" class="relative z-10 bg-white/10 hover:bg-white/20 border border-white/20 text-white font-bold py-2.5 px-5 rounded-xl transition-colors flex items-center justify-center gap-2 whitespace-nowrap self-start sm:self-center shadow-sm">
          <span class="material-symbols-outlined text-[18px]">logout</span>
          Keluar
        </button>
      </div>

      <!-- Filter Bulan -->
      <div class="bg-white border border-slate-200 rounded-xl p-5 shadow-sm">
        <div class="flex flex-col sm:flex-row sm:items-center gap-4">
          <label class="text-sm font-bold text-slate-700 uppercase tracking-wider flex items-center gap-2">
            <span class="material-symbols-outlined text-slate-400">calendar_today</span>
            Filter Bulan
          </label>
          <div class="flex items-center gap-3 flex-1">
            <input type="month" id="siswaFilterBulan" class="flex-1 sm:max-w-xs bg-slate-50 border border-slate-200 text-slate-800 rounded-lg px-4 py-2 text-sm focus:ring-2 focus:ring-blue-500/20 focus:border-blue-600 transition-colors font-medium">
            <button id="btnSiswaFilter" class="bg-slate-800 hover:bg-slate-900 text-white font-semibold py-2 px-5 rounded-lg shadow-sm transition-colors flex items-center gap-2 text-sm whitespace-nowrap">
              <span class="material-symbols-outlined text-[18px]">search</span>
              Tampilkan
            </button>
          </div>
        </div>
      </div>

      <!-- Stat Cards -->
      <div class="grid grid-cols-2 md:grid-cols-4 gap-4 sm:gap-6">
        <div class="bg-white border border-slate-200 p-5 rounded-xl shadow-sm relative overflow-hidden group hover:border-blue-200 transition-colors">
          <div class="absolute -right-4 -bottom-4 text-blue-50 opacity-50 group-hover:scale-110 transition-transform duration-300">
            <span class="material-symbols-outlined text-[80px]">how_to_reg</span>
          </div>
          <div class="relative z-10">
            <div id="siswaStHadir" class="text-3xl font-bold text-blue-600 tracking-tight">0</div>
            <div class="text-xs font-bold text-slate-500 uppercase tracking-wider mt-1">Hadir</div>
          </div>
        </div>
        <div class="bg-white border border-slate-200 p-5 rounded-xl shadow-sm relative overflow-hidden group hover:border-orange-200 transition-colors">
          <div class="absolute -right-4 -bottom-4 text-orange-50 opacity-50 group-hover:scale-110 transition-transform duration-300">
            <span class="material-symbols-outlined text-[80px]">schedule</span>
          </div>
          <div class="relative z-10">
            <div id="siswaStTerlambat" class="text-3xl font-bold text-orange-600 tracking-tight">0</div>
            <div class="text-xs font-bold text-slate-500 uppercase tracking-wider mt-1">Terlambat</div>
          </div>
        </div>
        <div class="bg-white border border-slate-200 p-5 rounded-xl shadow-sm relative overflow-hidden group hover:border-red-200 transition-colors">
          <div class="absolute -right-4 -bottom-4 text-red-50 opacity-50 group-hover:scale-110 transition-transform duration-300">
            <span class="material-symbols-outlined text-[80px]">person_off</span>
          </div>
          <div class="relative z-10">
            <div id="siswaStTidakHadir" class="text-3xl font-bold text-red-600 tracking-tight">0</div>
            <div class="text-xs font-bold text-slate-500 uppercase tracking-wider mt-1">Tidak Hadir</div>
          </div>
        </div>
        <div class="bg-white border border-slate-200 p-5 rounded-xl shadow-sm relative overflow-hidden group hover:border-green-200 transition-colors">
          <div class="absolute -right-4 -bottom-4 text-green-50 opacity-50 group-hover:scale-110 transition-transform duration-300">
            <span class="material-symbols-outlined text-[80px]">donut_large</span>
          </div>
          <div class="relative z-10">
            <div id="siswaStPersen" class="text-3xl font-bold text-green-600 tracking-tight">0%</div>
            <div class="text-xs font-bold text-slate-500 uppercase tracking-wider mt-1">Kehadiran</div>
          </div>
        </div>
      </div>

      <!-- Riwayat Table -->
      <div class="bg-white border border-slate-200 rounded-xl shadow-sm overflow-hidden flex flex-col">
        <div class="p-5 border-b border-slate-100 flex items-center justify-between">
          <div class="text-sm font-bold uppercase tracking-wider text-slate-800 flex items-center gap-2">
            <span class="material-symbols-outlined text-blue-600">history</span>
            Riwayat Absensi Harian
          </div>
        </div>
        <div class="overflow-x-auto w-full">
          <table class="w-full text-left border-collapse">
            <thead>
              <tr class="bg-slate-50 border-b border-slate-200">
                <th class="py-3 px-5 text-xs font-bold text-slate-600 uppercase tracking-wider whitespace-nowrap">No</th>
                <th class="py-3 px-5 text-xs font-bold text-slate-600 uppercase tracking-wider whitespace-nowrap">Tanggal</th>
                <th class="py-3 px-5 text-xs font-bold text-slate-600 uppercase tracking-wider whitespace-nowrap">Jam Masuk</th>
                <th class="py-3 px-5 text-xs font-bold text-slate-600 uppercase tracking-wider whitespace-nowrap text-right">Status</th>
              </tr>
            </thead>
            <tbody id="tabelSiswaRiwayat">
              <tr>
                <td colspan="4" class="text-center py-12 text-sm font-medium text-slate-500">Pilih bulan lalu klik Tampilkan</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
      
    </div>
  </div>'''

html = html.replace(old_login, new_login)
html = html.replace(old_riwayat, new_riwayat)

# Update Javascript logic to use proper classes
old_js_html = '''            html += `<tr>
              <td>${no++}</td>
              <td>${tgl}</td>
              <td>${jamMasuk}</td>
              <td><span style="background:${statusBg};color:${statusColor};padding:0.25rem 0.75rem;border-radius:9999px;font-size:0.75rem;font-weight:600;">${status}</span></td>
            </tr>`;'''

new_js_html = '''            html += `<tr class="border-b border-slate-100 hover:bg-slate-50 transition-colors">
              <td class="py-3 px-5 text-sm font-medium text-slate-700 whitespace-nowrap">${no++}</td>
              <td class="py-3 px-5 text-sm font-semibold text-slate-700 whitespace-nowrap">${tgl}</td>
              <td class="py-3 px-5 text-sm font-medium text-slate-700 whitespace-nowrap">${jamMasuk}</td>
              <td class="py-3 px-5 text-right whitespace-nowrap"><span style="background:${statusBg};color:${statusColor};padding:0.375rem 0.75rem;border-radius:9999px;font-size:0.75rem;font-weight:700;letter-spacing:0.025em;display:inline-block;">${status}</span></td>
            </tr>`;'''

html = html.replace(old_js_html, new_js_html)

# Update the display properties from block/flex to remove inline styles completely in JS
html = html.replace("siswaRiwayatPage.style.display = 'none';", "siswaRiwayatPage.classList.add('hidden');\n        siswaLoginPage.classList.remove('hidden');")
html = html.replace("siswaLoginPage.style.display = 'flex';", "") # handled above
html = html.replace("siswaLoginPage.style.display = 'none';", "siswaLoginPage.classList.add('hidden');\n          siswaRiwayatPage.classList.remove('hidden');")
html = html.replace("siswaRiwayatPage.style.display = 'block';", "") # handled above

with codecs.open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
