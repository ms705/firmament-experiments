#!/bin/bash

output=$1

export SCALA_HOME=/opt/scala-2.9.3/
export HIVE_HOME=/home/icg27/hive-0.9.0-bin/

uv_agg="INSERT OVERWRITE TABLE uservisits_aggre SELECT sourceIP, SUM(adRevenue) FROM uservisits GROUP BY sourceIP;";
uv_ad="INSERT OVERWRITE TABLE uv_ad SELECT visitDate, SUM(adRevenue) FROM uservisits GROUP BY visitDate;"
join="INSERT OVERWRITE TABLE rankings_uservisits_join SELECT sourceIP, avg(pageRank), sum(adRevenue) as totalRevenue FROM rankings R JOIN (SELECT sourceIP, destURL, adRevenue FROM uservisits UV WHERE UV.visitDate > '1999-01-01' AND UV.visitDate < '2000-01-01') NUV ON (R.pageURL = NUV.destURL) GROUP BY sourceIP ORDER BY totalRevenue DESC LIMIT 1;"
rank_sel="INSERT OVERWRITE TABLE rankings_select SELECT pageRank, pageURL FROM rankings WHERE pageRank > 10;"

mother_query=""
num_it=3
for it in `seq 1 ${num_it}`;
do
    mother_query=$mother_query$rank_sel
done

echo $mother_query | perf stat -e instructions,cycles,cache-misses /home/icg27/shark-0.2.1/bin/shark 2> ${output}
