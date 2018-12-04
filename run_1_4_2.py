# -*- coding: utf-8 -*-
"""
Created on Fri Jun 22 16:11:28 2018

@author: Nathan LeRoy

Version 1.4.1
	- You can now use command line arguments to specify program running conditions instead of editing source code
	- the flag, -t, indicates TESTING MODE (no posting to twitter or history updating)
	- the flag, -f, indicates FOLLOW MODE (follows users in between posts)
	- the flag, -u, indicates UNFOLLOW MODE (unfollows users in between posts)
	- You can use any combination of the flags in any order. It also recognizes invalid flags.

Version 1.4.0
	- Now includes support for gif retrieving and posting!
	- Added file naming conventions and conditions to catch gifs and appropriately retreive them
	- Also updated some file naming conventions (see get file name)
	- Added support to identify and skip video posts. Currently, videos are not suported due to the
	  way that reddit chooses to host them. Perhaps in the future they can be implemented.

Version: 1.3.3
	- Added color to some print statements to differnetiate from key processes and procedural
	  methods

Version: 1.3.2
	- Fixed issue where bot would scipt unfollow script if the follow script was enabled
	- Added a testing mode. If testing mode is set to True, then the bot will not post or retrieve
	  picutures. It will only simulate the act of doing so

Version: 1.3.1
	- Removed 'The Office' search tag as too many Trump supporters were following the bot,
	and the timeline/following of the bot was becoming very politically charged

Version: 1.3.0
	- Now includes follow mode
	- Will follow users of tweets from a pre-defined search tag
	- Follows a set number of accounts every 6th post
	- Hope is to soon introduce follow criteria, to make it more strategic

"""

# Function Definitions
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
def get_time_filename():

    This function will generate a filename for the picture extracted from redditself.
    It takes no inputs. It gets the time and date from the system and generates a
    string of the format YYYY_MM_DD-HR_MIN_SEC

    Function requires the time module to be imported

"""
def get_time_filename(url):

    local_time = time.localtime(time.time()) #get local time in pythonic format

    # Extract the necessary parameters
    year = str(local_time.tm_year)
    month = str(local_time.tm_mon)
    day = str(local_time.tm_mday)

    hour = str(local_time.tm_hour)
    min = str(local_time.tm_min)
    sec = str(local_time.tm_sec)

    #Create the filename based on url conditions (gif v jpg)
	#The file extensions must be included to avoid raising tweepy errors for lack of file-type.
    if not (url.endswith(".gif") or url.endswith(".gifv") or ("gfycat" in url)):
        filename = year + "_" + month + "_" + day + "-" + hour + "_" + min + "_" + sec + ".png"

    if url.endswith(".gif") or url.endswith(".gifv") or ("gfycat" in url):
        filename = year + "_" + month + "_" + day + "-" + hour + "_" + min + "_" + sec + ".gif"

    return filename

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
def sleeper(time_mesh,interval):

	time_mesh = array of time points to iterate through and update console
				to notify function is still sleeping

	interval = time between timepoints in time_mesh

	Simple function that sleeps the bot. It requires a time_mesh and a time interval.
	It will sleep the bot and it will give an update after every pre-defined
	interval, with the amount of time left until it posts again.

	The function returns nothing (void)

"""
def sleeper(time_mesh,interval):

	for time_point in time_mesh:
		print(str(int(time_point/60)) + " minutes until next post . . .")
		time.sleep(interval)

	return


"""
def update_history(pic_url_name):

	pic_url_name = A string that contains the alphanumeric string from
				   the Reddit picture's url.


	This function will update the text file that logs and keeps track of all posts made.
	The file is used to ensure that there are no reposts.

	The function returns nothing (void)

"""
def update_history(pic_url_name):

	with open("./" + "picture_history.txt", "a") as f:
		f.write(pic_url_name + "\n") # Not repost, so write new pic name to log

	return

def post2twitter(file_storage_name,submission):

	print("Posting to twitter... ")
	api.update_with_media("./pictures/" + file_storage_name, submission.title + "   " + submission.shortlink)

	return

def retrieve_file(pic_url_name,filename):

	print("Retrieving file...  " + pic_url_name)
	file_storage_name = pic_url_name + "-" + filename
	urllib.request.urlretrieve(submission.url,"./pictures/" + file_storage_name)

	return file_storage_name

def check_repost(pic_url_name):
	with open("./" + "picture_history.txt", "r") as f:
		repost = 0 # assume not repost
		pic_names = f.readlines() #extract contents
		# Check each line in the file for an instance of the most recently found photo
		for name in pic_names:
			name_stripped = name.strip()
			if name_stripped == pic_url_name:
				print("Picture already posted! Skipping to next post...  ")
				repost = 1
	return repost


