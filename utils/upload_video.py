from utils.RedditBot import RedditBot
import os
import time
<<<<<<< HEAD
from utils.CreateMovie import CreateMovie

from selenium.webdriver.common.by import By
from utils.cleanStrings import clean
from utils.selenium import startSelenium,xpathElement,navigateToChannelSelect,getChannel_btn
=======
import utils.YT_api
from utils.CreateMovie import CreateMovie

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
>>>>>>> 0d6aa02d036ce42cc5968277be2a4f3408b56015

def upload_vid_chrome(video_data, channel_name):
  
  bot = navigateToChannelSelect()

<<<<<<< HEAD
  channel_btn = getChannel_btn(bot,channel_name)
  channel_btn.click()
  time.sleep(3)

  upload_button = xpathElement(bot,'//*[@id="upload-icon"]')
=======
from utils.YT_api import add_comment
from utils.YT_api import get_last_video_id
from utils.cleanStrings import clean



def upload_vid_chrome(video_data, channel_name):
  
  timeout = 10
  options = webdriver.ChromeOptions()
  # options.add_experimental_option('excludeSwitches', ['enable-logging'])
  options.add_argument("--log-level=3")
  options.add_argument("user-data-dir=C:\\Users\\User\\AppData\\Local\Google\\Chrome\\User Data\\")
  options.binary_location = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"

  bot = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=options)
  
  url = "https://studio.youtube.com/"
  bot.get(url)


  acct_btn = WebDriverWait(bot, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="account-button"]')))
  acct_btn.click()
  time.sleep(3)

  #channels_btn = bot.find_element(By.XPATH,"//*[contains(text(),'Switch account')]"))
  channels_btn = WebDriverWait(bot, timeout).until(EC.visibility_of_element_located((By.XPATH,'//*[contains(text(),"Switch account")]')))
  print("switch account button clicked")
  channels_btn.click()
  time.sleep(3)

  search = f'//*[contains(text(),"{channel_name}")]'
  channel_btn = WebDriverWait(bot, timeout).until(EC.visibility_of_element_located((By.XPATH, search)))
  print(f"{channel_name} button clicked")
  channel_btn.click()
  time.sleep(3)

  # continueSub = input("continue? y/n")
  # if continueSub.lower() != "y":
    #  exit

  upload_button = WebDriverWait(bot, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="upload-icon"]')))
>>>>>>> 0d6aa02d036ce42cc5968277be2a4f3408b56015
  upload_button.click()

  time.sleep(3)
  file_input = bot.find_element(By.XPATH, '//*[@id="content"]/input')
  # file_input = WebDriverWait(bot, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/input')))
  simp_path = 'video.mp4'
  abs_path = os.path.abspath(simp_path)
  file_input.send_keys(abs_path)
<<<<<<< HEAD
  next_button = xpathElement(bot,'//*[@id="next-button"]')

  description = video_data['description']

  try:
    title_textbox =xpathElement(bot,'//*[contains(@aria-label,"Add a title")]')
    title_textbox.clear()
    title = video_data['title']
    title = clean(title)
    if len(title) > 99:
       description = title + "\n" + description
       title = "Got a video you want featured? Send us a DM!"
    title_textbox.send_keys(title)
  except:
     print("Error setting video title")

  desc_textbox = xpathElement(bot, '//*[contains(@aria-label,"Tell viewers about your video")]')
  desc_textbox.clear()
  desc_textbox.send_keys(description + " " + video_data['hashtags'])
=======
  next_button = WebDriverWait(bot,timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="next-button"]')))

  try:
    title_textbox = WebDriverWait(bot,timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[contains(@aria-label,"Add a title")]')))
    title_textbox.clear()
    title_textbox.send_keys(video_data['title'])
  except:
     print("Error setting video title")

  # desc_textbox = WebDriverWait(bot,timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@aria-label="Tell viewers about your video"]')))
  # desc_textbox.clear()
  # desc_textbox.send_keys(video_data['description'])
>>>>>>> 0d6aa02d036ce42cc5968277be2a4f3408b56015

  for i in range(3):
      next_button.click()
      time.sleep(1)

  print("clicking radio button")
<<<<<<< HEAD
  public_btn =xpathElement(bot,'//*[@name="PUBLIC"]')
=======
  public_btn = WebDriverWait(bot,timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@name="PUBLIC"]')))
>>>>>>> 0d6aa02d036ce42cc5968277be2a4f3408b56015
  public_btn.click()

  done_button = bot.find_element(By.XPATH, '//*[@id="done-button"]')
  done_button.click()
<<<<<<< HEAD
  time.sleep(30)

  bot.quit()

def postVideo(post,reddit_post_data,test=False):
    hashtags = post['hashtags']
=======
  time.sleep(10)

  bot.quit()

def postVideo(post, redditbot,test=False):
    subreddit = post['subreddit']
>>>>>>> 0d6aa02d036ce42cc5968277be2a4f3408b56015
    channel_name = post['channel_name']
    channel_id = post['channel_id']
    comment = post['comment']

    # Gets our new posts pass if image related subs. Default is memes

<<<<<<< HEAD
    

    # Create the movie itself!
    CreateMovie.CreateMP4(reddit_post_data)
    vid_title = f"\"{reddit_post_data[0]['title']}\""
=======
    posts = redditbot.get_posts(subreddit,"video")

    # Create folder if it doesn't exist
    redditbot.create_data_folder()

    # Go through posts and find 1 that will work for us.
    for post in posts:
        txt=""
        redditbot.save_image(post)

    # Create the movie itself!
    CreateMovie.CreateMP4(redditbot.post_data)
    vid_title = f"\"{redditbot.post_data[0]['title']}\""
>>>>>>> 0d6aa02d036ce42cc5968277be2a4f3408b56015
    vid_title = clean(vid_title)
    video_data = {
            "file": "video.mp4",
            "title": vid_title,
            "description": "",
<<<<<<< HEAD
            "hashtags": hashtags,
=======
>>>>>>> 0d6aa02d036ce42cc5968277be2a4f3408b56015
            "keywords":"",
            "privacyStatus":"public"
    }

    if not test:
      print(video_data["title"])
<<<<<<< HEAD
      print("video downloaded, posting in 1 minute")
      time.sleep(60)

      print("Posting Video...")
      upload_vid_chrome(video_data, channel_name)
          
=======
      
      print("Posting Video...")
      upload_vid_chrome(video_data, channel_name)

      

      if comment != "":
          print("Waiting 1 minute before adding comment")
          time.sleep(60)
          print("Getting last video id")
          id = get_last_video_id(channel_id)
          if id != "":
              print("adding comment")
              add_comment(id,channel_id,comment)
>>>>>>> 0d6aa02d036ce42cc5968277be2a4f3408b56015
