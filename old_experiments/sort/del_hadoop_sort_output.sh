#!/bin/bash
CNT=1
while [ $CNT -lt $1 ]; do
    echo sorted$CNT
    hadoop fs -rm -r -f /user/icg27/sorted$CNT
    let CNT=CNT*2
done
