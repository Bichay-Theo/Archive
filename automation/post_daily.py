import os
import tweepy
import sys
import urllib.parse
import datetime
import unicodedata

# =============================================================================
# THE UNIVERSAL POSTER: NORMALIZATION & PATH SOVEREIGNTY
# =============================================================================

IMAGE_FOLDER = "assets/images"

def normalize_arabic(text):
    """تـَوْحـِيدُ تـَرْمـِيـزِ الـحـُروفِ الـعـَرَبـِيـَّةِ لـِتـَفـادِي الـتـَّضـارُب"""
    return unicodedata.normalize('NFC', text)

def get_x_auth():
    keys = [os.getenv(f"X_{k}", "").strip() for k in ["API_KEY", "API_SECRET", "ACCESS_TOKEN", "ACCESS_TOKEN_SECRET"]]
    auth = tweepy.OAuth1UserHandler(keys[0], keys[1], keys[2], keys[3])
    return tweepy.API(auth), tweepy.Client(consumer_key=keys[0], consumer_secret=keys[1], access_token=keys[2], access_token_secret=keys[3])

def find_article_image(article_filename):
    """بـَحـثٌ شـامـِلٌ يـَعـتـَمـِدُ عـلـى الـتـَّطـبـِيـقِ لـِلـصـُّورَة"""
    if not os.path.exists(IMAGE_FOLDER): return None
    
    target_name = normalize_arabic(os.path.splitext(article_filename)[0].strip())
    
    for f in os.listdir(IMAGE_FOLDER):
        current_f = normalize_arabic(os.path.splitext(f)[0].strip())
        if current_f == target_name:
            return os.path.join(IMAGE_FOLDER, f)
    return None

def run():
    path = "Public_Articles"
    if not os.path.exists(path):
        print(f"❌ Folder {path} not found."); return

    # جـَلـبُ الـمـَقـالاتِ بـِتـَرْمـِيـزٍ مـُوَحـَّد
    raw_articles = [f for f in os.listdir(path) if f.endswith(('.html', '.md')) and f != 'index.html']
    articles = sorted([normalize_arabic(f) for f in raw_articles])
    
    if not articles:
        print("❌ No articles found."); return

    # اخـتـِيـارُ مـَقـالِ الـيـَوْم
    day_idx = (datetime.datetime.now().timetuple().tm_yday - 1) % len(articles)
    article_file = articles[day_idx]
    
    # 🛡️ مـُعـالـَجـَةُ الـرَّابـِطِ الـحـَرِجـَة (لـِحـَلِّ 404)
    # نـَقـُومُ بـِتـَشـفـِيـرِ كـُلِّ جـُزءٍ بـِمـُفـرَدِه لـِضـَمـانِ الـقـُبـُولِ الـسـَّحـابـِي
    safe_filename = urllib.parse.quote(article_file)
    link = f"https://bichay-theo.github.io/Archive/Public_Articles/{safe_filename}"
    
    title = os.path.splitext(article_file)[0].replace("_", " ").replace("-", " ")
    tweet_text = f"من كنوز الأرشيف اليوم:\n\n📜 {title}\n\nلقراءة المقال كاملاً:\n{link}"

    print(f"🚀 Mission: {title}")
    print(f"🔗 Target Link: {link}")

    try:
        api_v1, client_v2 = get_x_auth()
        image_path = find_article_image(article_file)
        
        if image_path:
            print(f"📸 Image Found: {image_path}")
            # رَفـعُ الـصـُّورَةِ بـِتـَرْمـِيـزٍ ثـُنـائـِيّ
            media = api_v1.media_upload(filename=image_path)
            client_v2.create_tweet(text=tweet_text, media_ids=[media.media_id])
            print("✨ Posted with Image.")
        else:
            print("⚠️ Image Not Found. Posting Text Only.")
            client_v2.create_tweet(text=tweet_text)
            print("✨ Posted Text-Only.")
            
    except Exception as e:
        print(f"❌ Failure: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run()
