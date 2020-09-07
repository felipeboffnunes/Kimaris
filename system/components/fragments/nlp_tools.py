# Python Standard Libraries
from collections import Counter
import string
import re
# External Libraries
from nltk.corpus import stopwords
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer
from sklearn.decomposition import LatentDirichletAllocation as LDA
import numpy as np
import pyLDAvis
import pyLDAvis.sklearn

STOPWORDS = set(stopwords.words("english"))

def tokenize_string(string:str) -> list:
    tknzr = TweetTokenizer()
    return tknzr.tokenize(string)

def get_most_common_words(data):
    common_words = Counter()
    #for row in data:
    for word in data.split(" "):
        if len(word) > 3 and not word in STOPWORDS:
            punctuation = str.maketrans(dict.fromkeys(string.punctuation))
            word = word.translate(punctuation)
            common_words[word] += 1
    return common_words

def get_most_common_bigrams(data):
    common_bigrams = Counter()
    
    last_word = ""
    rows = data.split(" ")
    for word in rows:
        punctuation = str.maketrans(dict.fromkeys(string.punctuation))
        word = word.translate(punctuation)
        if len(word) > 3 and not word in STOPWORDS:
            if len(last_word) > 3 and not word in STOPWORDS:
                common_bigrams[f"{last_word} {word}"] += 1
        last_word = word
    return common_bigrams

def get_most_common_trigrams(data):
    common_trigrams = Counter()
    
    last_word = ""
    last_last_word = ""
    rows = data.split(" ")
    for word in rows:
        punctuation = str.maketrans(dict.fromkeys(string.punctuation))
        word = word.translate(punctuation)
        if len(word) > 3 and not word in STOPWORDS:
            if len(last_word) > 3 and not word in STOPWORDS:
                if len(last_last_word) > 3 and not word in STOPWORDS:
                    common_trigrams[f"{last_last_word} {last_word} {word}"] += 1
        last_last_word = last_word
        last_word = word
    return common_trigrams

import nltk
from nltk.tokenize import word_tokenize
import re
#nltk.download('averaged_perceptron_tagger')          
def get_most_common_speech_tagging(data):
    common_speech_tagging = Counter()
    
    for word in data.split(" "):
        word = re.sub('[^A-Za-z0-9]+', '', word)
        print(word)
        if len(word) > 1:
            punctuation = str.maketrans(dict.fromkeys(string.punctuation))
            word = word.translate(punctuation)
            tagged = nltk.pos_tag([word])
            print(word)
            print(tagged[0][1])
            tag = tagged[0][1]
            common_speech_tagging[tag] += 1
            print("here")
    return common_speech_tagging
    


def get_most_common_words_lemmatized(data):
    common_words = Counter()
    for row in data:
        tokens = tokenize_string(row)
        for word in tokens:
            punctuation = str.maketrans(dict.fromkeys(string.punctuation))
            word = word.translate(punctuation)
            common_words[word] += 1
    return common_words

def remove_common_stop_words(common_words):
    for i, word in enumerate(list(common_words)):
        # This allows the method to be used on bigrams
        if isinstance(word, tuple):
            words = word[0].split(" ")
            for word in words:
                if word in stopwords.words("english") or len(word) < 3:
                    common_words[i] = ("", 0)
        else:
            if word in stopwords.words("english") or len(word) < 3:
                    common_words[word] = 0
    return common_words

def topic_modelling(title, data):
    # Remove punctuation
    data = re.sub('[,\.!?]', '', data)
    
    # Remove numbers
    data = re.sub('[0-9]', '', data)
    
    
    # Convert the titles to lowercase
    data = data.lower()
    length = len(data)
    index = 0
    last_i = 0
    n=256
    snnipets = []
    while index < length:
        i = data.rfind(". ", index, index + n)
        if i == -1 or i == index:
            i = index + n
        text = data[index : i + 2]
        index = i + 2
        snnipets.append(text)
        
    tf_vectorizer  = CountVectorizer(stop_words='english')
    #dtm_tf  = tf_vectorizer.fit_transform(snnipets)
    #print(dtm_tf.shape)
    
    tfidf_vectorizer = TfidfVectorizer(**tf_vectorizer.get_params())
    dtm_tfidf = tfidf_vectorizer.fit_transform(snnipets)

    number_topics = 3
    number_words = 10
    
    #lda_tf  = LDA(n_components=number_topics, n_jobs=1)
    #lda_tf.fit(dtm_tf)
    
    lda_tfidf = LDA(n_components=number_topics, random_state=0)
    lda_tfidf.fit(dtm_tfidf)
    
    data = pyLDAvis.sklearn.prepare(lda_tfidf, dtm_tfidf, tfidf_vectorizer, mds='mmds')
   
    html = pyLDAvis.prepared_data_to_html(data, template_type="simple")
    return html



import spacy
from spacy.lang.en import English
import networkx as nx
import matplotlib.pyplot as plt

def getSentences(text):
    nlp = English()
    nlp.add_pipe(nlp.create_pipe('sentencizer'))
    document = nlp(text)
    return [sent.string.strip() for sent in document.sents]

def printToken(token):
    print(token.text, "->", token.dep_)

def appendChunk(original, chunk):
    return original + ' ' + chunk

def isRelationCandidate(token):
    deps = ["ROOT", "adj", "attr", "agent", "amod", "cc"]
    return any(subs in token.dep_ for subs in deps)

def isConstructionCandidate(token):
    deps = ["compound", "noun", "mod", "nsubj", "conj","prep", "pobj"]
    return any(subs in token.dep_ for subs in deps)

def processSubjectObjectPairs(tokens):
    subject = ''
    object = ''
    relation = ''
    subjectConstruction = ''
    objectConstruction = ''
    for token in tokens:
        printToken(token)
        if "punct" in token.dep_:
            continue
        if isRelationCandidate(token):
            relation = appendChunk(relation, token.text)
        if isConstructionCandidate(token):
            if subjectConstruction:
                subjectConstruction = appendChunk(subjectConstruction, token.text)
            if objectConstruction:
                objectConstruction = appendChunk(objectConstruction, token.text)
        if "subj" in token.dep_:
            subject = appendChunk(subject, token.text)
            subject = appendChunk(subjectConstruction, subject)
            subjectConstruction = ''
        if "obj" in token.dep_:
            object = appendChunk(object, token.text)
            object = appendChunk(objectConstruction, object)
            objectConstruction = ''

    print (subject.strip(), ",", relation.strip(), ",", object.strip())
    return (subject.strip(), relation.strip(), object.strip())

def processSentence(nlp_model,sentence):
    tokens = nlp_model(sentence)
    return processSubjectObjectPairs(tokens)

def printGraph(triples):
    G = nx.Graph()
    for triple in triples:
        G.add_node(triple[0])
        G.add_node(triple[1])
        G.add_node(triple[2])
        G.add_edge(triple[0], triple[1])
        G.add_edge(triple[1], triple[2])
    print("196")
    pos = nx.layout.spring_layout(G, dim=3)
    print(pos)
    return pos, G