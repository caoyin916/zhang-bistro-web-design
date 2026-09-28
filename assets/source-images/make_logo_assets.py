import numpy as np
from PIL import Image

SRC = '../../logo/logo.png'
OUT = '../img/'

rgb = np.asarray(Image.open(SRC).convert('RGB')).astype(np.float64)

# Color-to-alpha against white: keeps anti-aliased edges and exact ink colors.
alpha = (255.0 - rgb).max(axis=2) / 255.0
alpha[alpha < 0.03] = 0.0
safe = np.where(alpha > 0, alpha, 1.0)[..., None]
color = (rgb - (1.0 - alpha[..., None]) * 255.0) / safe
color = np.clip(color, 0, 255)
rgba = np.dstack([color, alpha * 255.0]).round().astype(np.uint8)
logo = Image.fromarray(rgba, 'RGBA')

PAD = 12
MARK_BOX = (354 - PAD, 110 - PAD, 949 + PAD, 708 + PAD)
FULL_BOX = (232 - PAD, 110 - PAD, 1020 + PAD, 1120 + PAD)


def fit(im, *, width=None, height=None):
    w, h = im.size
    if width:
        return im.resize((width, round(h * width / w)), Image.LANCZOS)
    return im.resize((round(w * height / h), height), Image.LANCZOS)


mark = logo.crop(MARK_BOX)
full = logo.crop(FULL_BOX)

fit(mark, height=240).save(OUT + 'logo-mark.png', optimize=True)
fit(full, width=560).save(OUT + 'logo-full.png', optimize=True)

square = Image.new('RGBA', (max(mark.size),) * 2, (0, 0, 0, 0))
square.paste(mark, ((square.width - mark.width) // 2, (square.height - mark.height) // 2), mark)
square.resize((64, 64), Image.LANCZOS).save(OUT + 'favicon.png', optimize=True)

touch = Image.new('RGBA', (180, 180), (251, 241, 225, 255))
icon = square.resize((150, 150), Image.LANCZOS)
touch.paste(icon, (15, 15), icon)
touch.convert('RGB').save(OUT + 'apple-touch-icon.png', optimize=True)

for name in ('logo-mark.png', 'logo-full.png', 'favicon.png', 'apple-touch-icon.png'):
    print(name, Image.open(OUT + name).size)
