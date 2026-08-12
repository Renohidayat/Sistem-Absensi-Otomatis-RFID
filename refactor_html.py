import codecs
import re

with codecs.open('admin.html', 'r', encoding='utf-8') as f:
    html = f.read()

# 1. Insert mobile header and overlay
header_injection = '''    <!-- Mobile Header & Overlay -->
    <div class="mobile-header">
      <div class="flex items-center gap-3">
        <img alt="Logo" class="w-8 h-8 rounded-lg shadow-sm" src="assets/logo.png">
        <span class="font-bold text-sm tracking-tight text-slate-800 uppercase">Sistem Absensi</span>
      </div>
      <button id="btnMobileMenu" class="p-2 -mr-2 flex items-center justify-center text-slate-600 hover:bg-slate-100 rounded-lg transition-colors">
        <span class="material-symbols-outlined text-2xl">menu</span>
      </button>
    </div>
    <div id="mobileOverlay" class="mobile-overlay"></div>
    
    <!-- SIDEBAR -->'''

html = html.replace('<!-- SIDEBAR -->', header_injection)

# 2. Add id to aside for JS targeting
html = html.replace('<aside>', '<aside id="mainSidebar">')

# 3. Replace text-slate-400 with text-slate-500
html = html.replace('text-slate-400', 'text-slate-500')

# 4. Replace text-[10px] with text-xs
html = html.replace('text-[10px]', 'text-xs')

# 5. Make sure all tables have overflow-x-auto wrapper (most already do, but we will ensure whitespace nowrap on th/td)
html = html.replace('<th ', '<th class="whitespace-nowrap" ')
html = html.replace('<td ', '<td class="whitespace-nowrap" ')

# But some <th> already have classes. Let's do regex to add whitespace-nowrap safely.
def add_nowrap(match):
    class_content = match.group(1)
    if 'whitespace-nowrap' not in class_content:
        return 'class="whitespace-nowrap ' + class_content + '"'
    return match.group(0)

html = re.sub(r'class="([^"]*)"', lambda m: 'class="whitespace-nowrap ' + m.group(1) + '"' if ('py-' in m.group(1) and ('text-xs' in m.group(1) or 'uppercase' in m.group(1)) and 'whitespace-nowrap' not in m.group(1)) else m.group(0), html)

# 6. Change bg-blue-50 to bg-blue-100 for better border contrast, or just ensure text is dark enough.

with codecs.open('admin.html', 'w', encoding='utf-8') as f:
    f.write(html)
