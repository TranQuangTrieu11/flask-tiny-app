import requests
from bs4 import BeautifulSoup
import json
import os
from datetime import datetime

# URL
URL = "https://techcrunch.com/"

# Load existing posts to get the next ID
def load_posts():
    if os.path.exists("posts.json"):
        with open("posts.json", "r", encoding="utf-8") as f:
            return json.load(f)
    return []

# Save posts to JSON file
def save_posts(posts):
    with open("posts.json", "w", encoding="utf-8") as f:
        json.dump(posts, f, indent=4, ensure_ascii=False)

# Crawl data from TechCrunch
def crawl_techcrunch():
    # Send request to TechCrunch
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, "html.parser")

    # Find articles 
    articles = soup.find_all("article")  
    existing_posts = load_posts()
    next_id = len(existing_posts) + 1

    new_posts = []
    for article in articles:
        title_elem = article.find("h2") or article.find("h3")  
        content_elem = article.find("div", class_="article-content")  
        if title_elem and content_elem:
            title = title_elem.get_text().strip()
            content = content_elem.get_text().strip()[:200]  
            author = "user2"  
            date = datetime.now().strftime("%Y-%m-%d")  
            task = "Đã đăng"  

            post = {
                "id": next_id,
                "title": title,
                "content": content,
                "author": author,
                "date": date,
                "task": task
            }
            new_posts.append(post)
            next_id += 1

    # Kết hợp posts cũ và mới
    all_posts = existing_posts + new_posts
    save_posts(all_posts)
    print(f"Crawled and saved {len(new_posts)} new posts. Total posts: {len(all_posts)}")

if __name__ == "__main__":
    crawl_techcrunch()