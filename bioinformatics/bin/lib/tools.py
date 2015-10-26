from math import log
def load_line(line,dic):
    amino_acids = 'IVLFCMAGTWSYPHEQDNKR'
    sp = line.split("\t")
    for i in range(len(amino_acids)):
        el = sp[i]
        dic[amino_acids[i]] = float(el)

def load_single_model(fp):
    amino_acids = 'IVLFCMAGTWSYPHEQDNKR'
    model = {'matrix':{},'stationary':{},'seqs':0}
    matrix = model['matrix']
    stationary = model['stationary']
    ln_count = 0
    for line in fp:
        if line[0] == '#': 
            continue
        ln_count += 1
        if ln_count == 21:
            load_line(line,stationary)
            continue
        if ln_count == 22:
            model['seqs'] = int(line)
            continue
        aa = amino_acids[ln_count-1]
        matrix[aa] = {}
        load_line(line,matrix[aa])
    return model

def load_models(fs):
    res = {}
    for lb in fs:
        f = open(fs[lb])
        res[lb] = load_single_model(f)
        f.close()
    total_seq = sum([res[lb]['seqs'] for lb in res])+0.0
    for lb in res:
        res[lb]['prob'] = res[lb]['seqs'] / total_seq
    return res

def calculate_prior(seq,models,model_label):
    model = models[model_label]
    mtx = model['matrix']
    stat = model['stationary']
    prior = 0
    for i, ch in enumerate(seq):
        if i == 0: 
            prior += log(stat[ch],10)
            prev = ch
            continue
        if ch not in stat: continue
        if prev not in mtx: 
            prev = ch
            continue
        if ch not in mtx[prev]: continue
        prior += log(mtx[prev][ch],10)
        prev = ch
    prior += log(model['prob'],10)
    return prior
