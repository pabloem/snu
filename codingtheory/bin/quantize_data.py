#!/usr/bin/env python
import sys
import csv
import os
import subprocess
import re

def check_or_exit(av,ac,val):
    if av[ac] != val:
        print(usage)
        sys.exit(0)
        pass
    return ac + 1

def parse_result(res,row):
    s = str(res)
    s = s.replace("\n"," ")
    m = re.match("MSE: ([0-9.e-]*) |.*",s[s.find("MSE: "):])
    row['mse'] = float(m.group(1))
    m = re.match("Points: ([0-9.]*) |.*",s[s.find("Points: "):])
    row['qpoints'] = int(m.group(1))
    m = re.match(".*Square Error: ([0-9.]*) |.*",s[s.find("Square Error: "):])
    row['tse'] = float(m.group(1))
    m = re.match("topology: ([0-9.]*) arcs.*",s[s.find("topology:"):])
    row['arcs'] = int(m.group(1))
    m = re.match("prune: retained ([0-9.]*) /.*",s[s.find("prune:"):])
    row['retainedarcs'] = int(m.group(1))
    m = re.match("arcs, ([0-9.]*) points*",s[s.find("arcs, "):])
    row['finalpoints'] = int(m.group(1))

    m = re.match("bounds: (([0-9.]* )+[0-9.]+)",s[s.find("bounds:"):])
    bbox = [float(y) for y in m.group(1).split()]
    row['xmin'] = bbox[0]
    row['xmax'] = bbox[2]
    row['ymin'] = bbox[1]
    row['ymax'] = bbox[3]
    
usage = """
./quantize_data.py [-v variables] [-q 1000,2000,...] -i file -op mx_q_ -csv output.csv -b topojson
\tOptions:
\t\t-v - Variables to convert. Optional field. For the Mexican map, this field must have value "-p name=name -p state_code=state_code -p mun_code=mun_code"
\t\t-i - Input file. This is the source TopoJSON or GeoJSON file.
\t\t-op - Output prefix. This is the prefix of the output file (it will be appended with the quantization level, and JSON extension)
\t\t-csv - Output csv file. This contains the data of the quantization results.
\t\t-q - These are the comma-separated quantization levels. By default, the levels are [1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,12000,15000,20000,25000,30000].
\t\t-b - The location of the topojson binary
"""

if len(sys.argv) < 7:
    print(usage)
    sys.exit(0)
    pass

ac = 1

var_string = ""
if sys.argv[ac] == "-v":
    ac += 1
    var_string = sys.argv[ac]
    ac += 1
    pass

qlevels = [1000,2000,3000,4000,5000,6000,7000,8000,9000,10000,12000,15000,20000,25000,30000]
if sys.argv[ac] == "-q":
    ac += 1
    qlevels = [int(lv) for lv in sys.argv[ac].split(",")]
    ac += 1
    pass

ac = check_or_exit(sys.argv,ac,"-i")
in_file = sys.argv[ac]
ac += 1

ac = check_or_exit(sys.argv,ac,"-op")
out_prefix = sys.argv[ac]
ac += 1

ac = check_or_exit(sys.argv,ac,"-csv")
out_csv = sys.argv[ac]
ac += 1

ac = check_or_exit(sys.argv,ac,"-b")
topojson = sys.argv[ac]
ac += 1

f = open(out_csv,'w')
fields = ['source','file','fsize','quantization','mse','qpoints','tse','arcs','finalpoints','retainedarcs',
          'xmin','xmax','ymin','ymax']
wr = csv.DictWriter(f,fields)
wr.writeheader()

for lv in qlevels:
    fname = out_prefix+str(lv)+'.json'
    row = {'source':in_file, 'quantization':lv, 'file':fname}
    command = [topojson,"-v "]+var_string.split(" ")+["-q",str(lv),"-o",fname,in_file]
    print("Command: "+' '.join(command))
    # RUN THE COMMAND
    res = subprocess.check_output(command,stderr=subprocess.STDOUT)
    parse_result(res,row)
    #Afterwards, check file size
    row['fsize'] = os.stat(fname).st_size
    wr.writerow(row)
    print(row)
    pass

f.close()
