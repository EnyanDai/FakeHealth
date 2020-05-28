#%%
import os
import json
import time
import random
import argparse
from collect_tweets import TweetCollector
from util.TwythonConnector import TwythonConnector

parser = argparse.ArgumentParser(description='crawl')
parser.add_argument("--news_type",type=str,default="HealthStory")
parser.add_argument("--save_dir",type=str,default="../dataset")
args = parser.parse_known_args()[0]


tweet_keys_file = "./resources/tweet_keys_file.txt"
connector = TwythonConnector(tweet_keys_file)

#%%
engagements_path = "../dataset/engagements/{}.json".format(args.news_type)
with open(engagements_path,"r") as f:
    engagements = json.load(f)

# %%
for news_id, engage in engagements.items():
    print("==================================================")
    print(news_id)

    tweet_collector = TweetCollector(args.save_dir,args.news_type,news_id,engage,connector)
    print("===============get tweets=================")

    tweet_collector.get_tweets()
    print("===============get replies================")

    tweet_collector.get_replies()
    print("===============get retweets===============")

    tweet_collector.get_retweets()
# %%
from news import News
from collect_users import UserCollector

user_root = os.path.join(args.save_dir, "user_network")

for news_id in engagements.keys():
    print("==================================================")
    print(news_id)

    news = News(args.save_dir,args.news_type,news_id)
    user_collector = UserCollector(user_root,connector)
    print("===============get user profiles=================")

    user_collector.collect_user_profiles(news.get_all_users())
    print("===============get user timelines=================")

    user_collector.collect_user_recent_tweets(news.get_all_users())
# %%
