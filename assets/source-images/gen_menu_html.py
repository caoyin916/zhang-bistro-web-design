# Regenerates menu.html's category blocks (MENU:START/END) and its schema.org Menu data (MENU-LD:START/END).
import json, re
from html import escape
from menu_photos import photo_plan

MENU_HTML = '../../menu.html'
SITE = 'https://www.zhangsbistro.com/'

CATEGORY_CN = {
    'Appetizer': '小菜',
    'Small Eats': '小吃',
    'Cold Dish': '凉菜',
    'Soup': '汤类',
    'Noodles/Rice': '面饭',
    'Beef': '牛肉',
    'Lamb': '羊肉',
    'Chicken': '鸡肉',
    'Duck': '鸭',
    'Pork': '猪肉',
    'Cured Meats': '腊味',
    'Tofu': '豆腐',
    'Vegetable': '素菜',
    'Chef Special': '招牌菜',
    'Dry Hot Pot': '干锅',
    'Seafood': '海鲜',
    'Snakehead Fish Fillets': '黑鱼片',
    'Live Fish': '活鱼',
    'Side Order': '配餐',
    'Dessert': '甜品',
    'Beverages': '饮品',
}


def slug(name):
    return re.sub(r'[^a-z0-9]+', '-', name.lower()).strip('-')


def item_html(item, photo):
    flags = ''
    cls = 'menu-item'
    if item['popular']:
        flags += '<span class="pop-flag">Popular</span>'
    if item['soldOut']:
        flags += '<span class="soldout-flag">Sold Out</span>'
        cls += ' is-sold-out'
    attrs = ''
    icon = ''
    if photo:
        cls += ' has-photo'
        attrs = f' data-photo="{photo}"'
        icon = '<span class="photo-icon" aria-hidden="true"></span>'
    return (
        f'<button type="button" class="{cls}"{attrs}><span class="menu-item-name">'
        f'<span class="menu-item-en">{escape(item["name"], quote=False)}{icon}{flags}</span>'
        f'<span class="menu-item-cn cn">{item["cn"]}</span>'
        f'</span><span class="menu-item-price">{item["price"]}</span></button>'
    )


def menu_ld(categories, photos):
    sections = []
    for cat in categories:
        items = []
        for it in cat['items']:
            entry = {
                '@type': 'MenuItem',
                'name': it['name'],
                'alternateName': it['cn'],
                'offers': {'@type': 'Offer', 'price': it['price'].lstrip('$'), 'priceCurrency': 'USD'},
            }
            if it['name'] in photos:
                entry['image'] = SITE + photos[it['name']]
            items.append(entry)
        sections.append({'@type': 'MenuSection', 'name': cat['name'],
                         'alternateName': CATEGORY_CN[cat['name']], 'hasMenuItem': items})
    data = {
        '@context': 'https://schema.org',
        '@type': 'Menu',
        '@id': SITE + 'menu.html#menu',
        'name': "Zhang's Bistro 川味张 Menu",
        'url': SITE + 'menu.html',
        'inLanguage': ['en', 'zh'],
        'hasMenuSection': sections,
    }
    return '<script type="application/ld+json">\n' + json.dumps(data, ensure_ascii=False, indent=1) + '\n</script>'


def splice(page, start, end, content):
    head, rest = page.split(start)
    _, tail = rest.split(end)
    return head + start + '\n' + content + '\n' + end + tail


with open('menu.json', encoding='utf-8') as f:
    categories = json.load(f)

photos, _ = photo_plan(categories)

blocks = []
for cat in categories:
    items = ''.join(item_html(it, photos.get(it['name'])) for it in cat['items'])
    blocks.append(
        f'  <div class="menu-category" id="{slug(cat["name"])}">'
        f'<div class="menu-category-head"><span>{escape(cat["name"], quote=False)}</span>'
        f'<span class="cn">{CATEGORY_CN[cat["name"]]}</span></div>'
        f'<div class="menu-item-list">{items}</div></div>'
    )

with open(MENU_HTML, encoding='utf-8') as f:
    page = f.read()

page = splice(page, '<!-- MENU:START -->', '<!-- MENU:END -->', '\n\n'.join(blocks))
page = splice(page, '<!-- MENU-LD:START -->', '<!-- MENU-LD:END -->', menu_ld(categories, photos))

with open(MENU_HTML, 'w', encoding='utf-8', newline='\n') as f:
    f.write(page)

print('Wrote', len(blocks), 'categories,', sum(len(c['items']) for c in categories), 'items,',
      len(photos), 'with photos')
