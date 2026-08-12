import codecs

with codecs.open('js/UIManager.js', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_lines = []
for i, line in enumerate(lines):
    if i == 255: # Line 256 in 1-indexed (which is "    this.dom.btnGoogleLogin.addEventListener('click', () => this.handleGoogleLogin());")
        # Inject the missing block before this line
        injection = """
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
"""
        new_lines.append(injection)
        new_lines.append(line)
    else:
        new_lines.append(line)

with codecs.open('js/UIManager.js', 'w', encoding='utf-8') as f:
    f.writelines(new_lines)
