#!/usr/bin/env python
# coding: utf-8

# In[131]:


import time
import random
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import requests
import pandas as pd
import openpyxl

class NameChecker:
    def __init__(self, driver):
        self.driver = driver
        
    def search_name(self, search_file):
        print("닉네임을 확인합니다...")
        names = search_file['닉네임']
        result = []
        
        for name in names:
            try:
                self.driver.get("http://zh-kr-g-account.awesomepiece.com/v2/coupon")
                self.driver.find_element('xpath', '//*[@id="inputNickname"]').send_keys(name)
                self.driver.find_element('xpath', '//*[@id="inputNicknameConfirm"]').send_keys(name)    
                self.driver.find_element('xpath', '/html/body/div/form/div[2]/button').click()
                
                #time.sleep(random.uniform(1,3))
                element = WebDriverWait(self.driver, 3).until(EC.title_is('좀비고등학교 쿠폰 입력'))
                url = self.driver.current_url

                if "http://zh-kr-g-coupon.awesomepiece.com/coupon/?key=" in url:
                    result.append('O')

            except:
                result.append('X')
                
        for i in range(len(result)):
            search_file["존재 여부"] = result
        
        search_file.to_excel('output.xlsx', sheet_name = "Sheet1", index = False)
        print("확인이 끝났습니다!")
        #display(search_file)

        
        
        
options = webdriver.ChromeOptions()
options.add_experimental_option("excludeSwitches", ["enable-logging"])
options.add_argument('headless')
driver = webdriver.Chrome(options=options)

file = pd.read_excel('input.xlsx', header = 0, engine = "openpyxl")
Nc = NameChecker(driver)
Nc.search_name(file)

driver.quit()

