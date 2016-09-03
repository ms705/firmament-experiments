#!/bin/bash
ssh srguser@caelum-305.cl.cam.ac.uk 'screen -d -m iperf -s'
ssh srguser@caelum-313.cl.cam.ac.uk 'screen -d -m iperf -s'
ssh srguser@caelum-401.cl.cam.ac.uk 'screen -d -m iperf -s'
ssh srguser@caelum-204.cl.cam.ac.uk 'screen -d -m iperf -s'
ssh srguser@caelum-310.cl.cam.ac.uk 'screen -d -m iperf -s'
ssh srguser@caelum-414.cl.cam.ac.uk 'screen -d -m iperf -s'
ssh srguser@caelum-406.cl.cam.ac.uk 'screen -d -m iperf -s'

# 305
ssh srguser@caelum-306.cl.cam.ac.uk 'screen -d -m iperf -c 10.0.0.38 -i 2 -t 10000'
ssh srguser@caelum-307.cl.cam.ac.uk 'screen -d -m iperf -c 10.0.0.38 -i 2 -t 10000'
# 313
ssh srguser@caelum-308.cl.cam.ac.uk 'screen -d -m iperf -c 10.0.0.46 -i 2 -t 10000'
ssh srguser@caelum-309.cl.cam.ac.uk 'screen -d -m iperf -c 10.0.0.46 -i 2 -t 10000'
# 401
ssh srguser@caelum-402.cl.cam.ac.uk 'screen -d -m iperf -c 10.0.0.48 -i 2 -t 10000'
ssh srguser@caelum-403.cl.cam.ac.uk 'screen -d -m iperf -c 10.0.0.48 -i 2 -t 10000'
# 414
ssh srguser@caelum-404.cl.cam.ac.uk 'screen -d -m iperf -c 10.0.0.61 -i 2 -t 10000'
ssh srguser@caelum-405.cl.cam.ac.uk 'screen -d -m iperf -c 10.0.0.61 -i 2 -t 10000'
# 204
ssh srguser@caelum-208.cl.cam.ac.uk 'screen -d -m iperf -c 10.0.0.23 -i 2 -t 10000'
ssh srguser@caelum-209.cl.cam.ac.uk 'screen -d -m iperf -c 10.0.0.23 -i 2 -t 10000'
# 406
ssh srguser@caelum-407.cl.cam.ac.uk 'screen -d -m iperf -c 10.0.0.53 -i 2 -t 10000'
ssh srguser@caelum-408.cl.cam.ac.uk 'screen -d -m iperf -c 10.0.0.53 -i 2 -t 10000'
# 310
ssh srguser@caelum-311.cl.cam.ac.uk 'screen -d -m iperf -c 10.0.0.43 -i 2 -t 10000'
ssh srguser@caelum-312.cl.cam.ac.uk 'screen -d -m iperf -c 10.0.0.43 -i 2 -t 10000'

# 105
#ssh srguser@caelum-105.cl.cam.ac.uk 'screen -d -m cd firmament-experiments/workloads/nginx ; mkdir html ; cp index.html html/ ; cp muppet.jpg html/ ; nginx -p . -g 'error_log stderr;' -c nginx.conf'
ssh srguser@caelum-106.cl.cam.ac.uk 'screen -d -m ab -n 10000000000 -c 20 http://10.0.0.14:8082/'
ssh srguser@caelum-107.cl.cam.ac.uk 'screen -d -m ab -n 10000000000 -c 20 http://10.0.0.14:8083/'
ssh srguser@caelum-109.cl.cam.ac.uk 'screen -d -m ab -n 10000000000 -c 20 http://10.0.0.14:8084/'
# 410
#ssh srguser@caelum-410.cl.cam.ac.uk 'screen -d -m cd firmament-experiments/workloads/nginx ; mkdir html ; cp index.html html/ ; cp muppet.jpg html/ ; nginx -p . -g 'error_log stderr;' -c nginx.conf'
ssh srguser@caelum-411.cl.cam.ac.uk 'screen -d -m ab -n 10000000000 -c 20 http://10.0.0.57:8082/'
ssh srguser@caelum-412.cl.cam.ac.uk 'screen -d -m ab -n 10000000000 -c 20 http://10.0.0.57:8083/'
# 210
#ssh srguser@caelum-210.cl.cam.ac.uk 'screen -d -m cd firmament-experiments/workloads/nginx ; mkdir html ; cp index.html html/ ; cp muppet.jpg html/ ; nginx -p . -g 'error_log stderr;' -c nginx.conf'
ssh srguser@caelum-211.cl.cam.ac.uk 'screen -d -m ab -n 10000000000 -c 20 http://10.0.0.29:8082/'
ssh srguser@caelum-314.cl.cam.ac.uk 'screen -d -m ab -n 10000000000 -c 20 http://10.0.0.29:8083/'
