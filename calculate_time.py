"""
def time_stamp():

    Simple function that prints a specifically formatted time stamp string..
    It returns it in the format [MM/DD/YYYY - HR:MIN:SEC]

"""
def time_stamp():
    PM_AM = "AM"
    local_time = time.localtime(time.time())
    # Extract the necessary parameters
    year = str(local_time.tm_year)
    month = str(local_time.tm_mon)
    day = str(local_time.tm_mday)

    hour = str(local_time.tm_hour)
    if (int(hour) >= 12):
        hour = str(int(hour) - 12)
        PM_AM = "PM"

    if int(hour) == 0:
        hour = str(12)

    min = str(local_time.tm_min)
    if (int(min) < 10):
        min = "0" + min

    sec = str(local_time.tm_sec)
    if (int(sec) < 10):
        sec = "0" + sec

    # Format the time stamp properly.
    time_stamp = "[" + month + "/" + day + "/" + year + " - " + hour + ":" + min + ":" + sec + " " + PM_AM + "]"
    print(time_stamp)
    return time_stamp

"""
def token_extract(filename):

    filename : A string with the filename and extension of the text file containing
               containing the OAuth access keys/tokens/secrets for the Twitter API.

    Function parses oAuth keys text file for the relevant access tokens and consumer keys.
    The text file must be in the same directory as the script. In addition, the
    keys must be in the following format with the proper identifiers...
    (Not necessarily in the the displayed order)

            consumer_key = #######
            consumer_secret = ######
            access_token = ######
            access_token_secret = ######

    The function returns an array containing the key strings...
            [consumer_key, consumer_secret, access_token, access_token_secret]


"""
def token_extract(filename):

    with open(filename,"r") as file: # open the file in readonly
        contents = file.readlines()
        for line in contents:
            lineStrip = line.strip() # remove whitespace from each line
            splitLine = lineStrip.split(" ") # Split the string based on spaces and place in array

            # Read the identifier (which is always the first string)
            # Then get the alpha-numeric key which is always the last element.
            if splitLine[0] == "consumer_key":
                consumer_key = splitLine[-1]
            if splitLine[0] == "consumer_secret":
                consumer_secret = splitLine[-1]
            if splitLine[0] == "access_token":
                access_token = splitLine[-1]
            if splitLine[0] == "access_token_secret":
                access_token_secret = splitLine[-1]


    token_array = [consumer_key, consumer_secret, access_token, access_token_secret]
    return token_array

"""
Function that determines if the current time is between two specified times.
It requires two inputs:
    lower - integer - the lower time bound in MILITARY time. Required to be in military time for function to
                      work properly
    upper - integer - the upper time bound, also in military time

The function will return a logical boolean value, True or False. IF the current time does fall between
our bounds, it returns true, else it returns false.

"""
def time_is_between(lower,upper):
    #determine if a time of day is between two hours
    #first get local time and convert to military time
    local_time = time.localtime(time.time())
    local_mil_time = local_time.tm_hour*100 + local_time.tm_min

    if (local_mil_time >= lower) and (local_mil_time <= upper):
        return True

    return False #return false if not caught by if statement

def time_addition(night_low,night_high,morn_low,morn_high):
    #get the current time
    local_time = time.localtime(time.time())
    local_mil_time = local_time.tm_hour*100 + local_time.tm_min

    #check where the time is and return the appropriate value
    if time_is_between(0,night_low-1):
        return int(0)

    elif time_is_between(night_low,night_high-1):
        return 2*(local_mil_time - night_low)/(night_high - night_low)

    elif time_is_between(night_high,morn_low-1):
        return 2

    elif time_is_between(morn_low,morn_high-1):
        return 2*(1 - ((local_mil_time - morn_low)/(morn_high - morn_low)))
    else:
        return int(0) #catch everything else.

def post_freq():
    num_posts = 50

    #Get the 50 newest posts in the DunderMifflin SubReddit
    new_posts = reddit.subreddit("DunderMifflin").new(limit=num_posts)
    time_list = []
    
    for submission in new_posts:
        time_list.append(submission.created_utc)

    del_t = max(time_list) - min(time_list) #time change in seconds
    del_t = del_t/60/60 #time change in hrs

    rate = num_posts/del_t

    return rate

def rate_addition(rate):
    #determine how much time to add

    if rate > 20: #new posts per hour
        return int(0) #return 0 hours added
    elif 10 <= rate <= 20:
        return 1
    else:
        return 2 # return two if rate is less than 20 new pe hour

def all_time_upvotes():
    top_all_time = reddit.subreddit("DunderMifflin").top(limit=5)
    for post in top_all_time:
        top_upvotes_alltime = post.score
        break

    return top_upvotes_alltime

def hot_upvote_avg(num_posts):
    hot_posts = reddit.subreddit("DunderMifflin").hot(limit=num_posts)
    num_upvotes = 0

    for post in hot_posts:
        num_upvotes = num_upvotes + post.score

    upvote_avg = num_upvotes/num_posts

    return upvote_avg

def hot_buzz_addition(top_upvotes,hot_upvote_avg):
    hrs_2_give = 1

    return (hrs_2_give)*(1- (hot_upvote_avg/top_upvotes))

def main():
    wait_time = 1
    time_add = time_addition(100,300,800,1000)
    rate_add = rate_addition(post_freq())
    hot_add = hot_buzz_addition(all_time_upvotes(),hot_upvote_avg(2))

    print("Calculating wait time...")
    print("Time added from local_time: ", time_addition(100,300,800,1000))
    print("Time added from post_freq: ", rate_addition(post_freq()), "(",post_freq()," posts/hr)")
    print("Time added from hot post buzz: ",hot_buzz_addition(all_time_upvotes(),hot_upvote_avg(2)))
    print("-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=--=-=-=")
    print("Total Wait Time: ",wait_time + time_add + rate_add + hot_add, " hours\n")

    return wait_time + time_add + rate_add + hot_add

#Import necessary modules
import praw
import urllib.request
import tweepy
import os
import time
import sys
import random
from colorama import init,Fore
init()

# authenticate twitter app and API
# print(Fore.GREEN + "Authenticating Twitter API...")
# apiKeyFile = "..//..//oAuth_keys.txt"
# consumer_key, consumer_secret, access_token, access_token_secret = token_extract(apiKeyFile)
# auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
# auth.set_access_token(access_token,access_token_secret)
# api = tweepy.API(auth)
# print(Fore.GREEN + "Authentication Success!")

#authenticate reddit app
print(Fore.GREEN + "\nAuthenticating Reddit API for wait calculations...")
reddit = praw.Reddit(client_id="VO3nsWUK9UBV8g",
                     client_secret = "nyoXYhUFnqo7Axo2dkmnVxywga0",
                     user_agent = "pawsibility")
print(Fore.GREEN + "Authentication Success!\n")
