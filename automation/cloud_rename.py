import os

def rename_on_cloud():
    articles_path = "Public_Articles"
    images_path = "assets/images"
    
    os.makedirs(images_path, exist_ok=True)
    if not os.path.exists(articles_path):
        print("❌ مجلد المقالات غير موجود.")
        return

    # 🛡️ بـُروتوكولُ الـتـَّحـصـِيـن: جـَلـبُ الـمـَقـالاتِ الـتـِي تـَمـلـِكُ اسـمـاً حـَقـِيـقـِيـّاً فـَقـَط
    # نـَسـتـثـنـِي أَيَّ مـَلـَفٍّ يـَبـدَأُ بـِـنـُقـطـَةٍ (مـِثـل .md)
    articles = sorted([f for f in os.listdir(articles_path) 
                      if f.endswith(('.md', '.html')) and not f.startswith('.')])
    
    article_names = [os.path.splitext(f)[0] for f in articles]
    
    # جـَلـبُ الـصـُّوَرِ مـَعَ اسـتـِثـنـاءِ الـمـَلـَفـاتِ الـخـَفـِيـَّة
    images = sorted([f for f in os.listdir(images_path) 
                    if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp')) and not f.startswith('.')])
    
    if not images:
        print("ℹ️ لا توجد صور حقيقية للمعالجة.")
        return

    limit = min(len(article_names), len(images))
    for i in range(limit):
        old_path = os.path.join(images_path, images[i])
        extension = os.path.splitext(images[i])[1]
        
        # تـَأكـِيـدُ أنَّ الاسـمَ الـجـَدِيـدَ لـَيـسَ فـَارِغـاً
        if not article_names[i]: continue
        
        new_name = f"{article_names[i]}{extension}"
        new_path = os.path.join(images_path, new_name)
        
        if old_path != new_path:
            print(f"🔄 مـَيْكـَنـَة: {images[i]} -> {new_name}")
            os.rename(old_path, new_path)

if __name__ == "__main__":
    rename_on_cloud()
