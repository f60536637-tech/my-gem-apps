from google_play_scraper import search, app
import json

# Jyada aur flexible search terms
keywords = ['utility tools', 'productivity', 'indie tools', 'smart tools', 'daily apps']
apps_data = []

print("Searching Play Store...")

for kw in keywords:
    try:
        results = search(kw, lang="en", country="in", n_hits=30)
        for item in results:
            try:
                app_id = item['appId']
                details = app(app_id)
                
                installs = details.get('realInstalls', 0)
                score = details.get('score', 0)
                
                # Condition ko thoda relax kiya hai taaki jyada apps match hon:
                # Rating >= 3.8 aur Downloads 50 se 100,000 ke beech
                if score >= 3.8 and 50 <= installs <= 100000:
                    apps_data.append({
                        'title': details.get('title', 'Unknown App'),
                        'icon': details.get('icon', ''),
                        'score': round(score, 1),
                        'installs': details.get('installs', '0+'),
                        'url': details.get('url', ''),
                        'description': details.get('summary', 'Useful App')[:100] + '...'
                    })
            except Exception:
                continue
    except Exception:
        continue

# Direct save without empty check
if len(apps_data) > 0:
    with open('apps.json', 'w', encoding='utf-8') as f:
        json.dump(apps_data, f, ensure_ascii=False, indent=4)
    print(f"Success! Saved {len(apps_data)} apps to apps.json")
else:
    print("No apps found matching criteria.")
