# -*- coding: utf-8 -*-

import codecs, sys, os, json
import numpy as np
from optparse import OptionParser
from scipy.spatial import distance
from sklearn.cluster import AgglomerativeClustering
from sklearn.preprocessing import Normalizer
from sklearn import metrics

def clustering(fname, queries, n_clusters, linkage, normalization):
	print(f"File name: {fname}")
	# Load result file in json format.
	with codecs.open(os.path.join("mesh", "pairwise_distances", fname), "r", encoding="utf-8") as fin:
		sml = json.load(fin)

	# Build condensed matrix.
	condensed_dist_matrix = []
	diseases_id = []
	for index,line in enumerate(queries):
		condensed_dist_matrix.append(float(sml[line[0]][line[1]]))
        #
		if not line[0] in diseases_id:
			diseases_id.append(line[0])
		if index+1 == len(queries):
			diseases_id.append(line[1])

	print(f"Length of considered diseases: {len(diseases_id)}")
	print(f"Length of condensed distance matrix: {len(condensed_dist_matrix)}")

	uncondensed_dist_matrix = distance.squareform(condensed_dist_matrix)

	if normalization:
		print("Normalization: ON")
		transform = Normalizer().fit_transform(uncondensed_dist_matrix)
		uncondensed_dist_matrix = transform

	clustering = AgglomerativeClustering(n_clusters=n_clusters, linkage=linkage).fit(uncondensed_dist_matrix)
	labels = clustering.labels_

	silhouette = metrics.silhouette_score(uncondensed_dist_matrix, labels, metric="euclidean")
	print(f"Silhouette score: {silhouette}")

	print(f"# of unique cluster: {len(np.unique(labels))}")

	if len(diseases_id) != len(labels):
		return "Error!"

	clusters = {}
	for i in range(len(labels)):
		clusters[diseases_id[i]] = int(labels[i])

	with codecs.open(os.path.join("mesh", "clusters", fname), "w", "utf-8") as fout:
		json.dump(clusters, fout, indent=4)

if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option("-f", "--file",
	    default="baseline.json", help="file name in pairwise_distances folder")
	parser.add_option("-c", "--cluster",
		default=24, help="number of desired clusters")
	parser.add_option("-l", "--linkage",
	    default="ward", help="linkage metric")
	parser.add_option("-n", "--normalize", action="store_true",
	    default=False, help="normalize distance matrix")
	parser.add_option("-a", "--all_files", action="store_true",
	    default=False, help="process all file in the pairwise_distances folder")
	(options, args) = parser.parse_args()

	# Load queries file in json format.
	with codecs.open(os.path.join("mesh", "data", "queries.json"), "r", encoding="utf-8") as fin:
		queries = json.load(fin)

	if options.all_files == True:
		for fname in os.listdir(os.path.join("mesh", "pairwise_distances")):
			clustering(fname, queries, options.cluster, options.linkage, options.normalize)
			print("-----------------------------------")
	else:
		clustering(options.file, queries, options.cluster, options.linkage, options.normalize)
