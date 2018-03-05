# Copyright (C) 2018  Gavin

#!/usr/bin/env python
# -*- coding: UTF-8 -*-


import re
import string
import time
import sys
import requests
import codecs
from selenium import webdriver
#from selenium.webdriver.support.wait import WebDriverWait
#from selenium.webdriver.support import expected_conditions as EC
#from selenium.webdriver.common.by import By
try:
    user = open("Username&Password.txt")
except IOError:
    print
    'ERROR: where is your Username&Password.txt???'
else:
    username = user.readline()
    password = user.readline()
    user.close()
    username = re.findall("Username:(.*)",username)
    password = re.findall("Password:(.*)",password)
    DreverPath = sys.path[0] + r'\chromedriver.exe'
    driver = webdriver.Chrome(executable_path= DreverPath)
    loginUrl = 'https://www.shanbay.com/web/account/login/'
    driver.get(loginUrl)
    driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/form/div[1]/input').send_keys(username[0])
    driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/form/div[2]/input').send_keys(password[0])
    driver.find_element_by_xpath('/html/body/div[2]/div/div[2]/form/div[6]/button').click()
    time.sleep(1)
    req = requests.Session()
    cookies = driver.get_cookies()
    for cookie in cookies:
       req.cookies.set(cookie['name'],cookie['value'])
    webpage = req.get('https://www.shanbay.com/api/v1/bdc/library/master/?page=1')
    max = re.findall('"total": (.*?),', webpage.content.decode())
    MAX = int (((int (max[0])) + 9)/10)
    print (MAX)
    List_of_words = re.findall ('"content": "(.*?)",' ,webpage.content.decode())
    List_of_phonogram = re.findall ('"pron": "([\s\S]*?)", ' ,webpage.content.decode())
    List_of_chinese = re.findall ('"definition": "([\s\S]*?)",' ,webpage.content.decode())
    filename = "Master_Words of " + username[0] + ".txt"
    fo = codecs.open(filename, "w","utf-8")
    fo.write ('The number of words: '+max[0] +'\n')
    for index in range(len(List_of_words)):
        listofchi = List_of_chinese[index].encode('utf-8').decode('unicode_escape')
        listofchi = listofchi.replace("\r\n", " ")
        line = (List_of_words[index] + "   " + List_of_phonogram[index].encode('utf-8').decode('unicode_escape') + "          " + listofchi.replace("\n", " "))
        fo.write(line+'\n')
    page = 1;
    while (page < MAX):
        page += 1
        newURL = 'https://www.shanbay.com/api/v1/bdc/library/master/?page=' + str(page)
        newpage = req.get(newURL)
        List_of_words = []
        List_of_phonogram = []
        List_of_chinese = []
        List_of_words = re.findall('"content": "(.*?)",', newpage.content.decode())
        List_of_phonogram = re.findall('"pron": "([\s\S]*?)", ', newpage.content.decode())
        List_of_chinese = re.findall('"definition": "([\s\S]*?)",', newpage.content.decode())
        for index in range(len(List_of_words)):
            newlistofchi = List_of_chinese[index].encode('utf-8').decode('unicode_escape')
            newlistofchi = newlistofchi.replace("\r\n", " ")
            line = (List_of_words[index] + "   " + List_of_phonogram[index].encode('utf-8').decode('unicode_escape') + "          " + newlistofchi.replace("\n", " "))
            fo.write(line + '\n')
        newURL = None
        newpage = None

    fo.close()


'''
driver.get('https://www.shanbay.com/bdc/learnings/library/#master_tab_p1')
WebDriverWait(driver, 20, 0.5).until(EC.presence_of_element_located((By.CLASS_NAME, "learning")))
web = driver.page_source
maxpage = re.findall('<li class="disabled"><a href="javascript:;" data-page="..">..</a></li>\n<li><a href="javascript:;" data-page=".*?">(.*?)</a></li>\n<li><a href="javascript:;" data-page="2">&gt;</a></li>' ,web)
MAX=int(maxpage[0])
List_of_words = re.findall ('<span class="word" style="width: 30%; display: block; float:left;">([\s\S]*?)</span>' ,web)
List_of_phonogram = re.findall ('<span class="pronunciation" style="display:block; float: left;">([\s\S]*?)</span>' ,web)
List_of_chinese = re.findall ('<span class="definition" style="width: 30%; display: block; float: left;">([\s\S]*?)</span>' ,web)
#Line = []
#print(List_of_words)
#print(List_of_phonogram)
#print(List_of_chinese)

for index in range(len(List_of_words)):
    line = (List_of_words[index] + "   " + List_of_phonogram[index] + "     " + List_of_chinese[index].replace("\n", " "))
    #Line.append(line)
page = 1;
while (page < MAX):
    page += 1
    newURL = 'https://www.shanbay.com/bdc/learnings/library/#master_tab_p' + str(page)
    driver.get (newURL)
    List_of_words = []
    List_of_phonogram = []
    List_of_chinese = []
    List_of_words = re.findall('<span class="word" style="width: 30%; display: block; float:left;">([\s\S]*?)</span>',web)
    List_of_phonogram = re.findall('<span class="pronunciation" style="display:block; float: left;">([\s\S]*?)</span>',web)
    List_of_chinese = re.findall('<span class="definition" style="width: 30%; display: block; float: left;">([\s\S]*?)</span>', web)
    for index in range(len(List_of_words)):
        line = (List_of_words[index] + "   " + List_of_phonogram[index] + "     " + List_of_chinese[index].replace("\n", " "))

'''
