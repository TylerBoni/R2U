from utils.RedditBot import RedditBot
import os
import time
from utils.CreateMovie import CreateMovie

from selenium.webdriver.common.by import By
from utils.cleanStrings import clean
from utils.selenium import startSelenium,xpathElement,navigateToChannelSelect,getChannel_btn

def upload_vid_chrome(video_data, channel_name):
  
  bot = navigateToChannelSelect()

  channel_btn = getChannel_btn(bot,channel_name)
  channel_btn.click()
  time.sleep(3)

  upload_button = xpathElement(bot,'//*[@id="upload-icon"]')
  upload_button.click()

  time.sleep(3)
  file_input = bot.find_element(By.XPATH, '//*[@id="content"]/input')
  # file_input = WebDriverWait(bot, timeout).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="content"]/input')))
  simp_path = 'video.mp4'
  abs_path = os.path.abspath(simp_path)
  file_input.send_keys(abs_path)
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

  for i in range(3):
      next_button.click()
      time.sleep(1)

  print("clicking radio button")
  public_btn =xpathElement(bot,'//*[@name="PUBLIC"]')
  public_btn.click()

  done_button = bot.find_element(By.XPATH, '//*[@id="done-button"]')
  done_button.click()
  time.sleep(30)

  bot.quit()

def postVideo(post,reddit_post_data,test=False):
    hashtags = post['hashtags']
    channel_name = post['channel_name']
    channel_id = post['channel_id']
    comment = post['comment']

    # Gets our new posts pass if image related subs. Default is memes

    

    # Create the movie itself!
    CreateMovie.CreateMP4(reddit_post_data)
    vid_title = f"\"{reddit_post_data[0]['title']}\""
    vid_title = clean(vid_title)
    video_data = {
            "file": "video.mp4",
            "title": vid_title,
            "description": "",
            "hashtags": hashtags,
            "keywords":"",
            "privacyStatus":"public"
    }

    if not test:
      print(video_data["title"])
      print("video downloaded, posting in 1 minute")
      time.sleep(60)

      print("Posting Video...")
      upload_vid_chrome(video_data, channel_name)
          