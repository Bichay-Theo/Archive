import os
import tweepy
import random
import sys

def get_x_client():
    # استدعاء المفاتيح مع تنظيف آلي لأي فراغات مخفية
    api_key = os.getenv("nMrZgehraDWDPb3lvadMzARvR", "").strip()
    api_secret = os.getenv("EjIROfsex95sfhSLDupCb4AFwiNxuDtSR7L79kYnIDK0s9iy6i", "").strip()
    access_token = os.getenv("1601075372606513154-DgUxhiSLSu4ZbqT9fXJpKyYlLdfSjg", "").strip()
    access_token_secret = os.getenv("UMVNHbW6Llm56feTfVF54Lroyr9WnDvftlchDZ9iQZYUa", "").strip()

    # التأكد من وجود كافة المفاتيح
    if not all([api_key, api_secret, access_token, access_token_secret]):
        print("❌ خطأ: أحد مفاتيح API مفقود في إعدادات GitHub Secrets.")
        sys.exit(1)

    return tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

def get_random_article():
    possible_paths = ["Public_Articles", "public_articles", "articles"]
    target_path = next((p for p in possible_paths if os.path.exists(p)), None)
    
    if not target_path:
        print(f"❌ لم نجد مجلد المقالات. الموجود: {os.listdir('.')}")
        return None

    all_files = os.listdir(target_path)
    # القناص: يبحث عن ملفات html أو md
    articles = [f for f in all_files if f.lower().endswith(('.html', '.htm', '.md')) and f.lower() != 'index.html']
    
    if not articles:
        print(f"❌ المجلد {target_path} فارغ من المقالات الصالحة.")
        return None
        
    return os.path.join(target_path, random.choice(articles))

def run():
    article_full_path = get_random_article()
    if not article_full_path:
        sys.exit(1)

    article_file = os.path.basename(article_full_path)
    # تنظيف العنوان
    title = article_file.replace(".html", "").replace(".htm", "").replace(".md", "").replace("_", " ")
    
    # تحويل الرابط ليتوافق مع GitHub Pages (Markdown إلى HTML)
    web_path = article_full_path.replace(".md", ".html")
    link = f"https://bichay-theo.github.io/Archive/{web_path}"
    
    tweet_text = f"مقال اليوم من الأرشيف:\n\n📜 {title}\n\nلقراءة المقال كاملاً:\n{link}"

    try:
        client = get_x_client()
        # محاولة النشر الرسمية
        client.create_tweet(text=tweet_text)
        print(f"✅ تم النشر بنجاح سيادي: {title}")
    except Exception as e:
        print(f"❌ فشل الاتصال بـ X (خطأ 401 أو 403): {e}")
        print("💡 نصيحة: تأكد من تحديث الأسرار في GitHub بالمفاتيح الجديدة كلياً.")
        sys.exit(1)

if __name__ == "__main__":
    run()
