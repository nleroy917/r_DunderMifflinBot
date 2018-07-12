     r_DunderMifflin_Bot
:------------------------------:
Author: Nathan LeRoy
Creation Date: June 21st, 2018
Latest Version: 1.0.1
:------------------------------:

OVERVIEW:
This python program is a very simple script that will retrieve the hot posts from http://reddit/r/DunerMifflin.com and post them to the twitter account @rDunderMifflin with a set frequency. After a given number of posts, it will refresh the hot queue and re-retrieve to obtain the latest posts.

RETRIEVING:
The program retrieves an iterable list of submissions from the subreddit's hot page, checks to make sure the post is a picture and not a pinned post by the subreddit's moderators, then extracts the unique picture identifer from the url. Typically, it is a random alpha-numeric string ending in ".png" or ".jpg". Each retrieved file is time-stamped and displayed to the command line.

REPOST AVOIDANCE:
This string is compared to a picture history log. If the string matches an entry in the log, that submission is skipped and the iterator moves on to the next post - repeating the retrieving process. If the string is found to be unique, then the program moves forward with that submission for further processing.


FILE PROCESSING, NAMING, AND POSTING:
Once the picture is found to be unique, the program assigns it a unique name based on the time of retrieval with the format:
YYYY/MM/DD-HR-MIN-SEC. The photo is saved to a folder in the same directory as the script being run. The log is updated with the pictures unique identifier assigned by reddit, and the program proceeds to post the photo to @rDunderMifflin's timeline with the title of the photo as the text associated with the post.

SLEEP
Once posted, to avoid hitting twitter and reddit's API rate-limit, and to avoid spamming, the program will "cool-down" and sleep for a set time in the script (wait_time). It will give updates every five minutes indicating the time until next post.


	Version History:
:--------------------------------------------------------------:
Version 1.0.1:
  - Updated the picture file naming convention to reflect the original url name
	  to help identify pictures that have been posted before.
  - Added print statements to indicate authentication and authentication success.

Version 1.0.0:
	- Initial creation and functionality proof
	- Includes repost avoidance
	- Includes hot-queue refreshing every 12 hours