def log_err(err,script_start_time):
	with open("./" + "crash_log.txt", "a") as f:
		if hasattr(err, 'message'):
			f.write("\n" + "Start: " + script_start_time + "\n")
			f.write("End: " + time_Stamp())
			f.write(err.message + "\n")
		else:
			f.write("\n" + "Start: " + script_start_time + "\n")
			f.write("End: " + time_Stamp())
			f.write(err + "\n")
	return

def run_follow(tags,limit,pause):

	tag = random.choice(tags)

	print("Following users of tweets containing",tag) # tell user what type of tweets are being examined
	#Get list of users from certain tweet search
	tweet_list = tweepy.Cursor(api.search,q=tag).items(limit)
	for tweet in tweet_list:
		try:
			print("\nTweet found:")
			print(tweet.text)
			api.create_friendship(tweet.author.screen_name)
			print("Followed: " + tweet.author.screen_name + "\n")
			time.sleep(pause) # wait ten minutes before following new user

		except tweepy.error.TweepError:
			print(" ")
			print("Probable limit exceeding")
			time.sleep(15*60)
			continue
	return

def run_follow(tags,limit,pause):

	tag = random.choice(tags)

	print("Following users of tweets containing",tag) # tell user what type of tweets are being examined
	#Get list of users from certain tweet search
	tweet_list = tweepy.Cursor(api.search,q=tag).items(limit)
	for tweet in tweet_list:
		try:
			print("\nTweet found:")
			print(tweet.text)
			api.create_friendship(tweet.author.screen_name)
			print("Followed: " + tweet.author.screen_name + "\n")
			time.sleep(pause) # wait ten minutes before following new user

		except tweepy.error.TweepError:
			print(" ")
			print("Probable limit exceeding")
			time.sleep(15*60)
			continue
	return

def run_unfollow(limit,pause):

	print("Begining unfollow script . . .") # tell user that the bot is running the unfollow script
	#Get list of users from certain tweet search
	followers = tweepy.Cursor(api.friends, screen_name="rDunderMifflin").items(limit)
	print(limit, "users to unfollow.\n")
	for user in followers:
		try:
			api.destroy_friendship(user.screen_name)
			print("unfollowed: " +  user.screen_name + "\n")
			time.sleep(pause) # wait before following new user

		except tweepy.error.TweepError:
			print(" ")
			print("Probable limit exceeding")
			time.sleep(15*60)
			continue
	return

#function to check the arguments passed to our script from the command line
def check_args():
	#define the program name and pass arguments to a list
	program_name = sys.argv[0]
	arguments = sys.argv[1:]

	#set inner-script-functions to off (false) by default
	testing_mode = False
	follow_mode = False
	unfollow_mode = False

	#Check to make sure there werent any invalid arguments passed
	for arg in arguments:
		if (arg != "-t") and (arg != "-f") and (arg != "-u"):
			raise IOError("Invalid argument flag!")

	#check arguments and create script settings
	for arg in arguments:
		if arg == "-t":
			print(Fore.YELLOW + '[RUNNING IN TESTING MODE - NOTHING WILL BE POSTED]')
			testing_mode = True
		if arg == "-f":
			print(Fore.YELLOW + '[RUNNING WITH FOLLOW MODE - WILL FOLLOW USERS BETWEEN POSTS]')
			follow_mode = True
		if arg == "-u":
			print(Fore.YELLOW + '[RUNNING WITH UNFOLLOW MODE - WILL UNFOLLOW USERS BETWEEN POSTS]')
			unfollow_mode = True

		# store script parameters into a list to return back.
	params = [testing_mode, follow_mode, unfollow_mode]

	time.sleep(1)
	print("|")
	time.sleep(1)
	print("|")
	time.sleep(1)
	print("|\n" + Fore.WHITE)

	return params #return to main

#Import necessary modules
import praw
import urllib.request
import tweepy
import os
import time
import sys
import random
from colorama import init,Fore
import calculate_time

init()

script_start_time = time_stamp()

# authenticate twitter app and API
print(Fore.GREEN + "Authenticating Twitter API...")
apiKeyFile = "oAuth_keys.txt"
consumer_key, consumer_secret, access_token, access_token_secret = token_extract(apiKeyFile)
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token,access_token_secret)
api = tweepy.API(auth)
print(Fore.GREEN + "Authentication Success!")


# authenticate reddit app
print(Fore.GREEN + "Authenticating Reddit API...")
reddit = praw.Reddit(client_id="VO3nsWUK9UBV8g",
                     client_secret = "nyoXYhUFnqo7Axo2dkmnVxywga0",
                     user_agent = "pawsibility")

