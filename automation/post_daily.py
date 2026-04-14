import os
import tweepy
import sys
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
    
    # جلب كافة المقالات
    articles = [os.path.join(path, f) for f in os.listdir(path) 
                if f.lower().endswith(('.html', '.htm', '.md')) and f.lower() != 'index.html']
    
    if not articles: return None

    # الترتيب الزمني التصاعدي (من الأقدم إلى الأحدث)
    articles.sort(key=lambda x: os.path.getmtime(x), reverse=False)
    
    # معادلة "سيد الزمن": اختيار المقال بناءً على رقم اليوم في السنة
    # هذا يضمن أننا ننتقل للمقال التالي كل يوم بالتسلسل
    day_of_year = datetime.now().timetuple().tm_yday
    index = day_of_year % len(articles)
    
    return articles[index]

def run():
    article_full_path = get_article_by_order()
    if not article_full_path:
        print("❌ لم يتم العثور على مقالات.")
        sys.exit(1)

    article_file = os.path.basename(article_full_path)
    # تنظيف العنوان
    title = article_file.replace(".html", "").replace(".htm", "").replace(".md", "").replace("_", " ")
    
    # تصحيح الرابط: GitHub Pages غالباً ما يحول المسافات لشرطات والرموز لروابط نظيفة
    # سنبقي على المسار الحالي مع التأكد من الامتداد
    web_path = article_full_path.replace(".md", ".html")
    link = f"https://bichay-theo.github.io/Archive/{web_path}"
    
    tweet_text = f"من كنوز الأرشيف اليوم:\n\n📜 {title}\n\nلقراءة المقال كاملاً:\n{link}"

    try:
        client = get_x_client()
        client.create_tweet(text=tweet_text)
        print(f"✅ تم نشر المقال (بناءً على الترتيب الزمني): {title}")
    except Exception as e:
        print(f"❌ خطأ في التواصل مع X: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
