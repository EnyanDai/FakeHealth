
#%%
import os
import json

class News:

    def __init__(self, root_location,news_type,news_id):

        self.dir = os.path.join(root_location,"engagements",news_type,news_id)
        self.tweets  = self.get_json("tweets")
        self.retweets = self.get_json("retweets")
        self.replies = self.get_json("replies")

    def get_tweets_users(self):
        return self.get_tweet_object_users(self.tweets,add_user_mentioned=True)

    def get_replies_users(self):
        return self.get_tweet_object_users(self.replies,add_user_mentioned=True)
    
    def get_retweet_users(self):
        return self.get_tweet_object_users(self.retweets,add_user_mentioned=True)
        return retweet_users


    def get_all_users(self):
        users = set()
        users.update(self.get_tweet_object_users(self.tweets,add_user_mentioned=True))
        users.update(self.get_replies_users())
        users.update(self.get_retweet_users())

        return users

    def get_tweet_object_users(self,tweets,add_user_mentioned):
        user_screen_name_set = set()
        for tweet_object in tweets:
            if("user" in tweet_object):
                user_screen_name_set.add(tweet_object["user"]["id"])
            if(add_user_mentioned and "user_mentions" in tweet_object):
                for user_mention in tweet_object["user_mentions"]:
                    user_screen_name_set.add(user_mention["id"])
        return user_screen_name_set
        
    def get_json(self,tweet_type):

        tweets = []
        tweets_dir = os.path.join(self.dir,tweet_type)
        if(os.path.exists(tweets_dir)):
            file_names = os.listdir(tweets_dir)
            for name in file_names:
                tweet_object = json.load(open(os.path.join(tweets_dir,name)))
                if(tweet_object):
                    tweets.append(tweet_object)
        return tweets

# %%
