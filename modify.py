import re

def process_admin():
    with open('admin.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove Student Login & Riwayat Page
    content = re.sub(r'<!-- ===== STUDENT LOGIN PAGE.*?<!-- ===== MAIN DASHBOARD ===== -->', '<!-- ===== MAIN DASHBOARD ===== -->', content, flags=re.DOTALL)

    # 2. Modify btnPortalSiswa
    content = content.replace('<div class="tab-btn" id="btnPortalSiswa"', '<a href="index.html" class="tab-btn" id="btnPortalSiswa" style="text-decoration:none;"')
    content = content.replace('<span class="material-symbols-outlined text-[20px]">school</span> Portal Siswa\n          </div>', '<span class="material-symbols-outlined text-[20px]">school</span> Portal Siswa\n          </a>')

    # 3. Remove Student Portal Logic JS
    content = re.sub(r'// ===== STUDENT PORTAL LOGIC =====.*?function countWeekdays.*?\}', '', content, flags=re.DOTALL)

    with open('admin.html', 'w', encoding='utf-8') as f:
        f.write(content)

def process_index():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    # 1. Remove Main Dashboard
    content = re.sub(r'<!-- ===== MAIN DASHBOARD ===== -->.*?(?=\s*<script>)', '', content, flags=re.DOTALL)

    # 2. Add Login Admin button
    admin_btn = """      <div style="margin-top:1.5rem; padding-top:1.25rem; border-top:1px solid #e2e8f0; text-align:center;">
        <a href="admin.html" style="background:none;border:none;color:#64748b;font-size:0.8125rem;font-weight:600;text-decoration:none;display:inline-flex;align-items:center;gap:0.375rem;">
          <span class="material-symbols-outlined" style="font-size:16px">admin_panel_settings</span>
          Masuk sebagai Admin
        </a>
      </div>"""
    
    # replace backToDashboard button with Login Admin button
    content = re.sub(r'<div style="margin-top:1.5rem; padding-top:1.25rem; border-top:1px solid #e2e8f0;">.*?</div>', admin_btn, content, flags=re.DOTALL)
    
    # 3. Set display to flex/block instead of none
    content = content.replace('<div id="siswaLoginPage" class="siswa-login-container" style="display:none;">', '<div id="siswaLoginPage" class="siswa-login-container" style="display:flex;">')

    # 4. Remove app.js import
    content = content.replace('<script src="js/app.js?v=6" type="module"></script>', '')

    # 5. Hide btnSiswaLogout if it tries to switch display of mainDashboard
    # Actually just leave JS as is, but remove references to mainDashboard
    content = content.replace('mainDashboard.style.display', '// mainDashboard.style.display')

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(content)

process_admin()
process_index()
print("Done")
