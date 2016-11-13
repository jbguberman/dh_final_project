import csv
import json
import requests
import sys
from twitter import *
from configparser import SafeConfigParser


# Converts CSV to JSON (adapted from
# http://stackoverflow.com/questions/19697846/python-csv-to-json)
def csv_to_json(yourfile):
    with open(yourfile, 'r',
              encoding='utf-8', errors='ignore') as csvfile:
        with open('file.json', 'w') as jsonfile:
            fieldnames = ("Date", "Screen Name", "Full Name", "Tweet Text",
                          "Tweet ID", "App", "Followers", "Follows",
                          "Retweets", "Favorites", "Verified", "User Since",
                          "Location", "Bio", "Profile Image", "Google Maps")
            reader = csv.DictReader(csvfile, fieldnames)
            for row in reader:
                # row = make_unicode(row)
                json.dump(row, jsonfile)
                jsonfile.write('\n')
    # This leaves two rows that will need to be ignored when
    # querrying the API. Use counter in `for` loop


def get_tags():
    with open('jsonfile', 'r') as json_data:
        tweets = json.load(json_data)

    # for loop counter
    count = 0

    for each in tweets:
        if count > 1:
            # Get hashtags for tweets
            # write hashtags to json
        count += 1

# Main function
if __name__ == '__main__':
    # gets your configuration settings from the config file
    config = SafeConfigParser()
    config.read('settings.cfg')
    FILE_PATH = config.get('settings', 'file_path')

    csv_to_json(FILE_PATH)

    # connect to the API using OAuth credentials
    api = Twitter(api_version='1.1', auth=OAuth(config.get('twitter', 'access_token'),
                  config.get('twitter', 'access_token_secret'),
                  config.get('twitter', 'consumer_key'),
                  config.get('twitter', 'consumer_secret')))

    
