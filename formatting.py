# -*- coding: utf-8 -*-

import codecs, os, sys, json
from optparse import OptionParser

# Convert the txt queries file to json format.
def queries():
	queries = []
	with codecs.open(os.path.join("mesh", "data", "queries.tsv"), "r", encoding="utf-8") as fin:
		content = fin.readlines()
		for line in content:
			spl_line = line.strip().split("\t")
			if len(spl_line) == 2:
				# Delete [D]D000162.
				spl_line[0] = spl_line[0][1:]
				spl_line[1] = spl_line[1][1:]
				queries.append(spl_line)
				
	with codecs.open(os.path.join("mesh", "data", "queries.json"), "w", "utf-8") as fout:
		json.dump(queries, fout, indent=4)
		
# Extract the col-th column of sml result file and return a json format file.
def sml_results(content, headers, col, normalize):
	res = {}
	line_length = len(headers)
	min_value = max_value = 0.0
	if len(content) > 0:
		spl_line = content[0].strip().split("\t")
		min_value = float(spl_line[col])
		max_value = float(spl_line[col])
	
	for index,line in enumerate(content):
		if index % 500000 == 0:
			print(index,"/",len(content))
		
		spl_line = line.strip().split("\t")
        # Take into account header in file.
		if len(spl_line) == line_length:
			# Delete [D]D000163.
			spl_line[0] = spl_line[0][1:]
			spl_line[1] = spl_line[1][1:]
			# Extract a specific column.
			if spl_line[0] in res:
				res[spl_line[0]][spl_line[1]] = float(spl_line[col])
			else:
				res[spl_line[0]] = {spl_line[1]: float(spl_line[col])}
			
			if float(spl_line[col]) < min_value:
				min_value = float(spl_line[col])
			if float(spl_line[col]) > max_value:
				max_value = float(spl_line[col])
	
	# Convert similarity to distance.
	for d1 in res:
		for d2 in res[d1]:
			if normalize:
				normalize_value = (res[d1][d2] - min_value) / (max_value - min_value)
				res[d1][d2] = 1.0 - normalize_value
			else:
				res[d1][d2] = 1.0 - res[d1][d2]
	
	fname = f"{headers[col]}.json"
	with codecs.open(os.path.join("mesh", "pairwise_distances", fname), "w", "utf-8") as fout:
		json.dump(res, fout, indent=4)

if __name__ == "__main__":
	parser = OptionParser()
	parser.add_option("-r", "--result", action="store_true",
		default=False, help="extract results from sml results file")
	parser.add_option("-c", "--column",
		default=2, help="index of extracted column with -r option (default 2)")
	parser.add_option("-a", "--all_results", action="store_true",
        default=False, help="extract all results from sml results file")
	parser.add_option("-n", "--normalize", action="store_true",
		default=False, help="normalize similarity measures")
	parser.add_option("-q", "--query", action="store_true",
        default=False, help="formatting queries file")
	(options, args) = parser.parse_args()
	
	if options.result == True or options.all_results == True:
		with codecs.open(os.path.join("mesh", "sml_results.tsv"), "r", encoding="utf-8") as fin:
			content = fin.readlines()
		headers = content[0].strip().split("\t")
		content = content[1:]
        
		if options.normalize:
			print("Normalization: ON")
		if options.result == True:
			sml_results(content, headers, options.column, options.normalize)
		if options.all_results == True:
			for i in range(2,len(headers)):
				sml_results(content, headers, i, options.normalize)
	
	if options.query == True:
		queries()



