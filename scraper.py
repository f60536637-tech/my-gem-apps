from google_play_scraper import search, app
import json

keywords = ['utility tools', 'productivity', 'daily apps']
apps_data = []

print("Searching Play Store...")

for kw in keywords:
    try:
        results = search(kw, lang="en", country="in", n_hits=15)
        for item in results:
            try:
                app_id = item.get('appId')
                if not app_id:
                    continue
                    
                details = app(app_id)
                installs = details.get('realInstalls', 0)
                score = details.get('score', 0)
                
                # Condition: Score >= 3.8 aur Installs 50 se 100,000 ke beech
                if score >= 3.8 and 50 <= installs <= 100000:
                    apps_data.append({
                        'title': details.get('title', 'Unknown App'),
                        'icon': details.get('icon', ''),
                        'score': round(score, 1) if score else 4.0,
                        'installs': details.get('installs', '100+'),
                        'url': details.get('url', f'https://play.google.com/store/apps/details?id={app_id}'),
                        'description': details.get('summary', 'Useful App')[:100] + '...'
                    })
            except Exception:
                continue
    except Exception:
        continue

# File overwrite safeguard
if len(apps_data) > 0:
    with open('apps.json', 'w', encoding='utf-8') as f:
        json.dump(apps_data, f, ensure_ascii=False, indent=4)
    print(f"Success! Saved {len(apps_data)} apps to apps.json")
else:
    print("No apps found, keeping existing apps.json")
