import csv
from selenium.common import exceptions
from YouTubeAnalysis.Util import utils


def getTitleAndUrl(driver):
    authorName = ""
    items = []
    try:
        items = driver.find_elements_by_xpath('//*[@id="video-title"]')
        authorName = driver.find_elements_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-browse/div['
                                                   '3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp'
                                                   '-yt-app-header/div[2]/div[2]/div/div[1]/div/div['
                                                   '1]/ytd-channel-name/div/div/yt-formatted-string')
        authorName = authorName[0].text
    except exceptions.NoSuchElementException:
        error = "Error: Double check sel  ector OR "
        error += "element may not yet be on the screen at the time of the find operation"
        print(error)

    with open("../Resource/Urls/" + authorName + ".txt", "a+", encoding="utf-8") as f:

        for item in items:
            f.write(item.text + "   " + item.get_attribute("href"))


def run(url):
    driver = utils.OpenChromeAndUrl(url)
    utils.ScrollWindowsToLowestEnd(driver)
    getTitleAndUrl(driver)


if __name__ == '__main__':
    # 这里输入视频主页URL
    run("https://www.youtube.com/channel/UCu7NhIfuD79werXU8I52oaQ/videos")
