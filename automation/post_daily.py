import os
import tweepy
import sys
import urllib.parse
from datetime import datetime

# الـمـَسـَارُ الـمـُعـْتـَمـَد
IMAGE_FOLDER = "assets/images"

def get_x_auth():
    api_key = os.getenv("X_API_KEY", "").strip()
    api_secret = os.getenv("X_API_SECRET", "").strip()
    access_token = os.getenv("X_ACCESS_TOKEN", "").strip()
    access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET", "").strip()
    
    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    return tweepy.API(auth), tweepy.Client(
        consumer_key=api_key, consumer_secret=api_secret,
        access_token=access_token, access_token_secret=access_token_secret
    )

def find_article_image(article_filename):
    """بـُروتوكولُ بـَحـثٍ يـَدعـَمُ الـتـَّرمـِيـزَ الـعـَرَبـِي"""
    base_name = os.path.splitext(article_filename)[0]
    if not os.path.exists(IMAGE_FOLDER): return None
    
    # مـَسـحُ كـافـَّةِ الـمـَلـَفـَاتِ لـِضـَمـانِ الـتـَّطـابـُقِ الـنـَّصـِّي
    for f in os.listdir(IMAGE_FOLDER):
        if os.path.splitext(f)[0] == base_name:
            return os.path.join(IMAGE_FOLDER, f)
    return None

def run():
    path = "Public_Articles"
    articles = sorted([f for f in os.listdir(path) if f.endswith(('.html', '.md')) and f != 'index.html'])
    
    if not articles:
        print("❌ لا يوجد مقالات.")
        return

    day_index = (datetime.now().timetuple().tm_yday - 1) % len(articles)
    article_file = articles[day_index]
    title = os.path.splitext(article_file)[0].replace("_", " ")
    
    # تـَشـفـِيـرُ الـرَّابـِطِ لـِلـمـُتـَصـَفـَّح
    encoded_file = urllib.parse.quote(article_file)
    link = f"https://bichay-theo.github.io/Archive/Public_Articles/{encoded_file}"
    
    tweet_text = f"من كنوز الأرشيف اليوم:\n\n📜 {title}\n\nلقراءة المقال كاملاً:\n{link}"

    try:
        api_v1, client_v2 = get_x_auth()
        image_path = find_article_image(article_file)
        
        if image_path and os.path.exists(image_path):
            print(f"🔍 صـُورةٌ مـُرصـَدَة: {image_path}")
            # الـتـَّأكـُّد مـن قـابـلـِيـَةِ قـِراءَةِ الـمـَلـَف
            media = api_v1.media_upload(filename=image_path)
            client_v2.create_tweet(text=tweet_text, media_ids=[media.media_id])
            print("✅ تـَمـَّتِ الـتـَّغـرِيـدةُ مـَعَ الـصـُّورَة.")
        else:
            print("⚠️ لـَم يـَتـَمـَكـَّن الـنـِّظـامُ مـن رَصـدِ الـصـُّورَة، جـَارٍ الـنـَّشـرُ نـَصـِّيـّاً...")
            client_v2.create_tweet(text=tweet_text)
            print("✅ تـَمـَّتِ الـتـَّغـرِيـدةُ نـَصـِّيـّاً.")
            
    except Exception as e:
        print(f"❌ فـَشـَلٌ فـِي الـبـُروتوكول: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run()
