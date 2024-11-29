#!/bin/bash

# Lock file to store when LOFTI output last changed
touch $3
seq 0 $(cat "$1" | wc -l) | parallel --bar --eta python run_lofti.py "$1" "$2" '{} &> /dev/null'
