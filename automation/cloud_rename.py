import os

def rename_on_cloud():
    articles_path = "Public_Articles"
    images_path = "assets/images"
    
    # الـتـَّأَكـُّدُ مـِن وُجـُودِ مـُجـَلـَّدِ الـمـَقـالاتِ
    if not os.path.exists(articles_path):
        print(f"❌ Error: Folder {articles_path} not found!")
        return

    # الـتـَّأَكـُّدُ مـِن وُجـُودِ مـُجـَلـَّدِ الـصـُّوَرِ (وإنـْشـاؤُهُ إِن كـانَ مـَفـْقـُوداً)
    if not os.path.exists(images_path):
        print(f"⚠️ Warning: {images_path} not found. Creating it now...")
        os.makedirs(images_path, exist_ok=True)
        print("Folder created. Please upload your images to assets/images first.")
        return
    
    # جـَلـْبُ وتـَرْتـِيـبُ الـمـَقـالاتِ
    articles = sorted([f for f in os.listdir(articles_path) if f.endswith(('.md', '.html')) and f != 'index.html'])
    article_names = [os.path.splitext(f)[0] for f in articles]
    
    # جـَلـْبُ وتـَرْتـِيـبُ الـصـُّوَرِ الـحـالـِيـَّةِ
    images = sorted([f for f in os.listdir(images_path) if f.lower().endswith(('.jpg', '.jpeg', '.png', '.webp'))])
    
    if not images:
        print("ℹ️ Observation: No images found in assets/images to rename.")
        return

    limit = min(len(article_names), len(images))
    
    for i in range(limit):
        old_path = os.path.join(images_path, images[i])
        extension = os.path.splitext(images[i])[1]
        new_name = article_names[i] + extension
        new_path = os.path.join(images_path, new_name)
        
        if old_path != new_path:
            print(f"🔄 Renaming: {images[i]} -> {new_name}")
            os.rename(old_path, new_path)

if __name__ == "__main__":
    rename_on_cloud()
