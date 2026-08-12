import codecs
with codecs.open('index.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

new_content = """        <div class="siswa-stat-item">
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

# Replace lines 142 to 213 (inclusive) (0-indexed: 141 to 213)
# Note: lines are 1-indexed in the previous print, so lines[141] is '142:'
del lines[141:214]

# Insert the new content at line index 141
lines.insert(141, new_content)

with codecs.open('index.html', 'w', encoding='utf-8') as f:
    f.writelines(lines)
