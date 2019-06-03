# -*- coding: utf-8 -*-

"""
Baseline TF-IDF and euclidean distance.
"""

import codecs, os, sys, json
import numpy as np
from optparse import OptionParser
from sklearn.cluster import KMeans
from sklearn.preprocessing import Normalizer


def pairwise_distance(binary_features, normalization):

    # Load diseases dictionnary with symptoms and associated tfidf.
    with codecs.open(os.path.join("mesh", "data", "diseases-symptoms.json"), "r", encoding="utf-8") as fin:
        diseases = json.load(fin)

    # Load symptoms index to have symptoms id vector.
    with codecs.open(os.path.join("mesh", "data", "index-symptoms.json"), "r", encoding="utf-8") as fin:
        symptoms_id = json.load(fin)

    #  Load queries file.
    # [["DD015658", "DD000163"], ...]
    with codecs.open(os.path.join("mesh", "data", "queries.json"), "r", encoding="utf-8") as fin:
        queries = json.load(fin)

    # Build matrix like diseases_id X symptoms_id.
    diseases_id = list(diseases.keys())
    print(f"Length of diseases: {len(diseases_id)}")
    # Keep to each disease, tfidf or binary values for each symptom.
    features = []
    for d_id in diseases_id:
        feature = []
        for s in symptoms_id:
            value = 0.0
            if s in diseases[d_id]["symptoms"]:
                if binary_features:
                    value = 1.0
                else:
                    value = diseases[d_id]["tfidf"][diseases[d_id]["symptoms"].index(s)]
            feature.append(value)
        features.append(feature)

    if normalization:
        print("Normalization: ON")
        features = Normalizer().fit_transform(features)

    # Kmeans on observation vectors.
    kmeans = KMeans(n_clusters=24, random_state=0).fit(features)
    clusters = {}
    for index, d_id in enumerate(diseases_id):
        clusters[d_id] = int(kmeans.labels_[index])

    fname = "kmeans.json"
    with codecs.open(os.path.join("mesh", "clusters", fname), "w", "utf-8") as fout:
        json.dump(clusters, fout, indent=4)

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-b", "--binary", action="store_true",
        default=False, help="use binary features")
    parser.add_option("-n", "--normalize", action="store_true",
	    default=False, help="normalize distance matrix")
    (options, args) = parser.parse_args()

    pairwise_distance(options.binary, options.normalize)
