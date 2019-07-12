# -*- coding: utf-8 -*-

import codecs, os, sys, json
import matplotlib.pyplot as plt

def statistics():
	# Load diseases dictionnary with symptoms and associated tfidf.
	with codecs.open(os.path.join("mesh", "data", "diseases-symptoms.json"), "r", encoding="utf-8") as fin:
		diseases = json.load(fin)
	# Load label's diseases.
	with codecs.open(os.path.join("mesh", "diseases-symptoms-labels.json"), "r", encoding="utf-8") as fin:
		labels = json.load(fin)
		# Load label's diseases.
	with codecs.open(os.path.join("mesh", "diseases-symptoms-labels-full.json"), "r", encoding="utf-8") as fin:
		full_labels = json.load(fin)
	# Load label's diseases.
	with codecs.open(os.path.join("mesh", "diseases-symptoms-1_label.json"), "r", encoding="utf-8") as fin:
		one_labels = json.load(fin)
	# Load symptoms index to have symptoms descriptors.
	with codecs.open(os.path.join("mesh", "data", "index-symptoms.json"), "r", encoding="utf-8") as fin:
		symptom_descriptors = json.load(fin)

	mean = []
	depths = []
	for d in diseases:
		mean.append(len(diseases[d]["symptoms"]))
		for s in diseases[d]["symptoms"]:
			depth = 0
			for l in full_labels[s]:
				spl = l.strip().split(".")
				if len(spl) > depth:
					depth = len(spl)
			depths.append(depth)

	print(f"Number of diseases: {len(diseases)}")
	print(f"Mean of symptoms: {sum(mean)/len(mean)}")

	fig1, ax1 = plt.subplots()
	ax1.set_title('Number of symptoms by disease')
	boxP = ax1.boxplot(mean)
	plt.savefig(os.path.join("mesh", "images", "symptoms_by_disease.png"))
	# clears the entire current figure with all its axes, but leaves the window opened, such that it may be reused for other plots.
	plt.clf()
	plt.close()
	# Limit max of whiskers.
	limit_sup = boxP["whiskers"][1].get_data()[1][1]
	print(f"Limit sup: {limit_sup} symptoms max")
	# Depth of symptoms.
	fig1, ax1 = plt.subplots()
	ax1.set_title('Depth of symptoms')
	boxP = ax1.boxplot(depths)
	plt.savefig(os.path.join("mesh", "images", "depth_symptoms.png"))
	plt.clf()
	plt.close()

	# Most represented symptoms.
	one_label = {}
	symptoms = {}
	for d_id in diseases:
		label = one_labels[d_id]
		if not label in one_label:
			one_label[label] = {}

		for s_id in diseases[d_id]["symptoms"]:
			if s_id in symptoms:
				symptoms[s_id] += 1
			else:
				symptoms[s_id] = 1

			if s_id in one_label[label]:
				one_label[label][s_id] += 1
			else:
				one_label[label][s_id] = 1

	sorted_symptoms = sorted(symptoms.items(), key=lambda kv: kv[1], reverse=True) # Desc order.
	symptoms = {"categories": [], "values": []}
	for i in range(30):
		symptoms["categories"].append("; ".join(symptom_descriptors[sorted_symptoms[i][0]]))
		symptoms["values"].append(sorted_symptoms[i][1])
	fig1, ax1 = plt.subplots(figsize=(20,10))
	ax1.set_title('Most represented symptoms')
	plt.barh(symptoms["categories"], symptoms["values"])
	plt.xticks(rotation=40)
	plt.savefig(os.path.join("mesh", "images", "most_represented_symptoms.png"))
	plt.clf()
	plt.close()

	# Most represented symptoms by labels (class).
	with codecs.open(os.path.join("mesh", "images", "most_represented_symptoms_by_class.txt"), "w", encoding="utf-8") as fout:
		for i in range(1,27):
			# Ordering labels.
			label = "C"
			if i < 10:
			    label += "0"
			label += str(i)
			if label in one_label:
				fout.write(f"{label}\n")
				sorted_symptoms = sorted(one_label[label].items(), key=lambda kv: kv[1], reverse=True) # Desc order.
				for i in range(len(sorted_symptoms[:3])):
					fout_str = "; ".join(symptom_descriptors[sorted_symptoms[i][0]])
					esp = 50 - len(fout_str)
					if esp <= 0:
						esp = 1
					for j in range(esp):
						fout_str += " "
					fout.write(f"\t{fout_str} | {sorted_symptoms[i][1]}\n")
					#print("\t", "; ".join(symptom_descriptors[sorted_symptoms[i][0]]), " | ", sorted_symptoms[i][1])

	# Limitation on number of symptoms by diseases.
	limit_inf = 5
	limit_sup = 40

	kept_diseases = []
	set_labels = set()
	for d in diseases:
		if len(diseases[d]["symptoms"]) >= limit_inf and len(diseases[d]["symptoms"]) <= limit_sup:
			kept_diseases.append(d)
			for l in labels[d]:
				if l[0] == "C":
					set_labels.add(l)

	print(f"Number of diseases with a limitation: {len(kept_diseases)}")
	print(f"Number of labels with a limitation: {len(set_labels)}")

if __name__ == "__main__":
	statistics()