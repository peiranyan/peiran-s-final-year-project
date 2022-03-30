import time
import pymongo
from selenium import webdriver


def OpenChromeAndUrl(url):
    driver = webdriver.Chrome('webdrivers/chromedriver')
    driver.get(url)
    driver.maximize_window()
    time.sleep(5)
    return driver


def ScrollWindowsToLowestEnd(driver):
    last_height = driver.execute_script("return document.documentElement.scrollHeight")
    new_height = 0
    while last_height != new_height:
        new_height = last_height
        driver.execute_script("window.scrollTo(0, document.documentElement.scrollHeight);")

        time.sleep(5)

        last_height = driver.execute_script("return document.documentElement.scrollHeight")


@DeprecationWarning
def getCollection2MongoDB(collectionName):
    client = pymongo.MongoClient("127.0.0.1", 27017)
    db = client["YouTube"]
    collection = db[collectionName]
    return collection


def readStopWord():
    content_lines = []
    fp = open("../resource/StopWords/stopWord.txt", "r", encoding="utf-8")
    for i in fp.readlines():
        content_lines.append(i)
    fp.close()

    fp = open("../resource/StopWords/chinese_stopwords.txt", "r", encoding="utf-8")
    for i in fp.readlines():
        content_lines.append(i)
    fp.close()
    # 去除行末的换行符，否则会在停用词匹配的过程中产生干扰
    for i in range(len(content_lines)):
        content_lines[i] = content_lines[i].rstrip("\n")
    return content_lines
