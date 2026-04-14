import os
import tweepy
import sys
import urllib.parse
from datetime import datetime

# مـسـار مـُجـلـد الـصـور (اخـتـيـاري)
IMAGE_FOLDER = "assets/images" 

def get_x_auth():
    api_key = os.getenv("X_API_KEY", "").strip()
    api_secret = os.getenv("X_API_SECRET", "").strip()
    access_token = os.getenv("X_ACCESS_TOKEN", "").strip()
    access_token_secret = os.getenv("X_ACCESS_TOKEN_SECRET", "").strip()

    auth = tweepy.OAuth1UserHandler(api_key, api_secret, access_token, access_token_secret)
    return tweepy.API(auth), tweepy.Client(
        consumer_key=api_key,
        consumer_secret=api_secret,
        access_token=access_token,
        access_token_secret=access_token_secret
    )

def get_article_by_order():
    path = "Public_Articles"
    if not os.path.exists(path): return None
    articles = sorted([f for f in os.listdir(path) if f.lower().endswith(('.html', '.htm', '.md')) and f.lower() != 'index.html'])
    if not articles: return None
    day_index = (datetime.now().timetuple().tm_yday - 1) % len(articles)
    return os.path.join(path, articles[day_index])

def find_article_image(article_filename):
    base_name = os.path.splitext(article_filename)[0]
    extensions = ['.jpg', '.jpeg', '.png', '.webp']
    if not os.path.exists(IMAGE_FOLDER): return None
    for ext in extensions:
        img_path = os.path.join(IMAGE_FOLDER, base_name + ext)
        if os.path.exists(img_path):
            return img_path
    return None

def run():
    article_full_path = get_article_by_order()
    if not article_full_path: sys.exit(1)

    article_file = os.path.basename(article_full_path)
    title = article_file.replace(".html", "").replace(".htm", "").replace(".md", "").replace("_", " ")
    
    # الـرَّابـِطُ الـنـَّظـِيـفُ والـمـُشـفـَّر
    web_path = article_full_path.replace(".md", "").replace(".html", "")
    encoded_path = urllib.parse.quote(web_path)
    link = f"https://bichay-theo.github.io/Archive/{encoded_path}"
    
    tweet_text = f"من كنوز الأرشيف اليوم:\n\n📜 {title}\n\nلقراءة المقال كاملاً:\n{link}"

    try:
        api_v1, client_v2 = get_x_auth()
        image_path = find_article_image(article_file)
        
        # مـَنـطـِقُ الـنـَّشـرِ الـذَّكـِي:
        if image_path:
            print(f"🔍 وجدنا صورة: {image_path}")
            media = api_v1.media_upload(filename=image_path)
            client_v2.create_tweet(text=tweet_text, media_ids=[media.media_id])
        else:
            # إذا لـم نـجـد صـورة، نـنـشـر الـنـص فـقـط بـدون مـعـلـمـات إضـافـيـة
            print("💡 لا توجد صورة للمقال، سيتم النشر بنص ورابط فقط.")
            client_v2.create_tweet(text=tweet_text)
            
        print(f"✅ تم النشر بنجاح: {title}")
    except Exception as e:
        print(f"❌ خطأ: {e}")
        sys.exit(1)

if __name__ == "__main__":
    run()
