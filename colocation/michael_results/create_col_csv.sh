#!/bin/bash
output=$1
for f_name in `ls 4*.1st`
do
    sec=`grep "seconds time elapsed" ${f_name} | awk '{ print $1 }'`
    cycles=`grep "cycles" ${f_name} | awk '{ print $1 }'`
    instr=`grep "instructions" ${f_name} | awk '{ print $1 }'`
    c_misses=`grep "cache-misses" ${f_name} | awk '{ print $1 }'`
    f2_name=`echo ${f_name%???}2nd`
    sec2=`grep "seconds time elapsed" ${f2_name} | awk '{ print $1 }'`
    cycles2=`grep "cycles" ${f2_name} | awk '{ print $1 }'`
    instr2=`grep "instructions" ${f2_name} | awk '{ print $1 }'`
    c_misses2=`grep "cache-misses" ${f2_name} | awk '{ print $1 }'`
    echo $f_name | awk -F'.' '{printf $1","$2","$4","$5}' >> unsorted_${output}
    echo ","$sec","${cycles//[,]/}","${instr//[,]/}","${c_misses//[,]/}","$sec2","${cycles2//[,]/}","${instr2//[,]/}","${c_misses2//[,]/} >> unsorted_${output}
done

sort -t',' -o ${output} unsorted_${output}
rm unsorted_${output}
