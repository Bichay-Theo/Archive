import os
import tweepy
import sys
import urllib.parse
from datetime import datetime

def get_x_client():
    return tweepy.Client(
        consumer_key=os.getenv("X_API_KEY").strip(),
        consumer_secret=os.getenv("X_API_SECRET").strip(),
        access_token=os.getenv("X_ACCESS_TOKEN").strip(),
        access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET").strip()
    )

def get_article_by_order():
    path = "Public_Articles"
    if not os.path.exists(path): return None
    
    # جلب كافة المقالات التي تنتهي بـ html أو md
    articles = [f for f in os.listdir(path) 
                if f.lower().endswith(('.html', '.htm', '.md')) and f.lower() != 'index.html']
    
    if not articles: return None

    # الترتيب الأبجدي الصارم (لضمان البداية من أول مقال في السلسلة)
    articles.sort()
    
    # اختيار المقال بناءً على رقم اليوم في السنة (0-indexed)
    # هذا يضمن التنقل بين المقالات يومياً بالتسلسل
    day_index = (datetime.now().timetuple().tm_yday - 1) % len(articles)
    
    return os.path.join(path, articles[day_index])

def run():
    article_full_path = get_article_by_order()
    if not article_full_path:
        print("❌ لم يتم العثور على مقالات.")
        sys.exit(1)

    article_file = os.path.basename(article_full_path)
    # تنظيف العنوان للعرض في التغريدة
    title = article_file.replace(".html", "").replace(".htm", "").replace(".md", "").replace("_", " ")
    
    # تحويل المسار ليكون متوافقاً مع الويب (تغيير md لـ html)
    web_path = article_full_path.replace(".md", ".html")
    
    # الخطوة السيادية: تشفير الحروف العربية في الرابط ليقبله المتصفح كاملاً
    # هذا سيمنع الرابط من التوقف عند المجلد ويجبره على فتح المقال
    encoded_path = urllib.parse.quote(web_path)
    link = f"https://bichay-theo.github.io/Archive/{encoded_path}"
    
    tweet_text = f"من كنوز الأرشيف اليوم:\n\n📜 {title}\n\nلقراءة المقال كاملاً:\n{link}"

    try:
        client = get_x_client()
        client.create_tweet(text=tweet_text)
        print(f"✅ تم بنجاح نشر المقال: {title}")
        print(f"🔗 الرابط المشفر: {link}")
    except Exception as e:
        print(f"❌ خطأ في التواصل مع X: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
