import codecs
import re

with codecs.open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

pattern = re.compile(r'<!-- ===== STUDENT LOGIN PAGE \(SPLIT LAYOUT\) ===== -->.*?<!-- ===== STUDENT RIWAYAT PAGE', re.DOTALL)

new_login = '''<!-- ===== STUDENT LOGIN PAGE (SPLIT LAYOUT) ===== -->
  <div id="siswaLoginPage" class="min-h-screen flex items-center justify-center bg-slate-50 relative overflow-hidden" style="display:block;">
    
    <div class="w-full max-w-5xl mx-auto flex flex-col lg:flex-row bg-white lg:rounded-[2rem] lg:shadow-xl overflow-hidden min-h-screen lg:min-h-[80vh] m-0 lg:m-6 border border-slate-100">
      
      <!-- Kiri: Branding & Ilustrasi (Hanya Desktop) -->
      <div class="hidden lg:flex lg:w-5/12 bg-gradient-to-br from-blue-700 via-blue-800 to-indigo-900 relative p-10 flex-col justify-between text-white overflow-hidden">
        <!-- Giant Watermark Logo -->
        <div class="absolute -right-20 -bottom-20 w-[400px] h-[400px] opacity-10 mix-blend-overlay pointer-events-none">
          <img alt="Watermark" src="assets/logo.png" class="w-full h-full object-contain grayscale brightness-200">
        </div>
        
        <!-- Abstract Shapes -->
        <div class="absolute top-0 left-0 w-full h-full overflow-hidden z-0 pointer-events-none opacity-30">
          <div class="absolute -top-[10%] -left-[20%] w-[70%] h-[70%] rounded-full bg-blue-400 blur-[80px]"></div>
          <!-- Grid Pattern -->
          <div class="absolute inset-0" style="background-image: radial-gradient(rgba(255, 255, 255, 0.15) 1px, transparent 1px); background-size: 32px 32px;"></div>
        </div>
        
        <div class="relative z-10">
          <div class="w-20 h-20 rounded-full overflow-hidden shadow-lg border-4 border-white/20 bg-white mb-8 flex items-center justify-center p-1.5">
            <img alt="SMK PGRI 2" src="assets/logo.png" class="w-full h-full object-contain">
          </div>
          <h1 class="text-4xl font-extrabold tracking-tight mb-4 leading-tight text-transparent bg-clip-text bg-gradient-to-br from-white to-blue-200">Sistem Absensi<br>RFID Berbasis IoT</h1>
          <p class="text-blue-100/90 text-base font-medium max-w-sm leading-relaxed">Pantau kedisiplinan dan riwayat kehadiran siswa SMK PGRI 2 Sumedang secara real-time dan akurat.</p>
        </div>
        
        <div class="relative z-10 text-xs text-blue-200/70 font-medium tracking-wide uppercase">
          &copy; 2026 SMK PGRI 2 Sumedang
        </div>
      </div>
      
      <!-- Kanan: Form Login -->
      <div class="w-full lg:w-7/12 p-6 sm:p-10 lg:p-14 flex flex-col justify-center relative min-h-screen lg:min-h-0 bg-white">
        <!-- Mobile Logo (Muncul hanya di HP) -->
        <div class="lg:hidden w-16 h-16 rounded-full mx-auto overflow-hidden shadow-md border border-slate-100 bg-white mb-6 flex items-center justify-center p-1.5">
          <img alt="SMK PGRI 2" src="assets/logo.png" class="w-full h-full object-contain">
        </div>

        <div class="max-w-sm w-full mx-auto">
          <div class="mb-8 text-center lg:text-left">
            <h2 class="text-2xl font-extrabold text-slate-900 tracking-tight mb-2">Portal Siswa</h2>
            <p class="text-slate-500 text-sm font-medium leading-relaxed">Masukkan Nomor Induk Siswa Nasional (NISN) Anda untuk melihat riwayat kehadiran bulan ini.</p>
          </div>
          
          <div class="hidden bg-red-50 border border-red-200 text-red-600 px-4 py-3 rounded-xl text-sm mb-6 font-semibold items-start gap-2" id="siswaLoginError">
            <span class="material-symbols-outlined text-[20px]">error</span>
            <span id="siswaLoginErrorText">NISN tidak ditemukan.</span>
          </div>
          
          <form id="formSiswaLogin" class="text-left mb-8">
            <div class="mb-6 relative">
              <label for="inputNISN" class="block text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-2">Nomor Induk Siswa Nasional</label>
              <div class="relative group">
                <div class="absolute inset-y-0 left-0 flex items-center pl-3.5 pointer-events-none text-slate-400 group-focus-within:text-blue-600 transition-colors">
                  <span class="material-symbols-outlined text-[22px]">badge</span>
                </div>
                <input id="inputNISN" type="text" placeholder="Contoh: 0012345678" maxlength="10" pattern="[0-9]{10}" required 
                  class="w-full pl-11 pr-4 py-3 bg-slate-50/50 border border-slate-200 text-slate-900 rounded-xl focus:bg-white focus:ring-4 focus:ring-blue-500/10 focus:border-blue-600 transition-all text-sm font-semibold shadow-sm placeholder:text-slate-400 placeholder:font-normal">
              </div>
            </div>
            
            <button type="submit" class="btn-login w-full bg-blue-600 hover:bg-blue-700 text-white font-bold py-3 px-4 rounded-xl shadow-md shadow-blue-600/20 flex items-center justify-center gap-2 transition-all active:scale-[0.98] focus:outline-none focus:ring-4 focus:ring-blue-500/30">
              <span class="material-symbols-outlined text-[18px]">login</span>
              Masuk sebagai Siswa
            </button>
          </form>
          
          <!-- Tombol Admin (Subtle Ghost Link) -->
          <div class="text-center mt-12">
             <button id="btnAdminDirectLogin" type="button" class="inline-flex items-center justify-center gap-1.5 text-[13px] font-bold text-slate-400 hover:text-blue-600 transition-colors focus:outline-none focus:text-blue-600">
                <span class="material-symbols-outlined text-[16px]">admin_panel_settings</span>
                Masuk sebagai Petugas
             </button>
          </div>
          
          <div class="mt-10 text-center lg:hidden">
            <p class="text-[11px] text-slate-400 font-medium uppercase tracking-wider">&copy; 2026 SMK PGRI 2 Sumedang.</p>
          </div>
        </div>
      </div>
      
    </div>
  </div>

  <!-- ===== STUDENT RIWAYAT PAGE'''

html = pattern.sub(new_login, html)

with codecs.open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
