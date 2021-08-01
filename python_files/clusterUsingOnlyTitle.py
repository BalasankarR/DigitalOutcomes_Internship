# -*- coding: utf-8 -*-
"""clusterUsingOnlyTitle.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1VezwnNkCXhP-3nmx4xtpEX-Fur5czZp2
"""

import json, os, sys
import numpy as np
import time
import csv
import re
import pandas as pd
from bs4 import BeautifulSoup
import requests
import html

"""#### We connect to MongoDB and load the News Articles data from the Fortune1000 database and NewsArticles Collection."""

cluster_uri = 'mongodb+srv://Balasankar:balasankar01@cluster0.k4d0t.mongodb.net/Fortune1000?retryWrites=true&w=majority'
comp_client = pymongo.MongoClient(cluster_uri)

comps = comp_client['Fortune1000']['NewsArticles']
companies_newsArticles = []
for x in comps.find():
    del x['_id']
    companies_newsArticles.append(x)
    
titles = []
for j in range(len(companies_newsArticles)):
    d = companies_newsArticles[j]
    i_max = len(d.keys()) - 2
    
    t = []
    c = []
    for i in range(i_max):
        if(not pd.isna(d[str(i)])):
            t.append(d[str(i)])
    titles.append(t)

comp_l = []
from sklearn.feature_extraction import text

my_stop_words = text.ENGLISH_STOP_WORDS

for j in range(len(companies_newsArticles)):
    words_list = []
    for i in titles[j]:
        word_list = i.split(" ")
        for word in word_list:
            word = re.sub(r"[^A-Za-z0-9]+",'',word)
            if(word != '' and not(word in my_stop_words)):
                words_list.append(word.lower())
    words = " ".join(words_list)
    comp_l.append(words)

comp_l[0]

from sklearn.feature_extraction.text import TfidfVectorizer

vectorizer = TfidfVectorizer(stop_words = my_stop_words,ngram_range = (1,2))
X = vectorizer.fit_transform(comp_l)
print(X.shape)

from sklearn.decomposition import TruncatedSVD
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import Normalizer
svd = TruncatedSVD(n_components = 100, n_iter = 10, random_state = 0)
normalizer = Normalizer(copy = False)
lsa = make_pipeline(svd, normalizer)

X = lsa.fit_transform(X)

print(X.shape)

from sklearn.cluster import KMeans
no_clusters = 50
km = KMeans(n_clusters=no_clusters, init='k-means++', max_iter=1000, n_init=100)
cluster_list = km.fit_predict(X).tolist()

count = np.zeros(no_clusters)
for i in cluster_list:
    count[i] += 1
count

comp = []
for j in range(1000):
    comp.append(companies_newsArticles[j]['Name'])

for j in range(no_clusters):
    print("------ Cluster {} -----".format(j))
    for i in range(len(cluster_list)):
        if(cluster_list[i] == j):
            print(comp[i])
