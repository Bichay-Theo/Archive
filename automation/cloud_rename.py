import os
import glob

def rename_on_cloud():
    articles_path = "Public_Articles"
    images_path = "assets/images"
    
    # 1. جلب وترتيب المقالات
    articles = sorted([f for f in os.listdir(articles_path) if f.endswith(('.md', '.html')) and f != 'index.html'])
    article_names = [os.path.splitext(f)[0] for f in articles]
    
    # 2. جلب وترتيب الصور الحالية
    images = sorted([f for f in os.listdir(images_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])
    
    if len(article_names) != len(images):
        print(f"⚠️ تحذير: عدد المقالات ({len(article_names)}) لا يطابق عدد الصور ({len(images)})!")
        # سنستمر في التسمية حتى نصل لنهاية القائمة الأقصر
    
    limit = min(len(article_names), len(images))
    
    for i in range(limit):
        old_path = os.path.join(images_path, images[i])
        extension = os.path.splitext(images[i])[1]
        new_name = article_names[i] + extension
        new_path = os.path.join(images_path, new_name)
        
        if old_path != new_path:
            print(f"🔄 إعادة تسمية: {images[i]} -> {new_name}")
            os.rename(old_path, new_path)

if __name__ == "__main__":
    rename_on_cloud()
