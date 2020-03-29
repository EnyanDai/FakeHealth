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

    def get_own_user_screen_name(self,dump_dir):
        existed_screen_name_set = set()
        if(os.path.exists(dump_dir)):
            file_names = os.listdir(dump_dir)
            for name in file_names:
                if(name.endswith(".json")):
                    file_id = name.replace(".json",'')
                    existed_screen_name_set.add(file_id)
        return existed_screen_name_set

    def collect_user_profiles(self,users):
        dump_location = self.user_profiles_dir
        create_dir(dump_location)

        existed_screen_name_set = self.get_own_user_screen_name(dump_location)
        new_users_set = users - existed_screen_name_set
        print("existed: {}, found: {}, add: {}".format(len(existed_screen_name_set),len(users),len(new_users_set)))
        print("We are adding {} user profiles to {}".format(len(new_users_set),dump_location))

        user_chunks = equal_chunks(list(new_users_set),100)

        number = 0
        for chunk in user_chunks:
            try:
                user_objects_map = self.twython_connector.get_twython_connection(Constants.GET_USER).lookup_user(screen_name=chunk,include_entities=True)
                for user_object in user_objects_map:
                    json.dump(user_object, open("{}/{}.json".format(dump_location, user_object["screen_name"]), "w"))
                    
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
        # users = self.get_own_user_screen_name(self.user_profiles_dir)
        existed_screen_name_set = self.get_own_user_screen_name(self.user_timelines_dir)
        
        
        new_users_set = users - existed_screen_name_set
        print("We are adding {}/{} to user_timelines".format(len(new_users_set),len(users)))

        for i,screen_name in enumerate(new_users_set):
            try:
                time_lines = self.twython_connector.get_twython_connection(Constants.GET_USER_TWEETS).get_user_timeline(screen_name=screen_name,count=200)
                json.dump(time_lines, open("{}/{}.json".format(self.user_timelines_dir,screen_name),'w'))
            except TwythonRateLimitError:
                print("Twython API rate limit exception")
            except TwythonAuthError:
                print("{} timelines, we have authorized execption".format(screen_name))
            except:
                print("Other exception")
            if(i%100==0):
                print("{} users timelines are attained".format(i))

    def collect_user_followers(self,users):
        """
        users should be a set that you want to crawl
        """
        create_dir(self.user_followers_dir)
        # users = self.get_own_user_screen_name(self.user_profiles_dir)
        existed_screen_name_set = self.get_own_user_screen_name(self.user_followers_dir)
        
        new_users_set = users - existed_screen_name_set
        print("We are adding {}/{} to {}".format(len(new_users_set),len(users),self.user_followers_dir))

        for i,screen_name in enumerate(new_users_set):
            try:
                save_dir = "{}/{}.json".format(self.user_followers_dir,screen_name)
                followers = self.twython_connector.get_twython_connection(Constants.GET_FOLLOWERS_ID).get_followers_list(screen_name=screen_name,count=200)
                json.dump(followers, open(save_dir,'w'))
            except TwythonRateLimitError:
                print("Twython API rate limit exception")
            except TwythonAuthError:
                print("{} followers, we have authorized execption".format(screen_name))
            except:
                print("Other execption")
            if(i%15==0):
                print("{}/{} followers are attained".format(i,len(new_users_set)))

    def collect_user_followings(self,users):
        create_dir(self.user_following_dir)
        # users = self.get_own_user_screen_name(self.user_profiles_dir)
        existed_screen_name_set = self.get_own_user_screen_name(self.user_following_dir)
        
        new_users_set = users - existed_screen_name_set
        print("We are adding {}/{} to {}".format(len(new_users_set),len(users),self.user_following_dir))

        for i,screen_name in enumerate(new_users_set):
            try:
                save_dir = "{}/{}.json".format(self.user_following_dir,screen_name)
                friends = self.twython_connector.get_twython_connection(Constants.GET_FRIENDS_ID).get_friends_list(screen_name=screen_name,count=200)
                json.dump(friends, open(save_dir,'w'))
            except TwythonRateLimitError:
                print("Twython API rate limit exception")
            except TwythonAuthError:
                print("{} following, we have authorized execption".format(screen_name))
            except:
                print("other execption")
            if(i%15==0):
                print("{}/{} following are attained".format(i,len(new_users_set)))

# %%
