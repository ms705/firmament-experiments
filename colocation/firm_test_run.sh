#!/bin/bash
export GRAPHCHI_ROOT=/home/icg27/colocation_test/graphchi
test_name=$1
cpu=$2
input=$3
output=$4
graph_file=$5
perf_out=$6
if [[ $test_name != "shark" ]];
then
    echo $$ > /sys/fs/cgroup/cpuset/cpu${cpu}only/tasks
    cat /proc/self/cgroup
fi
num_rows=$(stat -c%s "$input")
num_rows=$((($num_rows-136)/144))
perf_opt=instructions,cycles,cache-misses
if [ "$test_name" = "pthread_sort" ]; then
    perf stat -e ${perf_opt} -o ${perf_out} -- ./pthread_sort ${input} ${num_rows} ${output}
else
    if [ "$test_name" = "quick_sort" ]; then
	perf stat -e ${perf_opt} -o ${perf_out} -- ./quick_sort ${input} ${num_rows} ${output}
    else
	if [ "$test_name" = "mpi_local_merge" ]; then
	    perf stat -e ${perf_opt} -o ${perf_out} -- mpiexec -np 1 mpi_mergesort ${input} ${num_rows} ${output}
	else
	    if [ "$test_name" = "page_rank" ]; then
		perf stat -e ${perf_opt} -o ${perf_out} -- ./graphchi/bin/example_apps/pagerank file ${graph_file}
	    else
		if [ "$test_name" = "binoptions" ]; then
		    perf stat -e ${perf_opt} -o ${perf_out} -- ./binoptions 100 100 1 0.3 0.03 -1 94000 94000 1 | ./binoptions 100 100 1 0.3 0.03 -1 94000 94000 0 | ./binoptions 100 100 1 0.3 0.03 -1 94000 94000 0
		else
		    if [ "$test_name" = "ab" ]; then
			perf stat -e ${perf_opt} -o ${perf_out} -- ssh icg27@uriel "ab -n 600000 -c 40 http://michael/index4.html >> lat_${perf_out}"
                    else
			if [ "$test_name" = "shark" ]; then
			    su - -c "cd colocation_test; perf stat -e ${perf_opt} -o ${perf_out} /home/icg27/shark-0.2.1/bin/shark -i /home/icg27/colocation_test/shark.hql" icg27
			else
			    echo "Unknown test name."
			fi
		    fi
		fi
	    fi
	fi
     fi
fi