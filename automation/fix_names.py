import os, re, sys

def slugify(text):
    """تـَحـوِيـلُ الـعـَنـاوِيـنِ الـعـَرَبـِيـَّةِ لـِأَسـمـاءٍ لَاتـِيـنـِيـَّةٍ تـَقـْنـِيـَّة"""
    mapping = {
        "إكليسيا": "ecclesia",
        "أغابي_وفيلو": "agape-philo",
        "أغابي وفيلو": "agape-philo",
        "الرمزية_في_رسالة_العبرانيين": "hebrews-typology",
        "الرمزية في رسالة العبرانيين": "hebrews-typology",
        "الوحش": "the-beast"
    }
    
    # اسـتـخـلاصُ الاسـمِ وتـنـظـيـفـُه مـن الـنـُّقـاطِ الـزائـِدَة
    base = os.path.splitext(text)[0].strip().strip('.')
    if base in mapping: return mapping[base]
    
    # تـَحـوِيـلٌ عـَامٌّ لـِلـمـَقـالاتِ الأخـرَى
    slug = re.sub(r'[^\w\s-]', '', base).strip().lower()
    slug = re.sub(r'[-\s_]+', '-', slug)
    return slug[:50] if slug else "article"

def fix_all():
    print("🚀 Starting Archive Sanitization Protocol...")
    
    # 1. تـَصـحـِيـحُ الـمـَقـالات
    art_path = "Public_Articles"
    if os.path.exists(art_path):
        for f in os.listdir(art_path):
            if f.startswith('.') and f != ".md": continue
            old_path = os.path.join(art_path, f)
            
            # مـُعـالـَجـَة الـمـَلـَفِّ الـذي لَا اسـمَ لـَه
            name = "hebrews-typology" if f == ".md" else slugify(f)
            new_name = f"{name}.html"
            new_path = os.path.join(art_path, new_name)
            
            if old_path != new_path:
                print(f"📦 Article: {f} -> {new_name}")
                os.rename(old_path, new_path)
    else:
        print(f"❌ Error: {art_path} missing.")
        sys.exit(1)

    # 2. تـَصـحـِيـحُ الـصـُّوَر
    img_path = "assets/images"
    if os.path.exists(img_path):
        for f in os.listdir(img_path):
            if f.startswith('.') or not f.lower().endswith(('.jpg', '.png', '.jpeg', '.webp')): 
                continue
            old_path = os.path.join(img_path, f)
            ext = os.path.splitext(f)[1]
            new_name = f"{slugify(f)}{ext}"
            new_path = os.path.join(img_path, new_name)
            
            if old_path != new_path:
                print(f"🖼️ Image: {f} -> {new_name}")
                os.rename(old_path, new_path)

if __name__ == "__main__":
    try:
        fix_all()
        print("✨ Protocol finished successfully.")
    except Exception as e:
        print(f"💥 CRITICAL ERROR: {str(e)}")
        sys.exit(1)
