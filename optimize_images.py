# -*- coding: utf-8 -*-
"""Otimiza imagens da raiz: backup -> redimensiona -> comprime. Mantem nomes."""
import os, glob, shutil
from PIL import Image, ImageOps

BASE = os.path.dirname(os.path.abspath(__file__))
BACKUP = os.path.join(BASE, "_img_originais")
os.makedirs(BACKUP, exist_ok=True)

# papel: (lado_maximo, formato)  format: 'jpg' | 'png' | 'png-alpha'
TARGETS = {
    "favicon.png": (64, "png"),
    "logo-splink.png": (400, "png"),
    "logo-splink-v2.png": (400, "png"),
    "Criar_um_foto_profssional_porfavor_202605051827 (1).jpeg": (1080, "jpg"),
    "automacao-whatsapp-splink.png": (1200, "png"),   # og/social
    "google-maps-capa.png": (1024, "png"),
    "fundador-marco-matias-splink.png": (1080, "png-alpha"),
    "image.png": (1280, "png"),
}

def human(n): return f"{n/1024:.0f} KB" if n < 1024*1024 else f"{n/1024/1024:.2f} MB"

files = sorted(glob.glob(os.path.join(BASE, "*.png")) + glob.glob(os.path.join(BASE, "*.jpeg")) + glob.glob(os.path.join(BASE, "*.jpg")))
tot_before = tot_after = 0
for path in files:
    name = os.path.basename(path)
    if name == "_img_originais": continue
    before = os.path.getsize(path)
    tot_before += before
    # backup (so na primeira vez)
    bpath = os.path.join(BACKUP, name)
    if not os.path.exists(bpath):
        shutil.copy2(path, bpath)
    maxside, kind = TARGETS.get(name, (1280, "png-alpha" if name.endswith(".png") else "jpg"))
    im = Image.open(path)
    im = ImageOps.exif_transpose(im)
    # redimensiona mantendo proporcao
    if max(im.size) > maxside:
        im.thumbnail((maxside, maxside), Image.LANCZOS)
    if kind == "jpg":
        im = im.convert("RGB")
        im.save(path, "JPEG", quality=82, optimize=True, progressive=True)
    elif kind == "png-alpha":
        im = im.convert("RGBA")
        q = im.quantize(colors=256, method=Image.Quantize.FASTOCTREE)
        q.save(path, "PNG", optimize=True)
    else:  # png (sem alpha)
        im = im.convert("RGB")
        q = im.quantize(colors=256, method=Image.Quantize.MEDIANCUT)
        q.save(path, "PNG", optimize=True)
    after = os.path.getsize(path)
    tot_after += after
    print(f"{name:48} {human(before):>9} -> {human(after):>9}  (-{100*(before-after)//before}%)")

print("-"*80)
print(f"TOTAL imagens: {human(tot_before)} -> {human(tot_after)}  (-{100*(tot_before-tot_after)//tot_before}%)")
