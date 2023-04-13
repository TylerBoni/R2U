## Setup
- Clone Project
- pip install -r requirements.txt 
- Install imageMagick
- create a .env file with your reddit API details.
    ````
    reddit_client_id=MYCLIENTID
    reddit_client_secret=MYSECRET
    reddit_user_agent=<MyAppName>
    ````
- create a client_secrets.json for your YouTube API details.
    ```json
    {
        "web":{
            "client_id":"",
            "auth_uri":"",
            "token_uri":"https://oauth2.googleapis.com/token",
            "client_secret":"",
            "redirect_uris":["http://localhost"]
        }
    }
    ```
- create a email_secrets.json with your email details
    ```json
    {
        "email": {
            "sender_email": "R2UMedia@gmail.com",
            "sender_pw": "tgfsdaliqzvsewkb"
        }
    }
    ```
- create a post_data.json with the information to use for posting
    ```json
    [
        {
            "channel_name": "MyChannel",
            "channel_id": "ChannelIDFoundInURL",
            "subreddit": "Aww",
            "hashtags": "#cutenessoverload #petscorner #animallovers #cutecats #cutepuppies",
            "comment": "Be sure to like and subscribe for more Awwdorable clips! Have you spoiled your cat lately? Get them something overnight on sale at Amazon here! https://amzn.to/AFFILIATELINK"
        }
    ]
    ```
## Reddit setup
- Have a reddit account and make an app to aquire access credentials, not much more to it

## YT Setup
- create youtube channel
- Open settings and set the default to not be content for children

## To Run

----first run should be babysat, as this doesn't automatically log you in to youtube, and the first run requires oauth with the YT api

- open terminal and cd to project
- activate env with:
    source env/bin/activate
- run script with
    python3.10 main.py
    enter delay time in seconds and hit enter
    profit

