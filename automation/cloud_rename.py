import os

def rename_on_cloud():
    articles_path = "Public_Articles"
    images_path = "assets/images"
    
    os.makedirs(images_path, exist_ok=True)
    if not os.path.exists(articles_path): return

    articles = sorted([f for f in os.listdir(articles_path) if f.endswith(('.md', '.html')) and f != 'index.html'])
    article_names = [os.path.splitext(f)[0] for f in articles]
    images = sorted([f for f in os.listdir(images_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])
    
    limit = min(len(article_names), len(images))
    for i in range(limit):
        old_path = os.path.join(images_path, images[i])
        extension = os.path.splitext(images[i])[1]
        new_path = os.path.join(images_path, f"{article_names[i]}{extension}")
        
        if old_path != new_path:
            os.rename(old_path, new_path)
            print(f"🔄 {images[i]} -> {article_names[i]}")

if __name__ == "__main__":
    rename_on_cloud()
