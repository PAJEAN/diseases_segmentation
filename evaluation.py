
import codecs, json, sys, os
import numpy as np
from optparse import OptionParser

def purity(clusters, labels):
    # Purity.
    # https://stats.stackexchange.com/questions/95731/how-to-calculate-purity

    labels_id = set()
    for id in labels:
        for label in labels[id]:
            # Keep only C class on MESH tree and each considered disease have only one label on C class.
            if label[0] == "C":
                labels_id.add(label)
    labels_id = list(labels_id)
    # To have C01, C02, ..., C26.
    labels_id.sort()
    
    # confusion matrix --> class X #Ind.
    confusion = []
    
    # Init a square confusion matrix.
    for i in range(len(labels_id)):
        confusion.append(np.zeros(len(labels_id)))

    #       C01, C02, ..., Cn
    # Cl0: [0  , 0  , ..., 0]
    # Cl1: [0  , 0  , ..., 0]
    # Cl2: [0  , 0  , ..., 0]
    
    total = 0
    for id in clusters: # Loop on diseases id.
        for label in labels[id]: # Loop on labels associated to diseases id.
            if label in labels_id: # Only one C class.
                confusion[clusters[id]][labels_id.index(label)] += 1
                total += 1
    
    if total != len(clusters):
        return("Error! Only one C class authorized")

    inter = 0
    total = 0
    for c in confusion:
        inter += max(c)
        total += sum(c)
    print(f"Purity: {inter/total}")


def true_false_positive_negative(clusters, queries, labels):
    # We want to assign two documents to the same cluster if and only if they are similar. A true positive (TP) decision assigns two similar documents to the same cluster, a true negative (TN) decision assigns two dissimilar documents to different clusters. There are two types of errors we can commit. A (FP) decision assigns two dissimilar documents to the same cluster. A (FN) decision assigns two similar documents to different clusters. The Rand index ( ) measures the percentage of decisions that are correct.
    TP = 0 # Si deux documents avec le même label sont dans le même cluster.
    FP = 0 # Si deux documents n'ayant pas le même label sont dans le même cluster.
    FN = 0 # Si deux documents avec le même label sont dans des clusters différents.
    TN = 0

    for q in queries:
        # Keep only C labels.
        label1 = set()
        for l in labels[q[0]]:
            if l[0] == "C":
                label1.add(l)
        label2 = set()
        for l in labels[q[1]]:
            if l[0] == "C":
                label2.add(l)
        # Similar if inter is not null.
        inter = label1.intersection(label2)
        if len(inter) > 0: # Similaire.
            if clusters[q[0]] == clusters[q[1]]:
                TP += 1
            else:
                FN += 1
        else: # Dissimilaire.
            if clusters[q[0]] == clusters[q[1]]:
                FP += 1
            else:
                TN += 1

    return {"TP": TP, "FP": FP, "FN": FN, "TN": TN}


def f1_mesure(stats):
    # F1-Mesure.
    # https://nlp.stanford.edu/IR-book/html/htmledition/evaluation-of-clustering-1.html.        
    precision = stats["TP"] / (stats["TP"]+stats["FP"])
    recall = stats["TP"] / (stats["TP"]+stats["FN"])
    f1_mesure = (2*precision*recall) / (precision + recall)
    print(f"F1-mesure: {f1_mesure} - [Precision: {precision}, Recall: {recall}]")
    
def rand_index(stats):
    rand_index = (stats["TP"]+stats["TN"]) / (stats["TP"]+stats["FP"]+stats["FN"]+stats["TN"])
    print(f"Rand index: {rand_index}")


if __name__ == "__main__":
    parser = OptionParser()
    parser.add_option("-f", "--file",
        default="baseline.json", help="file name")
    parser.add_option("-a", "--all_files", action="store_true",
        default=False, help="process all file in the clusters folder")
    (options, args) = parser.parse_args()
    
    # Load label's diseases.
    with codecs.open(os.path.join("mesh", "diseases-symptoms-labels.json"), "r", encoding="utf-8") as fin:
        labels = json.load(fin)
    # Load queries.
    with codecs.open(os.path.join("mesh", "data", "queries.json"), "r", encoding="utf-8") as fin:
        queries = json.load(fin)
    
    if options.all_files == True:
        for fname in os.listdir(os.path.join("mesh", "clusters")):
            print(f"--- {fname} ---")
            with codecs.open(os.path.join("mesh", "clusters", fname), "r", encoding="utf-8") as fin:
                clusters = json.load(fin)
                
            cluster = set()
            for c in clusters:
                cluster.add(clusters[c])
            print(f"#Cluster by AgglomerativeClustering: {len(cluster)}")
            
            stats = true_false_positive_negative(clusters, queries, labels)
            print(f"TP: {stats['TP']}, FP: {stats['FP']}, FN: {stats['FN']}, TN: {stats['TN']}")
            print("#####")
            purity(clusters, labels)
            f1_mesure(stats)
            rand_index(stats)
            print("#####\n")
    else:
        # Load cluster file.
        print(f"--- {options.file} ---")
        with codecs.open(os.path.join("mesh", "clusters", options.file), "r", encoding="utf-8") as fin:
            clusters = json.load(fin)
            
        cluster = set()
        for c in clusters:
            cluster.add(clusters[c])
        print(f"#Cluster by AgglomerativeClustering: {len(cluster)}")
        
        stats = true_false_positive_negative(clusters, queries, labels)
        print(f"TP: {stats['TP']}, FP: {stats['FP']}, FN: {stats['FN']}, TN: {stats['TN']}")
        print("#####")
        purity(clusters, labels)
        f1_mesure(stats)
        rand_index(stats)
        print("#####\n")
    








