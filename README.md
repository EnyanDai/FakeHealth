# FakeHealth
FakeHealth repository is to supplement the paper "[Ginger Cannot Cure Cancer: Battling Fake Health News with a Comprehensive Data Repository](https://arxiv.org/abs/2002.00837)".
This repository (FakeHealth) is collected to address challenges in Fake Health News detection, which includes news contents, news reviews, social engagements and user network. 

## Overviews
Our repository consist of two datasets: HealthStory and HealthRelease. Due to the twitter policy of protecting user privacy, the fullcontents of user social engagements and network are not al-lowed to directly publish. Instead, we store the IDs of all social engagements and related user network into json files, and supplement them with a API to trivially attain the social engagements and user network from twitter. The IDs are stored in `./dataset/engagements/HealthRelease.json` , `./dataset/engagements/HealthStory.json` , `./dataset/user_network/followers/` , and `./dataset/user_network/following/`. Due to the size limitation, the IDs of followers and following is uploaded to [zenodo as version 2 of FakehHealth](https://zenodo.org/record/3606756).

## Requirements
* twython==3.7.0
* [Developer APP](https://developer.twitter.com/en/docs/basics/apps/overview) of twitter to generate `app_key`,`app_secret`,`oauth_token` and `oauth_token_secret`



## Running Code
1. set the `.\API\resources\tweet_keys_file.txt` in the format of:

       app_key,app_secret,oauth_token,oauth_token_secret
       XXXXXX,XXXXXXX,XXXXXXXXX,XXXXXXXXXXXXX
2. Build HealthStory:
   
       python main.py news_type=HealthStory sav_dir=../dataset
3. Build HealthRelease:
   
       python main.py news_type=HealthRelease sav_dir=../dataset

4. Build user network: <br>
   1. Download the `dataset/user_network/followers` and `dataset/user_network/followering` from `https://zenodo.org/record/3606756`.
   2. (optional) Collect the followers and followerings profiles and save it into `dataset/user_network/user_profiles`:
      
          python crawl_friends_profiles.py sav_dir=../dataset
      Note that the number of friends are extremely large. We only recommend you crawl the friends profiles if it is necessary.


## Data Format

The data provided here only cantain the 
The downloaded dataset will have the following  folder structure,
* content
  * HealthStory
    * \<news_id>.json: a list of news contents wich include **URL**, **Title**, **Key words**, **Tags**, **Image URL**, **Author** and **Publishing Date**.
  * HealthRelease.json: ~
* reviews
  * HealthStory.json: a list of news reviews which include **Rating**, **news source**,**description**, **summary of the review**, **ground truth labels of the ten standard criteria**, **explanations of the criteria judgements** and **image link**. 
  * HealthRelease.json: ~
* engagements
  * HealthStory
    * \<news_id>
      * tweets
        * \<ID>.json: The json file of the tweet object. The detailed attributes of tweet object is [here](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/tweet-object).
        * ......
      * retweets
        * \<ID>.json
        * ......
      * replies
        * \<ID>.json
    * HealthRelase
      * ......
* user_network
  * user_profiles
    * \<user_name>.json: The json file of the user profile object. The detailed attributes of user profile object is [here](https://developer.twitter.com/en/docs/tweets/data-dictionary/overview/user-object)
    * ......
  * user_timelines
    * \<user_name>.json: a list of tweet objects
    * ......
  * user_followers
    * \<user_name>.josn: a list of user follower IDs (up to 200 per user)
    * ......
  * user_following
    * \<user_name>.json: a list of user following IDs (up to 5000 per user)
    * ......

## Refercences
If you use the FakeHealth datasets, please cite the following paper:

~~~~
@article{dai2020ginger,
  title={Ginger Cannot Cure Cancer: Battling Fake Health News with a Comprehensive Data Repository},
  author={Dai, Enyan and Sun, Yiwei and Wang, Suhang},
  journal={arXiv preprint arXiv:2002.00837},
  year={2020}
}
~~~~
   
   

