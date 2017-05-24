from sklearn.multiclass import OneVsOneClassifier
from sklearn.svm import LinearSVC
import numpy as np

def equal_float(a, b):
    #return abs(a - b) <= sys.float_info.epsilon
    return abs(a - b) <= 1E-3 #see edit below for more info

def main():
	ar = np.loadtxt('output.txt',delimiter=',')
	trainX = ar[:,0:2]
	trainy = ar[:,2]

	predX = trainX
	predY = OneVsOneClassifier(LinearSVC(random_state=0)).fit(trainX, trainy).predict(predX)
	
	seq = ""
	for i in predY:
		if  equal_float(1,i):
			seq+="a"
		elif equal_float(2,i):
			seq+="b"
		else:
			seq+="-"
	print(seq)

if __name__ == '__main__':
	main()