Atomberg Share of Voice (SoV) Analysis

This project analyzes YouTube comments to quantify Atomberg’s Share of Voice compared to competitors in the smart fan market. The pipeline fetches video links, scrapes comments, filters relevant ones, performs sentiment analysis, and computes engagement-weighted SoV metrics.

Features

Collects top YouTube videos for relevant keywords (e.g., “smart fan”, “smart ceiling fan”).

Filters comments mentioning Atomberg vs competitors.

Performs multilingual sentiment analysis.

Computes:

Share of Voice (SoV)

Weighted Sentiment Score

Share of Positive Voice

Normalizes results using engagement metrics.

Generates plots for sentiment distribution and brand comparison.

Usage

Install dependencies:

pip install -r requirements.txt


Place your YouTube API key in the config section of the scripts.

Run the scripts in order:

Atomberg_tasks.py→ fetch video links

Comment_extract_revised.py→ scrape and label comments

 sentiment_analysis→ calculate sentiment 
SOV_with_sentiment.py→ generate plots

Results

CSV files with labeled comments and calculated metrics.

Plots showing sentiment distribution, positive share, and overall SoV.

Insights

Atomberg has highly positive sentiment among its viewers but low overall presence.

Competitors dominate conversation volume, indicating an opportunity to grow Atomberg’s visibility and engagement.

<img width="999" height="635" alt="image" src="https://github.com/user-attachments/assets/e212cf0a-de1a-4529-9e31-aff06e7cea98" />
<img width="792" height="609" alt="image" src="https://github.com/user-attachments/assets/f5c20792-1e7b-4cd8-a313-3d9df1cad47a" />
<img width="801" height="597" alt="image" src="https://github.com/user-attachments/assets/0cf26eee-0773-4b21-8bfb-d06c1d331ee9" />

