import codecs
with codecs.open('admin.html', 'r', encoding='utf-8') as f:
    lines = f.readlines()

def print_select(id):
    for i, line in enumerate(lines):
        if f'id="{id}"' in line:
            print(f'--- {id} ---')
            for j in range(i, min(i+10, len(lines))):
                print(lines[j].strip())
                if '</select>' in lines[j]:
                    break

print_select('statJurusan')
print_select('lapJurusan')
print_select('regJurusan')
print_select('editJurusan')
