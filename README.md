#r_DunderMifflin_Bot
:--------------------------:
Author: Nathan LeRoy
Creation Date: June 21st, 2018
Latest Version: 1.4.0
:--------------------------:

OVERVIEW:
This python program is a very simple script that will retrieve the hot posts from http://reddit/r/DunerMifflin.com and post them to the twitter account @rDunderMifflin with a set frequency. After a given number of posts, it will refresh the hot queue and re-retrieve to obtain the latest posts.

RETRIEVING:
The program retrieves an iterable list of submissions from the subreddit's hot page, checks to make sure the post is a picture and not a pinned post by the subreddit's moderators, then extracts the unique picture identifer from the url. Typically, it is a random alpha-numeric string ending in ".png" or ".jpg". Each retrieved file is time-stamped and displayed to the command line.

REPOST AVOIDANCE:
This string is compared to a picture history log. If the string matches an entry in the log, that submission is skipped and the iterator moves on to the next post - repeating the retrieving process. If the string is found to be unique, then the program moves forward with that submission for further processing.


FILE PROCESSING, NAMING, AND POSTING:
Once the picture is found to be unique, the program assigns it a unique name based on the time of retrieval with the format:
YYYY/MM/DD-HR-MIN-SEC. The photo is saved to a folder in the same directory as the script being run. The log is updated with the pictures unique identifier assigned by reddit, and the program proceeds to post the photo to @rDunderMifflin's timeline with the title of the photo as the text associated with the post.

SLEEP:
Once posted, to avoid hitting twitter and reddit's API rate-limit, and to avoid spamming, the program will "cool-down" and sleep for a set time in the script (wait_time). It will give updates every five minutes indicating the time until next post.

FOLLOW SCRIPT:
About every 12 hours, the bot will search twitter for the latest tweets that contain specific strings set by the user. (Ex. Dunder Mifflin, The Office, Schrute, etc). It will parse through a specific number of tweets and follow each user (default 100)
The follow script is highly rate limited so as not to exceed the twitter API regulations and receive a ban/suspension.

	Version History:
:--------------------------------------------------------------:

Version 1.4.2
	- Wait time is now calculated using three parameters... Hot post buzz, time of day, and the post frequency on the subreddit
	- After each post, the bot will calculate how much time is needed in between posts.
	- The math behind all of this can be adjusted easily. Also the algorithm that calculates this is encapsulated in a spearate python file.

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
	- Added support to identify and skip video posts. 

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
	- Hope is to soon introduce follow criteria, to make it more strategic and only follow those within certain limits

Version 1.2.0:
	- Introduced error handling and exception raising
	- The hope is that the program will be able to run for much more extended perods of time
	- Orgranized simple tasks into functions to clean up code and aid debugging in future.

Version 1.1.1:
	- Bug fix where imgur posts lacking a file extension would not get posted
    - Added capability to determine the file extension of a url and add one if it doesnt
      exist

Version 1.1.0:
	- "Weak Hot" avoidance has been added. Occasionally posts will make it to the
	   hot page with a small number of upvotes. The program will skip any and all
	   posts that do not reach a minimum upvote requirement
	-  The wait_time for a post was decreased from 3 hours to 2 hours.

Version 1.0.1:
    - Updated the picture file naming convention to reflect the original url name
	  to help identify pictures that have been posted before.
    - Added print statements to indicate authentication and authentication success.

Version 1.0.0:
	- Initial creation and functionality proof
	- Includes repost avoidance
	- Includes hot-queue refreshing every 12 hours
