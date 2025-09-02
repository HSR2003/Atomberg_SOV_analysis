import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load comments with sentiment
df = pd.read_csv(r"C:\Users\Haris\Atomberg\Data\youtube_comments_sentiment.csv") 


if "Atomberg" not in df.columns:
    df['Atomberg'] = df['comment'].apply(lambda x: "Atomberg" if "Atomberg" in x else "Competitors")

#  Weighted Count 
if "weight" not in df.columns:
    df['weight'] = 1
df['WeightedCount'] = df['weight']

#  Sentiment Distribution
sentiment_dist = df.groupby(["Atomberg", "FinalSentiment"]).size().unstack(fill_value=0)
sentiment_percent = sentiment_dist.div(sentiment_dist.sum(axis=1), axis=0) * 100
print("Sentiment distribution by Atomberg (%):")
print(sentiment_percent.round(2))

#  bar chart for sentiment distribution
sentiment_percent.plot(kind='bar', stacked=True, figsize=(8,5), colormap='RdYlGn')
plt.title('Sentiment Distribution by Brand')
plt.ylabel('Percentage (%)')
plt.xlabel('Brand')
plt.legend(title='Sentiment', bbox_to_anchor=(1.05,1))
plt.tight_layout()
plt.show()

#  Normalized Share of Voice (weighted) 
sov_weighted = df.groupby('Atomberg')['WeightedCount'].sum()
sov_weighted = sov_weighted / sov_weighted.sum() * 100
print("\nNormalized Weighted Share of Voice (%):")
print(sov_weighted.round(2))

#  Weighted Sentiment Score 
weights = {
    "Very Positive": 2,
    "Positive": 1,
    "Neutral": 0,
    "Negative": -1,
    "Very Negative": -2
}
df["SentimentScore"] = df["FinalSentiment"].map(weights)
brand_sentiment = df.groupby("Atomberg")["SentimentScore"].mean()
print("\nWeighted Sentiment Score (higher = better sentiment):")
print(brand_sentiment.round(2))

#  Share of Positive Voice 
positive_labels = ["Positive", "Very Positive"]
share_positive = df.groupby('Atomberg')['FinalSentiment'].apply(
    lambda x: (x.isin(positive_labels).sum() / len(x) * 100) if len(x)>0 else 0
)
print("\nShare of Positive Voice (%):")
print(share_positive.round(2))

# Plot positive share
sns.barplot(x=share_positive.index, y=share_positive.values, palette='Greens')
plt.ylabel('Share of Positive Voice (%)')
plt.title('Positive Sentiment Comparison')
plt.show()

#  Weighted SoV vs Weighted Sentiment 
brand_stats = df.groupby('Atomberg').agg({
    'SentimentScore':'mean',
    'WeightedCount':'sum',
    'comment':'count'
}).reset_index()

sns.scatterplot(
    data=brand_stats,
    x='WeightedCount',
    y='SentimentScore',
    size='comment',
    hue='Atomberg',
    sizes=(100,1000),
    palette=['green','red'],
    legend='full'
)
plt.xlabel('Weighted Share of Voice')
plt.ylabel('Weighted Sentiment Score')
plt.title('Brand SoV vs Sentiment')
plt.show()
