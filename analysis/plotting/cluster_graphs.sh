#!/bin/bash

DATE=$(date "+%Y%m%d")

for r in 3 4; do
  for i in `seq ${r}01 ${r}14`; do
    python plot_collectl_timeline.py ../../results/machine_stats/collectl-12\:45-13\:10-caelum-${i}-${DATE}.tab caelum-${i} caelum-${i}.png '[CPU]Totl%' '[MEM]Anon' '[DSK]KbTot' '[NET]RxKBTot' '[NET]TxKBTot';
  done;
done
