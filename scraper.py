from google_play_scraper import search, app
import json

keywords = ['productivity utility', 'cool tools', 'indie apps', 'daily tools']
apps_data = []

print("Play Store se nayi apps khoji ja rahi hain...")

for kw in keywords:
    results = search(kw, lang="en", country="in", n_hits=25)
    for item in results:
        try:
            app_id = item['appId']
            details = app(app_id)
            
            installs = details.get('realInstalls', 0)
            score = details.get('score', 0)
            
            # Condition: Rating >= 4.0 aur Downloads 100 se 50,000 ke beech
            if score >= 4.0 and 100 <= installs <= 50000:
                apps_data.append({
                    'title': details['title'],
                    'icon': details['icon'],
                    'score': round(score, 1),
                    'installs': details['installs'],
                    'url': details['url'],
                    'description': details.get('summary', '')[:100] + '...'
                })
        except Exception as e:
            continue

# Overwrites apps.json with fresh data
with open('apps.json', 'w', encoding='utf-8') as f:
    json.dump(apps_data, f, ensure_ascii=False, indent=4)

print(f"Total {len(apps_data)} apps update ho gayi hain!")
