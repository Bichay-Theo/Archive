import os, tweepy, sys, datetime

def get_x_auth():
    keys = [os.getenv(f"X_{k}", "").strip() for k in ["API_KEY", "API_SECRET", "ACCESS_TOKEN", "ACCESS_TOKEN_SECRET"]]
    auth = tweepy.OAuth1UserHandler(*keys)
    return tweepy.API(auth), tweepy.Client(consumer_key=keys[0], consumer_secret=keys[1], access_token=keys[2], access_token_secret=keys[3])

def run():
    path = "Public_Articles"
    articles = sorted([f for f in os.listdir(path) if f.endswith('.html')])
    if not articles: return

    day_idx = (datetime.datetime.now().timetuple().tm_yday - 1) % len(articles)
    file_name = articles[day_idx]
    
    # 🛡️ سـِيـادَةُ الـرَّابـِط: اسـمٌ لَاتـِيـنـِيٌّ يـَعـمـَلُ 100%
    link = f"https://bichay-theo.github.io/Archive/Public_Articles/{file_name}"
    
    # 📜 بـَهـاءُ الـعـُنـوان: نـَسـتـَعـِيـدُ الـعـَرَبـِيـَّةَ لـِلـتـَّغـرِيـدَةِ فـَقـَط
    titles = {"ecclesia": "إكليسيا", "agape-philo": "أغابي وفيلو", "hebrews-typology": "الرمزية في رسالة العبرانيين"}
    display_title = titles.get(os.path.splitext(file_name)[0], file_name)
    
    tweet_text = f"من كنوز الأرشيف اليوم:\n\n📜 {display_title}\n\nلقراءة المقال كاملاً:\n{link}"

    try:
        api_v1, client_v2 = get_x_auth()
        img_name = os.path.splitext(file_name)[0]
        img_path = None
        for f in os.listdir("assets/images"):
            if os.path.splitext(f)[0] == img_name:
                img_path = os.path.join("assets/images", f); break

        if img_path:
            media = api_v1.media_upload(filename=img_path)
            client_v2.create_tweet(text=tweet_text, media_ids=[media.media_id])
        else:
            client_v2.create_tweet(text=tweet_text)
        print(f"✨ Posted: {display_title}")
    except Exception as e: print(f"❌ Error: {e}"); sys.exit(1)

if __name__ == "__main__": run()
