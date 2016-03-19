import sys
filename = ''
try:
	filename = sys.argv[1]
except:
	print ('filename missing')
	exit()
try:
	img = open(filename)
	print (9003)
except:
	print ('file not found')
