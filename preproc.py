#usage: enter PyMol, enter: run preproc.py
import pymol
from pymol import stored, cmd

pdblist = ["1bk8", "1kao"]

fnl = "./data/pdblist.txt"
with open(fnl, 'w') as f:
	line = ','.join(pdblist)
	f.write(line)

# fetch some molecule; yes, 1foo exists in the PDB
for pdb in pdblist:
	cmd.fetch(pdb, async=0)
	
	pdbName = "./data/%s.pdb" % pdb
	cmd.save(pdbName)
	# get the sequence from PyMOL
	stored.alphaSeq = []
	cmd.iterate( "ss h" , "stored.alphaSeq.append(resi)")
	
	stored.betaSeq = []
	cmd.iterate( "ss s" , "stored.betaSeq.append(resi)")

	fna = "./data/%s_alpha.txt" % pdb
	fnb = "./data/%s_beta.txt" % pdb
	with open(fna, 'w') as fa:
		sa = set(stored.alphaSeq)
		line = ','.join(sorted(sa, key=int))
		fa.write(line)
	with open(fnb, 'w') as fb:
		sb = set(stored.betaSeq)
		line = ','.join(sorted(sb, key=int))
		fb.write(line)	

	cmd.delete (pdb)
