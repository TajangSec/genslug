# scripts/gen_slug.py
import os
import hashlib
from datetime import datetime
import traceback
import frontmatter  # 正确导入
from dateutil import parser

CONTENT_DIR = "../content/posts/"

for root, _, files in os.walk(CONTENT_DIR):
    for filename in files:
        if filename.endswith(".md"):
            filepath = os.path.join(root, filename)
            try:
                post = frontmatter.load(filepath)  # 正确加载 Front Matter
            except Exception as e:
                print(f"处理文件失败: {filepath}")
                print(f"错误详情:\n{traceback.format_exc()}")
                continue
            
            # 生成哈希逻辑
            title = post.get("title", os.path.splitext(filename)[0])
            date_str = post.get("date", datetime.now())

            # 如果 date_str 是字符串，进行转换
            date_format = "%Y-%m-%d %H:%M:%S"  # 日期格式
            if isinstance(date_str, str):
                try:
                    dt = datetime.strptime(date_str, date_format)
                except:
                    dt = parser.isoparse(date_str)

            # 转换为 Unix 时间戳
            date_str = int(dt.timestamp())
            print(title)
            print(date_str)
            hash_input = f"{title}|{date_str}".encode()
            hash_hex = hashlib.md5(hash_input).hexdigest()[:6]
            
            # 更新 Slug
            if "slug" not in post.metadata:
                post.metadata["slug"] = hash_hex
                with open(filepath, "w", encoding="utf-8") as f:
                    f.write(frontmatter.dumps(post))
                print(f"Updated: {filepath}")