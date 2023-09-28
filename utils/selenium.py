import time
import utils.emailClient
#from utils.helpers import getJsonFromFile
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
import undetected_chromedriver as uc
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from pathlib import Path

def startSelenium(url="https://google.com/", runHeadless=False):
  email_secrets = utils.emailClient.getSecrets()
  options = webdriver.ChromeOptions()
  # options.add_experimental_option('excludeSwitches', ['enable-logging'])
  options.add_argument("--log-level=3")
  user_data_dir = str(Path("../data/chrome_data").resolve())
  options.add_argument(f"user-data-dir={user_data_dir}")
  if runHeadless:
    options.add_argument('--headless')
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

  #options.binary_location = '/usr/bin/chromedriver'

  bot = uc.Chrome(options=options)
  #bot = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=options)
  
  # print("Deleting cookies")
  # bot.delete_all_cookies()
  # bot.refresh()

  print("opening login page")
  bot.get('https://accounts.google.com/ServiceLogin')
  time.sleep(2)

  if "accounts.google.com" in bot.current_url:
    username = email_secrets['email']['sender_email']
    password = email_secrets['email']['sender_pw']

    print("entering username")
    bot.find_element("xpath", '//input[@type="email"]').send_keys(username)
    bot.find_element("xpath", '//*[@id="identifierNext"]').click()
    time.sleep(2)

    print("entering pw")
    bot.find_element("xpath", '//input[@type="password"]').send_keys(password)
    bot.find_element("xpath", '//*[@id="passwordNext"]').click()
    time.sleep(2)

  if url != "":
    bot.get(url)
  return bot

def xpathElement(bot,query,timeout=10):
  element= WebDriverWait(bot, timeout).until(EC.presence_of_element_located((By.XPATH, query)))
  return element

def navigateToChannelSelect(bot=None):
  if bot==None:
    bot = startSelenium("https://studio.youtube.com/")
  print("Pressing acct button")
  time.sleep(3)
  acct_btn = xpathElement(bot,'//*[@id="account-button"]',120)
  acct_btn.click()
  time.sleep(3)

  #channels_btn = bot.find_element(By.XPATH,"//*[contains(text(),'Switch account')]"))
  channels_btn = xpathElement(bot,'//*[contains(text(),"Switch account")]')
  print("switch account button clicked")
  channels_btn.click()
  time.sleep(3)

  return bot

def getChannel_btn(bot,channel_name):
    channels = bot.find_elements(By.XPATH,'//*[@id="channel-title"]')
    channel_btn = None
    for channel in channels:
       c:WebElement = channel
       if channel_name in c.text:
          channel_btn = c
    return channel_btn

# def createChannel():
#    bot = navigateToChannelSelect()

# def addComment(channel_name,video_id,comment,pinned=False):
#     bot:webdriver.Chrome = navigateToChannelSelect()

#     channels = bot.find_elements(By.XPATH,'//*[@id="channel-title"]')
#     channel_btn = None
#     for channel in channels:
#        c:WebElement = channel
#        if channel_name in c.text:
#           channel_btn = c
       
#     if channel == None:
#        print(f"Channel element with text {channel_name} not found")
#        bot.quit()
#        exit
#     #search = f'//*[contains(text(),"{channel_name}")]'
#     #channel_btn = xpathElement(bot, search)
#     channel_btn.click()
#     time.sleep(3)

#     bot.get('https://youtube.com/video/' + video_id)

#     body:WebElement = xpathElement(bot,'//body')
#     body.send_keys(Keys.END)

#     comment_box = bot.find_element(By.CSS_SELECTOR,"div[id='placeholder-area'] textarea")
#     comment_box.click()

#     comment_box.send_keys(comment)

#     # comment_placeholder:WebElement = xpathElement(bot, '//*[@id="simplebox-placeholder"]')
#     # comment_placeholder.click()

#     # comment_field:WebElement = xpathElement(bot,'//*[contains(@aria-label,"Add a comment")]')
#     #comment_field.clear()
#     # comment_field.send_keys(comment)
    
#     submit_btn = xpathElement(bot,'//*[@id="submit-button"]')
#     submit_btn.click()
#     time.sleep(3)
#     print("Comment posted")
#     bot.quit()
