FROM ubuntu:14.04
MAINTAINER firmament-dev@camsas.org

RUN echo "" >> /etc/apt/sources.list
RUN echo "deb [arch=amd64] http://archive.cloudera.com/cdh5/ubuntu/trusty/amd64/cdh trusty-cdh5.8.0 contrib" >> /etc/apt/sources.list
RUN echo "deb-src http://archive.cloudera.com/cdh5/ubuntu/trusty/amd64/cdh trusty-cdh5.8.0 contrib" >> /etc/apt/sources.list
RUN apt-get -y update
RUN apt-get -y install git-core build-essential make && git clone https://github.com/camsas/firmament /firmament
RUN bash -c 'source /firmament/include/pkglist.Ubuntu-14.04 && sudo apt-get -y install ${BASE_PKGS} ${COMPILER_PKGS} ${GOOGLE_PKGS} ${BOOST_PKGS} ${MISC_PKGS} ${HDFS_PKGS}'
RUN apt-get -y install git-core build-essential make && git clone https://github.com/ms705/firmament-experiments /firmament-experiments
RUN apt-get -y --force-yes install hadoop-hdfs-datanode
RUN apt-get clean
RUN wget https://www.cl.cam.ac.uk/~icg27/hadoop/hdfs-site.xml
RUN wget https://www.cl.cam.ac.uk/~icg27/hadoop/core-site.xml
RUN wget https://www.cl.cam.ac.uk/~icg27/hadoop/mapred-site.xml
RUN cp hdfs-site.xml /etc/hadoop/conf/
RUN cp core-site.xml /etc/hadoop/conf/
RUN cp mapred-site.xml /etc/hadoop/conf/
