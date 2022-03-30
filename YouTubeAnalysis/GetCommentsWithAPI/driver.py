import csv

import langid

import comment_extract

from YouTubeAnalysis.util import utils


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
    with open("commentOf" + ID + ".csv", "a", encoding="utf-8") as f:
        for comment in comments:
            f.write(comment.replace("\n", " ") + "\n")
            f.write("\n")
    sheet = utils.getCollection2MongoDB("comment")
    sheet.insert_one({"ID": ID, "comments": comments})
    with open("../comments/"+ID + ".csv", "a+", encoding='utf-16')as f:
        writer = csv.writer(f, delimiter=",", quoting=csv.QUOTE_ALL)
        for comment in comments:
            if langid.classify(comment)[0] == "en":
                writer.writerow([comment])
                print(comment)


def main():
    getComments("in3pYWFwPvE", 1000)


if __name__ == '__main__':
    main()
