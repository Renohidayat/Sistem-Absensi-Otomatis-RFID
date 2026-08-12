import codecs

with codecs.open('js/UIManager.js', 'r', encoding='utf-8') as f:
    js = f.read()

# Fix the butchered bindEvents and terakhir_diperbarui
broken_code = '''      if (this.cachePengaturan && this.cachePengaturan.terakhir_diperbarui && this.dom.pengaturanTerakhirUpdate) {
        const date = new Date(this.cachePengaturan.terakhir_diperbarui);
      console.log("Tombol Login Admin diklik");

      if (this.auth.isAdmin()) {
        await this.auth.logout();
        this.renderAdminState();
      } else {
        this.openLoginModal();
      }
    });'''

fixed_code = '''      if (this.cachePengaturan && this.cachePengaturan.terakhir_diperbarui && this.dom.pengaturanTerakhirUpdate) {
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

    this.dom.btnAdminToggle.addEventListener('click', async () => {
      console.log("Tombol Login Admin diklik");

      if (this.auth.isAdmin()) {
        await this.auth.logout();
        this.renderAdminState();
      } else {
        this.openLoginModal();
      }
    });'''

js = js.replace(broken_code, fixed_code)

# Now inject handleDeleteSiswa correctly
handle_delete = '''  }

  /**
   * Handler untuk menghapus siswa dari database.
   */
  async handleDeleteSiswa(uid) {
    if (!uid) return;
    
    // Tampilkan konfirmasi menggunakan bawaan browser
    const studentData = this.daftarSiswaCache[uid];
    const studentName = studentData ? (studentData.nama || 'Tanpa Nama').replace(/_/g, ' ') : uid;
    
    const confirmDelete = window.confirm(`PERINGATAN!\\n\\nApakah Anda yakin ingin menghapus data siswa bernama "${studentName}" secara permanen?\\nData yang dihapus tidak dapat dikembalikan.`);
    
    if (confirmDelete) {
      try {
        await this.dbService.deleteSiswa(uid);
        this.showAlert('success', `Data siswa ${studentName} berhasil dihapus.`);
      } catch (error) {
        console.error('Error saat menghapus siswa:', error);
        this.showAlert('error', 'Gagal menghapus siswa: ' + error.message);
      }
    }
  }

  /**
   * Helper function untuk merender options admin
'''

js = js.replace("  }\n\n  /**\n   * Helper function untuk merender options admin", handle_delete)
js = js.replace("  }\r\n\r\n  /**\r\n   * Helper function untuk merender options admin", handle_delete)


with codecs.open('js/UIManager.js', 'w', encoding='utf-8') as f:
    f.write(js)
