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
from collections import Counter


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


def get_tweet_data(tweetIDs, api):

    the_data = {}



    for id in tweetIDs:
        count = 0
        print('the count is ' + str(count))
        try:
            # gets the tweet corresponding to the id
            fullTweet = api.statuses.show(id=id)
            print('got a tweet!')

            # print(fullTweet['id'])

            # not sure which to use in the following ocnditional
            userID = fullTweet['user']['id']
            userIDstr = fullTweet['user']['id_str']
            screenName = fullTweet['user']['screen_name']
            hashtags = []

            print(str(len(fullTweet['entities']['hashtags'])) + 'found')
            for each in fullTweet['entities']['hashtags']:
                hashtags.append(each['text'])

            # checks to see if user is already in dict

            if len(the_data) <= 0:
                usernum = "user{}".format(count)
                print('new user found ---- zero')
                the_data[usernum] = {'user_id': '', 'screen_name': '', 'hashtags': ''}
                the_data[usernum]['user_id'] = userID
                the_data[usernum]['screen_name'] = screenName
                the_data[usernum]['hashtags'] = hashtags

                print('got screen name and hashtags! moving on')

            else:
                for key in list(the_data):
                    print('check2')
                    print('key is:' + str(key))
                    # if user in dict, see if tweet contains any new
                    # hashtags not already in dict
                    if key == userID | key == userIDstr:

                        print('this user exists within data')

                        existing = key['hashtags']
                        compared = existing.subtract(hashtags)

                        if compared:
                            print('new hashtags added for this user, moving on')
                            key['hashtags'].append(compared)


                        else:
                            print('no new hashtags for this user, moving on')


                    else:
                        print('new user found --- non-zero')
                        the_data[usernum] = {'user_id': '', 'screen_name': '', 'hashtags': ''}
                        the_data[usernum]['user_id'] = userID
                        the_data[usernum]['screen_name'] = screenName
                        the_data[usernum]['hashtags'] = hashtags

                        print('got screen name and hashtags! moving on')
            count += 1

        except TwitterHTTPError as e:
            # if rate-limit exceeded, sleep for 15 minutes
            if e.e.code == 429:
                print("Rate limit exceeded. Sleeping for 15 minutes.")
                sleep(60 * 15)

    return(the_data)

# Main function
if __name__ == '__main__':
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

    #with open('tweetIDs.txt', 'w') as textfile:
    #    for each in tweetIDs:
    #        textfile.write(each + '\n')

    tweet_data = get_tweet_data(tweetIDs, api)

    # saves the data in a JSON file_path
    with open('the_data.json', 'w') as jsonfile:
        json.dump(tweet_data, jsonfile)
