from scholarly import scholarly, ProxyGenerator
import json
from datetime import datetime
import os
import sys

print("🎯 Starting Google Scholar Crawler...")

# ====== 1. 设置代理 ======
print("🛡️ Attempting to set up free proxy...")
pg = ProxyGenerator()
if pg.FreeProxies():
    scholarly.use_proxy(pg)
    print("✅ Proxy set successfully.")
else:
    print("⚠️ Failed to set proxy. Proceeding without proxy...")

# ====== 2. 获取 Scholar ID 并爬取 ======
try:
    scholar_id = os.environ['GOOGLE_SCHOLAR_ID']
    print(f"🔍 Fetching author by ID: {scholar_id}")
    author: dict = scholarly.search_author_id(scholar_id)
    print("✅ Author found. Now filling details...")
    scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
    print("✅ Author data filled.")
except Exception as e:
    print(f"❌ Exception during scholar fetch: {e}", file=sys.stderr)
    sys.exit(1)

# ====== 3. 写入文件 ======
print("💾 Saving results to disk...")
author['updated'] = str(datetime.now())
author['publications'] = {
    v['author_pub_id']: v for v in author.get('publications', [])
}

os.makedirs('results', exist_ok=True)
with open('results/gs_data.json', 'w') as f:
    json.dump(author, f, ensure_ascii=False)

shieldio_data = {
    "schemaVersion": 1,
    "label": "citations",
    "message": f"{author['citedby']}",
}
with open('results/gs_data_shieldsio.json', 'w') as f:
    json.dump(shieldio_data, f, ensure_ascii=False)

print("🎉 Finished successfully.")
