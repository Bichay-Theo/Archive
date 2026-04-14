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
    # البحث عن المجلد بغض النظر عن حالة الأحرف
    possible_paths = ["Public_Articles", "public_articles", "articles"]
    target_path = None
    
    for p in possible_paths:
        if os.path.exists(p):
            target_path = p
            break
            
    if not target_path:
        print(f"❌ خَطَأٌ سِيَادِيٌّ: لَمْ نَجِدْ مُجَلَّدَ المَقَالَاتِ. المُلَجَّدَاتُ المَوْجُودَةُ هِيَ: {os.listdir('.')}")
        return None

    # رادار الملفات: البحث عن أي ملف ينتهي بـ html أو htm وبغض النظر عن حالة الأحرف
    all_files = os.listdir(target_path)
    print(f"🔍 الرَّادَارُ وَجَدَ هَذِهِ المَلَفَّاتِ فِي {target_path}: {all_files}")
    
    articles = [f for f in all_files if f.lower().endswith(('.html', '.htm')) and f.lower() != 'index.html']
    
    if not articles:
        print("❌ لَمْ نَجِدْ مَلَفَّاتِ HTML صَالِحَةً (هَلِ المَلَفَّاتُ تَنْتَهِي بـِـ .md مَثَلًا؟)")
        return None
        
    return os.path.join(target_path, random.choice(articles))

def run():
    article_full_path = get_random_article()
    if not article_full_path:
        sys.exit(1)

    article_file = os.path.basename(article_full_path)
    title = article_file.replace(".html", "").replace(".htm", "").replace("_", " ")
    
    # تأكد من أن الرابط يشير للمسار الصحيح على GitHub Pages
    link = f"https://bichay-theo.github.io/Archive/{article_full_path}"
    
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
