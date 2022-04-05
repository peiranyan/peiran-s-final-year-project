import collections
import jieba
from YouTubeAnalysis.Util import utils
from YouTubeAnalysis.Util import translate
from YouTubeAnalysis.Resource import videoInfo


def dealChinese(vid):
    bullets = utils.readFromFile("../Resource/Bullets/" + vid + ".txt")

    data = " ".join(bullets).lower()

    split_word = jieba.cut(data)

    stopWords = utils.ReadStopWord()

    result = []
    for word in split_word:

        word = word.strip()
        if word not in stopWords and len(word) > 0:
            result.append(word)

    word_count = collections.Counter(result)

    top100 = word_count.most_common(100)
    return top100


def dealEnglish(ID):
    comments = utils.readFromFile("../Resource/Comments/" + ID + ".txt")

    data = " ".join(comments).replace("\n", " ").lower()

    split_word = data.split(" ")

    stopWords = utils.ReadStopWord()

    result = []
    for word in split_word:
        word = word.strip()
        if word not in stopWords and len(word) > 0:
            result.append(word)

    word_count = collections.Counter(result)

    top100 = word_count.most_common(100)

    return top100


def compare(BID, YID):
    bulletin = dealChinese(BID)
    youtube = dealEnglish(YID)

    inBulletinNotInComment = []
    EnglishList = []
    for i in youtube:
        EnglishList.append(i[0].lower())
    for b in bulletin:
        trans = translate.translate(b[0]).lower()
        if trans not in EnglishList:
            inBulletinNotInComment.append((b[0], b[1]))
    print("result", inBulletinNotInComment)

    inCommentNotInBulletin = []
    ChineseList = []
    for i in bulletin:
        ChineseList.append(i[0])
    for c in youtube:
        trans = translate.translate(c[0], 'en', 'zh').lower()
        if trans not in ChineseList:
            inCommentNotInBulletin.append((c[0], c[1]))

    with open("../Resource/CompareResult/bid:" + BID + " yid:" + YID + ".txt", "a+", encoding="utf-8") as f:
        f.write("in bulletin but not in comment \n")
        for i in inCommentNotInBulletin:
            f.write(str(i[0]) + ", " + str(i[1]) + "\n")
        f.write("in comment but not in bulletin \n")
        for i in inBulletinNotInComment:
            f.write(str(i[0]) + ", " + str(i[1]) + "\n")


if __name__ == '__main__':
    for i in videoInfo.configs["videos"]:
        compare(i["Bid"], i["Yid"])
