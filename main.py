from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
import os
import platform
import time
import random
import argparse
from fetch_followers import followers
from fetch_following import following
from check_private import privacy

parser = argparse.ArgumentParser(description='Taking username and password.')
parser.add_argument('--username', metavar='username', type=str,
                    help='username of account')
parser.add_argument('--pwd', metavar='password', type=str,
                    help='password of account')
parser.add_argument('--stalk', metavar='stalk', type=str,
                    help='username of account to stalk')

args = parser.parse_args()
username,password,stalk=args.username,args.pwd,args.stalk

# Clear the console screen
if platform.system() == 'Linux' :
    os.system('clear')
elif platform.system() == 'Windows':
    os.system('cls')

# starting the webdriver
driver = webdriver.Chrome(ChromeDriverManager().install())
url="https://www.instagram.com"
driver.get(url)
time.sleep(5)

# Login with username and password
usernameElement = driver.find_element_by_name('username')
usernameElement.send_keys(username)
passwordElement = driver.find_element_by_name('password')
passwordElement.send_keys(password)
passwordElement.send_keys(Keys.RETURN)
time.sleep(5)


# check if user need to stalk someone
if stalk != None:
    print("Stalking ",stalk)
    isPrivate= privacy(driver,url,stalk)
    if isPrivate == False:
        following(driver,url,stalk)
        followers(driver,url,stalk)
    else:
        print("Sorry! It's a Private Account")
    
else: # user needs to only fetch his followers and followings
    following(driver,url,username)
    followers(driver,url,username)


driver.quit()