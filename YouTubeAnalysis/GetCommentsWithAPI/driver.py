import csv
import comment_extract
from YouTubeAnalysis.Util import utils

def readVideoIDsFromFile():
    IDs = []
    with open("urls.csv", "r", encoding="utf-8") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) >= 2:
                index = row[1].index("watch?v=")
                ID = row[1][index + 8:]
                IDs.append(ID)
    return IDs


def getComments(ID, countOfComment):
    videoId = ID

    count = countOfComment
    comments = comment_extract.commentExtract(videoId, count)
    with open("../Resource/Comments/" + ID + ".txt", "w", encoding="utf-8") as f:
        for comment in comments:
            f.write(comment.replace("\n", " ") + "\n")
            f.write("\n")


if __name__ == '__main__':
    YIDs = utils.GetAllYid()
    # Get all ids and crawl 1000 comments per video
    for i in YIDs:
        getComments(i, 1000)

