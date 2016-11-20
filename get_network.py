import json
from twitter import *
from time import sleep
from configparser import SafeConfigParser


def get_followers(userID, screen_name, api):
    followers = api.followers.ids(screen_name=screen_name,
                                  user_id=userID)
    ids = []
    for each in followers['ids']:
        ids.append(each)
    return(ids)


def get_friends(userID, screen_name, api):
        friends = api.friends.ids(screen_name=screen_name,
                                      user_id=userID)
        ids = []
        for each in friends['ids']:
            ids.append(each)
        return(ids)

if __name__ == '__main__':
    # gets your configuration settings from the config file
    config = SafeConfigParser()
    config.read('settings.cfg')
    # FILE_PATH = config.get('settings', 'json_path')
    FILE_PATH = '/Users/Josh/Documents/dh_final_project/thedata.json'

    # connect to the API using OAuth credentials
    # connect to the API using OAuth credentials
    api = Twitter(api_version='1.1',
                  auth=OAuth(config.get('twitter', 'access_token'),
                              config.get('twitter', 'access_token_secret'),
                              config.get('twitter', 'consumer_key'),
                              config.get('twitter', 'consumer_secret')))

    # loads json file w/ data already collected into memory
    with open(FILE_PATH) as json_data:
        tweet_data = json.load(json_data)

    # gets followers
    for user in tweet_data:
        screen_name = tweet_data[user]['screen_name']
        followers = get_followers(user, screen_name, api)

        tweet_data[user].update({'followers': followers})

    # get friends
        friends = get_friends(user, screen_name, api)

        tweet_data[user].update({'friends': friends})

    with open('sample.json', 'w') as json_data:
        json.dump(tweet_data, json_data)
