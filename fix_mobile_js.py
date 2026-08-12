import codecs

with codecs.open('js/UIManager.js', 'r', encoding='utf-8') as f:
    js = f.read()

mobile_logic = '''  bindEvents() {
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
'''

if "Mobile Sidebar Toggle" not in js:
    js = js.replace('''  bindEvents() {
    console.log("bindEvents dijalankan");''', mobile_logic)

with codecs.open('js/UIManager.js', 'w', encoding='utf-8') as f:
    f.write(js)
    
# cache bust app.js and admin.html
with codecs.open('js/app.js', 'r', encoding='utf-8') as f:
    app_js = f.read()
with codecs.open('js/app.js', 'w', encoding='utf-8') as f:
    f.write(app_js.replace('v=13', 'v=14'))

with codecs.open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()
with codecs.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(html.replace('js/app.js?v=13', 'js/app.js?v=14'))
