import json
import os
import sys
from PIL import Image, ImageOps, ImageDraw
from menu_photos import GBP_DIR, OUT_DIR, FOCAL_Y, photo_plan

W, H = 800, 600


def crop_43(im, fy):
    w, h = im.size
    if w / h > 4 / 3:
        cw, ch = round(h * 4 / 3), h
    else:
        cw, ch = w, round(w * 3 / 4)
    left = (w - cw) // 2
    top = min(max(round(fy * h - ch / 2), 0), h - ch)
    return im.crop((left, top, left + cw, top + ch))


with open('menu.json', encoding='utf-8') as f:
    categories = json.load(f)

dish_to_url, files = photo_plan(categories)
os.makedirs(OUT_DIR, exist_ok=True)

for filename, (stem, slug) in files.items():
    out = OUT_DIR + slug + '.jpg'
    if os.path.exists(out):
        continue
    im = ImageOps.exif_transpose(Image.open(GBP_DIR + filename)).convert('RGB')
    im = crop_43(im, FOCAL_Y.get(stem, 0.5)).resize((W, H), Image.LANCZOS)
    im.save(out, 'JPEG', quality=80, optimize=True, progressive=True)

total = sum(len(c['items']) for c in categories)
print(f'{len(files)} photos for {len(dish_to_url)} of {total} dishes')

# Optional contact sheet for a visual label check: python make_menu_photos.py --sheet
if '--sheet' in sys.argv:
    tiles = sorted(set(dish_to_url.values()))
    names = {}
    for en, url in dish_to_url.items():
        names.setdefault(url, en)
    cols, tw, th = 8, 220, 190
    sheet = Image.new('RGB', (cols * tw, ((len(tiles) + cols - 1) // cols) * th), 'white')
    draw = ImageDraw.Draw(sheet)
    for i, url in enumerate(tiles):
        im = Image.open('../../' + url)
        im.thumbnail((tw - 10, 155))
        x, y = (i % cols) * tw, (i // cols) * th
        sheet.paste(im, (x + 5, y + 2))
        draw.text((x + 5, y + 162), names[url][:32], fill='black')
    sheet.save(os.path.join(os.environ['TEMP'], 'zb-preview', 'menu-photos.jpg'), quality=85)
