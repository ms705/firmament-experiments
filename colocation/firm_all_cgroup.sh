#!/bin/bash
num_it=2
tests_name="quick_sort binoptions page_rank ab shark"
sort_input=input4194304/part1
#sort_input=input1/part0
sort_output=/dev/null
graph=soc-LiveJournal1.txt

function wait_for_finish {
  t_name=$1
  # waiting task to finish
  sleep 1
  while [ $(ps aux | grep "${t_name}" | wc -l) -gt 2 ]; do
    sleep 5
  done
}

function clear_cache {
  sync
  sudo echo 3 | sudo tee /proc/sys/vm/drop_caches >> /dev/null
}

function run_test {
  cpu1=$1
  cpu2=$2
  name1=$3"."$t_name1"."$t_name2"."$test_num".1st"
  name2=$3"."$t_name1"."$t_name2"."$test_num".2nd"
  if [[ $t_name1 == "shark" ]];
  then
      bash firm_test_run.sh ${t_name1} ${cpu1} ${sort_input} ${sort_output} ${graph} ${name1} &
      sleep 20
      bash firm_test_run.sh ${t_name2} ${cpu2} ${sort_input} ${sort_output} ${graph} ${name2} &
  elif [[ $t_name2 == "shark" ]];
  then
      bash firm_test_run.sh ${t_name2} ${cpu2} ${sort_input} ${sort_output} ${graph} ${name2} &
      sleep 20
      bash firm_test_run.sh ${t_name1} ${cpu1} ${sort_input} ${sort_output} ${graph} ${name1} &
  else
      bash firm_test_run.sh ${t_name1} ${cpu1} ${sort_input} ${sort_output} ${graph} ${name1} &
      bash firm_test_run.sh ${t_name2} ${cpu2} ${sort_input} ${sort_output} ${graph} ${name2} &
  fi
  wait_for_finish ${t_name1}
  wait_for_finish ${t_name2}
}

test_num=0
for t_name1 in ${tests_name}; do
  let "test_num+=1"
  clear_cache
  echo "R: ${t_name1} 4"
  cpu=4
  name="isolation."
  name=$name$t_name1
  bash firm_test_run.sh ${t_name1} ${cpu} ${sort_input} ${sort_output} ${graph} ${name} &
  wait_for_finish ${t_name1}

  for t_name2 in ${tests_name}; do
    if [[ $t_name1 == $t_name2 && $t_name1 == "shark" ]];
    then
	continue;
    fi
    for it in `seq 1 ${num_it}`;
    do
      name="4.5.$it"
      clear_cache
      echo "R: ${t_name1} ${t_name2} 4 5"
      run_test 4 5 $name
    done

    for it in `seq 1 ${num_it}`;
    do
      clear_cache
      name="4.6.$it"
      echo "R: ${t_name1} ${t_name2} 4 6"
      run_test 4 6 $name
    done

    for it in `seq 1 ${num_it}`;
    do
      clear_cache
      name="4.16.$it"
      echo "R: ${t_name1} ${t_name2} 4 16"
      run_test 4 16 $name
    done
  done
done