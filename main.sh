#!/bin/bash 
# Find ourselves 
cd $(pwd)/$(dirname $0)

# Load Python Module 
module load python/3.6 

# execute 
python main.py 

