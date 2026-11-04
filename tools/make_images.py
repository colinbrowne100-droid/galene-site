#!/usr/bin/env python3
"""Make web images for a product: python3 tools/make_images.py <slug> <source image>
Writes assets/img/products/<slug>.jpg (1200x1200, white, product centred) and <slug>-card.jpg (960x720)."""
import sys, os
from PIL import Image, ImageOps
slug, src = sys.argv[1], sys.argv[2]
out = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'assets', 'img', 'products')
im = Image.open(src); im = ImageOps.exif_transpose(im)
if im.mode in ('RGBA', 'LA', 'P'):
    bg = Image.new('RGB', im.size, 'white'); bg.paste(im.convert('RGBA'), mask=im.convert('RGBA').split()[-1]); im = bg
else: im = im.convert('RGB')
def fit(img, w, h, pad=0.06):
    c = img.copy(); c.thumbnail((int(w*(1-2*pad)), int(h*(1-2*pad))), Image.LANCZOS)
    canvas = Image.new('RGB', (w, h), 'white'); canvas.paste(c, ((w-c.width)//2, (h-c.height)//2)); return canvas
fit(im, 1200, 1200).save(os.path.join(out, f'{slug}.jpg'), quality=86, optimize=True, progressive=True)
fit(im, 960, 720).save(os.path.join(out, f'{slug}-card.jpg'), quality=84, optimize=True, progressive=True)
print('wrote', slug, [os.path.getsize(os.path.join(out, f)) // 1024 for f in (f'{slug}.jpg', f'{slug}-card.jpg')], 'KB')
