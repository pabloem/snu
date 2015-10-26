#!/usr/bin/env python
import sys
import numpy as np
from math import log
from Bio import SeqIO
import csv
from lib.tools import *

#if len(sys.argv) < 6:
#    print("Usage: ./test_posterior.py input_seqs.fasta model1 model2 model3 output.posterior")

input_seqs = sys.argv[1]
model_fs = {}
model_fs['COG1'] = sys.argv[2]
model_fs['COG160'] = sys.argv[3]
model_fs['COG161'] = sys.argv[4]

output = sys.argv[5]

model_dc = load_models(model_fs)


f = open(input_seqs)
fout = open(output,'w')
tab_wr = csv.DictWriter(fout,['id']+model_fs.keys()+['max'],dialect='excel-tab')
tab_wr.writeheader()

priors = {}
for s in SeqIO.parse(f,"fasta"):
    priors[s.id] = {}
    log_p_seq = 0
    for lb in model_dc:
        priors[s.id][lb] = calculate_prior(s.seq,model_dc,lb)

    priors[s.id]['max'] = max(priors[s.id],key=priors[s.id].get)
    priors[s.id]['id'] = s.id[0:5]
    tab_wr.writerow(priors[s.id])

f.close()
fout.close()
