import codecs
import re

with codecs.open('js/UIManager.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Add DOM references for mobile
if "btnMobileMenu: document.getElementById('btnMobileMenu')," not in js:
    js = js.replace("tabelLaporan: document.getElementById('tabelLaporan'),", "tabelLaporan: document.getElementById('tabelLaporan'),\n      btnMobileMenu: document.getElementById('btnMobileMenu'),\n      mobileOverlay: document.getElementById('mobileOverlay'),\n      mainSidebar: document.getElementById('mainSidebar'),")

# Add mobile toggle logic in bindEvents
mobile_logic = '''
    // Mobile Sidebar Toggle
    if (this.dom.btnMobileMenu && this.dom.mainSidebar && this.dom.mobileOverlay) {
      const toggleSidebar = () => {
        this.dom.mainSidebar.classList.toggle('mobile-open');
        this.dom.mobileOverlay.classList.toggle('active');
      };

      this.dom.btnMobileMenu.addEventListener('click', toggleSidebar);
      this.dom.mobileOverlay.addEventListener('click', toggleSidebar);

      // Close sidebar when clicking a tab on mobile
      this.dom.tabBtns.forEach(btn => {
        btn.addEventListener('click', () => {
          if (window.innerWidth <= 768 && this.dom.mainSidebar.classList.contains('mobile-open')) {
            toggleSidebar();
          }
        });
      });
    }
'''

if "Mobile Sidebar Toggle" not in js:
    js = js.replace("this.dom.btnLogout.addEventListener('click', () => this.auth.logout());", "this.dom.btnLogout.addEventListener('click', () => this.auth.logout());" + mobile_logic)

with codecs.open('js/UIManager.js', 'w', encoding='utf-8') as f:
    f.write(js)
