import codecs
with codecs.open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_content = """          <div class="stat-value" style="color:#16a34a;" id="siswaStPersen">0%</div>
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
                <th>Jam Pulang</th>
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
  </div>
"""

# indices 143 to 213 (inclusive) are deleted.
del lines[143:214]

lines.insert(143, new_content)

with codecs.open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)
