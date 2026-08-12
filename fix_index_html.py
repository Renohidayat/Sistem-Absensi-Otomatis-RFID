import codecs

with codecs.open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

html = html.replace('''            html += `<tr>
              <td>${no++}</td>
              <td>${tgl}</td>
              <td>${jamMasuk}</td>
              <td><span style="background:${statusBg};color:${statusColor};padding:0.25rem 0.75rem;border-radius:9999px;font-size:0.75rem;font-weight:600;">${status}</span></td>
            </tr>`;''', '''            html += `<tr>
              <td>${no++}</td>
              <td>${tgl}</td>
              <td>${jamMasuk}</td>
              <td>${jamPulang}</td>
              <td><span style="background:${statusBg};color:${statusColor};padding:0.25rem 0.75rem;border-radius:9999px;font-size:0.75rem;font-weight:600;">${status}</span></td>
            </tr>`;''')

html = html.replace('''colspan="5"''', '''colspan="6"''')

with codecs.open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
