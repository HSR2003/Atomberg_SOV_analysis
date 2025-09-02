import pandas as pd
import re
import math
from googleapiclient.discovery import build

API_KEY = "AIzaSyAhHlf9ecF1KSvcntdcoI0kdUtJBTYXGtI"
INPUT_CSV = "youtube_video_links.csv"
OUTPUT_CSV = "youtube_comments_labeled.csv"


youtube = build("youtube", "v3", developerKey=API_KEY)

# ---- COMPETITOR KEYWORDS ----
COMPETITORS = ["usha", "orient", "havells", "crompton", "bajaj", "v-guard", "polycab"]

def extract_video_id(url):
    match = re.search(r"v=([a-zA-Z0-9_-]{11})", url)
    if match:
        return match.group(1)
    match = re.search(r"youtu\.be/([a-zA-Z0-9_-]{11})", url)
    if match:
        return match.group(1)
    return None

def label_comment(comment, video_is_atomberg, fallback_label):
    text = comment.lower()
    
    # If a competitor is explicitly mentioned, label as Competitors
    for comp in COMPETITORS:
        if comp in text:
            return "Competitors"
    
    # Else, if video is Atomberg ,label as Atomberg
    if video_is_atomberg:
        return "Atomberg"
    
    #  fallback label 
    return fallback_label

def get_video_comments(video_id, video_is_atomberg, fallback_label):
    comments = []
    request = youtube.commentThreads().list(
        part="snippet",
        videoId=video_id,
        maxResults=100,
        textFormat="plainText"
    )
    response = request.execute()

    while response:
        for item in response["items"]:
            snippet = item["snippet"]["topLevelComment"]["snippet"]
            comment = snippet["textDisplay"]
            like_count = snippet.get("likeCount", 0)

            label = label_comment(comment, video_is_atomberg, fallback_label)
            weight = 1 + math.log1p(like_count)

            comments.append({
                "video_id": video_id,
                "brand": label,
                "comment": comment,
                "likes": like_count,
                "weight": weight
            })

        if "nextPageToken" in response:
            request = youtube.commentThreads().list(
                part="snippet",
                videoId=video_id,
                pageToken=response["nextPageToken"],
                maxResults=100,
                textFormat="plainText"
            )
            response = request.execute()
        else:
            break
    return comments


df_links = pd.read_csv(INPUT_CSV)
all_comments = []

for _, row in df_links.iterrows():
    url = row["link"]
    title = row["title"]

    video_id = extract_video_id(url)
    if not video_id:
        continue

   
    video_is_atomberg = "atomberg" in title.lower() or "atomberg" in url.lower()
    fallback_label = "Atomberg" if video_is_atomberg else "Competitors"

    try:
        comments = get_video_comments(video_id, video_is_atomberg, fallback_label)
        all_comments.extend(comments)
    except Exception as e:
        print(f"Error fetching comments for {url}: {e}")


df_comments = pd.DataFrame(all_comments)
df_comments.to_csv(OUTPUT_CSV, index=False, encoding="utf-8-sig")

print(f"Saved {len(df_comments)} relevant comments to {OUTPUT_CSV}")
    