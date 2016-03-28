#!/bin/bash
# Script that removes the last line from every table of a generated trace.
# $1 = path to the trace directory

for dir in $(ls $1) ; do
  for file in $(ls $1/$dir) ; do
    FILE_NAME=$1$dir/$file
    TMP_FILE_NAME="$FILE_NAME".tmp
    echo "Trimming: " $FILE_NAME
    head -n -1 $FILE_NAME > $TMP_FILE_NAME
    mv $TMP_FILE_NAME $FILE_NAME
  done
done
