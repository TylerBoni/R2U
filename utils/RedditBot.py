from datetime import date
import os
import praw
<<<<<<< HEAD
import prawcore
import subprocess
=======
>>>>>>> 0d6aa02d036ce42cc5968277be2a4f3408b56015
import pytube
from dotenv import load_dotenv
import requests
import json
from utils.Scalegif import scale_gif
import utils.Scalegif

load_dotenv()


class RedditBot():

    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.getenv('client_id'),
            client_secret=os.getenv('client_secret'),
            user_agent=os.getenv('user_agent'),
        )

        dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.data_path = os.path.join(dir_path, "data/")
        self.post_data = []
        self.already_posted = []

        #   Check for a posted_already.json file
        self.posted_already_path = os.path.join(
            self.data_path, "posted_already.json")
        if os.path.isfile(self.posted_already_path):
            print("Loading posted_already.json from data folder.")
            with open(self.posted_already_path, "r") as file:
                self.already_posted = json.load(file)

<<<<<<< HEAD


=======
>>>>>>> 0d6aa02d036ce42cc5968277be2a4f3408b56015
    def get_posts(self, sub="memes", type="all"):
        self.post_data = []
        subreddit = self.reddit.subreddit(sub)
        posts = []
        for submission in subreddit.top(time_filter="week", limit=100):
            if submission.stickied:
                print("Mod Post")
            else:
                
                url = submission.url.lower()
                # print(url)
                # print(type)
                if type == "video":
                    if "/v.redd" in url: posts.append(submission)
                elif type=="image":
                    if "/i.redd" in url: posts.append(submission)
                elif type=="all":
                    posts.append(submission)
        return posts

    def get_video(self, subreddit="memes", qty=1):
        posts = self.get_posts(subreddit,"video")
        self.create_data_folder()
        dataList = []
        for post in posts:
            vid = self.save_image(post,qty)
            if vid != None:
                dataList.append(vid)
        return dataList

    def create_data_folder(self):
        today = date.today()
        dt_string = today.strftime("%m%d%Y")
        data_folder_path = os.path.join(self.data_path, f"{dt_string}/")
        check_folder = os.path.isdir(data_folder_path)
        # If folder doesn't exist, then create it.
        if not check_folder:
            os.makedirs(data_folder_path)

<<<<<<< HEAD
    def get_vid(fileName,video_url):
        video_file = fileName+"-video.mp4"
        audio_file = fileName+"-audio.mp4"
        out_file = fileName+".mp4"
=======
    def save_image(self, submission, scale=(720, 1280)):
        #print(submission.url.lower())
        if (True): #"jpg" in submission.url.lower() or "png" in submission.url.lower() or "gif" in submission.url.lower() and "gifv" not in submission.url.lower():
            # try:
>>>>>>> 0d6aa02d036ce42cc5968277be2a4f3408b56015

        audio_url = video_url[:video_url.rfind('/')] + '/DASH_audio.mp4?source=fallback'

        # Download the video and audio streams using Prawcore
        #request = requests.get(video_url)
        response = requests.get(video_url)
        with open(video_file, 'wb') as f:
                f.write(response.content)
                
        response = requests.get(audio_url,)
        
        if response.status_code != 403:
            with open(audio_file, 'wb') as f:
                f.write(response.content)

            # Use ffmpeg to combine the video and audio streams into a single file
            with open('NUL', 'w') as devnull:
                return_code = subprocess.call(['ffmpeg','-y', '-i', video_file, '-i', audio_file, '-c:v', 'copy','-c:a', 'aac', '-b:a', '256k', out_file], stdout=devnull, stderr=devnull)
                
            if return_code != 0:
                print(f"ffmpeg failed with error code {return_code}")
                if os.path.exists(out_file):
                    os.remove(out_file)
                os.rename(video_file,out_file)
        
        if os.path.exists(out_file) == False:os.rename(video_file,out_file)
        if os.path.exists(video_file):os.remove(video_file)
        if os.path.exists(audio_file):os.remove(audio_file)

        return out_file


    def save_image(self, submission, scale=(720, 1280),qty=1):
        #print(submission.url.lower())

        if (submission.media != None): #"jpg" in submission.url.lower() or "png" in submission.url.lower() or "gif" in submission.url.lower() and "gifv" not in submission.url.lower():
            # try:
            video = submission.media['reddit_video']
            # Get all images to ignore
            dt_string = date.today().strftime("%m%d%Y")
            data_folder_path = os.path.join(self.data_path, f"{dt_string}/")
            CHECK_FOLDER = os.path.isdir(data_folder_path)
            
<<<<<<< HEAD
            if CHECK_FOLDER and len(self.post_data) < qty and video['height'] > 500 and not submission.over_18 and submission.id not in self.already_posted:
                fileName = f"{data_folder_path}Post-{submission.id}{submission.url.lower()[-4:]}"
                

                
                # # Get the image and write the path
                video_url = video['fallback_url']

                video_path = RedditBot.get_vid(fileName,video_url)
                # request = requests.get(video_url)
                # with open(image_path, 'wb') as f:
                #     f.write(request.content)
=======
            if CHECK_FOLDER and len(self.post_data) < 1 and not submission.over_18 and submission.id not in self.already_posted:
                image_path = f"{data_folder_path}Post-{submission.id}{submission.url.lower()[-4:]}.mp4"

                # Get the image and write the path
                video_url = submission.media['reddit_video']['fallback_url']
                request = requests.get(video_url)
                with open(image_path, 'wb') as f:
                    f.write(request.content)
>>>>>>> 0d6aa02d036ce42cc5968277be2a4f3408b56015

                # Could do transforms on images like resize!
                #image = cv2.resize(image,(720,1280))
                # Scalegif.scale_vid(image_path, scale)
                

                #cv2.imwrite(f"{image_path}", image)
                submission.comment_sort = 'best'

                # Get best comment.
                best_comment = None
                best_comment_2 = None

                for top_level_comment in submission.comments:
                    # Here you can fetch data off the comment.
                    # For the sake of example, we're just printing the comment body.
                    if len(top_level_comment.body) <= 140 and "http" not in top_level_comment.body:
                        if best_comment is None:
                            best_comment = top_level_comment
                        else:
                            best_comment_2 = top_level_comment
                            break

                best_comment.reply_sort = "top"
                best_comment.refresh()
                replies = best_comment.replies

                best_reply = None
                for top_level_comment in replies:
                    # Here you can fetch data off the comment.
                    # For the sake of example, we're just printing the comment body.
                    best_reply = top_level_comment
                    if len(best_reply.body) <= 140 and "http" not in best_reply.body:
                        break

                if best_reply is not None:
                    best_reply = best_reply.body
                else:
                    best_reply = "MIA"
                    if best_comment_2 is not None:
                        best_reply = best_comment_2.body

                data_file = {
                    "image_path": video_path,
                    'id': submission.id,
                    "title": submission.title,
                    "score": submission.score,
                    "18": submission.over_18,
                    "Best_comment": best_comment.body,
                    "best_reply": best_reply
                }
                self.post_data.append(data_file)
                with open(f"{data_folder_path}{submission.id}.json", "w") as outfile:
                    json.dump(data_file, outfile)
                with open(self.posted_already_path, "w") as outfile:
                    json.dump(self.already_posted, outfile)
                return data_file
            else:
                return None
        else:
            return None