import os, tweepy, sys, urllib.parse, datetime, unicodedata

def get_x_auth():
    keys = [os.getenv(f"X_{k}", "").strip() for k in ["API_KEY", "API_SECRET", "ACCESS_TOKEN", "ACCESS_TOKEN_SECRET"]]
    auth = tweepy.OAuth1UserHandler(*keys)
    return tweepy.API(auth), tweepy.Client(consumer_key=keys[0], consumer_secret=keys[1], access_token=keys[2], access_token_secret=keys[3])

def run():
    path = "Public_Articles"
    img_folder = "assets/images"
    
    # اسـتـخـدامُ نـَفـسِ مـَنْطـِقِ الـفـَلـتـَرَةِ الـصـَّارِم
    articles = sorted([f for f in os.listdir(path) if f.endswith(('.html', '.md')) and not f.startswith('.')])
    if not articles: return

    day_idx = (datetime.datetime.now().timetuple().tm_yday - 1) % len(articles)
    article_file = articles[day_idx]
    
    # حـَلُّ الـ 404: الـرَّابـِطُ يـَتـَّبـِعُ الامـتـِدادَ الـفـِعـلـِي لـلـمـَلـَف
    encoded_file = urllib.parse.quote(article_file)
    link = f"https://bichay-theo.github.io/Archive/Public_Articles/{encoded_file}"
    
    title = os.path.splitext(article_file)[0].replace("_", " ").replace("-", " ")
    tweet_text = f"من كنوز الأرشيف اليوم:\n\n📜 {title}\n\nلقراءة المقال كاملاً:\n{link}"

    try:
        api_v1, client_v2 = get_x_auth()
        base_name = os.path.splitext(article_file)[0]
        image_path = None
        
        if os.path.exists(img_folder):
            for f in os.listdir(img_folder):
                if os.path.splitext(f)[0] == base_name:
                    image_path = os.path.join(img_folder, f)
                    break

        if image_path:
            media = api_v1.media_upload(filename=image_path)
            client_v2.create_tweet(text=tweet_text, media_ids=[media.media_id])
            print(f"✅ تـَمَّ الـنـَّشـرُ بـِالـصـُّورَة: {title}")
        else:
            client_v2.create_tweet(text=tweet_text)
            print(f"✅ تـَمَّ الـنـَّشـرُ نـَصـِّيـّاً: {title}")
    except Exception as e:
        print(f"❌ فشل: {e}"); sys.exit(1)

if __name__ == "__main__":
    run()
