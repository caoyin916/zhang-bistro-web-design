import re, json, sys
from cn_names import CN_NAMES

NAME_FIXES = {
    'Sichusn-Style Liangfen': 'Sichuan-Style Liangfen',
    'Hunan-Stye Stir-Fried Bamboo Shoot': 'Hunan-Style Stir-Fried Bamboo Shoot',
    'Sichuan-style Poachedroasted Duck': 'Sichuan-Style Poached & Roasted Duck',
    'Cumin Lamb.': 'Cumin Lamb (Chef Special)',
    'Spicy Frog Dry Hot Pot.': 'Spicy Frog Dry Hot Pot',
    'Paper-Wrappedfish': 'Paper-Wrapped Fish',
    'Coconut Mlik': 'Coconut Milk',
    'Dr.Pepper': 'Dr. Pepper',
}


def clean_name(name):
    name = NAME_FIXES.get(name, name)
    name = name.replace('（', '(').replace('）', ')')
    name = re.sub(r'\s*\(', ' (', name)
    name = re.sub(r'\bw\.\s*', 'w. ', name)
    return re.sub(r'\s{2,}', ' ', name).strip()


with open('menu-raw.txt', encoding='utf-8') as f:
    lines = [l.strip() for l in f.read().splitlines() if l.strip()]

cat_re = re.compile(r'^(.+?) \((\d+)\)$')
skip_lines = {'Rice not included. Order separately.米飯不包含在內'}

categories = []
cur = None
i = 0
n = len(lines)
while i < n:
    line = lines[i]
    m = cat_re.match(line)
    if m and line not in skip_lines:
        cur = {'name': m.group(1), 'count': int(m.group(2)), 'items': []}
        categories.append(cur)
        i += 1
        continue
    if line in skip_lines:
        i += 1
        continue
    name = line
    i += 1
    price = None
    popular = False
    while i < n and lines[i].startswith('Price:'):
        price = lines[i].replace('Price:', '').strip()
        i += 1
    # "Sold Out" is the ordering site's stock status on the day of the scrape, not a menu fact — skip it.
    while i < n and lines[i] in ('Popular', 'Sold Out'):
        if lines[i] == 'Popular':
            popular = True
        i += 1
    if cur is not None and price:
        en = clean_name(name)
        cur['items'].append({'name': en, 'cn': CN_NAMES.get(en), 'price': price,
                             'popular': popular})

missing = [it['name'] for c in categories for it in c['items'] if not it['cn']]
used = {it['name'] for c in categories for it in c['items']}
unused = sorted(set(CN_NAMES) - used)
total_items = sum(len(c['items']) for c in categories)
print('Categories:', len(categories), '| Items:', total_items)
if missing or unused:
    print('Missing CN:', missing)
    print('Unused CN keys:', unused)
    sys.exit(1)

with open('menu.json', 'w', encoding='utf-8') as f:
    json.dump(categories, f, ensure_ascii=False, indent=2)
print('OK: every item has a Chinese name')
