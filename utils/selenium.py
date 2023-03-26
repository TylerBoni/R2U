import time
from utils.helpers import getJsonFromFile
from selenium.webdriver.remote.webelement import WebElement
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def startSelenium(url="https://google.com/", runHeadless=True):

  options = webdriver.ChromeOptions()
  # options.add_experimental_option('excludeSwitches', ['enable-logging'])
  options.add_argument("--log-level=3")
  options.add_argument(f"user-data-dir=data/chrome_data")
  if runHeadless:
    options.add_argument('--headless')
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")

  #options.binary_location = stored_options[os]['binary-location']

  bot = webdriver.Chrome(chrome_options=options)
  #bot = webdriver.Chrome(executable_path="chromedriver.exe", chrome_options=options)
  
  if url != "":
    bot.get(url)
  return bot

def xpathElement(bot,query,timeout=10):
  element= WebDriverWait(bot, timeout).until(EC.presence_of_element_located((By.XPATH, query)))
  return element

def navigateToChannelSelect(bot=None):
  if bot==None:
    bot = startSelenium("https://studio.youtube.com/")
  #input("Press enter to continue")
  acct_btn = xpathElement(bot,'//*[@id="account-button"]')
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
