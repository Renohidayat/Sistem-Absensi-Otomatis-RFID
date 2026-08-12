import codecs

with codecs.open('js/UIManager.js', 'r', encoding='utf-8') as f:
    js = f.read()

# 1. Inject Delete Button in Tabel Siswa
old_td_buttons = '''        <td>
          <button class="px-3 py-1.5 bg-blue-50 text-blue-600 rounded hover:bg-blue-100 text-xs font-semibold flex items-center gap-1 transition-colors"
            onclick="window.app.openEditModal('${uid}')">
            <span class="material-symbols-outlined" style="font-size:14px">edit</span>
            Edit
          </button>
        </td>'''

new_td_buttons = '''        <td class="flex gap-2">
          <button class="px-3 py-1.5 bg-blue-50 text-blue-600 rounded hover:bg-blue-100 text-xs font-semibold flex items-center gap-1 transition-colors"
            onclick="window.app.openEditModal('${uid}')">
            <span class="material-symbols-outlined" style="font-size:14px">edit</span>
            Edit
          </button>
          <button class="px-3 py-1.5 bg-red-50 text-red-600 rounded hover:bg-red-100 text-xs font-semibold flex items-center gap-1 transition-colors"
            onclick="window.app.handleDeleteSiswa('${uid}')">
            <span class="material-symbols-outlined" style="font-size:14px">delete</span>
            Hapus
          </button>
        </td>'''

js = js.replace(old_td_buttons, new_td_buttons)


# 2. Inject handleDeleteSiswa function
handle_delete_func = '''  }

  /**
   * Handler untuk menghapus siswa dari database.
   */
  async handleDeleteSiswa(uid) {
    if (!uid) return;
    
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

js = js.replace("  }\n\n  /**\n   * Helper function untuk merender options admin", handle_delete_func)
js = js.replace("  }\r\n\r\n  /**\r\n   * Helper function untuk merender options admin", handle_delete_func)

with codecs.open('js/UIManager.js', 'w', encoding='utf-8') as f:
    f.write(js)
