#usage: enter PyMol, enter: run preproc.py
import pymol
from pymol import stored, cmd

pdblist = []

fnl = "./testdata/predpdblist.txt"
with open(fnl, 'r') as f:
	lst = f.read()
	pdblist.extend(lst.split(','))

# fetch some molecule; yes, 1foo exists in the PDB
for pdb in pdblist:
	pdb = pdb.strip(' ')
	print (pdb)
	cmd.fetch(pdb, async=0)
	
	pdbName = "./testdata/%s.pdb" % pdb
	cmd.save(pdbName)
	# get the sequence from PyMOL
	stored.alphaSeq = []
	cmd.iterate( "ss h" , "stored.alphaSeq.append(resi)")
	
	stored.betaSeq = []
	cmd.iterate( "ss s" , "stored.betaSeq.append(resi)")

	fna = "./testdata/%s_alpha.txt" % pdb
	fnb = "./testdata/%s_beta.txt" % pdb
	with open(fna, 'w') as fa:
		sa = set(stored.alphaSeq)
		line = ','.join(sorted(sa, key=int))
		fa.write(line)
	with open(fnb, 'w') as fb:
		sb = set(stored.betaSeq)
		line = ','.join(sorted(sb, key=int))
		fb.write(line)	

	cmd.delete (pdb)
