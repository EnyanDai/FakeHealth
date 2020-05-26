#%%
import os
import json
import time
import random
import argparse
from collect_tweets import TweetCollector
from util.TwythonConnector import TwythonConnector

parser = argparse.ArgumentParser(description='crawl')
parser.add_argument("--save_dir",type=str,default="../dataset")
args = parser.parse_known_args()[0]
tweet_keys_file = "./resources/tweet_keys_file.txt"
connector = TwythonConnector(tweet_keys_file)

# %%
from news import News
from collect_users import UserCollector

user_root = os.path.join(args.save_dir, "user_network")
user_collector = UserCollector(user_root,connector)
user_collector.collect_user_follower_profiles()
user_collector.collect_user_following_profiles()
# %%
