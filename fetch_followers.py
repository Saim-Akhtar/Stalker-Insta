import time
import random
import os
from bs4 import BeautifulSoup
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By

COLUMNS=['Name','Username','Image Link']

def generateSoup(page):
    soup=BeautifulSoup(page,'html5lib')
    with open('followers.html','w',encoding='utf-8') as f:
        f.write(str(soup))
    responseSite='./followers.html'

    soup=BeautifulSoup(open(responseSite,encoding='utf-8'),'html5lib')
    os.remove('followers.html')
    return soup
    

def followers(driver,url,username):
    driver.get(url+"/"+username)
    time.sleep(1)

    total_followers=driver.find_elements_by_css_selector('ul.k9GMp li')[1]
    total_followers=total_followers.find_element_by_css_selector('span.g47SY')
    total_followers=int(total_followers.get_attribute('innerHTML')) # It will make error if the value is greater than 999
    # print("the total followers: ", total_followers)
    if total_followers == 0:
        print("No followers found")
        return

    followers_btn=driver.find_element_by_css_selector("ul.k9GMp a")
    followers_btn.click()
    time.sleep(1)
    try:
        dialog_followers = driver.find_element_by_css_selector('div.isgrP')
        print("Fetching Followers")
        #scroll down the page
        temp_check=0
        count=0
        while True:
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog_followers)
            temp_followers= len(driver.find_elements_by_css_selector("ul.jSC57 li"))
            print(temp_followers)
            time.sleep(50/100)
            # check if the value becomes equal to total mentioned in profile
            if temp_followers == total_followers:
                break
            # in case if the mentioned total followers is scammed in numbers
            if temp_check != temp_followers:
                count=0
                temp_check = temp_followers
            elif temp_check == temp_followers:
                count+=1
                if count == 5:
                    break
        
        soup=generateSoup(driver.page_source)
        
        followers_array=[]
        list_followers=soup.select('ul.jSC57 li')
        print("Total Followers: ", len(list_followers))
        print("Preparing Data File")
        
        for follower in list_followers:
            image=follower.select('._2dbep img')[0]['src']
            f_username=follower.select('a.FPmhX')[0].get_text()
            f_name=follower.select('div.wFPL8')[0].get_text()
            followers_array.append(\
                {COLUMNS[0]:f_name,COLUMNS[1]:f_username,COLUMNS[2]:image}
                )
        df=pd.DataFrame(followers_array,columns=COLUMNS)
        df.to_excel(username+'_followers.xlsx',index=None)
        print('Followers XLSX File Prepared')    
    except Exception as e:
        print(e)
        
        
    