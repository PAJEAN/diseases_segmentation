# -*- coding: utf-8 -*-

"""
Baseline TF-IDF and euclidean distance!
"""

import codecs, os, sys, json
import numpy as np
from optparse import OptionParser
from scipy.spatial.distance import cosine
from scipy.spatial.distance import euclidean

def pairwise_distance(binary_features, use_euclidean):

    # Load diseases dictionnary with symptoms and associated tfidf.
    with codecs.open(os.path.join("mesh", "data", "diseases-symptoms.json"), "r", encoding="utf-8") as fin:
        diseases = json.load(fin)

    # Load symptoms index to have symptoms id vector.
    with codecs.open(os.path.join("mesh", "data", "index-symptoms.json"), "r", encoding="utf-8") as fin:
        symptoms_id = json.load(fin)

    #  Load queries file compute distance between pairs of diseases (like SML inputs).
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

    if len(features) > 0:
        print(f"Number of symptoms: {len(features[0])}")

    # Compute distances between pairs of diseases.
    min_value = max_value = 0.0
    if len(queries) > 0:
        min_value = max_value = euclidean(features[diseases_id.index(queries[0][0])], features[diseases_id.index(queries[0][1])])

    res = {}
    for index,q in enumerate(queries):
        if index % 500000 == 0:
            print(f"query n° {index} on {len(queries)}")

        if use_euclidean:
            value = euclidean(features[diseases_id.index(q[0])], features[diseases_id.index(q[1])])
            if value < min_value:
                min_value = value
            if value > max_value:
                max_value = value
        else:
            value = cosine(features[diseases_id.index(q[0])], features[diseases_id.index(q[1])])
            # To avoid float innacuraccy (-2.e^-16).
            value = np.clip(value, 0.0, 1.0)

        if q[0] in res:
            res[q[0]][q[1]] = value
        else:
            res[q[0]] = {q[1]: value}

    if use_euclidean:
        for d1 in res:
            for d2 in res[d1]:
                normalize_value = (res[d1][d2] - min_value) / (max_value - min_value)
                res[d1][d2] = normalize_value

    fname = "baseline.json"
    if binary_features:
        fname = "baseline_binary.json"

    with codecs.open(os.path.join("mesh", "pairwise_distances", fname), "w", "utf-8") as fout:
        json.dump(res, fout, indent=4)

if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-b", "--binary", action="store_true",
        default=False, help="use binary features")
    parser.add_option("-e", "--euclidean_distance", action="store_true",
        default=False, help="use euclidean distance")
    (options, args) = parser.parse_args()

    pairwise_distance(options.binary, options.euclidean_distance)








