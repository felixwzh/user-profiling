import os
import sys


def simplify_file(file_path, line_num):
	if not os.path.isfile(file_path):
		print "ERROR: file not exist. " + file_path
		exit(-1)

	fi_path = file_path
	fo_path = file_path + '.simp.txt'

	if file_path.endswith('simp.txt'):
		print "Pass " + fi_path
	else:
		fi = open(fi_path, 'r')
		fo = open(fo_path, 'w')
		counter = 0
		for line in fi:
			fo.write(line)
			counter = counter + 1
			if counter > line_num:
				break;
		fi.close()
		fo.close()
		print "Done " + fo_path

def simplify(path, line_num):
	if not os.path.exists(path):
		print "ERROR: file/folder not exist. " + file_path
		exit(-1)
	elif os.path.isfile(path):
		simplify_file(path, line_num)
	elif os.path.isdir(path):
		for p in os.listdir(path): 
			simplify(os.path.join(path, p), line_num)
	else:
		print "Nothing happend."


def main():
	if len(sys.argv) < 3:
		print "Please input the file path. like\npython simplify.py file_path output_line_num"
		exit(-1)

	path = sys.argv[1]
	line_num = int(sys.argv[2])	

	simplify(path, line_num)



if __name__ == '__main__':
	main()