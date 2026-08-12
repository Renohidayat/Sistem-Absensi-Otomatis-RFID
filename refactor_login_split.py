import codecs

with codecs.open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. HTML Replacement for Login Page
old_login = '''  <div id="siswaLoginPage" class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4 relative overflow-hidden">
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
        <button type="submit" class="btn-login w-full bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700 text-white font-semibold py-3.5 px-4 rounded-xl shadow-lg shadow-blue-500/30 flex items-center justify-center gap-2 transition-all active:scale-[0.98]">
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

new_login = '''  <!-- ===== STUDENT LOGIN PAGE (SPLIT LAYOUT) ===== -->
  <div id="siswaLoginPage" class="min-h-screen flex items-center justify-center bg-slate-50 relative overflow-hidden">
    
    <div class="w-full max-w-6xl mx-auto flex flex-col lg:flex-row bg-white lg:rounded-[2.5rem] lg:shadow-2xl overflow-hidden min-h-screen lg:min-h-[85vh] m-0 lg:m-6">
      
      <!-- Kiri: Branding & Ilustrasi (Hanya Desktop) -->
      <div class="hidden lg:flex lg:w-5/12 bg-gradient-to-br from-blue-700 via-blue-800 to-indigo-900 relative p-12 flex-col justify-between text-white overflow-hidden">
        <!-- Abstract Shapes -->
        <div class="absolute top-0 left-0 w-full h-full overflow-hidden z-0 pointer-events-none opacity-40">
          <div class="absolute -top-[10%] -left-[20%] w-[70%] h-[70%] rounded-full bg-blue-400 blur-[80px]"></div>
          <div class="absolute bottom-[0%] -right-[20%] w-[60%] h-[60%] rounded-full bg-indigo-500 blur-[100px]"></div>
          <!-- Grid Pattern -->
          <div class="absolute inset-0" style="background-image: radial-gradient(rgba(255, 255, 255, 0.15) 1px, transparent 1px); background-size: 32px 32px;"></div>
        </div>
        
        <div class="relative z-10">
          <div class="w-24 h-24 rounded-full overflow-hidden shadow-xl border-4 border-white/20 bg-white mb-8 flex items-center justify-center p-2">
            <img alt="SMK PGRI 2" src="assets/logo.png" class="w-full h-full object-contain">
          </div>
          <h1 class="text-4xl font-extrabold tracking-tight mb-4 leading-tight">Sistem Absensi<br>RFID Berbasis IoT</h1>
          <p class="text-blue-100 text-lg font-medium max-w-sm">Pantau kedisiplinan dan riwayat kehadiran siswa SMK PGRI 2 Sumedang secara real-time dan akurat.</p>
        </div>
        
        <div class="relative z-10 text-sm text-blue-200/80 font-medium">
          &copy; 2026 SMK PGRI 2 Sumedang. Hak Cipta Dilindungi.
        </div>
      </div>
      
      <!-- Kanan: Form Login -->
      <div class="w-full lg:w-7/12 p-6 sm:p-12 lg:p-16 flex flex-col justify-center relative min-h-screen lg:min-h-0 bg-white">
        <!-- Mobile Logo (Muncul hanya di HP) -->
        <div class="lg:hidden w-20 h-20 rounded-full mx-auto overflow-hidden shadow-lg border-2 border-slate-100 bg-white mb-8 flex items-center justify-center p-2">
          <img alt="SMK PGRI 2" src="assets/logo.png" class="w-full h-full object-contain">
        </div>

        <div class="max-w-md w-full mx-auto lg:mx-0">
          <div class="mb-10 text-center lg:text-left">
            <h2 class="text-3xl font-extrabold text-slate-900 tracking-tight mb-3">Portal Siswa</h2>
            <p class="text-slate-500 font-medium">Masukkan Nomor Induk Siswa Nasional (NISN) Anda untuk melihat riwayat kehadiran bulan ini.</p>
          </div>
          
          <div class="hidden bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-xl text-sm mb-6 font-semibold flex items-start gap-2" id="siswaLoginError">
            <span class="material-symbols-outlined text-[20px]">error</span>
            <span id="siswaLoginErrorText">NISN tidak ditemukan.</span>
          </div>
          
          <form id="formSiswaLogin" class="text-left">
            <div class="mb-6 relative">
              <label for="inputNISN" class="block text-xs font-bold text-slate-600 uppercase tracking-wider mb-2">Nomor Induk Siswa Nasional</label>
              <div class="relative group">
                <div class="absolute inset-y-0 left-0 flex items-center pl-4 pointer-events-none text-slate-400 group-focus-within:text-blue-600 transition-colors">
                  <span class="material-symbols-outlined text-xl">badge</span>
                </div>
                <input id="inputNISN" type="text" placeholder="Contoh: 0012345678" maxlength="10" pattern="[0-9]{10}" required 
                  class="w-full pl-11 pr-4 py-3.5 bg-slate-50 border border-slate-200 text-slate-900 rounded-xl focus:bg-white focus:ring-4 focus:ring-blue-500/20 focus:border-blue-600 transition-all text-base font-semibold shadow-sm placeholder:text-slate-400 placeholder:font-normal">
              </div>
            </div>
            
            <button type="submit" class="btn-login w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3.5 px-4 rounded-xl shadow-lg shadow-blue-600/30 flex items-center justify-center gap-2 transition-all active:scale-[0.98] focus:ring-4 focus:ring-blue-500/30">
              <span class="material-symbols-outlined text-[20px]">login</span>
              Masuk sebagai Siswa
            </button>
          </form>
          
          <div class="mt-10 mb-6 flex items-center">
            <div class="flex-grow border-t border-slate-200"></div>
            <span class="flex-shrink-0 mx-4 text-slate-400 text-xs font-bold uppercase tracking-wider">Atau Khusus Petugas</span>
            <div class="flex-grow border-t border-slate-200"></div>
          </div>
          
          <button id="btnAdminDirectLogin" type="button" class="w-full bg-white hover:bg-slate-50 text-slate-700 border border-slate-300 font-bold py-3 px-4 rounded-xl shadow-sm flex items-center justify-center gap-2 transition-all active:scale-[0.98] focus:ring-4 focus:ring-slate-100">
            <span class="material-symbols-outlined text-[20px] text-slate-500">admin_panel_settings</span>
            Masuk sebagai Admin (Google)
          </button>
          
          <div class="mt-12 text-center lg:hidden">
            <p class="text-xs text-slate-400 font-medium">&copy; 2026 SMK PGRI 2 Sumedang.</p>
          </div>
        </div>
      </div>
      
    </div>
  </div>'''

html = html.replace(old_login, new_login)


# 2. Add Javascript logic for Admin Direct Login
# We'll inject it right after btnSiswaLogout logic
old_js = '''      btnSiswaLogout.addEventListener('click', () => {
        currentSiswaData = null;
        siswaRiwayatPage.style.display = 'none';
        siswaLoginPage.style.display = 'flex';
      });'''

new_js = '''      btnSiswaLogout.addEventListener('click', () => {
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
            await authManager.loginWithGoogle();
            
            // Cek apakah sukses dan terdaftar
            const isUserAdmin = await dbService.checkAdminEmail(authManager.currentUser.email);
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
      }'''

html = html.replace(old_js, new_js)

# Update Login error text logic
old_error_js = '''            siswaLoginError.textContent = 'NISN tidak ditemukan. Pastikan NISN Anda benar.';
            siswaLoginError.style.display = 'block';'''

new_error_js = '''            const errText = document.getElementById('siswaLoginErrorText');
            if (errText) errText.textContent = 'NISN tidak ditemukan. Pastikan NISN Anda benar.';
            siswaLoginError.style.display = 'flex';
            document.getElementById('inputNISN').classList.add('border-red-500', 'ring-4', 'ring-red-500/20');'''

html = html.replace(old_error_js, new_error_js)

old_error_js2 = '''          siswaLoginError.textContent = 'Terjadi kesalahan. Coba lagi.';
          siswaLoginError.style.display = 'block';'''

new_error_js2 = '''          const errText = document.getElementById('siswaLoginErrorText');
          if (errText) errText.textContent = 'Terjadi kesalahan jaringan. Coba lagi.';
          siswaLoginError.style.display = 'flex';
          document.getElementById('inputNISN').classList.add('border-red-500', 'ring-4', 'ring-red-500/20');'''
          
html = html.replace(old_error_js2, new_error_js2)

# Reset border error on submit
old_submit_js = '''        siswaLoginError.style.display = 'none';'''
new_submit_js = '''        siswaLoginError.style.display = 'none';
        document.getElementById('inputNISN').classList.remove('border-red-500', 'ring-4', 'ring-red-500/20');'''

html = html.replace(old_submit_js, new_submit_js)

# Fix block/flex in display init logic
html = html.replace("siswaLoginPage.style.display = 'flex';", "siswaLoginPage.style.display = 'block';")

with codecs.open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)

print("SUCCESS")
