import matplotlib.pyplot as plt
import pyLDAvis.gensim_models
from gensim import corpora, models
from gensim.models import CoherenceModel
from YouTubeAnalysis.util import utils


def calLDA(documents, topics):
    words_ls = []
    stopwords = utils.readStopWord()

    for text in documents:
        words = []
        for w in text.split(" "):
            if w not in stopwords and len(w) > 0:
                words.append(w)
        words_ls.append(words)

    # 生成语料词典
    dictionary = corpora.Dictionary(words_ls)
    # 生成稀疏向量集
    corpus = [dictionary.doc2bow(words) for words in words_ls]
    # LDA模型，num_topics设置聚类数，即最终主题的数量
    lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=topics)

    c = CoherenceModel(model=lda, texts=words_ls, dictionary=dictionary, coherence='c_v')

    plot = pyLDAvis.gensim_models.prepare(lda, corpus, dictionary)
    # 保存到本地html
    pyLDAvis.save_html(plot, 'pyLDAvis.html')

    # 展示每个主题的前5的词语
    with open("../GetCommentsWithAPI/topic.txt", "w+", encoding="utf-8") as f:
        for topic in lda.print_topics(num_words=10):
            print(topic)
            f.write(str(topic[0]) + " ---> " + str(topic[1]) + "\n")

    # 推断每个语料库中的主题类别
    print('推断：')
    result = []
    for e, values in enumerate(lda.inference(corpus)[0]):
        topic_val = 0
        topic_id = 0
        for tid, val in enumerate(values):
            if val > topic_val:
                topic_val = val
                topic_id = tid
        # print(topic_id, '->', documents[e])
        result.append(str(topic_id) + '->' + str(documents[e]))
    result.sort()
    coherenceScore = c.get_coherence()

    return result, coherenceScore


if __name__ == '__main__':
    texts = open("../resource/Comments/bGzbJpLExDM.txt").read().splitlines()
    comments = [i for i in texts if len(i) > 0]
    for t in texts:
        comments.append(t.replace("\n", " "))
    calLDA(comments, 5)

    # 获取一致性最大的结果
    # coherence = []
    # maxIndex = 1
    # maxValue = 0
    # for i in range(2, 11):
    #     c = calLDA(comments, i)[1]
    #     if c > maxValue:
    #         maxValue = c
    #         maxIndex = i


def drawCoherence(c):
    x = range(1, 11)
    plt.plot(x, c)
    plt.xlabel("Num Topics")
    plt.ylabel("coherence")
    plt.show()