print(Fore.GREEN + "Authentication Success!\n")

#define parameters
wait_time = 60*60*2 # 2 Hours in seconds
interval = 5*60 # 5 minutes in seconds
upvote_min = 100
follow_lim = 2
follow_flag = follow_lim # initialize flag for running follow sripts
unfollow_lim = 2
unfollow_flag = unfollow_lim #initialize flag for running unfollow scripts
num_updates = int(wait_time/interval)
time_mesh = [wait_time - interval * float(i) for i in range(num_updates)]
testing_mode, follow_mode, unfollow_mode = check_args()

while (True): # use ctrl-c KeyboardInterrupt to cancel program execution
	wait_time = calculate_time.main()*60*60 # convert from hours to seconds
	num_updates = int(wait_time/interval)
	time_mesh = [wait_time - interval * float(i) for i in range(num_updates)]
	print(Fore.BLUE + "[POSTING MODE - BEGIN]" + Fore.WHITE)
	print("Refreshing hot post queue... \n")
	post_count = 0
	repost_count = 0
	for submission in reddit.subreddit("DunderMifflin").hot(limit=15):

		repost = 0 # Flag that represents whether or not a newly found posthas been posted to the profile

		# Check for either stickied posts, or non-photo posts
		if submission.stickied == 1 or submission.selftext:
			print("Skipping stickied submission or non-photo")
			continue # Skip submission

		if submission.is_video:
			print("Video found. Video not currently supported with v 1.4.0... \n")

		if submission.stickied == 0 and (not submission.selftext):
			time_stamp()
			print("Accessing submission...  " + submission.url)
			pic_url_name = submission.url.split("/")[-1] # Snag the picture name from the url
			repost = check_repost(pic_url_name)

			if repost:
				repost_count += 1
				print("\n")
				continue # Skip if repost

			upvotes = submission.ups

			if upvotes <= upvote_min:
				print("Insufficient upvote count (%d/%d)... Skipping to next post\n" % (upvotes, upvote_min))
				continue

			url = submission.url.strip() # get full url to photo
			filename = get_time_filename(submission.url)

			try:
				file_storage_name = retrieve_file(pic_url_name,filename)
				print("File saved as " + file_storage_name)
				if testing_mode == False:
					post2twitter(file_storage_name,submission)

				print("Posted to Twitter!")
				post_count += 1

				if testing_mode == False:
					update_history(pic_url_name)

				follow_flag += 1
				unfollow_flag += 1


			except tweepy.error.TweepError as err:
				update_history(pic_url_name)
				print(Fore.RED + "Raised Tweepy Error... ")
				if hasattr(err, 'message'):
					print(err.message)
					print(Fore.RED + "Skipping post...\n" + Fore.WHITE)
				else:
					print(err)
					print(Fore.RED + "Skipping post...\n" + Fore.WHITE)
				continue

			except urllib.error.HTTPError as err:
				update_history(pic_url_name)
				print(Fore.RED + "Raised HTTPE Error, skipping post..." + Fore.WHITE)
				if hasattr(err, 'message'):
					print(err.message)
					print(Fore.RED + "Skipping post...\n" + Fore.WHITE)
				else:
					print(err)
					print(Fore.RED + "Skipping post...\n" + Fore.WHITE)
				continue

			except Exception as err:
				print(Fore.RED + "Unknown Error Found..." + Fore.WHITE)
				print(err)
				log_err(err.script_start_time)
				sys.exit()

			if (follow_flag >= follow_lim) and (follow_mode == True):
				try:
					follow_flag = 0 # reset flag
					print(Fore.BLUE + "\n[FOLLOW MODE - BEGIN]" + Fore.WHITE)
					tags = ['Schrute','Dunder Mifflin']
					if testing_mode == False:
						run_follow(tags,100,15) #run follow script to follow 100 people with a 15 second pause in between


				except tweepy.error.TweepError as err:
					 print(Fore.RED + "Error found, continuing on\n" + Fore.WHITE)#Skip following and err on side of caution - stay under radar


			if (unfollow_flag >= unfollow_lim) and (unfollow_mode == True):
				try:
					unfollow_flag = 0 # reset flag
					print(Fore.BLUE + "\n[UNFOLLOW MODE - BEGIN]" + Fore.WHITE)
					if testing_mode == False:
						run_unfollow(100,15) # run unfollow script on 100 of my followers with a 15 second pause in between

				except tweepy.error.TweepError as err:
					continue



			print("Sleeping . . .")

			# Sleeper loop
			sleeper(time_mesh,interval)

			print("\n")

			if post_count >= 2:
				break # break to refresh the submission feed.
