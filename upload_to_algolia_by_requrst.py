import os
import json
import re
import requests
from datetime import datetime
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# ============ 你的配置区 ============
# 从环境变量读取配置
ALGOLIA_APP_ID = os.getenv("ALGOLIA_APP_ID")
ALGOLIA_API_KEY = os.getenv("ALGOLIA_API_KEY")
ALGOLIA_INDEX_NAME = os.getenv("ALGOLIA_INDEX_NAME")
JEKYLL_ROOT = os.path.dirname(os.path.abspath(__file__))

# 验证必需的配置项
if not all([ALGOLIA_APP_ID, ALGOLIA_API_KEY, ALGOLIA_INDEX_NAME]):
    raise ValueError("请确保 .env 文件中配置了 ALGOLIA_APP_ID、ALGOLIA_API_KEY 和 ALGOLIA_INDEX_NAME")
# =====================================

# Algolia API端点
INDEXING_URL = f"https://{ALGOLIA_APP_ID}.algolia.net/1/indexes/{ALGOLIA_INDEX_NAME}/batch"

# 请求头
headers = {
    "X-Algolia-Application-Id": ALGOLIA_APP_ID,
    "X-Algolia-API-Key": ALGOLIA_API_KEY,
    "Content-Type": "application/json"
}

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

        # 简单提取标题、日期和分类
        title_match = re.search(r'title:\s*[\'"](.+?)[\'"]', front_matter)
        date_match = re.search(r'date:\s*(\d{4}-\d{2}-\d{2})', front_matter)
        url_match = re.search(r'permalink:\s*[\'"](.+?)[\'"]', front_matter)
        categories_match = re.search(r'categories:\s*\[(.+?)\]', front_matter)

        title = title_match.group(1) if title_match else filename
        date_str = date_match.group(1) if date_match else "1970-01-01"
        
        # 提取分类（可能有多个，取第一个）
        category = None
        if categories_match:
            categories_str = categories_match.group(1)
            # 提取第一个分类
            first_category = categories_str.split(',')[0].strip().strip('\'"')
            if first_category:
                category = first_category
        
        # 生成URL（根据你的Jekyll站点结构调整）
        if url_match:
            url = url_match.group(1)
        else:
            # 从文件名提取slug（去掉日期前缀）
            # 文件名格式：YYYY-MM-DD-title.md
            slug = filename.replace('.md', '').replace('.markdown', '')
            # 去掉日期前缀 (YYYY-MM-DD-)
            slug = re.sub(r'^\d{4}-\d{2}-\d{2}-', '', slug)
            
            if date_match:
                try:
                    date_obj = datetime.strptime(date_str, "%Y-%m-%d")
                    # Jekyll默认格式：/:categories/:year/:month/:day/:title.html
                    if category:
                        url = f"/{category}/{date_obj.year}/{date_obj.month:02d}/{date_obj.day:02d}/{slug}.html"
                    else:
                        url = f"/{date_obj.year}/{date_obj.month:02d}/{date_obj.day:02d}/{slug}.html"
                except:
                    url = f"/posts/{slug}.html"
            else:
                url = f"/posts/{slug}.html"

        # 3. 清理Markdown格式，获取纯文本（用于搜索）
        # 移除代码块、图片等
        text_for_search = re.sub(r'```.*?```', '', post_content, flags=re.DOTALL)
        text_for_search = re.sub(r'!\[.*?\]\(.*?\)', '', text_for_search)
        text_for_search = re.sub(r'\[(.*?)\]\(.*?\)', r'\1', text_for_search) # 保留链接文字
        text_for_search = re.sub(r'[#*`>\-]', '', text_for_search) # 移除部分Markdown符号
        text_for_search = re.sub(r'\s+', ' ', text_for_search).strip() # 合并多余空格

        # 4. 构建一条记录
        record = {
            "objectID": filename, # 唯一标识符
            "title": title,
            "date": date_str,
            "url": url,
            "content": text_for_search[:5000], # 限制长度
            "excerpt": text_for_search[:150] + ("..." if len(text_for_search) > 150 else ""), # 生成摘要
        }
        records.append(record)

# 5. 先清空索引（可选，如果想保留旧数据请注释掉这部分）
print("🗑️  清空旧索引数据...")
clear_url = f"https://{ALGOLIA_APP_ID}.algolia.net/1/indexes/{ALGOLIA_INDEX_NAME}/clear"
try:
    clear_response = requests.post(clear_url, headers=headers)
    clear_response.raise_for_status()
    print("✅ 旧数据已清空")
except requests.exceptions.RequestException as e:
    print(f"⚠️  清空索引失败（如果是新索引可忽略）: {e}")

# 6. 上传到Algolia（分批上传，每批最多1000条）
if records:
    batch_size = 1000
    total_batches = (len(records) + batch_size - 1) // batch_size
    
    for batch_num in range(total_batches):
        start_idx = batch_num * batch_size
        end_idx = min(start_idx + batch_size, len(records))
        batch = records[start_idx:end_idx]
        
        # 构建批量操作请求
        operations = []
        for record in batch:
            operations.append({
                "action": "addObject",
                "body": record
            })
        
        payload = {
            "requests": operations
        }
        
        try:
            response = requests.post(INDEXING_URL, headers=headers, json=payload)
            response.raise_for_status()  # 如果状态码不是200，会抛出异常
            
            result = response.json()
            print(f"✅ 成功上传批次 {batch_num + 1}/{total_batches}: {len(batch)} 篇文章")
            
        except requests.exceptions.RequestException as e:
            print(f"❌ 批次 {batch_num + 1} 上传失败!")
            print(f"   错误信息: {e}")
            if hasattr(e, 'response') and e.response is not None:
                print(f"   响应内容: {e.response.text}")
            break  # 如果出错，停止后续批次
    
    print(f"📊 总计处理了 {len(records)} 篇文章")
else:
    print("⚠️  未在 _posts 文件夹中找到文章。")