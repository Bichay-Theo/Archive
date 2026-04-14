import os
import tweepy
import random
import sys

def get_x_client():
    return tweepy.Client(
        consumer_key=os.getenv("X_API_KEY").strip(),
        consumer_secret=os.getenv("X_API_SECRET").strip(),
        access_token=os.getenv("X_ACCESS_TOKEN").strip(),
        access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET").strip()
    )

def get_latest_article():
    path = "Public_Articles"
    if not os.path.exists(path): return None
    
    # جلب قائمة الملفات مع استبعاد index.html
    articles = [os.path.join(path, f) for f in os.listdir(path) 
                if f.lower().endswith(('.html', '.htm', '.md')) and f.lower() != 'index.html']
    
    if not articles: return None

    # التعديل السيادي: ترتيب المقالات حسب تاريخ التعديل (الأحدث أولاً)
    articles.sort(key=lambda x: os.path.getmtime(x), reverse=True)
    
    # سنقوم بنشر أحدث مقال تمت إضافته للأرشيف
    return articles[0]

def run():
    article_full_path = get_latest_article()
    if not article_full_path:
        print("❌ لم يتم العثور على مقالات.")
        sys.exit(1)

    article_file = os.path.basename(article_full_path)
    title = article_file.replace(".html", "").replace(".htm", "").replace(".md", "").replace("_", " ")
    
    # تعديل الرابط ليتوافق مع بنية Jekyll (سنحذف Public_Articles إذا كان الموقع لا يستخدمها في الروابط)
    # ملاحظة: إذا كان الرابط لا يزال يفتح الخزانة، سنقوم بتعديل هذا السطر بعد تزويدنا برابط عينة
    web_path = article_full_path.replace(".md", ".html")
    link = f"https://bichay-theo.github.io/Archive/{web_path}"
    
    tweet_text = f"جديد الأرشيف اليوم:\n\n📜 {title}\n\nلقراءة المقال كاملاً:\n{link}"

    try:
        client = get_x_client()
        client.create_tweet(text=tweet_text)
        print(f"✅ تم نشر أحدث مقال بنجاح: {title}")
    except Exception as e:
        print(f"❌ خطأ في التواصل مع X: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
