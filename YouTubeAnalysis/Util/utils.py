import time
from selenium import webdriver
from wordcloud import WordCloud, STOPWORDS, wordcloud
import YouTubeAnalysis.Resource.videoInfo as config

import matplotlib.pyplot as plt


def readFromFile(fileName):
    content = []
    with open(fileName, "r", encoding="utf-8") as f:
        lines = f.readlines()
        for line in lines:
            if len(line) != 0:
                content.append(line)
    return content


def DrawWordCloud(split_word):
    sw = set(STOPWORDS)
    stopWords = ReadStopWord()
    for word in stopWords:
        sw.add(word)
    my_wordcloud = WordCloud(scale=4, font_path="/System/Library/fonts/PingFang.ttc", stopwords=sw,
                             background_color='white',
                             max_words=100, max_font_size=60, random_state=20).generate(" ".join(split_word))

    plt.imshow(my_wordcloud)
    plt.axis("off")
    plt.show()


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


def ReadStopWord():
    content_lines = []
    fp = open("../Resource/StopWords/stopWord.txt", "r", encoding="utf-8")
    for i in fp.readlines():
        content_lines.append(i)
    fp.close()

    fp = open("../Resource/StopWords/chinese_stopwords.txt", "r", encoding="utf-8")
    for i in fp.readlines():
        content_lines.append(i)
    fp.close()
    # 去除行末的换行符，否则会在停用词匹配的过程中产生干扰
    for i in range(len(content_lines)):
        content_lines[i] = content_lines[i].rstrip("\n")
    return content_lines


def GetAllYid():
    Yids = []
    for i in config.configs["videos"]:
        Yids.append(i["Yid"])
    return Yids


def GetAllBid():
    Bids = []
    for i in config.configs["videos"]:
        Bids.append(i["Bid"])
    return Bids
