import re

with open('latitude.json') as f:
	src = f.read()

with open('sane.json', 'w') as f:
	f.write('{\n  "data" : {\n    "items" : [')
	groups = re.findall('(?s)\[(.*?)\]', src)
	for i, group in enumerate(groups):
		f.write(group)
		if i != len(groups) - 1:
			f.write(',')
	f.write(']\n  }\n}')
