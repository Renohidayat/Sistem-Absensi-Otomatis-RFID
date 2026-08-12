import re
import codecs

try:
    with codecs.open('js/UIManager.js', 'r', encoding='utf-8') as f:
        content = f.read()
except UnicodeError:
    with codecs.open('js/UIManager.js', 'r', encoding='utf-16') as f:
        content = f.read()

content = re.sub(r'if \(this\.dom\.inputJamPulangBuka\).*?\n', '', content)
content = re.sub(r'if \(this\.dom\.inputJamPulangTutup\).*?\n', '', content)
content = re.sub(r'<td class="py-2\.5 text-\[#2563eb\] font-semibold">\$\{isAktif \? \(d\.pulang_buka \|\| \'-\'\) : \'-\'\}</td>\n', '', content)
content = re.sub(r'<td class="py-2\.5 text-\[#64748b\]">\$\{isAktif \? \(d\.pulang_tutup \|\| \'-\'\) : \'-\'\}</td>\n', '', content)
content = re.sub(r'const t4 = this\.timeToMinutes\(d\.pulang_buka\);\n', '', content)
content = re.sub(r'const t5 = this\.timeToMinutes\(d\.pulang_tutup\);\n', '', content)
content = re.sub(r'if \(t2 <= t1 \|\| t3 <= t2 \|\| t4 <= t3 \|\| t5 <= t4\) \{.*?\}', 'if (t2 <= t1 || t3 <= t2) {\n        this.showPengaturanAlert(\'error\', \'Format jam tidak valid: Jam Masuk Buka harus < Batas Terlambat < Jam Masuk Tutup.\');\n        return;\n      }', content, flags=re.DOTALL)

with codecs.open('js/UIManager.js', 'w', encoding='utf-8') as f:
    f.write(content)

# And now fix admin.html
try:
    with codecs.open('admin.html', 'r', encoding='utf-8') as f:
        html = f.read()
except UnicodeError:
    with codecs.open('admin.html', 'r', encoding='utf-16') as f:
        html = f.read()

# Remove CARD 2 completely
html = re.sub(r'<!-- CARD 2: Pengaturan Jam Pulang -->.*?<div class="card mb-6">\s*<div class="flex items-center justify-between border-b border-slate-200 pb-3 mb-4">', '<div class="card mb-6">\n            <div class="flex items-center justify-between border-b border-slate-200 pb-3 mb-4">', html, flags=re.DOTALL)

with codecs.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(html)

