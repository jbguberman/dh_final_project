# Pulls the tweetIDs from an existing CSV file_path.
# Uses the IDs to query the Twitter API to get the
# user who posted the tweet, the hashtags in the tweet,
# and the list of that user's followers/followed users

import csv
import json
from twitter import *
import sys
from time import sleep
from configparser import SafeConfigParser

# pulls the tweet IDs
def get_IDs(csvfile):
    with open(FILE_PATH, 'r',
              encoding='utf-8', errors='ignore') as csvfile:

        fieldnames = ("Date", "Screen Name", "Full Name", "Tweet Text",
                      "Tweet ID", "App", "Followers", "Follows",
                      "Retweets", "Favorites", "Verified", "User Since",
                      "Location", "Bio", "Profile Image", "Google Maps")
        reader = csv.DictReader(csvfile, fieldnames)

        tweetIDs = []
        count = 0
        for row in reader:
            if count > 1:
                tweetIDs.append(row['Tweet ID'])
            count += 1

        return(tweetIDs)

    # This leaves two rows that will need to be ignored when
    # querrying the API. Use counter in `for` loop


# gets the full data for each tweetID
def get_tweet_data(tweet_data, id, api, runs):
    try:
        tweet = api.statuses.show(id=id)
        return(tweet)

    except TwitterHTTPError as e:
        # if rate-limit exceeded, sleep for 15 minutes
        if e.e.code == 429:
            # saves in case something goes wrong
            with open('tmp_data{}.json'.format(str(runs)), 'w') as jsonfile:
                json.dump(tweet_data, jsonfile)
            print("Rate limit exceeded. Sleeping for 15 minutes.")
            sleep(60 * 15)
            tweet = api.statuses.show(id=id)
            return(tweet)
        else:
            print('a problem occcured, recovering and moving on')
            return([''])


def user_check(tweet_data, userID, userIDstr):
    # print('function')

    if tweet_data:
        if userID in tweet_data or userIDstr in tweet_data:
            # print('if cond')
            return('recurring')
        else:
            # print('else cond')
            return('new')
    else:
        # print('no data yet')
        return('new')


def compare_tags(old, new):
    novel_tags = []
    for each in new:
        # print(each)
        if each in old:
            pass
        else:
            # str_each = str(each)
            # str_each = str(each).replace('[]', '')
            old.append(each)
    # print('old: ' + str(old))

    return(old)

# Main function
if __name__ == '__main__':
    # counts number of get/sleep cycles
    runs = 0
    # gets your configuration settings from the config file
    config = SafeConfigParser()
    config.read('settings.cfg')
    FILE_PATH = config.get('settings', 'file_path')

    # connect to the API using OAuth credentials
    # connect to the API using OAuth credentials
    api = Twitter(api_version='1.1',
                  auth=OAuth(config.get('twitter', 'access_token'),
                              config.get('twitter', 'access_token_secret'),
                              config.get('twitter', 'consumer_key'),
                              config.get('twitter', 'consumer_secret')))

    tweetIDs = get_IDs(FILE_PATH)

    tweet_data = {}

    count = 0
    direct = False
    for id in tweetIDs:
        # print(id)
        flag = False
        # get full tweet
        tweet = get_tweet_data(tweet_data, id, api, runs)

        # in case querry returns nothing (i.e., case of deleted tweet)
        try:
            # print('tried')
            userID = tweet['user']['id']
            userIDstr = tweet['user']['id_str']
            screenName = tweet['user']['screen_name']
            hashtags = []
            if tweet['entities']['hashtags']:
                for tag in tweet['entities']['hashtags']:
                    hashtags.append(tag['text'])
                    # print('hashed')
            else:
                # print('no tags')
                flag = True

        except:
            flag = True

        if flag is False:
            # print('flag check passed')
            # gets the hashtags

            usertype = user_check(tweet_data, userID, userIDstr)
            # print(usertype)
            if usertype == 'new':
                # print('new user')
                tweet_data[userID] = {'screen_name': screenName,
                                      'hashtags': hashtags}
                # print('record created for new user')
            elif usertype == 'recurring':
                # print('repeat user')
                temptags = compare_tags(tweet_data[userID]['hashtags'],
                                        hashtags)
                # print(temptags)
                if temptags:
                    tweet_data[userID]['hashtags'] = temptags
                    # print('new tags for user found and added to dict')
                else:
                    pass
                    # print('no new tags for this user found')
            # for each in tweet_data[userID]['hashtags']:
                # print(each)
            # print(tweet_data[userID])
        status = 'working' + ('.' * count)
        print(status)
        if count > 10:
            direct = True
        elif count < 1:
            direct = False
        if direct:
            count -= 1
        elif not direct:
            count += 1


with open('test_data.json', 'w') as jsonfile:
    json.dump(tweet_data, jsonfile)
