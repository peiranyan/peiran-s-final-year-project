import csv
import jieba
from YouTubeAnalysis.util import utils
from wordcloud import WordCloud, STOPWORDS, wordcloud
import collections
import matplotlib.pyplot as plt
import translate


def readFromFile(fileName):
    result = []
    with open(fileName, "r", encoding="utf-16") as f:
        reader = csv.reader(f)
        for row in reader:
            if len(row) != 0:
                result.append(row[0])
                print(row)
    return result


def drawWordCloud(word_counts):
    wc = wordcloud.WordCloud(
        # 设置字体，不指定就会出现乱码

        # 设置背景色
        background_color='white',
        # 设置背景宽
        width=500,
        # 设置背景高
        height=350,
        # 最大字体
        max_font_size=50,
        # 最小字体
        min_font_size=10,
        mode='RGBA'
        # colormap='pink'
    ).generate_from_frequencies(word_counts)

    plt.imshow(wc, interpolation='bilinear')
    # 显示设置词云图中无坐标轴
    plt.axis('off')
    # plt.savefig("../comments/" + ID + ".png")
    plt.show()


def newDrawWordCloud(split_word, my_stop_words):
    sw = set(STOPWORDS)
    for word in my_stop_words:
        sw.add(word)
    my_wordcloud = WordCloud(scale=4, font_path="simhei", stopwords=sw, background_color='white',
                             max_words=100, max_font_size=60, random_state=20).generate(" ".join(split_word))

    plt.imshow(my_wordcloud)
    plt.axis("off")
    plt.show()


def dealChinese(vid):
    sheet = utils.getCollection2MongoDB("bullet")
    bullets = sheet.find_one({"vid": vid})["bullets"]

    data = " ".join(bullets).lower()

    split_word = jieba.cut(data)

    stopWords = utils.readStopWord()
    # newDrawWordCloud(split_word, StopWords)

    result = []
    for word in split_word:
        word = word.strip()
        if word not in stopWords and len(word) > 0:
            result.append(word)

    word_count = collections.Counter(result)

    top100 = word_count.most_common(100)
    # with open(vid + ".csv", "a+", encoding="utf-8") as f:
    #     f.write("词,词频\n")
    #     for i in top100:
    #         f.write(i[0] + " , " + str(i[1]) + "\n")
    return top100


def dealEnglish(ID):
    sheet = utils.getCollection2MongoDB("comment")
    comments = sheet.find_one({"ID": ID})["comments"]

    data = " ".join(comments).replace("\n", " ").lower()

    split_word = data.split(" ")

    stopWords = utils.readStopWord()
    # newDrawWordCloud(split_word, StopWords)

    result = []
    for word in split_word:
        word = word.strip()
        if word not in stopWords and len(word) > 0:
            result.append(word)

    word_count = collections.Counter(result)

    top100 = word_count.most_common(100)

    return top100


if __name__ == '__main__':
    # IDs = driver.readVideoIDsFromFile()
    # for ID in IDs:
    #     drawWordCloud(ID)
    bId = "BV1GS4y1o7Bs"
    yid = "in3pYWFwPvE"
    bulletin = dealChinese(bId)
    youtube = dealEnglish(yid)
    result = []
    #
    # # 中文转英文
    # englishList = []
    # for i in youtube:
    #     englishList.append(i[0].lower())
    # for b in bulletin:
    #     trans = translate.translate(b[0])
    #     if trans not in englishList:
    #         result.append((b[0], b[1]))
    #
    ChineseList = []
    for i in bulletin:
        ChineseList.append(i[0])
    for b in youtube:
        trans = translate.translate(b[0], 'en', 'zh')
        if trans not in ChineseList:
            result.append((b[0], b[1]))

    print(result)

    with open(bId + ".csv", "a+", encoding="utf-8") as f:
        f.write("单词, 次数\n")
        for r in result:
            f.write(str(r[0]) + "," + str(r[1]) + "\n")
