def privacy(driver,url,username):
    driver.get(url+"/"+username)
    try:
        driver.find_element_by_css_selector("div.Nd_Rl")
        return True
    except:
        return False