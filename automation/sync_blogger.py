import feedparser
import os
import re
from github import Github, Auth
from datetime import datetime

# =============================================================================
# مَنارةُ الأَرشيفِ - نُسخةُ الأرشفةِ النقيّة (v8.0)
# =============================================================================
BLOG_FEED = "https://bornbytheword.blogspot.com/feeds/posts/default?max-results=500"
REPO_PATH = "Bichay-Theo/Archive" 
BRANCH_NAME = "main" 
# يُفضل استخدام Secrets في GitHub بدلاً من وضع التوكن هنا
PUBLIC_ACCESS_TOKEN = os.environ.get("GH_TOKEN") 
SITE_URL = "https://bichay-theo.github.io/Archive"

def strip_tashkeel(text):
    tashkeel_pattern = re.compile(r'[\u064B-\u065F]')
    return tashkeel_pattern.sub('', text)

def generate_seo_slug(title):
    text = strip_tashkeel(title).lower()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text).strip('-')
    return text

def update_library_index(repo, articles_list):
    print("[SYSTEM] Updating Library Index...")
    articles_list.sort(key=lambda x: x['date'], reverse=True)
    article_links = ""
    for art in articles_list:
        article_links += f'''
        <li style="margin-bottom: 15px; border-bottom: 1px solid #f2f2f2; padding-bottom: 10px;">
            <a href="./{art["link"]}" style="font-size: 20px; font-weight: bold; color: #800000; text-decoration: none; font-family: 'Amiri', serif;">{art["title"]}</a>
            <br><span style="font-size: 14px; color: #888;">[{art["date_str"]}]</span>
        </li>'''

    html_template = f"""---
layout: default
title: "خزانة المقالات"
---
<div dir="rtl" style="text-align: right; max-width: 850px; margin: 0 auto; padding: 20px; font-family: 'Amiri', serif;">
    <h1 style="color: #800000; border-bottom: 2px solid #eee; padding-bottom: 15px; font-size: 30px;">📂 خزانة المقالات والبحوث</h1>
    <ul style="list-style: none; padding: 0;">
{article_links}    </ul>
</div>"""

    index_path = "Public_Articles/index.html"
    try:
        file_ref = repo.get_contents(index_path, ref=BRANCH_NAME)
        repo.update_file(index_path, "Daily Index Sync", html_template, file_ref.sha, branch=BRANCH_NAME)
    except:
        repo.create_file(index_path, "Index Creation", html_template, branch=BRANCH_NAME)

def execute_daily_sync():
    try:
        auth = Auth.Token(PUBLIC_ACCESS_TOKEN)
        g = Github(auth=auth)
        repo = g.get_repo(REPO_PATH)
        feed = feedparser.parse(BLOG_FEED)
        articles_to_index = []

        for entry in feed.entries:
            title = entry.title
            dt = datetime(*entry.published_parsed[:6])
            seo_slug = generate_seo_slug(title)
            file_destination = f"Public_Articles/{seo_slug}.html"
            
            articles_to_index.append({
                "title": title, "link": f"{seo_slug}.html", "date": dt, "date_str": dt.strftime('%Y-%m-%d')
            })

            raw_content = entry.content[0].value
            img_match = re.search(r'<img [^>]*src="([^"]+)"', raw_content)
            preview_img = img_match.group(1) if img_match else f"{SITE_URL}/assets/images/أكليسيا.jpg"

            html_content = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <title>{title}</title>
    <meta name="twitter:card" content="summary_large_image">
    <meta name="twitter:image" content="{preview_img}">
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Amiri&display=swap');
        body {{ background-color: #f4ece2; font-family: 'Amiri', serif; padding: 20px; }}
        .article-container {{ background: white; max-width: 850px; margin: 0 auto; padding: 40px; border-radius: 8px; }}
        h1 {{ color: #800000; }}
        .content {{ font-size: 22px; line-height: 1.8; }}
    </style>
</head>
<body>
    <div class="article-container">
        <h1>{title}</h1>
        <hr>
        <div class="content">{raw_content}</div>
        <hr>
        <a href="./index.html">⬅️ العودة للفهرس</a>
    </div>
</body>
</html>"""

            try:
                existing = repo.get_contents(file_destination, ref=BRANCH_NAME)
                repo.update_file(existing.path, f"Sync: {title}", html_content, existing.sha, branch=BRANCH_NAME)
            except:
                repo.create_file(file_destination, f"Archive: {title}", html_content, branch=BRANCH_NAME)

        update_library_index(repo, articles_to_index)
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    execute_daily_sync()
