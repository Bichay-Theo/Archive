import os
import tweepy
import sys
import urllib.parse
from datetime import datetime

# =============================================================================
# ROBUST DAILY POSTER: ARABIC ENCODING PROTECTION
# =============================================================================

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
    """بـُروتوكولُ رَصـدٍ ذَكـِي يـَتـَجـاهـَلُ تـَعـَقـِيـداتِ الـتـَّرمـِيـز"""
    # نـأخـذ الاسـم الـمـجـرد بـدون امـتـداد (مـثـل: إكـلـيـسـيـا)
    base_target = os.path.splitext(article_filename)[0].strip()
    
    if not os.path.exists(IMAGE_FOLDER):
        print(f"⚠️ Warning: {IMAGE_FOLDER} directory is missing.")
        return None
    
    # مـَسـحُ كـافـَّةِ الـمـَلـَفـَاتِ فـِي الـمـُجـَلـَّدِ لـِلـبـَحـثِ عـَن تـَطـابـُقٍ بـَصـَرِي
    for f in os.listdir(IMAGE_FOLDER):
        current_img_base = os.path.splitext(f)[0].strip()
        # مـُقـارَنـَة بـَسـيـطـَة بـَعـِيـداً عـَن تـَعـَقـِيـدات الـمـَسـارات
        if current_img_base == base_target:
            full_path = os.path.join(IMAGE_FOLDER, f)
            print(f"✅ Image Found: {f}")
            return full_path
            
    print(f"❌ No matching image found for: {base_target}")
    return None

def run():
    path = "Public_Articles"
    # جـَلـبُ الـمـَقـالاتِ بـِتـَرْتـِيـبٍ صـَارِم
    articles = sorted([f for f in os.listdir(path) if f.endswith(('.html', '.md')) and f != 'index.html'])
    
    if not articles:
        print("❌ Error: No articles found in Public_Articles.")
        return

    # اخـتـِيـارُ مـَقـالِ الـيـَوْم
    day_index = (datetime.now().timetuple().tm_yday - 1) % len(articles)
    article_file = articles[day_index]
    
    # اسـتـخـلاص الـعـُنـوان لـِلـتـَّغـرِيـدة
    title = os.path.splitext(article_file)[0].replace("_", " ")
    
    # تـَشـفـِيـرُ الـرَّابـِطِ لـِضـَمـانِ الـوُصـُولِ لـِلـمـَوْقـِع
    encoded_file = urllib.parse.quote(article_file)
    link = f"https://bichay-theo.github.io/Archive/Public_Articles/{encoded_file}"
    
    tweet_text = f"من كنوز الأرشيف اليوم:\n\n📜 {title}\n\nلقراءة المقال كاملاً:\n{link}"

    try:
        api_v1, client_v2 = get_x_auth()
        image_path = find_article_image(article_file)
        
        if image_path:
            print(f"🚀 Uploading Media: {image_path}")
            media = api_v1.media_upload(filename=image_path)
            client_v2.create_tweet(text=tweet_text, media_ids=[media.media_id])
            print("✨ Tweet posted WITH image.")
        else:
            client_v2.create_tweet(text=tweet_text)
            print("✨ Tweet posted WITHOUT image (not found).")
            
    except Exception as e:
        print(f"💥 Critical Failure: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run()
