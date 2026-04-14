import os
import tweepy
import random
import sys

# ... (بقية الدوال السابقة هنا: get_x_client, get_random_article)

def run():
    article_file = get_random_article()
    if not article_file:
        print("❌ لـَم يـَتـِمَّ الـعـُثـورُ عـَلى مـَقـالات.")
        return

    title = article_file.replace(".html", "").replace("_", " ")
    link = f"https://bichay-theo.github.io/Archive/Public_Articles/{article_file}"
    tweet_text = f"مقال اليوم من الأرشيف:\n\n📜 {title}\n\nلقراءة المقال كاملاً:\n{link}"

    try:
        client = get_x_client()
        client.create_tweet(text=tweet_text)
        print(f"✅ تـَمَّ الـنـَّشـرُ بـِـنـَجـاح: {title}")
    except Exception as e:
        print(f"❌ خـَطـأٌ صـَارِخٌ أثـنـاءَ الـنـَّشـر: {e}")
        sys.exit(1)  # هـذا مـا يـَجـعـلُ الـعـلامـَةَ تـتـحـولُ لـِلأَحـمـرِ فـي جـِيت هـاب

# هـذا الـسـَّطـرُ يـَجـبُ أَنْ يـَكـونَ فـي بـِدَايـَةِ الـسـَّطـرِ (بـِدونِ فـرَاغـَاتٍ قـَبـلـَه)
if __name__ == "__main__":
    run()
