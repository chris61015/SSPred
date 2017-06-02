from rosetta import *
import random
import math
from random import randint
from toolbox import cleanATOM


aminoAcidList = "ARNDCQEGHILKMFPSTWYV"

# initialize the pose
init()

pdblist = []
with open("predpdblist.txt", 'r') as f:
	lst = f.read()
	pdblist.extend(lst.split(','))

print(pdblist)

lines = []
for pdb in pdblist:
	pdb = pdb.strip(' \n')
	print(pdb)
	pdbName = "%s.pdb" % pdb
	cleanpdb = "%s.clean.pdb" % pdb
	alphaName = "%s_alpha.txt" % pdb
	betaName = "%s_beta.txt" % pdb
	testName = "test_%s.txt" % pdb
		
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

	seq = pose.sequence()
	print (pose.total_residue(), len(seq))
    with open(testName, 'w') as ft:
            lines = []      
            for i in range(1,pose.total_residue() + 1):
                    if str(i) in alphalst:
                            lines.append('{0},{1}\n'.format(aminoAcidList.index(str(seq[i-1])), 1))
                    elif str(i) in betalst:
                            lines.append('{0},{1}\n'.format(aminoAcidList.index(str(seq[i-1])), 2))
                    else:
                            lines.append('{0},{1}\n'.format(aminoAcidList.index(str(seq[i-1])), 0))
            ft.writelines(lines)

	



# # initialize the pose
# init()

# pdblist = []
# with open("predpdblist.txt", 'r') as f:
# 	lst = f.read()
# 	pdblist.extend(lst.split(','))

# print(pdblist)

# for pdb in pdblist:
# 	pdb = pdb.strip(' \n')
# 	print(pdb)
# 	pdbName = "%s.pdb" % pdb
# 	cleanpdb = "%s.clean.pdb" % pdb
# 	alphaName = "%s_alpha.txt" % pdb
# 	betaName = "%s_beta.txt" % pdb
# 	testName = "test_%s.txt" % pdb
		
# 	alphalst = []
# 	with open(alphaName, 'r') as fa:
# 		lst = fa.read()
# 		alphalst.extend(lst.split(','))

# 	betalst = []
# 	with open(betaName, 'r') as fb:
# 		lst = fb.read()
# 		betalst.extend(lst.split(','))	

# 	cleanATOM(pdbName)
# 	pose = pose_from_pdb(cleanpdb)

# 	print (pose.total_residue())

# 	with open(testName, 'w') as ft:
# 		lines = []
# 		for i in range(1,pose.total_residue() + 1):
# 			if str(i) in alphalst:
# 				lines.append('{0},{1},{2}\n'.format(pose.phi(i), pose.psi(i), 1))
# 			elif str(i) in betalst:
# 				lines.append('{0},{1},{2}\n'.format(pose.phi(i), pose.psi(i), 2))
# 			else:
# 				lines.append('{0},{1},{2}\n'.format(pose.phi(i), pose.psi(i), 0))
# 		ft.writelines(lines)		












