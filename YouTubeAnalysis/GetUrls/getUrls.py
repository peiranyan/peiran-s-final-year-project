import csv
from selenium.common import exceptions
from YouTubeAnalysis.util import utils


def getTitleAndUrl(driver):
    try:
        items = driver.find_elements_by_xpath('//*[@id="video-title"]')
        authorName = driver.find_elements_by_xpath('/html/body/ytd-app/div/ytd-page-manager/ytd-browse/div['
                                                   '3]/ytd-c4-tabbed-header-renderer/tp-yt-app-header-layout/div/tp'
                                                   '-yt-app-header/div[2]/div[2]/div/div[1]/div/div['
                                                   '1]/ytd-channel-name/div/div/yt-formatted-string')
        print(authorName[0].text)
        authorName = authorName[0].text
    except exceptions.NoSuchElementException:
        error = "Error: Double check sel  ector OR "
        error += "element may not yet be on the screen at the time of the find operation"
        print(error)

    with open('urls.csv', "a+", encoding="utf-8") as f:
        writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_ALL)
        writer.writerow(["title", "url"])
        for item in items:
            writer.writerow([item.text, item.get_attribute("href")])
    sheet = utils.getCollection2MongoDB("url")
    for item in items:
        print("插入mongodb")
        sheet.insert_one({"title": item.text, "href": item.get_attribute("href"), "author": authorName})


def run(url):
    driver = utils.OpenChromeAndUrl(url)
    utils.ScrollWindowsToLowestEnd(driver)
    getTitleAndUrl(driver)


if __name__ == '__main__':
    run("https://www.youtube.com/channel/UCu7NhIfuD79werXU8I52oaQ/videos")
