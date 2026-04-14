import os
import tweepy
import random
import sys

def get_x_client():
    # استدعاء المفاتيح مع تنظيف آلي
    keys = {
        "X_API_KEY": os.getenv("X_API_KEY", "").strip(),
        "X_API_SECRET": os.getenv("X_API_SECRET", "").strip(),
        "X_ACCESS_TOKEN": os.getenv("X_ACCESS_TOKEN", "").strip(),
        "X_ACCESS_TOKEN_SECRET": os.getenv("X_ACCESS_TOKEN_SECRET", "").strip()
    }

    # الرادار: يخبرنا أي مفتاح مفقود بالضبط
    for name, value in keys.items():
        if not value:
            print(f"❌ تـَنـبـِيـه سِـيَادِي: المِفتاح [{name}] غـَيرُ مـَوجـودٍ فـي إعدادات GitHub.")
            sys.exit(1)

    return tweepy.Client(
        consumer_key=keys["X_API_KEY"],
        consumer_secret=keys["X_API_SECRET"],
        access_token=keys["X_ACCESS_TOKEN"],
        access_token_secret=keys["X_ACCESS_TOKEN_SECRET"]
    )

def get_random_article():
    path = "Public_Articles"
    if not os.path.exists(path): return None
    articles = [f for f in os.listdir(path) if f.lower().endswith(('.html', '.htm', '.md')) and f.lower() != 'index.html']
    return os.path.join(path, random.choice(articles)) if articles else None

def run():
    article_full_path = get_random_article()
    if not article_full_path:
        print("❌ لم يتم العثور على مقالات.")
        sys.exit(1)

    article_file = os.path.basename(article_full_path)
    title = article_file.replace(".html", "").replace(".htm", "").replace(".md", "").replace("_", " ")
    web_path = article_full_path.replace(".md", ".html")
    link = f"https://bichay-theo.github.io/Archive/{web_path}"
    tweet_text = f"مقال اليوم من الأرشيف:\n\n📜 {title}\n\nلقراءة المقال كاملاً:\n{link}"

    try:
        client = get_x_client()
        client.create_tweet(text=tweet_text)
        print(f"✅ تَمَّ النَّشْرُ بـِـنَجَاحٍ سَاحِقٍ: {title}")
    except Exception as e:
        print(f"❌ خَطَأٌ فِي التَّواصُلِ مَعَ X: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
