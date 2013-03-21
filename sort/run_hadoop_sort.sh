#!/bin/bash
CNT=1
while [ $CNT -lt $1 ]; do
    echo input$CNT
    hadoop jar /usr/lib/hadoop-0.20-mapreduce/hadoop-examples.jar sort input$CNT sorted$CNT
    let CNT=CNT*2
done
