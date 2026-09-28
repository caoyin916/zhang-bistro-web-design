import os
from PIL import Image, ImageOps

SRC = '../../gbp-photo/'
OUT = '../img/dishes/'
os.makedirs(OUT, exist_ok=True)

# (source file, output name, focal x, focal y) — focal point is kept centered in the 4:3 crop.
JOBS = [
    ('麻婆豆腐.jpg', 'mapo-tofu.jpg', 0.45, 0.5),
    ('辣子鸡.jpg', 'chongqing-spicy-chicken.jpg', 0.5, 0.5),
    ('孜然羊.png', 'cumin-lamb.jpg', 0.5, 0.5),
    ('小炒肉.jpg', 'hunan-stir-fried-pork.jpg', 0.5, 0.5),
    ('水煮牛.JPG', 'spicy-boiled-beef.jpg', 0.5, 0.64),
    ('香辣鱼片.jpg', 'spicy-fish-fillet.jpg', 0.5, 0.6),
    ('干煸四季豆.jpg', 'dry-fried-green-beans.jpg', 0.5, 0.5),
    ('左宗鸡.jpg', 'general-tsos-chicken.jpg', 0.5, 0.56),
]


def crop_43(im, fx, fy):
    w, h = im.size
    if w / h > 4 / 3:
        cw, ch = round(h * 4 / 3), h
    else:
        cw, ch = w, round(w * 3 / 4)
    left = min(max(round(fx * w - cw / 2), 0), w - cw)
    top = min(max(round(fy * h - ch / 2), 0), h - ch)
    return im.crop((left, top, left + cw, top + ch))


for src, out, fx, fy in JOBS:
    im = ImageOps.exif_transpose(Image.open(SRC + src)).convert('RGB')
    im = crop_43(im, fx, fy).resize((1000, 750), Image.LANCZOS)
    im.save(OUT + out, 'JPEG', quality=82, optimize=True, progressive=True)
    print(out, os.path.getsize(OUT + out) // 1024, 'KB')
