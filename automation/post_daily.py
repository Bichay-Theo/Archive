import os, tweepy, sys, urllib.parse, datetime, re

def get_x_auth():
    keys = [os.getenv(f"X_{k}", "").strip() for k in ["API_KEY", "API_SECRET", "ACCESS_TOKEN", "ACCESS_TOKEN_SECRET"]]
    auth = tweepy.OAuth1UserHandler(*keys)
    return tweepy.API(auth), tweepy.Client(consumer_key=keys[0], consumer_secret=keys[1], access_token=keys[2], access_token_secret=keys[3])

def clean_for_x(text):
    """تـَنـْظـِيـفُ الـنـَّصِّ لـِيـَكـُونَ بـَهـِيـّاً فـِي الـتـَّغـرِيـدَة"""
    return text.replace("_", " ").replace("-", " ").strip()

def run():
    path = "Public_Articles"
    img_folder = "assets/images"
    
    # جـَلـبُ الـمـَقـالاتِ بـِتـَرْتـِيـبٍ أَبـْجـَدِيّ
    articles = sorted([f for f in os.listdir(path) if f.endswith(('.html', '.md')) and f != 'index.html'])
    if not articles:
        print("❌ المقلات مفقودة."); return

    # اخـتـِيـارُ مـَقـالِ الـيـَوْم
    day_idx = (datetime.datetime.now().timetuple().tm_yday - 1) % len(articles)
    file_name = articles[day_idx]
    
    # الـسـِّرُّ هـُنـا: اسـتـخـدامُ تـَشـفـِيـرٍ عـَالـِي الـدِّقـَّةِ لـِلـرَّابـِط
    encoded_file = urllib.parse.quote(file_name)
    link = f"https://bichay-theo.github.io/Archive/Public_Articles/{encoded_file}"
    
    # صـِيـاغـَةُ الـعـُنـوانِ الـعـَرَبـِي لـِلـتـَّغـرِيـدَة
    display_title = clean_for_x(os.path.splitext(file_name)[0])
    tweet_text = f"من كنوز الأرشيف اليوم:\n\n📜 {display_title}\n\nلقراءة المقال كاملاً:\n{link}"

    try:
        api_v1, client_v2 = get_x_auth()
        
        # بـُروتوكولُ رَصـدِ الـصـُّورَةِ الـمـُطـابـِقـَة
        image_path = None
        base_name = os.path.splitext(file_name)[0]
        if os.path.exists(img_folder):
            for f in os.listdir(img_folder):
                if os.path.splitext(f)[0] == base_name:
                    image_path = os.path.join(img_folder, f)
                    break

        if image_path:
            print(f"🚀 رَفـعُ الـصـُّورَة: {image_path}")
            # حـَلُّ مـُشـكـِلـَةِ الـصـُّورَة: نـَقـُومُ بـِتـَمـرِيـرِ الـمـَلـَفِّ كـَـ "تـَيـَّارِ بـَيـانـات"
            with open(image_path, 'rb') as img_file:
                media = api_v1.media_upload(filename=image_path, file=img_file)
                client_v2.create_tweet(text=tweet_text, media_ids=[media.media_id])
            print("✨ تـَمـَّتِ الـتـَّغـرِيـدةُ بـِالـصـُّورَة.")
        else:
            client_v2.create_tweet(text=tweet_text)
            print("✨ تـَمـَّتِ الـتـَّغـرِيـدةُ نـَصـِّيـّاً (الـصـُّورَةُ لـَم تـُرصـَد).")
            
    except Exception as e:
        print(f"💥 عـَطـَبٌ فـِي الـمـَهـَمـَّة: {e}"); sys.exit(1)

if __name__ == "__main__":
    run()
