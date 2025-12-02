import os
import json
from datetime import datetime
from algoliasearch import SearchClient
from bs4 import BeautifulSoup
import re

# ============ 你的配置区 ============
ALGOLIA_APP_ID = "FBCOWM9UO9"
ALGOLIA_API_KEY = "fe585fa7c5e384b3bc76abe3aa6c74e7"
ALGOLIA_INDEX_NAME = "ander1716_github_io_fbcowm9uo9_pages"
JEKYLL_ROOT = os.path.dirname(os.path.abspath(__file__))
# =====================================

client = SearchClient.create(ALGOLIA_APP_ID, ALGOLIA_API_KEY)
index = client.init_index(ALGOLIA_INDEX_NAME)

records = []

# 1. 读取 _posts 文件夹下的所有 markdown 文件
posts_dir = os.path.join(JEKYLL_ROOT, "_posts")
for filename in os.listdir(posts_dir):
    if filename.endswith(".md") or filename.endswith(".markdown"):
        filepath = os.path.join(posts_dir, filename)
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        # 2. 解析 Front Matter 和正文
        parts = content.split('---', 2)
        if len(parts) < 3:
            continue

        front_matter = parts[1]
        post_content = parts[2]

        # 简单提取标题和日期
        title_match = re.search(r'title:\s*[\'"](.+?)[\'"]', front_matter)
        date_match = re.search(r'date:\s*(\d{4}-\d{2}-\d{2})', front_matter)
        url_match = re.search(r'permalink:\s*[\'"](.+?)[\'"]', front_matter)

        title = title_match.group(1) if title_match else filename
        date_str = date_match.group(1) if date_match else "1970-01-01"
        # 生成URL（根据你的Jekyll站点结构调整，这里是一个通用示例）
        if url_match:
            url = url_match.group(1)
        else:
            url = "/" + filename.replace('.md', '.html').replace('.markdown', '.html')

        # 3. 清理Markdown格式，获取纯文本（用于搜索）
        # 移除代码块、图片等
        text_for_search = re.sub(r'```.*?```', '', post_content, flags=re.DOTALL)
        text_for_search = re.sub(r'!\[.*?\]\(.*?\)', '', text_for_search)
        text_for_search = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text_for_search) # 保留链接文字
        text_for_search = re.sub(r'[#*`>\-]', '', text_for_search) # 移除部分Markdown符号

        # 4. 构建一条记录
        record = {
            "objectID": filename, # 唯一标识符
            "title": title,
            "date": date_str,
            "url": url,
            "content": text_for_search[:5000], # 限制长度
            "excerpt": text_for_search[:150] + "...", # 生成摘要
        }
        records.append(record)

# 5. 上传到Algolia
if records:
    response = index.save_objects(records)
    print(f"成功上传 {len(records)} 篇文章到Algolia索引 '{ALGOLIA_INDEX_NAME}'。")
    print("响应:", response)
else:
    print("未找到文章。")