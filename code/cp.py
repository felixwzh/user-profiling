import os
import sys
import codecs

if len(sys.argv) < 3:
	print "python cp.py from_path to_path"
	exit(-1)

from_file = sys.argv[1]
to_file = sys.argv[2]

if not os.path.isfile(from_file):
	print "Original file is not existed."
	exit(-1)

if os.path.isfile(to_file):
	print "Warning: May override the existing file."

fi = codecs.open(from_file, 'r', encoding='gbk')
# fo = open(to_file, 'w')
fo = codecs.open(to_file, 'w', encoding='utf-8')
for line in fi:
	fo.write(line)

fi.close()
fo.close()

print "Copy done."