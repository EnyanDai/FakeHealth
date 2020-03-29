#%%
import json
import logging
import time
from resource_server.ResourceAllocator import ResourceAllocator
from twython import Twython


class TwythonConnector:

    def __init__(self, key_file):
        self.streams = []
        self.init_twython_objects(key_file)
        self.max_fail_count = 3
        self.keys_state = dict()
        print(len(self.streams))
        self.init_state(len(self.streams))

    def init_state(self,num_keys):

        print("No. of twitter keys : {}".format(num_keys))
        self.keys_state["get_retweet"] = ResourceAllocator(num_keys, time_window=905, window_limit=75)
        self.keys_state["get_tweet"] = ResourceAllocator(num_keys, time_window=905, window_limit=900)
        self.keys_state["get_followers_ids"] = ResourceAllocator(num_keys, time_window=900, window_limit=15)
        self.keys_state["get_friends_ids"] = ResourceAllocator(num_keys, time_window=900, window_limit=15)
        self.keys_state["get_user"] = ResourceAllocator(num_keys, time_window=905, window_limit=900)
        self.keys_state["get_user_tweets"] = ResourceAllocator(num_keys, time_window=925, window_limit=900)

    def init_twython_objects(self, keys_file):
        """
        Reads the keys file and initiates an array of twython objects
        :param keys_file: Twitter keys file
        :return:
        """
        with open(keys_file, 'r') as fKeysIn:
            next(fKeysIn)
            for line in fKeysIn:
                line = line.rstrip().split(',')

                self.streams.append(self._get_twitter_connection(connection_mode=1, app_key=line[0], app_secret=line[1],
                                                                 oauth_token=line[2], oauth_token_secret=line[3]))


    @staticmethod
    def _get_twitter_connection(connection_mode=0, app_key=None, app_secret=None, oauth_token=None,
                                oauth_token_secret=None):
        client_args = {
            'timeout': 30,
        }

        if connection_mode == 1:  # User auth mode
            return Twython(app_key=app_key, app_secret=app_secret, oauth_token=oauth_token,
                           oauth_token_secret=oauth_token_secret, client_args=client_args)

        elif connection_mode == 0:  # App auth mode - more requests are allowed
            # TODO: Fix the code later - app auth has more limit
            # twitter = Twython(app_key, app_secret, oauth_version=2)
            # access_token = twitter.obtain_access_token()
            # return Twython(app_key, access_token=access_token)

            twitter = Twython(app_key, app_secret, oauth_version=2)
            ACCESS_TOKEN = twitter.obtain_access_token()
            twython = Twython(app_key, access_token=ACCESS_TOKEN)
            return twython

    def get_twython_connection(self, resource_type):
        """
        Returns the twython object for making the requests and sleeps if all the twitter keys have reached the usage
        limits
        :return: Twython object for making API calls
        """
        resource_index = self.get_connector_index(resource_type)
        return self.streams[resource_index]

    def get_connector_index(self,resource_type):
        while True:
            alloctor = self.keys_state[resource_type]
            connector_index = alloctor.get_resource_index()
            if(connector_index < 0):
                sleep_time = abs(connector_index)
                print("sleeping for {} seconds".format(sleep_time))
                logging.info("sleeping for {} seconds".format(sleep_time))
                time.sleep(sleep_time)
            else:
                # print("resource id: {}".format(connector_index))
                return connector_index

#%%
