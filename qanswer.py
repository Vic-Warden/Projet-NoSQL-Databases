from pymongo import MongoClient

# Connect to MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["milano2026"]

# Basic stats
print(f"Q1. Users: {db.users.count_documents({})}")
print(f"Q2. Tweets: {db.tweets.count_documents({})}")
print(f"Q3. Unique hashtags: {len(db.tweets.distinct('hashtags'))}")
print(f"Q4. Tweets with #milano2026: {db.tweets.count_documents({'hashtags': 'milano2026'})}")
print(f"Q5. Users who used #milano2026: {len(db.tweets.distinct('user_id', {'hashtags': 'milano2026'}))}")
print(f"Q6. Reply tweets: {db.tweets.count_documents({'in_reply_to_tweet_id': {'$ne': None}})}")

# Top 10 most liked tweets
print("\nQ12. Top 10 tweets by likes:")
for t in db.tweets.find().sort("favorite_count", -1).limit(10):
    print(f"  - {t['tweet_id']} | Likes: {t.get('favorite_count', 0)}")

# Top 10 most used hashtags
print("\nQ13. Top 10 hashtags:")
pipeline = [
    {"$unwind": "$hashtags"},
    {"$group": {"_id": "$hashtags", "count": {"$sum": 1}}},
    {"$sort": {"count": -1}}, {"$limit": 10}
]
for h in db.tweets.aggregate(pipeline):
    print(f"  - #{h['_id']} : {h['count']}")