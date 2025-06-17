import requests
import json

# より安定しているOverpass APIミラー
overpass_url = "https://overpass.kumi.systems/api/interpreter"

# クエリ（千葉県JP-12内のモスバーガー取得）
query = """
[out:json][timeout:25];
area["ISO3166-2"="JP-13"]->.searchArea;
(
  node["amenity"="fast_food"]["name"~"フレッシュネス"](area.searchArea);
);
out body;
"""

# APIへリクエスト
response = requests.get(overpass_url, params={'data': query})
data = response.json()

# JSON整形（各レコードを辞書形式でまとめる）
results = []
for el in data['elements']:
    name = el.get('tags', {}).get('name', '')
    lat = el.get('lat')
    lng = el.get('lon')
    results.append({
        "name": name,
        "lat": lat,
        "lng": lng,
        "chain": "フレッシュネス",
    })

# 結果を表示
print(f"取得件数: {len(results)} 件")
print(json.dumps(results, ensure_ascii=False, indent=2))

# 保存
with open('chiba_mcd_burger_osm.json', 'w', encoding='utf-8') as f:
    json.dump(results, f, ensure_ascii=False, indent=2)
    print("出力が完了しました")