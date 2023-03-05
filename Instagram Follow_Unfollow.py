#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import time
import pandas as pd
from selenium import webdriver

def follow_unfollow(ID_Url, driver):
    # Navigate to the ID page
    driver.get(ID_Url)
    time.sleep(2)

    # Check if the user is already followed
    follow_button = driver.find_element_by_xpath("//button[contains(text(),'Follow')]")
    if follow_button.text == 'Follow':
        # Follow the user
        follow_button.click()
        print("User followed.")
    else:
        # Unfollow the user
        unfollow_button = driver.find_element_by_xpath("//button[contains(text(),'Following')]")
        unfollow_button.click()
        unfollow_confirm = driver.find_element_by_xpath("//button[contains(text(),'Unfollow')]")
        unfollow_confirm.click()
        print("User unfollowed.")

# Load login credentials from Excel sheet
df = pd.read_excel('credentials.xlsx')

# Open web driver
driver = webdriver.Chrome()

# Loop through each set of credentials
for index, row in df.iterrows():
    try:
        # Login to Instagram
        driver.get('https://www.instagram.com/')
        time.sleep(2)
        driver.find_element_by_name('username').send_keys(row['username'])
        driver.find_element_by_name('password').send_keys(row['password'])
        driver.find_element_by_css_selector("button[type='submit']").click()
        time.sleep(2)
        print("Login successful.")

        # Call the follow_unfollow function with the desired ID page URL
        follow_unfollow('https://www.instagram.com/username/', driver)

        # Logout of Instagram
        driver.get('https://www.instagram.com/accounts/logout/')
        time.sleep(2)
        driver.find_element_by_xpath("//button[contains(text(),'Log Out')]").click()
        print("Logout successful.")

    except Exception as e:
        print("Error:", e)
        continue

# Close web driver
driver.quit()

