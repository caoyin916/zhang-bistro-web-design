import os
import re
from cn_names import CN_NAMES

GBP_DIR = '../../gbp-photo/'
OUT_DIR = '../img/menu/'
OUT_URL = 'assets/img/menu/'

# Dishes whose Chinese menu name differs from the GBP filename but whose GBP photo shows that dish.
PHOTO_OVERRIDES = {
    'Half Peking Duck': '烤鸭',
    'Whole Peking Duck': '烤鸭',
    'Stir-Fried Wide Rice Noodles': '乾炒牛河',
    'Sichuan Style Braised Beef Noodle Soup': '牛肉面',
    'Spicy Grilled Live Fish': '烤活鱼',
    'Mala Grilled Live Fish': '烤活鱼',
    'Spicy Grilled Fish': '烤鱼',
    'Mala Grilled Fish': '烤鱼',
}

# Vertical focal point for portrait photos where the dish sits below center.
FOCAL_Y = {
    '水煮牛': 0.64,
    '香辣鱼片': 0.6,
    '左宗鸡': 0.56,
}


def gbp_index():
    return {os.path.splitext(f)[0]: f for f in os.listdir(GBP_DIR)}


def slug(text):
    return re.sub(r'[^a-z0-9]+', '-', text.lower()).strip('-')


def photo_plan(categories):
    """Map each dish name to its web photo URL, and each GBP file to its output slug."""
    files = gbp_index()
    stem_to_slug = {}
    dish_to_url = {}
    for cat in categories:
        for item in cat['items']:
            en = item['name']
            stem = PHOTO_OVERRIDES.get(en) or re.sub(r'（.*?）', '', CN_NAMES[en])
            if stem not in files:
                continue
            stem_to_slug.setdefault(stem, slug(re.sub(r'\(.*?\)', '', en)))
            dish_to_url[en] = OUT_URL + stem_to_slug[stem] + '.jpg'
    return dish_to_url, {files[s]: (s, sl) for s, sl in stem_to_slug.items()}
