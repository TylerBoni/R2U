"""
This is the main loop file for our AutoTube Bot!

Quick notes!
- Currently it's set to try and post a video then sleep for a day.
- You can change the size of the video currently it's set to post shorts.
    * Do this by adding a parameter of scale to the image_save function.
    * scale=(width,height)
"""
import time
import random

import utils.emailClient as email
from utils.emailClient import sendEmail
from datetime import datetime
from utils.CreateMovie import CreateMovie, GetDaySuffix
from utils.RedditBot import RedditBot
from utils.upload_video import postVideo

min = 60
hr = min*60
day = hr*24

#Create Reddit Data Bot
redditbot = RedditBot()

secrets = email.getSecrets()

post_data=[
    {
    "channel_name":"CatsOnCatsOnCats",
    "channel_id":"UCeYwxNwTDZGUAYBqr-UHboA",
    "subreddit":"Aww",
    "comment":'Be sure to like and subscribe for more Awwdorable clips! Have you spoiled your cat lately? Get them something overnight on sale at Amazon here! https://amzn.to/42vHELM'
    },
    {
    "channel_name":"DashCamDisasters",
    "channel_id":"UCyMCY5OUdmtGIpgDpxld_cg",
    "subreddit":"IdiotsInCars",
    "comment":'You really never know when something crazy is going to happen. It could save you thousands if you\'re ever in an accident. Check out our most submitted dashcam on Amazon here! https://amzn.to/3Z3j0PG'
    }
]

test = False
run = True
while run:
    for post in post_data:
        try:
            postVideo(post,redditbot)
        except Exception as ex:
            run = False
            msg = f"at {datetime.now} an error occurred trying to post {post}"
            print(msg)
            if test == False:
                sendEmail(secrets['email']['sender_email'],"Bot Error Occurred",msg + f"\n\n{str(ex)}")
            time.sleep(10)

    rand = random.randint(1,10*min)
    timeToWait = hr - rand
    minToWait = timeToWait/60
    msg = f"Waiting for {minToWait} minutes to post next videos."
    if test == False:
        sendEmail(secrets['email']['sender_email'],"Videos Posted",msg + "/n/n" + str(post_data))
    print(msg)
    time.sleep(timeToWait)
