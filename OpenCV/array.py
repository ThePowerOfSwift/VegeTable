import os

def parseLine(line):
	s = ''
	field = 0
	d = 0
	data = []
	for c in line:
		if ( c == '\n'):
			data.append(s)
			return (data)
		elif (c != ','):
			s = s + c
		else:
			if (field == 0):
				s = '\'' + s + '\''
				data.append(s)
				s = ''
			else:	
				data.append(s)
				s = ''
			field += 1
	data.append(s)
	return (data)

str_out = '['
with open('data.txt','r') as f:
	for line in f:
		data = parseLine(line)
		str_out += '['
		l = len(data)
		i = 0
		for i in range(l):
			str_out += data[i]
			if ( (l - i)>1):
				str_out += ','
		str_out += '],'
str_out += ']'
out_file = open('array.txt','w')
out_file.write(str_out)
