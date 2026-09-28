# Regenerates the category blocks in ../../menu.html between the MENU:START / MENU:END markers.
import json, re
from html import escape

MENU_HTML = '../../menu.html'
START, END = '<!-- MENU:START -->', '<!-- MENU:END -->'

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


def item_html(item):
    flags = ''
    cls = 'menu-item'
    if item['popular']:
        flags += '<span class="pop-flag">Popular</span>'
    if item['soldOut']:
        flags += '<span class="soldout-flag">Sold Out</span>'
        cls += ' is-sold-out'
    return (
        f'<div class="{cls}"><span class="menu-item-name">'
        f'<span class="menu-item-en">{escape(item["name"], quote=False)}{flags}</span>'
        f'<span class="menu-item-cn cn">{item["cn"]}</span>'
        f'</span><span class="menu-item-price">{item["price"]}</span></div>'
    )


with open('menu.json', encoding='utf-8') as f:
    categories = json.load(f)

blocks = []
for cat in categories:
    items = ''.join(item_html(it) for it in cat['items'])
    blocks.append(
        f'  <div class="menu-category" id="{slug(cat["name"])}">'
        f'<div class="menu-category-head"><span>{escape(cat["name"], quote=False)}</span>'
        f'<span class="cn">{CATEGORY_CN[cat["name"]]}</span></div>'
        f'<div class="menu-item-list">{items}</div></div>'
    )

with open(MENU_HTML, encoding='utf-8') as f:
    page = f.read()

head, rest = page.split(START)
_, tail = rest.split(END)
page = head + START + '\n' + '\n\n'.join(blocks) + '\n' + END + tail

with open(MENU_HTML, 'w', encoding='utf-8', newline='\n') as f:
    f.write(page)

print('Wrote', len(blocks), 'categories,', sum(len(c['items']) for c in categories), 'items')
