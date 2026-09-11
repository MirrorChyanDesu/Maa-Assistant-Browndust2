# -*- coding: utf-8 -*-
"""从源图生成多尺寸 .ico（用于 mxu.exe / launcher 图标）。
先用预览确认裁剪构图，再加 --final 输出最终 ico。"""
import sys, os
from PIL import Image, ImageDraw

SRC = r"C:\Users\ALKAID\.workbuddy\clipboard-images\clipboard-2026-09-11T07-37-48-826Z-e8e1c192.jpg"
CACHE = r"F:\BD2MAA\cache"
ROOT = r"F:\BD2MAA"

# 裁剪框：聚焦角色头部/面部，避开左侧蓝色人物与右下角水印
BOX = (322, 38, 678, 394)      # 400x400
RADIUS_RATIO = 0.16            # 圆角比例（0 = 直角）

def rounded(img, ratio):
    w, h = img.size
    r = int(min(w, h) * ratio)
    if r <= 0:
        return img
    mask = Image.new("L", (w, h), 0)
    d = ImageDraw.Draw(mask)
    d.rounded_rectangle([0, 0, w - 1, h - 1], radius=r, fill=255)
    out = img.convert("RGBA")
    out.putalpha(mask)
    return out

def main():
    final = "--final" in sys.argv
    im = Image.open(SRC).convert("RGB")
    print("SRC_SIZE", im.size)
    crop = im.crop(BOX)
    # 预览：256 圆角
    prev = rounded(crop.resize((256, 256), Image.LANCZOS), RADIUS_RATIO)
    prev_path = os.path.join(CACHE, "_icon_preview.png")
    prev.save(prev_path)
    print("PREVIEW", prev_path, "BOX", BOX)

    if final:
        sizes = [16, 20, 24, 32, 40, 48, 64, 96, 128, 256]
        # 基准 256 圆角图，逐尺寸重采样（保持圆角干净）
        base = rounded(crop.resize((256, 256), Image.LANCZOS), RADIUS_RATIO)
        frames = []
        for s in sizes:
            f = base.resize((s, s), Image.LANCZOS)
            frames.append(f)
        ico = os.path.join(ROOT, "mxu.ico")
        base.save(ico, format="ICO", sizes=[(s, s) for s in sizes])
        print("ICO", ico, os.path.getsize(ico))
        png = os.path.join(ROOT, "mxu_icon.png")
        base.save(png)
        print("PNG", png)

if __name__ == "__main__":
    main()
