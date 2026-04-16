import os

def fix_article_names():
    path = "Public_Articles"
    if not os.path.exists(path): return

    for file in os.listdir(path):
        old_path = os.path.join(path, file)
        
        # 1. تـَصـحـِيـحُ الـمـَلـَفِّ الـذي لَا اسـمَ لـَه
        if file == ".md":
            new_name = "الرمزية_في_رسالة_العبرانيين.html"
            os.rename(old_path, os.path.join(path, new_name))
            print(f"✅ Fixed hidden file: {new_name}")
            
        # 2. تـَحـويـلُ كـافـَّةِ الـمـَلـَفـاتِ لـِتـَنـسـِيـقِ HTML لـِضـَمـانِ الـرَّوابـِط
        elif file.endswith(".md"):
            new_name = file.replace(".md", ".html")
            os.rename(old_path, os.path.join(path, new_name))
            print(f"✅ Converted to HTML: {new_name}")

if __name__ == "__main__":
    fix_article_names()
