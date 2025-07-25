import requests
from bs4 import BeautifulSoup
import json
import os

CONFIG_PATH = os.path.join(os.path.dirname(__file__), '..', 'config.json')
OUTPUT_PATH = os.path.join(os.path.dirname(__file__), '..', 'output', 'subscriptions.txt')

with open(CONFIG_PATH, 'r', encoding='utf-8') as f:
    config = json.load(f)

url = config['url']
protocols = config['protocols']

response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

lines = []
for pre_tag in soup.find_all('pre'):
    content = pre_tag.get_text()
    for line in content.strip().splitlines():
        line = line.strip()
        if any(line.startswith(proto) for proto in protocols):
            lines.append(line)

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with open(OUTPUT_PATH, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f"Extracted {len(lines)} links.")

