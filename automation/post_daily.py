import os
import tweepy
import random
import sys

def get_x_client():
    return tweepy.Client(
        consumer_key=os.getenv("X_API_KEY"),
        consumer_secret=os.getenv("X_API_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET")
    )

def get_random_article():
    # الرادار يبحث في كل الاحتمالات الممكنة للمجلد
    possible_paths = ["Public_Articles", "public_articles", "articles"]
    target_path = None
    
    for p in possible_paths:
        if os.path.exists(p):
            target_path = p
            break
            
    if not target_path:
        print(f"❌ لم نجد مجلد المقالات. المجلدات الحالية: {os.listdir('.')}")
        return None

    all_files = os.listdir(target_path)
    
    # التحديث السيادي: البحث عن ملفات .html و .md معاً
    articles = [f for f in all_files if f.lower().endswith(('.html', '.htm', '.md')) and f.lower() != 'index.html']
    
    if not articles:
        print(f"❌ المجلد {target_path} لا يحتوي على مقالات صالحة.")
        return None
        
    return os.path.join(target_path, random.choice(articles))

def run():
    article_full_path = get_random_article()
    if not article_full_path:
        sys.exit(1)

    article_file = os.path.basename(article_full_path)
    
    # تنظيف العنوان من الامتدادات والرموز
    title = article_file.replace(".html", "").replace(".htm", "").replace(".md", "").replace("_", " ")
    
    # معالجة الرابط: إذا كان الملف .md، نحوله في الرابط إلى .html لأن جيت هاب يعرضه هكذا
    web_path = article_full_path.replace(".md", ".html")
    link = f"https://bichay-theo.github.io/Archive/{web_path}"
    
    tweet_text = f"مقال اليوم من الأرشيف:\n\n📜 {title}\n\nلقراءة المقال كاملاً:\n{link}"

    try:
        client = get_x_client()
        client.create_tweet(text=tweet_text)
        print(f"✅ تم النشر بنجاح ساحق: {title}")
    except Exception as e:
        print(f"❌ خطأ في التواصل مع X: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
