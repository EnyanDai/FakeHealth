#%%
import json
from util.TwythonConnector import TwythonConnector
from util import Constants
from util.util import create_dir, equal_chunks
from twython import TwythonRateLimitError, TwythonAuthError,TwythonError
import os
class UserCollector:
    def __init__(self,root_location,twython_connector):
        self.root_location = root_location
        create_dir(root_location)

        self.twython_connector = twython_connector
        self.user_profiles_dir = os.path.join(self.root_location,"user_profiles")
        self.user_followers_dir = os.path.join(self.root_location,"user_followers")
        self.user_following_dir = os.path.join(self.root_location,"user_following")
        self.user_timelines_dir = os.path.join(self.root_location,"user_timeline_tweets")

    def get_own_user_id(self,dump_dir):
        existed_id_set = set()
        if(os.path.exists(dump_dir)):
            file_names = os.listdir(dump_dir)
            for name in file_names:
                if(name.endswith(".json")):
                    file_id = name.replace(".json",'')
                    existed_id_set.add(int(file_id))
        return existed_id_set

    def collect_user_profiles(self,users):
        dump_location = self.user_profiles_dir
        create_dir(dump_location)

        existed_id_set = self.get_own_user_id(dump_location)
        new_users_set = users - existed_id_set
        print("existed: {}, found: {}, add: {}".format(len(existed_id_set),len(users),len(new_users_set)))
        print("We are adding {} user profiles to {}".format(len(new_users_set),dump_location))

        user_chunks = equal_chunks(list(new_users_set),100)

        number = 0
        for chunk in user_chunks:
            try:
                user_objects_map = self.twython_connector.get_twython_connection(Constants.GET_USER).lookup_user(user_id=chunk,include_entities=True)
                for user_object in user_objects_map:
                    json.dump(user_object, open("{}/{}.json".format(dump_location, user_object["id"]), "w"))
                    
                    number += 1
                print("{} has been added".format(number))
            except TwythonError:
                print("Twythonerror")
            except TwythonRateLimitError:
                print("Twython API rate limit exception")
            except:
                print("Exception")
        print("Finish")

    def collect_user_recent_tweets(self,users):
        """
        users should be a set that you want to crawl
        """
        create_dir(self.user_timelines_dir)
        # users = self.get_own_user_id(self.user_profiles_dir)
        existed_id_set = self.get_own_user_id(self.user_timelines_dir)
        
        
        new_users_set = users - existed_id_set
        print("We are adding {}/{} to user_timelines".format(len(new_users_set),len(users)))

        for i,id in enumerate(new_users_set):
            try:
                time_lines = self.twython_connector.get_twython_connection(Constants.GET_USER_TWEETS).get_user_timeline(user_id=id,count=200)
                json.dump(time_lines, open("{}/{}.json".format(self.user_timelines_dir,id),'w'))
            except TwythonRateLimitError:
                print("Twython API rate limit exception")
            except TwythonAuthError:
                print("{} timelines, we have authorized execption".format(id))
            except:
                print("Other exception")
            if(i%100==0):
                print("{} users timelines are attained".format(i))

    def collect_user_followers(self,users):
        """
        users should be a set that you want to crawl
        """
        create_dir(self.user_followers_dir)
        # users = self.get_own_user_id(self.user_profiles_dir)
        existed_id_set = self.get_own_user_id(self.user_followers_dir)
        
        new_users_set = users - existed_id_set
        print("We are adding {}/{} to {}".format(len(new_users_set),len(users),self.user_followers_dir))

        for i,id in enumerate(new_users_set):
            try:
                save_dir = "{}/{}.json".format(self.user_followers_dir,id)
                followers = self.twython_connector.get_twython_connection(Constants.GET_FOLLOWERS_ID).get_followers_ids(user_id=id,count=200)
                json.dump(followers, open(save_dir,'w'))
            except TwythonRateLimitError:
                print("Twython API rate limit exception")
            except TwythonAuthError:
                print("{} followers, we have authorized execption".format(id))
            except:
                print("Other execption")
            if(i%15==0):
                print("{}/{} followers are attained".format(i,len(new_users_set)))

    def collect_user_follower_profiles(self,follower_dir=None):
        if follower_dir == None:
            follower_dir = self.user_followers_dir
        file_names = os.listdir(follower_dir)

        for i,name in enumerate(file_names):
            followers_object = json.load(open(os.path.join(follower_dir,name),'r'))
            if 'ids' in followers_object:
                ids = set(followers_object['ids'])
                self.collect_user_profiles(ids)
            if i + 1 % 100 == 0:
                print("{} users' followers profiles has been collected".format(i + 1))
                break

    def collect_user_following_profiles(self,following_dir=None):
        if following_dir==None:
            following_dir = self.user_following_dir
        file_names = os.listdir(following_dir)

        for i,name in enumerate(file_names):
            followers_object = json.load(open(os.path.join(following_dir,name),'r'))
            if 'ids' in followers_object:
                ids = set(followers_object['ids'])
                self.collect_user_profiles(ids)
            if i + 1 % 100 == 0:
                print("{} users' followers profiles has been collected".format(i + 1))
                break

    def collect_user_followings(self,users):
        create_dir(self.user_following_dir)
        # users = self.get_own_user_id(self.user_profiles_dir)
        existed_id_set = self.get_own_user_id(self.user_following_dir)
        
        new_users_set = users - existed_id_set
        print("We are adding {}/{} to {}".format(len(new_users_set),len(users),self.user_following_dir))

        for i,id in enumerate(new_users_set):
            try:
                save_dir = "{}/{}.json".format(self.user_following_dir,id)
                friends = self.twython_connector.get_twython_connection(Constants.GET_FRIENDS_ID).get_friends_ids(user_id=id,count=5000)
                json.dump(friends, open(save_dir,'w'))
            except TwythonRateLimitError:
                print("Twython API rate limit exception")
            except TwythonAuthError:
                print("{} following, we have authorized execption".format(id))
            except:
                print("other execption")
            if(i%15==0):
                print("{}/{} following are attained".format(i,len(new_users_set)))
#%%
# import json
# from collect_tweets import TweetCollector

# config = json.load(open("config.json"))
# connector = TwythonConnector(config["tweet_keys_file"])
# news_type = config["data_collection_choice"][0]
# with open(news_type,"r",encoding="utf-8") as f:
#     articles = json.load(f)
# user_collector = UserCollector(config["dump_location"],connector)
# # users = set()
# # for i,article in enumerate(articles[0:1700]):
# #     tweet_collector = TweetCollector(config["dump_location"], news_type,article,connector)
# #     user_id_set = tweet_collector.get_own_user_id()
# #     users.update(user_id_set)
# # print("{} users founded".format(len(users)))
# # user_collector.collect_user_profiles(users)
# user_collector.collect_user_followers()

# %%
