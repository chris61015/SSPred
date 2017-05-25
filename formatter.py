from random import shuffle

def equal_float(a, b):
    #return abs(a - b) <= sys.float_info.epsilon
    return abs(a - b) <= 1E-3 #see edit below for more info

def main():
	sourcelist = []
	with open("sourceList.txt", 'r') as f:
		lst = f.read()
		sourcelist.extend(lst.split(','))


	shuffle(sourcelist)
	
	newList = ['"' + item + '"' for item in sourcelist]

	with open("trainpdblist.txt", 'w') as tf:
		tf.write(",".join(sourcelist[:1000]))	

	with open("predpdblist.txt", 'w') as tf:
		tf.write(",".join(sourcelist[-500:]))	

if __name__ == '__main__':
	main()