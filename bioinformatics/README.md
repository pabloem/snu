### Machine learning in Bioinformatics
Student: Pablo Estrada <pablo@snu.ac.kr>
ID: 2014-25245

Results available: `results/` directory! : )

#### Environment information
* Linux / Ubuntu
* Python 2.7
    * Using the Biopython and Numpy libraries

#### Commands to run

**To run COG1 **

./bin/ML-2014-25245-posterior.py data/COG1.train.T1.fasta data/COG1.train.T1.model data/COG160.train.T1.model data/COG161.train.T1.model results/COG1.test.T1.vs.COG1.COG160.COG161.posterior
./bin/ML-2014-25245-posterior.py data/COG1.train.T2.fasta data/COG1.train.T2.model data/COG160.train.T2.model data/COG161.train.T2.model results/COG1.test.T2.vs.COG1.COG160.COG161.posterior


**To run COG160 **

./bin/ML-2014-25245-posterior.py data/COG160.train.T1.fasta data/COG1.train.T1.model data/COG160.train.T1.model data/COG161.train.T1.model results/COG160.test.T1.vs.COG1.COG160.COG161.posterior
./bin/ML-2014-25245-posterior.py data/COG160.train.T2.fasta data/COG1.train.T2.model data/COG160.train.T2.model data/COG161.train.T2.model results/COG160.test.T2.vs.COG1.COG160.COG161.posterior


**To run COG161 **

./bin/ML-2014-25245-posterior.py data/COG161.train.T1.fasta data/COG1.train.T1.model data/COG160.train.T1.model data/COG161.train.T1.model results/COG161.test.T1.vs.COG1.COG160.COG161.posterior
./bin/ML-2014-25245-posterior.py data/COG161.train.T2.fasta data/COG1.train.T2.model data/COG160.train.T2.model data/COG161.train.T2.model results/COG161.test.T2.vs.COG1.COG160.COG161.posterior

