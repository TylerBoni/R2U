"""
This is the main loop file for our AutoTube Bot!

Quick notes!
- Currently it's set to try and post a video then sleep for a day.
- You can change the size of the video currently it's set to post shorts.
    * Do this by adding a parameter of scale to the image_save function.
    * scale=(width,height)
"""
import time

import pytz
import random
import json
import utils.selenium

import random


import utils.emailClient as email
from utils.emailClient import sendEmail
from datetime import datetime
from utils.createMovie import CreateMovie, GetDaySuffix
from utils.redditDownloader import RedditBot
from utils.uploadVideo import postVideo

from utils.helpers import getJsonFromFile
from utils.youtubeHelpers import get_last_video_id,add_comment
#from utils.selenium import addComment


min = 60
hr = min*60
day = hr*24
timezone = pytz.timezone("US/Pacific")


#Create Reddit Data Bot
redditbot = RedditBot()

secrets = email.getSecrets()


##########################################
print("Set delay in seconds to start running:")
strDelay = input("")
if strDelay != None and strDelay != '':
    intDelay = int(strDelay)
else:
    intDelay = 0
print(f"Waiting for {intDelay/min} minutes")
time.sleep(intDelay)

##########################################
errCount=0
test = False
checkTime = True
run = True
start_time = time.time()
print(f"Started posting at:{start_time}")
while run:
    
    # get the current time in the PST timezone
    current_time = datetime.now(timezone)
    rand = random.randint(1,10*min)
    timeToWait = hr - rand
    minToWait = timeToWait/60

    # check if the current time is between 9am and 10pm PST
    if (current_time.hour >= 9 and current_time.hour < 22) or checkTime == False:
        
        msg = f"Waiting for {minToWait} minutes to post next videos."
        post_data=getJsonFromFile('post_data.json')
        for post in post_data:
            
            try:
                print("Downloading reddit post")
                reddit_post_data = redditbot.get_video(post['subreddit'])

                print("Creating video")
                postVideo(post,reddit_post_data)

                for p in reddit_post_data:
                    redditbot.already_posted.append(p['id'])

                print("Adding comment to last video")
                
                vidID = get_last_video_id(post['channel_id'])
                
                add_comment(post['channel_id'],post['comment'],vidID)
                print(f"Elapsed Time since start: {time.time()-start_time}")
            except Exception as ex:
                errCount = errCount+1
                msg = f"at {datetime.now} an error occurred trying to post {post}"
                print(msg +"\n"+ str(ex))
                
                if test == False:
                    sendEmail(secrets['email']['sender_email'],"Bot Error Occurred",msg + f"\n\n{str(ex)}")

                if errCount > 100:
                    run = False
                time.sleep(10)
        if test == False:
            sendEmail(secrets['email']['sender_email'],"Videos Posted",msg + "/n/n" + str(post_data))
        


    print(msg)
    time.sleep(timeToWait)
