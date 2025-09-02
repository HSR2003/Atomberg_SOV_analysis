import sys
import io
import requests
import pandas as pd

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')


API_KEY = "##"  
CX_ID = "##"  


KEYWORDS = [
    "smart fan",
    "smart ceiling fan",
    "smart fan BLDC",
]

NUM_RESULTS_PER_KEYWORD = 10  # Top 10 results per keyword


def google_search(query, api_key, cx, num_results=10):
    results = []
    start = 1

    while len(results) < num_results:
        
        num = min(10, num_results - len(results))
        url = "https://www.googleapis.com/customsearch/v1"
        params = {
            "key": api_key,
            "cx": cx,
            "q": query,
            "start": start,
            "num": num
        }
        response = requests.get(url, params=params)
        data = response.json()

        if "items" not in data:
            break

        for item in data["items"]:
            link = item.get("link", "")
            # filter only video links
            if "youtube.com/watch?v=" in link:
                results.append({
                    "title": item.get("title"),
                    "link": link,
                    "keyword": query
                })

        start += num

    return results


all_results = []
for kw in KEYWORDS:
    search_results = google_search(f"{kw} site:youtube.com", API_KEY, CX_ID, NUM_RESULTS_PER_KEYWORD)
    all_results.extend(search_results)

df = pd.DataFrame(all_results)
print(df.head().to_string(index=False))

# Save   video links to CSV
df.to_csv(r"C:\Users\Haris\Atomberg\Data\youtube_video_links.csv", index=False, encoding="utf-8-sig")
print(f"Saved {len(df)} YouTube video links to youtube_video_links.csv")
