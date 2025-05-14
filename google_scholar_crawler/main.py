from scholarly import scholarly, ProxyGenerator
import json
from datetime import datetime
import os
import sys
import traceback

def fetch_author_data(use_proxy=True):
    if use_proxy:
        print("🛡️ Attempting to set up free proxy...", flush=True)
        pg = ProxyGenerator()
        if pg.FreeProxies():
            scholarly.use_proxy(pg)
            print("✅ Proxy set successfully.", flush=True)
        else:
            print("⚠️ Proxy setup failed. Proceeding without proxy...", flush=True)

    scholar_id = os.environ['GOOGLE_SCHOLAR_ID']
    print(f"🔍 Fetching author by ID: {scholar_id}", flush=True)
    author = scholarly.search_author_id(scholar_id)
    print("✅ Author found. Filling details...", flush=True)
    scholarly.fill(author, sections=['basics', 'indices', 'counts', 'publications'])
    return author

# ==== 主流程开始 ====
print("🎯 Starting Google Scholar Crawler...", flush=True)

try:
    author = fetch_author_data(use_proxy=True)
except Exception as e:
    print(f"❌ Proxy fetch failed: {e}", file=sys.stderr, flush=True)
    traceback.print_exc()
    print("🔁 Retrying without proxy...", flush=True)
    try:
        author = fetch_author_data(use_proxy=False)
    except Exception as e2:
        print(f"💀 Final fetch failed: {e2}", file=sys.stderr, flush=True)
        traceback.print_exc()
        sys.exit(1)

# ==== 数据写入 ====
print("💾 Writing results to files...", flush=True)
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

print("🎉 Fetch and save completed successfully.", flush=True)
