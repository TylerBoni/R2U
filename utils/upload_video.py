import httplib2
import os
import random
import sys
import time
import utils.YT_api
from utils.CreateMovie import CreateMovie

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


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
  upload_button.click()

  time.sleep(3)
  file_input = bot.find_element(By.XPATH, '//*[@id="content"]/input')
  # file_input = WebDriverWait(bot, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/input')))
  simp_path = 'video.mp4'
  abs_path = os.path.abspath(simp_path)
  file_input.send_keys(abs_path)
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

  for i in range(3):
      next_button.click()
      time.sleep(1)

  print("clicking radio button")
  public_btn = WebDriverWait(bot,timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@name="PUBLIC"]')))
  public_btn.click()

  done_button = bot.find_element(By.XPATH, '//*[@id="done-button"]')
  done_button.click()
  time.sleep(10)

  bot.quit()

def postVideo(post, redditbot,test=False):
    subreddit = post['subreddit']
    channel_name = post['channel_name']
    channel_id = post['channel_id']
    comment = post['comment']

    # Gets our new posts pass if image related subs. Default is memes

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
    vid_title = clean(vid_title)
    video_data = {
            "file": "video.mp4",
            "title": vid_title,
            "description": "",
            "keywords":"",
            "privacyStatus":"public"
    }

    if not test:
      print(video_data["title"])
      
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