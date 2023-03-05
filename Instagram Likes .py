#!/usr/bin/env python
# coding: utf-8

# In[2]:


import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import NoSuchElementException

def login(username, password, proxy):
    # Configure proxy
    proxy_config = Proxy()
    proxy_config.proxy_type = ProxyType.MANUAL
    proxy_config.http_proxy = proxy
    proxy_config.ssl_proxy = proxy

    # Configure webdriver with proxy
    options = webdriver.ChromeOptions()
    options.add_argument('--proxy-server=%s' % proxy)
    driver = webdriver.Chrome(options=options)

    # Login to Instagram
    try:
        driver.get("https://www.instagram.com/accounts/login/")
        time.sleep(2)
        username_input = driver.find_element_by_name("username")
        username_input.send_keys(username)
        password_input = driver.find_element_by_name("password")
        password_input.send_keys(password)
        password_input.send_keys(Keys.ENTER)
        time.sleep(3)
        try:
            not_now_btn = driver.find_element_by_xpath("//button[text()='Not Now']")
            not_now_btn.click()
        except NoSuchElementException:
            pass
        return driver
    except:
        print(f"Login error for username: {username}")
        driver.quit()
        return None

def main():
    # Load credentials from Excel file
    df = pd.read_excel('credentials.xlsx')

    # Load proxies from text file
    with open('proxies.txt') as f:
        proxies = f.read().splitlines()

    # Iterate through credentials and proxies
    for index, row in df.iterrows():
        username = row['username']
        password = row['password']
        link = row['link']
        proxy = proxies[index % len(proxies)]  # Cycle through proxies

        # Login to Instagram
        driver = login(username, password, proxy)
        if not driver:
            continue

        # Go to specified link
        driver.get(link)
        time.sleep(3)

        # Click on the like button
        try:
            like_button = driver.find_element_by_xpath("//span[@class='fr66n']/button[@class='wpO6b']")
            like_button.click()
        except NoSuchElementException:
            pass

        # Click on the comment button and paste comment
        try:
            comment_button = driver.find_element_by_xpath("//span[@class='fr66n']/button[@class='sqdOP yWX7d     _8A5w5   ']")
            comment_button.click()
            time.sleep(2)
            comment_input = driver.find_element_by_xpath("//textarea[@class='X7cDz']")
            comment_input.send_keys("Your comment here.")
            comment_input.submit()
        except NoSuchElementException:
            pass

        # Logout of Instagram
        try:
            profile_button = driver.find_element_by_xpath("//a[@class='-qQT3']")
            profile_button.click()
            time.sleep(1)
            logout_button = driver.find_element_by_xpath("//div[@class='mt3GC']/button[text()='Log Out']")
            logout_button.click()
            time.sleep(1)
            driver.quit()
        except NoSuchElementException:
            pass

if __name__ == '__main__':
    main()


# In[ ]:




