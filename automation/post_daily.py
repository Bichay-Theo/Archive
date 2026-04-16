import os
import tweepy
import sys
import urllib.parse
from datetime import datetime

# =============================================================================
# ULTIMATE DAILY POSTER: URL & ENCODING SOVEREIGNTY
# =============================================================================

# مـُجـَلـَّدُ الـصـُّوَرِ الـمـُعـْتـَمـَد
IMAGE_FOLDER = "assets/images"

def get_x_auth():
    """بـُروتوكولُ الـمـُصـادَقـَةِ لـِمـَنـَصـَّةِ X"""
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
    """الـبـَحـثُ عـَنِ الـصـُّورَةِ الـمـُطـابـِقـَةِ مـَعَ تـَجـاوُزِ عـُقـَدِ الـتـَّرمـِيـز"""
    base_target = os.path.splitext(article_filename)[0].strip()
    if not os.path.exists(IMAGE_FOLDER):
        return None
    
    for f in os.listdir(IMAGE_FOLDER):
        if os.path.splitext(f)[0].strip() == base_target:
            return os.path.join(IMAGE_FOLDER, f)
    return None

def run():
    """تـَنـْفـِيذُ مـَهـَمـَّةِ الـنـَّشـرِ الـيـَوْمـِيـَّةِ بـِأَقـْصـَى دِقـَّة"""
    path = "Public_Articles"
    
    # جـَلـبُ الـمـَقـالاتِ بـِتـَرْتـِيـبٍ صـَارِمٍ لـِضـَمـانِ الـتـَّسـَلـْسـُل
    if not os.path.exists(path):
        print(f"❌ Error: Folder {path} missing.")
        return

    articles = sorted([f for f in os.listdir(path) if f.endswith(('.html', '.md')) and f != 'index.html'])
    
    if not articles:
        print("❌ Error: No articles found for posting.")
        return

    # اخـتـِيـارُ مـَقـالِ الـيـَوْمِ بـِنـاءً عـَلـَى تـَقـوِيـمِ الـسـَّنـَة
    day_index = (datetime.now().timetuple().tm_yday - 1) % len(articles)
    article_file = articles[day_index]
    
    # صـِيـاغـَةُ الـعـُنـوانِ لـِلـتـَّغـرِيـدة
    title = os.path.splitext(article_file)[0].replace("_", " ")
    
    # 🛡️ بـُروتوكولُ حـِمـايـَةِ الـرَّابـِط (لـِحـَلِّ مـُشـكـِلـَةِ 404)
    # تـَشـفـِيـرُ اسـمِ الـمـَلـَفِّ فـَقـَط لـِيـَتـَوافـَقَ مـَعَ خـَوادِمِ GitHub Pages
    encoded_filename = urllib.parse.quote(article_file)
    link = f"https://bichay-theo.github.io/Archive/Public_Articles/{encoded_filename}"
    
    tweet_text = f"من كنوز الأرشيف اليوم:\n\n📜 {title}\n\nلقراءة المقال كاملاً:\n{link}"

    print(f"🚀 Preparing to post: {title}")
    print(f"🔗 Generated Link: {link}")

    try:
        api_v1, client_v2 = get_x_auth()
        image_path = find_article_image(article_file)
        
        if image_path and os.path.exists(image_path):
            print(f"📸 Found matching image: {image_path}")
            media = api_v1.media_upload(filename=image_path)
            client_v2.create_tweet(text=tweet_text, media_ids=[media.media_id])
            print("✅ Success: Posted with image.")
        else:
            print("⚠️ No matching image found. Posting text only.")
            client_v2.create_tweet(text=tweet_text)
            print("✅ Success: Posted text-only.")
            
    except Exception as e:
        print(f"❌ Critical Failure: {str(e)}")
        sys.exit(1)

if __name__ == "__main__":
    run()
