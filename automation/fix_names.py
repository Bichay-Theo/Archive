import os, re

def slugify(text):
    # مـُحـَرِّكُ الـتـَّحـوِيـلِ لِأَسـمـَاءٍ تـِقـنـِيـَّةٍ بـَسـِيـطـَة
    mapping = {
        "إكليسيا": "ecclesia",
        "أغابي_وفيلو": "agape-philo",
        "الرمزية_في_رسالة_العبرانيين": "hebrews-typology",
        "الوحش": "the-beast"
    }
    base = os.path.splitext(text)[0]
    return mapping.get(base, base.lower().replace(" ", "-"))

def fix_all():
    # 1. تـَصـحـِيـحُ الـمـَقـالات
    path = "Public_Articles"
    for f in os.listdir(path):
        if f.startswith('.') and f != ".md": continue
        old_path = os.path.join(path, f)
        name = "hebrews-typology" if f == ".md" else slugify(f)
        new_name = f"{name}.html"
        os.rename(old_path, os.path.join(path, new_name))
        print(f"✅ Article: {f} -> {new_name}")

    # 2. تـَصـحـِيـحُ الـصـُّوَر
    img_path = "assets/images"
    for f in os.listdir(img_path):
        if f.startswith('.') or not f.lower().endswith(('.jpg', '.png')): continue
        old_path = os.path.join(img_path, f)
        new_name = f"{slugify(f)}{os.path.splitext(f)[1]}"
        os.rename(old_path, os.path.join(img_path, new_name))
        print(f"✅ Image: {f} -> {new_name}")

if __name__ == "__main__": fix_all()
