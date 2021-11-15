#!/usr/bin/env python3

from selenium import webdriver
import random, json, csv
import time
from bs4 import BeautifulSoup
from contextlib import redirect_stdout

wantedFigs = []
wishlist = {}

def loadWishList():
    global wishlist
    with open ('wanted.json', 'r') as fp:
        wishlist = json.load(fp)

def repeator():
    while(True):
        random_wait_time = random.randrange(900, 1200)
        time.sleep(random_wait_time)
        loadWishList()
        preowned = checkPreowned("https://www.amiami.com/eng/search/list/?s_st_condition_flg=1&s_sortkey=preowned&pagecnt=")
        display(preowned)
        clean_up(preowned)


def checkPreowned(url):
    preownedFigs = {}

    random_wait_time = random.randrange(5.0, 15.0)
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument("--test-type")
    options.binary_location = "/usr/bin/chromium"
    wd = webdriver.Chrome(chrome_options=options)
    curPage = 1
    currentURL = url + str(curPage)
    wd.get(currentURL)
    time.sleep(random_wait_time)
    soup = BeautifulSoup(wd.page_source,features="html.parser")
    cleaned_soup = checkIndiPage(soup)
    stringProcessing(cleaned_soup, preownedFigs)
    while(cleaned_soup != ""): #cleaned_soup != ""
        random_wait_time = random.randrange(5.0, 15.0)
        curPage = curPage + 1
        currentURL = url + str(curPage)
        wd.get(currentURL)
        time.sleep(random_wait_time)
        soup = BeautifulSoup(wd.page_source,features="html.parser")
        cleaned_soup = checkIndiPage(soup)
        preownedFigs = stringProcessing(cleaned_soup, preownedFigs)
    
    return preownedFigs

def checkIndiPage(soup):
     for data in soup.find_all('div', {'class':'wrapper'}):
        for ulTag in data.find_all('ul', {'class':'new-items__inner'}):
            return ulTag.text

def stringProcessing(input, preownedFigs):
    global wantedFigs, wishlist
    parsed1 = []
    if(input):
        items = input.split("\n")
        for item in items:
            item = item.strip()
            index = item.find("Closed")
            if(index != -1):
                item = item[index:]
                item = item.replace("Closed", "", 1)
                if (item in wishlist):
                    preownedFigs[item] = wishlist.get(item)
    
    return preownedFigs

def display(preowned):
    if(preowned):
        print(preowned)
    else :
        print("No matches")
def clean_up(preowned):
    preowned.clear()

loadWishList()
preowned = checkPreowned("https://www.amiami.com/eng/search/list/?s_st_condition_flg=1&s_sortkey=preowned&pagecnt=")
display(preowned)
clean_up(preowned)
repeator()