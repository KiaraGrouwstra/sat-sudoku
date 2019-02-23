import numpy as np

def read_file(file_name):
	with open(file_name) as f:
		contents = f.readlines()
	return contents

def parse_dimacs_dict(dimacs_file_contents):
	clause_dict = {}
	rows = list(filter(lambda s : s[0] not in ['c', 'p', 'd'], dimacs_file_contents))
	for i in range(len(rows)):
		temp_dict = {}
		term_list = rows[i].split(' ')
		del term_list[-1]
		for term in term_list:
			key = int(''.join(list(term)[1:])) if term[0] == '-' else int(term)
			temp_dict[key] = -1 if term[0] == '-' else 1
		clause_dict[i] = temp_dict
	return clause_dict

contents = read_file('sudoku-example.txt')
clause_dict = parse_dimacs_dict(contents)
print(clause_dict)