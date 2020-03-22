import time
import random
import os
from bs4 import BeautifulSoup
import pandas as pd

COLUMNS=['Name','Username','Image Link']

def generateSoup(page):
    soup=BeautifulSoup(page,'html5lib')
    with open('following.html','w',encoding='utf-8') as f:
        f.write(str(soup))
    responseSite='./following.html'

    soup=BeautifulSoup(open(responseSite,encoding='utf-8'),'html5lib')
    os.remove('following.html')
    return soup
    

def following(driver,url,username):
    driver.get(url+"/"+username)
    time.sleep(1)

    total_following=driver.find_elements_by_css_selector('ul.k9GMp li')[2]
    total_following=total_following.find_element_by_css_selector('span.g47SY')
    total_following=int(total_following.get_attribute('innerHTML')) # It will make error if the value is greater than 999
    # print("the total following: ", total_following)
    if total_following == 0:
        print("No following found")
        return

    following_btn=driver.find_elements_by_css_selector("ul.k9GMp a")[1]
    following_btn.click()
    time.sleep(1)
    try:
        dialog_following = driver.find_element_by_css_selector('div.isgrP')
        print("Fetching Followings")
        #scroll down the page
        temp_check=0
        count=0
        while True:
            driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight", dialog_following)
            temp_following= len(dialog_following.find_elements_by_css_selector("ul.jSC57 li"))
            print(temp_following)
            time.sleep(50/100)
            # check if the value becomes equal to total mentioned in profile
            if temp_following == total_following:
                break
            # in case if the mentioned total following is scammed in numbers
            if temp_check != temp_following:
                count=0
                temp_check = temp_following
            elif temp_check == temp_following:
                count+=1
                if count == 8:
                    break

        print("we got total: ", temp_following)
        soup=generateSoup(driver.page_source)
        
        list_following=soup.select('ul.jSC57 li')
        print("Total Followings: ", len(list_following))

        print("Preparing Data File")
        following_array=[]
        for following in list_following:
            image=following.select('._2dbep img')[0]['src']
            f_username=following.select('a.FPmhX')[0].get_text()
            test=following.select('div._7UhW9')
            if len(test) == 0:
                f_name=following.select('div.wFPL8')[0].get_text()
            else:
                f_name=following.select('div._7UhW9')[0].get_text()
            following_array.append(\
                {COLUMNS[0]:f_name,COLUMNS[1]:f_username,COLUMNS[2]:image}
                )

        df=pd.DataFrame(following_array,columns=COLUMNS)
        df.to_excel(username+'_following.xlsx',index=None)
        print('Following XLSX File Prepared')    
    except BaseException as e:
        print(e)
    
