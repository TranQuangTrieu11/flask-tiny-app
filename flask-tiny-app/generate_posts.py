import json
import random
from datetime import datetime, timedelta

#tác giả
authors = ["Admin", "Tin AI", "Thành"]

#từ khóa 
titles = ["Phát triển ứng dụng", "AI trong công nghệ", "Học lập trình", "Xu hướng công nghệ", "Thiết kế giao diện"]
contents = ["Nội dung bài viết về ", "Hướng dẫn chi tiết về ", "Tìm hiểu thêm về ", "Cập nhật mới nhất về "]

#200 bài viết
posts = []
start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 3, 7)

for i in range(1, 201):
    title = f"{random.choice(titles)} {random.randint(100, 199)}: {random.choice(contents)}"
    content = f"{random.choice(contents)}{title.lower()} với các bước thực hiện. Hãy theo dõi để biết thêm chi tiết!"
    author = random.choice(authors)
    date = (start_date + timedelta(days=random.randint(0, (end_date - start_date).days))).strftime("%Y-%m-%d")
    task = "Đã đăng"

    post = {
        "id": i,
        "title": title,
        "content": content,
        "author": author,
        "date": date,
        "task": task
    }
    posts.append(post)

# Lưu vào posts.json
with open("posts.json", "w", encoding="utf-8") as f:
    json.dump(posts, f, indent=4, ensure_ascii=False)

print("Đã tạo và lưu 200 bài viết vào posts.json")