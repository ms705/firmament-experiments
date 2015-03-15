#!/bin/bash
output=$1
for f_name in `ls iso*`
do
    sec=`grep "seconds time elapsed" ${f_name} | awk '{ print $1 }'`
    cycles=`grep "cycles" ${f_name} | awk '{ print $1 }'`
    instr=`grep "instructions" ${f_name} | awk '{ print $1 }'`
    c_misses=`grep "cache-misses" ${f_name} | awk '{ print $1 }'`
    echo $f_name | awk -F'.' '{printf $2}' >> unsorted_${output}
    echo ","$sec","${cycles//[,]/}","${instr//[,]/}","${c_misses//[,]/} >> unsorted_${output}
done

sort -t',' -o ${output} unsorted_${output}
rm unsorted_${output}
