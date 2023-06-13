import os
import requests
import json
import praw
import prawcore
import subprocess
from datetime import date
from dotenv import load_dotenv

load_dotenv()

#Currently only supports downloading videos TB 04/13/23
class RedditBot:
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.getenv('reddit_client_id'),
            client_secret=os.getenv('reddit_client_secret'),
            user_agent=os.getenv('reddit_user_agent'),
        )

        dir_path = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        self.data_path = os.path.join(dir_path, "data/")
        self.data_folder_path = self.create_data_folder(self.data_path)
        self.post_data = []
        self.already_posted = []

        # Load posted_already.json if it exists
        self.load_posted_already()

    def load_posted_already(self):
        self.posted_already_path = os.path.join(self.data_path, "posted_already.json")
        if os.path.isfile(self.posted_already_path):
            print("Loading posted_already.json from data folder.")
            with open(self.posted_already_path, "r") as file:
                self.already_posted = json.load(file)

    def get_posts(self, sub="memes", type="all", limit=100, after = ''):
        # Retrieve posts from the given subreddit
        self.post_data = []
        subreddit = self.reddit.subreddit(sub)
        posts = []
        submissions = subreddit.top(time_filter="all", limit=limit, params={'after': after})

        for submission in submissions:
            # print(submission.id)
            if submission.stickied:
                print("Mod Post")
            else:
                url = submission.url.lower()
                if type == "video":
                    if "/v.redd" in url:
                        posts.append(submission)
                elif type == "image":
                    if "/i.redd" in url:
                        posts.append(submission)
                elif type == "all":
                    posts.append(submission)
        after = submissions.params['after']
        return posts, after

    def get_video(self, subreddit="memes", qty=1):
        # Get video data and save it
        postQueryLimit = 100
        posts, after = self.get_posts(subreddit, "video", postQueryLimit)
        count = len(posts)
        posts = self.filterPosts(posts)
        while (len(posts)<qty):
            print(count)
            postQueryLimit = postQueryLimit + 100
            if (postQueryLimit > 10000):
                print("Post query limit reached in redditDownloader")
                return
            posts, after = self.get_posts(subreddit, "video", postQueryLimit, after)
            count = count + len(posts)
            posts = self.filterPosts(posts)

        data_list = []
        for post in posts:
            vid = self.save_content(post, qty)
            if vid is not None:
                data_list.append(vid)
        return data_list
    
    def filterPosts(self,posts):
        filteredPosts = []
        for post in posts:
            if post.media is not None:
                if self.post_is_legal(post):
                    filteredPosts.append(post)
        return filteredPosts
                    


    def create_data_folder(self, data_path):
        # Create a data folder for the current date if it doesn't exist
        today = date.today()
        dt_string = today.strftime("%m%d%Y")
        data_folder_path = os.path.join(data_path, f"{dt_string}/")
        if not os.path.isdir(data_folder_path):
            os.makedirs(data_folder_path)
        return data_folder_path

    @staticmethod
    def download_vid(fileName, video_url):
        # Download video and audio streams and combine them into a single file
        video_file = fileName + "-video.mp4"
        audio_file = fileName + "-audio.mp4"
        out_file = fileName + ".mp4"

        audio_url = video_url[:video_url.rfind('/')] + '/DASH_audio.mp4?source=fallback'

        response = requests.get(video_url)
        with open(video_file, 'wb') as f:
            f.write(response.content)

        # get reddit autio and combine if audio exists
        response = requests.get(audio_url, )
        if response.status_code != 403:
            with open(audio_file, 'wb') as f:
                f.write(response.content)

            with open('/dev/null', 'w') as devnull:
                return_code = subprocess.call(
                    ['ffmpeg', '-y', '-i', video_file, '-i', audio_file, '-c:v', 'copy', '-c:a', 'aac', '-b:a', '256k',
                        out_file
                ], stdout=devnull, stderr=devnull)

            if return_code != 0:
                print(f"ffmpeg failed with error code {return_code}")
                if os.path.exists(out_file):
                    os.remove(out_file)
                os.rename(video_file, out_file)

        # do some cleanup so we don't bloat our Data folder
        if not os.path.exists(out_file):
            os.rename(video_file, out_file)
        if os.path.exists(video_file):
            os.remove(video_file)
        if os.path.exists(audio_file):
            os.remove(audio_file)

        return out_file

    def post_is_legal(self, submission):
        # Check if the post meets the criteria
        video = submission.media['reddit_video']
        result = True
        if video['height'] > 500 and not submission.over_18 and submission.id not in self.already_posted:
            result = True
        else:
            result = False

        illegal_words = ["children", "kids", "kid", "child", "death", "dies", "killed", "kills"]
        for word in illegal_words:
            if word in submission.title.lower():
                result = False
                break

        return result

    def save_content(self, submission, scale=(720, 1280), qty=1):
        if submission.media is not None:
            video = submission.media['reddit_video']
            check_folder = os.path.isdir(self.data_folder_path)

            if check_folder and len(self.post_data) < qty and self.post_is_legal(submission):
                file_name = f"{self.data_folder_path}Post-{submission.id}{submission.url.lower()[-4:]}"
                video_url = video['fallback_url']
                video_path = RedditBot.download_vid(file_name, video_url)
                submission.comment_sort = 'best'

                # Get the best comment and reply
                best_comment, best_reply = self.get_best_comment_and_reply(submission)

                # Save the data to a JSON file
                self.save_data_to_file(submission, self.data_folder_path, video_path, best_comment, best_reply)

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
                return data_file
            else:
                return None
        else:
            return None

    def get_best_comment_and_reply(self, submission):
        best_comment = None
        best_comment_2 = None
        best_reply = None

        for top_level_comment in submission.comments:
            if len(top_level_comment.body) <= 140 and "http" not in top_level_comment.body:
                if best_comment is None:
                    best_comment = top_level_comment
                else:
                    best_comment_2 = top_level_comment
                    break

        best_comment.reply_sort = "top"
        best_comment.refresh()
        replies = best_comment.replies

        for top_level_comment in replies:
            best_reply = top_level_comment
            if len(best_reply.body) <= 140 and "http" not in best_reply.body:
                break

        if best_reply is None:
            best_reply = "MIA"
            if best_comment_2 is not None:
                best_reply = best_comment_2.body

        return best_comment, best_reply

    def save_data_to_file(self, submission, data_folder_path, video_path, best_comment, best_reply):
        with open(f"{data_folder_path}{submission.id}.json", "w") as outfile:
            json.dump({
            "image_path": video_path,
            'id': submission.id,
            "title": submission.title,
            "score": submission.score,
            "18": submission.over_18,
            "best_comment": best_comment.body,
            "best_reply": best_reply.body
            }, outfile)
        with open(self.posted_already_path, "w") as outfile:
            json.dump(self.already_posted, outfile)