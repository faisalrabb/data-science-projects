#!/bin/bash

if [ $(wc -l < $1) -lt 10000 ]
then
    echo "This file is too small (<10,000 lines)"
fi  

wc -l < $1
head -n 1 $1
tail -n10000 $1 | grep -c -i "potus" 
sed -n '100,200 p' $1 |  grep -c -w "fake" 

