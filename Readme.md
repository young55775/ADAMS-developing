# ADAMS: Align Distance Matrix with SIFT algorithm enables GPU-Accelerated protein structre comparison

## Requirements

opencv == 4.7.0.72

numpy >= 1.17.2

cuda > 11.x

cupy-cuda111 == 12.2.0 or same as cuda version

biopython == 1.81

scipy == 1.11.2

tqdm == 4.66.1

cuda == 11.x or same as cupy version

pickle

## Installation

A pypi package coming soon. Python source code is available above

Please contact: guozy23@mails.tsinghua.edu.cn for more information

## Tutorial and description

### Introduction

We've developed a method to address the issue of numerous proteins 
exhibiting high structural similarity despite having no sequence 
similarities. This problem has become increasingly critical as 
Alphafold2 continues to predict new structures, resulting in a massive 
database (23TiB ver 4) that lacks an effective data mining tool.

Foldseek offers a solution by embedding local structure into the 
sequence and transforming this issue into a sequence alignment problem. 
It's significantly faster than DALI, TM-Align, and CE-Align and 
outperforms them on structure comparison benchmarks.

However, according to the Foldseek paper, we observed that Foldseek occasionally underperforms 
compared to DALI, indicating that some 'overall information' 
may not be captured within local structure embedding.

Our Align Distance Matrix with SIFT algorithm (ADAMS) is 
similar to DALI but uses an enhanced version of the renowned 
computer vision algorithm - Scale Invariant Feature Transform (SIFT). 
It extracts key features from protein distance matrices at different 
scales and compares their similarities. Most calculations can benefit 
from GPU acceleration. This zero-shot model enables more precise 
structure comparisons at speeds comparable to Foldseek-TM tools. 
Users can create their own pdb databases on PCs for all-vs-all 
comparisons with increased speed and reduced memory usage 
(approximately 500MB - 3GB GPU memory for a 20000 all vs all comparison).

The algorithm is illustrated in Fig.1: The original SIFT algorithm is 
applied on distance matrixes to extract detectable features across 
various scales. These features are represented as 128-dimension vectors 
which are then stacked into an n X 128 matrix for comparison between 
two structures using cosine similarity calculated between two feature 
matrices by A X B.T operation. Given these features have nearly identical
lengths (512 ± 1.5), feature distances are determined by angles rather 
than length differences between them; thus when normalized beforehand, 
similarity calculation becomes straightforward on GPUs.

![image](img/fig1.jpg)

The performance metrics are as follows - it took between 3-4 seconds 
to search for the protein structure 'OSM-3' (699aa) within a C.elegans protein 
structure database (19361 structures) using an Nvidia RTX2080Ti (11GiB) GPU. When loading 
the entire database onto the dataset, total GPU memory usage was around
4000MB. However, when loaded separately, it only consumed about 500MB 
of memory. Importantly, these different methods did not impact search 
speed. 

This article is published in bioinformatics: https://academic.oup.com/bioinformatics/article/40/3/btae064/7601449


### Tutorial
##### Installation
```commandline
pip install adams
```
##### 1.check if the script has already been added to PATH (IMPORTANT):
```commandline
compare_all.py
```
if not, just add it to the PATH.
if you want to show the path and perform step 2:
```commandline
which compare_all.py
```
this will show the path to compare_all.py
##### 2.if permission denied:
```commandline
chmod +x path/to/compare_all.py
```
##### 3. Download a pdb set and make it a cuda_database or a compatible one'
```commandline
import adams
from adams.toolkit import *
from adams.db_maker import DatabaseMaker
db = DatabaseMaker(device=0, chunk_size=5000, process=40) # use GPU-0, 5000 pdb every block, 40*1.5 process.
db.make('./pdb','./pdb_db') # put your pdb dataset in one folder and make your database in another one
```
##### 4. Match your protein structure to different databases
```commandline
import adams
from adams.tool_kit import *
from adams.matcher import ADAMS_match
matcher = ADAMS_match('./protein.pdb',threshold=0.95,gpu_usage=[0,1]) #use gpu 0,1 to calculate the result.
result = matcher.match('./pdb_db','tmp') # search similar protein structure from a database, return a pandas dataframe. oops, you need an empty 'tmp' folder to do so
```



