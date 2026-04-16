import os, tweepy, sys, urllib.parse, datetime, unicodedata

# مـُجـَلـَّدَاتُ الـسـِّيـادَة
ARTICLES_PATH = "Public_Articles"
IMAGE_FOLDER = "assets/images"

def get_x_auth():
    keys = [os.getenv(f"X_{k}", "").strip() for k in ["API_KEY", "API_SECRET", "ACCESS_TOKEN", "ACCESS_TOKEN_SECRET"]]
    auth = tweepy.OAuth1UserHandler(*keys)
    return tweepy.API(auth), tweepy.Client(consumer_key=keys[0], consumer_secret=keys[1], access_token=keys[2], access_token_secret=keys[3])

def normalize_text(text):
    return unicodedata.normalize('NFC', text).strip()

def run():
    if not os.path.exists(ARTICLES_PATH): return
    
    # جـَلـبُ الـمـَقـالاتِ بـِتـَرْمـِيـزٍ مـُوَحـَّد
    articles = sorted([normalize_text(f) for f in os.listdir(ARTICLES_PATH) if f.endswith(('.html', '.md')) and f != 'index.html'])
    if not articles: return

    day_idx = (datetime.datetime.now().timetuple().tm_yday - 1) % len(articles)
    article_file = articles[day_idx]
    
    # حـَلُّ مـُشـكـِلـَةِ 404: الـتـَّأكـُّد مـن أنَّ الـرَّابـِطَ يـُطـابـِقُ الـمـَلـَفَّ الـمـَرْفـُوعَ تـَمـامـاً
    encoded_filename = urllib.parse.quote(article_file)
    link = f"https://bichay-theo.github.io/Archive/Public_Articles/{encoded_filename}"
    
    title = os.path.splitext(article_file)[0].replace("_", " ").replace("-", " ")
    tweet_text = f"من كنوز الأرشيف اليوم:\n\n📜 {title}\n\nلقراءة المقال كاملاً:\n{link}"

    try:
        api_v1, client_v2 = get_x_auth()
        
        # الـبـَحـثُ عـَنِ الـصـُّورَة (بـِدُونِ حـَسـَّاسـِيـَّةِ لـِلِامـتـِداد)
        image_path = None
        base_name = normalize_text(os.path.splitext(article_file)[0])
        if os.path.exists(IMAGE_FOLDER):
            for f in os.listdir(IMAGE_FOLDER):
                if normalize_text(os.path.splitext(f)[0]) == base_name:
                    image_path = os.path.join(IMAGE_FOLDER, f)
                    break

        if image_path:
            media = api_v1.media_upload(filename=image_path)
            client_v2.create_tweet(text=tweet_text, media_ids=[media.media_id])
            print(f"✅ Success: Posted with image {image_path}")
        else:
            client_v2.create_tweet(text=tweet_text)
            print("⚠️ No image found in assets/images, posted text only.")
            
    except Exception as e:
        print(f"❌ Failure: {e}"); sys.exit(1)

if __name__ == "__main__":
    run()
