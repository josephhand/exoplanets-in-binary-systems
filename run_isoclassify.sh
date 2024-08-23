#!/usr/bin/env bash

python create_isoclassify_input.py "$1" "$2"

[ -e intermediates/isoclassify ] || mkdir data/intermediates/isoclassify
rm -r data/intermediates/isoclassify/*

(echo 'set -v'; isoclassify batch grid "$2" -o data/intermediates/isoclassify | sed 's/save-png/none/') | bash
isoclassify scrape-output 'data/intermediates/isoclassify/*/output.csv' "$3"

python refine_isoclassify_input.py "$2" "$3" "$2"

(echo 'set -v'; isoclassify batch grid "$2" -o data/intermediates/isoclassify | sed 's/save-png/none/') | bash
isoclassify scrape-output 'data/intermediates/isoclassify/*/output.csv' "$3"


