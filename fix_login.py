import codecs

with codecs.open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Remove style="display:flex;" from login page container
html = html.replace('id="siswaLoginPage" class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4 relative overflow-hidden" style="display:flex;"', 'id="siswaLoginPage" class="min-h-screen flex items-center justify-center bg-gradient-to-br from-blue-50 to-indigo-100 p-4 relative overflow-hidden"')

# 2. Revert logic back to style.display so it overrides Tailwind classes safely
old_logout = "siswaRiwayatPage.classList.add('hidden');\\n        siswaLoginPage.classList.remove('hidden');"
# Using string replace with actual newline characters
old_logout = "siswaRiwayatPage.classList.add('hidden');\n        siswaLoginPage.classList.remove('hidden');"
new_logout = "siswaRiwayatPage.style.display = 'none';\n        siswaLoginPage.style.display = 'flex';"
html = html.replace(old_logout, new_logout)

old_login_js = "siswaLoginPage.classList.add('hidden');\n          siswaRiwayatPage.classList.remove('hidden');"
new_login_js = "siswaLoginPage.style.display = 'none';\n          siswaRiwayatPage.style.display = 'block';"
html = html.replace(old_login_js, new_login_js)

# Also fix the innerHTML that my script missed earlier
old_js_html = '''            html += `<tr>
              <td>${no++}</td>
              <td>${tgl}</td>
              <td>${jamMasuk}</td>
              <td><span style="background:${statusBg};color:${statusColor};padding:0.25rem 0.75rem;border-radius:9999px;font-size:0.75rem;font-weight:600;">${status}</span></td>
            </tr>`;'''

new_js_html = '''            html += `<tr class="border-b border-slate-100 hover:bg-slate-50 transition-colors">
              <td class="py-3 px-5 text-sm font-medium text-slate-700 whitespace-nowrap">${no++}</td>
              <td class="py-3 px-5 text-sm font-semibold text-slate-700 whitespace-nowrap">${tgl}</td>
              <td class="py-3 px-5 text-sm font-medium text-slate-700 whitespace-nowrap">${jamMasuk}</td>
              <td class="py-3 px-5 text-right whitespace-nowrap"><span style="background:${statusBg};color:${statusColor};padding:0.375rem 0.75rem;border-radius:9999px;font-size:0.75rem;font-weight:700;letter-spacing:0.025em;display:inline-block;">${status}</span></td>
            </tr>`;'''

html = html.replace(old_js_html, new_js_html)

with codecs.open('index.html', 'w', encoding='utf-8') as f:
    f.write(html)
