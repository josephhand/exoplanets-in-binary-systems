#!/bin/sh
cat $1 | grep -v '#' > $2
