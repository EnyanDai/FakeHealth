#%%
import json
from util.TwythonConnector import TwythonConnector
from util import Constants
from twython import TwythonError, TwythonRateLimitError
import logging
from util.util import create_dir

#%%
import os
class TweetCollector:

    def __init__(self, root_location, news_type,news_id,engagements,twython_connector):

        self.root_location = root_location
        self.twython_connector = twython_connector
        self.news_type = news_type
        self.news_id = news_id
        self.engagements = engagements
        self.dump_dir = "{}/{}/{}/{}".format(self.root_location,"engagements",self.news_type,self.news_id)

    def get_tweets(self):
        dump_dir = os.path.join(self.dump_dir,"tweets")
        self.collect_tweets2dir(dump_dir,self.engagements["tweets"])

    def get_replies(self):
        dump_dir = os.path.join(self.dump_dir,"replies")
        self.collect_tweets2dir(dump_dir,self.engagements["replies"])

    def get_retweets(self):
        dump_dir = os.path.join(self.dump_dir,"retweets")
        self.collect_tweets2dir(dump_dir,self.engagements["retweets"])

    @staticmethod
    def get_tweetID_from_dir(dump_dir):
        existed_tweet_set = set()
        if(os.path.exists(dump_dir)):
            file_names = os.listdir(dump_dir)
            for name in file_names:
                if(name.endswith(".json")):
                    file_id = int(name.replace(".json",''))
                    existed_tweet_set.add(file_id)
        return existed_tweet_set

    def dump_tweet_information(self,tweet_chunk, dump_dir):
        """Collect info and dump info of tweet chunk containing atmost 100 tweets"""
        try:
            tweet_objects_map = self.twython_connector.get_twython_connection(Constants.GET_TWEET).lookup_status(id=tweet_chunk,
                                                                                                        include_entities=True,
                                                                                                        map=True)['id']
            for tweet_id in tweet_chunk:
                tweet_object = tweet_objects_map[str(tweet_id)]
                if tweet_object:
                    create_dir(dump_dir)

                    json.dump(tweet_object, open("{}/{}.json".format(dump_dir, tweet_id), "w"))

        except TwythonRateLimitError:
            logging.exception("Twython API rate limit exception")

        except Exception as ex:
            logging.exception("exception in collecting tweet objects")

        return None

    def collect_tweets2dir(self,dump_dir,tweet_ids):
        search_tweet_set = set(tweet_ids)
        if(os.path.exists(dump_dir)):
            existed_tweet_set = self.get_tweetID_from_dir(dump_dir)
            search_tweet_set = search_tweet_set - existed_tweet_set
        else:
            existed_tweet_set = set()
            create_dir(dump_dir)
        print("{} tweets will be added, {} searched, {} existed".format(len(search_tweet_set),len(tweet_ids),len(existed_tweet_set)))
        from util.util import equal_chunks
        chunks = equal_chunks(list(search_tweet_set),chunk_size=100)
        for tweet_chunk in chunks:
            self.dump_tweet_information(tweet_chunk,dump_dir)

    @staticmethod
    def get_user_tweet_dir(dump_dir):
        user_screen_name_set = set()
        if(os.path.exists(dump_dir)):
            file_names = os.listdir(dump_dir)
            for name in file_names:
                if(name.endswith(".json")):
                    tweet_object = json.load(open(os.path.join(dump_dir,name)))
                    if("user" in tweet_object):
                        user_screen_name_set.add(tweet_object["user"]["screen_name"])
        return user_screen_name_set


# %%
