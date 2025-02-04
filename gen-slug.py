# gen_slug.py
import os
import hashlib
from datetime import datetime, timezone
import traceback
import frontmatter
from dateutil import parser
import tempfile
from zoneinfo import ZoneInfo

CONTENT_DIR = "../content/posts/"

for root, _, files in os.walk(CONTENT_DIR):
    for filename in files:
        if filename.endswith(".md"):
            filepath = os.path.join(root, filename)
            try:
                post = frontmatter.load(filepath)
            except Exception as e:
                print(f"处理文件失败: {filepath}")
                print(f"错误详情:\n{traceback.format_exc()}")
                continue

            # 生成哈希逻辑
            title = post.get("title", os.path.splitext(filename)[0])
            print(f"标题：{title}")
            date_value = post.get("date")
            print(f"时间：{date_value}")

            # 处理日期
            if isinstance(date_value, datetime):
                dt = date_value.astimezone(timezone.utc)
            elif isinstance(date_value, str):
                try:
                    # 解析无时区字符串，假设为本地时间 (如 UTC+8)
                    dt_naive = datetime.strptime(date_value, "%Y-%m-%d %H:%M:%S")
                    dt_local = dt_naive.replace(tzinfo=ZoneInfo("Asia/Shanghai"))  # 替换为你的本地时区
                    dt = dt_local.astimezone(timezone.utc)
                except ValueError:
                    # 处理带时区的 ISO 格式字符串
                    dt = parser.isoparse(date_value).astimezone(timezone.utc)
            elif isinstance(date_value, (int, float)):
                dt = datetime.fromtimestamp(date_value, tz=timezone.utc)
            else:
                dt = datetime.now(timezone.utc)

            date_timestamp = int(dt.timestamp())
            print(f"时间戳：{date_timestamp}")
            hash_input = f"{title}|{date_timestamp}".encode()
            hash_hex = hashlib.md5(hash_input).hexdigest()[:6]
            print(f"slug：{hash_hex}")
            post.metadata["slug"] = hash_hex
            try:
                # 获取目标文件的目录路径
                target_dir = os.path.dirname(os.path.abspath(filepath))
                
                # 在目标目录创建临时文件
                with tempfile.NamedTemporaryFile(
                    mode="w", 
                    delete=False, 
                    encoding="utf-8",
                    dir=target_dir,  # 关键修改：确保临时文件与目标文件在同一目录
                    suffix=".md"     # 保持文件后缀一致
                ) as tmp:
                    tmp.write(frontmatter.dumps(post))
                    tmp_path = tmp.name
                
                # 安全替换原文件（同一磁盘）
                os.replace(tmp_path, os.path.abspath(filepath))
                print(f"已更新: {filepath}")
                print("\n")

            except Exception as e:
                print(f"写入失败: {filepath}")
                print(f"错误详情:\n{traceback.format_exc()}")
