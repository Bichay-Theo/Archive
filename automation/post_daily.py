import os
import tweepy
import random

# جلب المفاتيح من بيئة عمل جيت هاب (التي سنضبطها لاحقاً)
def get_x_client():
    return tweepy.Client(
        consumer_key=os.getenv("X_API_KEY"),
        consumer_secret=os.getenv("X_API_SECRET"),
        access_token=os.getenv("X_ACCESS_TOKEN"),
        access_token_secret=os.getenv("X_ACCESS_TOKEN_SECRET")
    )

def get_random_article():
    path = "Public_Articles"
    articles = [f for f in os.listdir(path) if f.endswith('.html') and f != 'index.html']
    if not articles:
        return None
    return random.choice(articles)

def run():
    article_file = get_random_article()
    if not article_file:
        print("لم يتم العثور على مقالات.")
        return

    title = article_file.replace(".html", "").replace("_", " ")
    link = f"https://bichay-theo.github.io/Archive/Public_Articles/{article_file}"
    
    # صياغة المنشور بوقار وبساطة
    tweet_text = f"مقال اليوم من الأرشيف:\n\n📜 {title}\n\nلقراءة المقال كاملاً:\n{link}"

    try:
        client = get_x_client()
        client.create_tweet(text=tweet_text)
        print(f"تم النشر بنجاح: {title}")
    except Exception as e:
        print(f"خطأ أثناء النشر: {e}")

if __name__ == "__main__":
    run()
