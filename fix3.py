import codecs

with codecs.open('index.html', 'r', encoding='utf-8') as f:
    html = f.read()

bad_str = """        const btn = formSiswaLogin.querySelector('.btn-login');
        if(btn) {
            btn.innerHTML = '<span class="material-symbols-outlined" style="font-size:20px">login</span> Masuk';
            btn.disabled = false;
        }
      });"""

good_str = """        if(btn) {
            btn.innerHTML = '<span class="material-symbols-outlined" style="font-size:20px">login</span> Masuk';
            btn.disabled = false;
        }
      });"""

if bad_str in html:
    html = html.replace(bad_str, good_str)
    with codecs.open('index.html', 'w', encoding='utf-8') as f:
        f.write(html)
    print('Fixed duplicate const btn')
else:
    print('Could not find duplicate const btn')
