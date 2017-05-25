from rosetta import *
import random
import math
from random import randint
from toolbox import cleanATOM

# initialize the pose
init()

pdblist = []
with open("trainpdblist.txt", 'r') as f:
	lst = f.read()
	pdblist.extend(lst.split(','))

print(pdblist)

with open('trainingSet.txt', 'w') as output:
	lines = []
	for pdb in pdblist:
		pdb = pdb.strip(' \n')
		print(pdb)
		pdbName = "%s.pdb" % pdb
		cleanpdb = "%s.clean.pdb" % pdb
		alphaName = "%s_alpha.txt" % pdb
		betaName = "%s_beta.txt" % pdb
		
		alphalst = []
		with open(alphaName, 'r') as fa:
			lst = fa.read()
			alphalst.extend(lst.split(','))

		betalst = []
		with open(betaName, 'r') as fb:
			lst = fb.read()
			betalst.extend(lst.split(','))	

		cleanATOM(pdbName)
		pose = pose_from_pdb(cleanpdb)

		print (pose.total_residue())
		for i in range(1,pose.total_residue() + 1):
			if str(i) in alphalst:
				lines.append('{0},{1},{2}\n'.format(pose.phi(i), pose.psi(i), 1))
			elif str(i) in betalst:
				lines.append('{0},{1},{2}\n'.format(pose.phi(i), pose.psi(i), 2))
			else:
				lines.append('{0},{1},{2}\n'.format(pose.phi(i), pose.psi(i), 0))
	output.writelines(lines)













