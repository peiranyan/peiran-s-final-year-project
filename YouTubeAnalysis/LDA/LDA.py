import matplotlib.pyplot as plt
import pyLDAvis.gensim_models
from gensim import corpora, models
from gensim.models import CoherenceModel
from YouTubeAnalysis.Util import utils


def calLDA(documents, topics):
    words_ls = []
    stopwords = utils.ReadStopWord()

    for text in documents:
        words = []
        for w in text.split(" "):
            if w not in stopwords and len(w) > 0:
                words.append(w)
        words_ls.append(words)

    # Generate a dictionary of idiomatic expressions
    dictionary = corpora.Dictionary(words_ls)
    # Generate sparse vector sets
    corpus = [dictionary.doc2bow(words) for words in words_ls]
    # LDA model
    lda = models.ldamodel.LdaModel(corpus=corpus, id2word=dictionary, num_topics=topics)

    c = CoherenceModel(model=lda, texts=words_ls, dictionary=dictionary, coherence='c_v')

    plot = pyLDAvis.gensim_models.prepare(lda, corpus, dictionary, mds='mmds')
    # Save as .html file
    pyLDAvis.save_html(plot, 'pyLDAvis.html')

    # Show the top 10 words in one topic
    with open("../GetCommentsWithAPI/topic.txt", "w+", encoding="utf-8") as f:
        for topic in lda.print_topics(num_words=10):
            print(topic)
            f.write(str(topic[0]) + " ---> " + str(topic[1]) + "\n")


    print('Result：')
    result = []
    for e, values in enumerate(lda.inference(corpus)[0]):
        topic_val = 0
        topic_id = 0
        for tid, val in enumerate(values):
            if val > topic_val:
                topic_val = val
                topic_id = tid
        result.append(str(topic_id) + '->' + str(documents[e]))
    result.sort()
    return result





if __name__ == '__main__':
    yid = "T3_oj9hh1ag"
    texts = utils.readFromFile("../Resource/Comments/" + yid + ".txt")
    comments = []
    for t in texts:
        comments.append(t.replace("\n", " "))
    calLDA(comments, 4)
