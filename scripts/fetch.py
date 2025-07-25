import requests
from bs4 import BeautifulSoup
import json
import os
import re

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.json')
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), '..', 'output', 'subscriptions.txt')

with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

url = config['url']
protocols = config['protocols']

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')
text = soup.get_text()  # 获取整页文本内容

lines = []
for proto in protocols:
    # 正则匹配如 vmess://xxx、vless://xxx 等
    matches = re.findall(rf'{re.escape(proto)}[^\s<>"]+', text)
    lines.extend(matches)

# 去重（可选）
lines = list(set(lines))

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"Extracted {len(lines)} links.")
