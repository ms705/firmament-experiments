#!/bin/bash
CNT=1
while [ $CNT -lt $1 ]; do
    FILESIZE=$(stat -c%s input"$CNT"/part0)
    let FILESIZE=(FILESIZE-136)/144
    echo input$CNT $FILESIZE
    mpiexec -np $2 --hostfile mp.hosts --rankfile rank_file mpi_mergesort input$CNT/part0 $FILESIZE input$CNT/sorted
    rm input$CNT/sorted
    let CNT=CNT*2
done
