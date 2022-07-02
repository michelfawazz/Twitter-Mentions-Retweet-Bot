#create a twitter bot that retweesm tweets that contain a certain keyword


import tweepy
import time
import os
import sys
import json


# Twitter API credentials
# 
consumer_key = "env"
consumer_secret = "env"
access_key = "env"
access_secret = "env"

bearer_token = "env"
since_id = "env"

users = "@userMentioned -from:BotThatretweets"

id = 1539730546112200711

# Create the api endpoint ith oauth2
client = tweepy.Client(bearer_token=bearer_token)
#access token and access secret
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_key, access_secret)
api = tweepy.API(auth)


# The url to use for quote retweets
url_status = "https://twitter.com/twitter/statuses/"



class Linstener(tweepy.StreamingClient):
    def on_connect(self):
        """
        It prints "Connected to Twitter" when the connection is established.
        """
        print("Connected to Twitter")

    
           

    def on_tweet(self, tweet):
        """
        If the tweet id is not in the text file, then add it to the text file and retweet the tweet
        
        :param tweet: The tweet object that is returned by the Twitter API
        :return: The tweet is being returned
        """
        #check who the author
        print(tweet)
        #check if tweet id is in the textfile  if it is then skip
        with open("tweets.txt", "r") as f:
            if str(tweet.id) in f.read():
                print("Tweet already exists")
                return


            
            else:
                print("New Tweet")
                with open("tweets.txt", "a") as f:
                    f.write(str(tweet.id) + "\n")
                #retweet the tweet
                userr= api.get_user(user_id=1539730546112200711)
                statusescountvalue = userr.statuses_count +1
                print(statusescountvalue)

                status_url = url_status + str(tweet.id)
                api.update_status(f"{statusescountvalue}",attachment_url=status_url)
                print("Retweeted")

   

    def on_error(self, status_code):
        """
        If the status code is not 200, print the error code and return True.
        
        :param status_code: The HTTP status code returned
        :return: The on_data method of the StreamListener is called when new data arrives. The on_error
        method is called when an error occurs.
        """
        print("Error: " + str(status_code))
        return True

    
# Creating a new instance of the Linstener class.
stream_tweet = Linstener(bearer_token=bearer_token)




#get rules and delete them
rules = stream_tweet.get_rules()
print(rules)

# save the rule id in a list 
if rules.data != None:
    rule_ids = []
    for rule in rules.data:
        rule_ids.append(rule.id)
        print(rule.id)


    print("deleteing rules")

    #delete all rules
    stream_tweet.delete_rules(rule_ids)
    rules = stream_tweet.get_rules()
    print(rules)


#create rule for when user mentions a user
stream_tweet.add_rules(tweepy.StreamRule(value=users))
stream_tweet.filter()


#start stream
stream_tweet


