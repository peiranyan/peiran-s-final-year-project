import numpy as np
import pyLDAvis
import pyLDAvis.gensim_models
from biterm.cbtm import oBTM
from sklearn.feature_extraction.text import CountVectorizer
from biterm.utility import vec_to_biterms, topic_summuary  # helper functions
from YouTubeAnalysis.Util import utils


def BTM(file, topicNum):
    comment = open(file).read().splitlines()

    texts = [i for i in comment if len(i) > 0 and len(set(i.split(" "))) > 1]

    vec = CountVectorizer(stop_words='english')
    X = vec.fit_transform(texts).toarray()

    # For processing broken sentences
    for i in range(len(X)):
        if sum(X[i]) <= 2:
            X[i][0] = 1
            X[i][-1] = 1

    # get vocabulary
    vocab = np.array(vec.get_feature_names_out())

    # get biterms
    biterms = vec_to_biterms(X)

    # create btm
    btm = oBTM(num_topics=topicNum, V=vocab)

    print("\n\n Train Online BTM ..")
    for i in range(0, len(biterms), 100):  # prozess chunk of 200 texts
        biterms_chunk = biterms[i:i + 100]
        btm.fit(biterms_chunk, iterations=50)
    topics = btm.transform(biterms)

    print("\n\n Visualize Topics ..")
    vis = pyLDAvis.prepare(btm.phi_wz.T, topics, np.count_nonzero(X, axis=1), vocab, np.sum(X, axis=0), mds='mmds')

    pyLDAvis.save_html(vis, "./online_btm.html")

    print("\n\n Topic coherence ..")
    topic_summuary(btm.phi_wz.T, X, vocab, 10)

    print("\n\n Texts & Topics ..")
    for i in range(len(texts)):
        print("{} (topic: {})".format(texts[i], topics[i].argmax()))


if __name__ == "__main__":
    yid = "T3_oj9hh1ag"
    BTM("../Resource/Comments/" + yid + ".txt", 4)
