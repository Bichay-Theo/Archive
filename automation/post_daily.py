import os
import tweepy
import random
import sys

# 1. دالة جلب عميل X باستخدام المفاتيح السرية
def get_x_client():
    return tweepy.Client(
        consumer_key=os.getenv("X_API_KEY"),
        consumer_secret=os.getenv("X_API_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET")
    )

# 2. دالة اختيار مقال عشوائي من الأرشيف
def get_random_article():
    path = "Public_Articles"
    # التأكد من وجود المجلد أولاً
    if not os.path.exists(path):
        print(f"❌ المجلد {path} غير موجود في المستودع.")
        return None
    
    articles = [f for f in os.listdir(path) if f.endswith('.html') and f != 'index.html']
    return random.choice(articles) if articles else None

# 3. الدالة الرئيسية لتنفيذ عملية النشر
def run():
    article_file = get_random_article()
    if not article_file:
        print("❌ لم يتم العثور على مقالات صالحة للنشر.")
        return

    # تجهيز محتوى التغريدة
    title = article_file.replace(".html", "").replace("_", " ")
    link = f"https://bichay-theo.github.io/Archive/Public_Articles/{article_file}"
    tweet_text = f"مقال اليوم من الأرشيف:\n\n📜 {title}\n\nلقراءة المقال كاملاً:\n{link}"

    try:
        client = get_x_client()
        client.create_tweet(text=tweet_text)
        print(f"✅ تم النشر بنجاح: {title}")
    except Exception as e:
        print(f"❌ خطأ صارخ أثناء النشر: {e}")
        sys.exit(1) # لجعل علامة GitHub Actions تتحول للأحمر عند الفشل

# 4. نقطة انطلاق السكريبت
if __name__ == "__main__":
    run()
