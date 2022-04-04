import requests
import time
import sys
import langid

YOUTUBE_IN_LINK = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&order=relevance&pageToken={pageToken}&videoId={videoId}&key={key}'
YOUTUBE_LINK = 'https://www.googleapis.com/youtube/v3/commentThreads?part=snippet&maxResults=100&order=relevance&videoId={videoId}&key={key}'
key = 'AIzaSyB79D7aUsAxJUla6gJqqFsXvelkin3y434'


def commentExtract(videoId, count=-1):
    print("Comments downloading")
    page_info = requests.get(YOUTUBE_LINK.format(videoId=videoId, key=key))
    while page_info.status_code != 200:
        if page_info.status_code != 429:
            print("Comments disabled")
            sys.exit()

        page_info = requests.get(YOUTUBE_LINK.format(videoId=videoId, key=key))

    page_info = page_info.json()
    comments = []
    co = 0

    for i in range(len(page_info['items'])):
        comment = page_info['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal']
        if langid.classify(comment)[0] == "en":
            comments.append(comment)
            print(comment)
            co += 1
            if co == count:
                return comments

    while 'nextPageToken' in page_info:
        temp = page_info
        page_info = requests.get(YOUTUBE_IN_LINK.format(videoId=videoId, key=key, pageToken=page_info['nextPageToken']))

        while page_info.status_code != 200:
            time.sleep(20)
            page_info = requests.get(YOUTUBE_IN_LINK.format(videoId=videoId, key=key, pageToken=temp['nextPageToken']))
        page_info = page_info.json()

        for i in range(len(page_info['items'])):
            comment = page_info['items'][i]['snippet']['topLevelComment']['snippet']['textOriginal']
            if langid.classify(comment)[0] == "en":
                comments.append(comment)
                print(comment)
                co += 1
                if co == count:
                    return comments

    return comments
