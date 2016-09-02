FROM ubuntu:14.04
MAINTAINER firmament-dev@camsas.org

RUN echo "" >> /etc/apt/sources.list \
  && echo "deb [arch=amd64] http://archive.cloudera.com/cdh5/ubuntu/trusty/amd64/cdh trusty-cdh5.8.0 contrib" >> /etc/apt/sources.list \
  && echo "deb-src http://archive.cloudera.com/cdh5/ubuntu/trusty/amd64/cdh trusty-cdh5.8.0 contrib" >> /etc/apt/sources.list \
  && apt-get -y update \
  && apt-get -y install git-core build-essential make && git clone https://github.com/camsas/firmament /firmament \
  && bash -c 'source /firmament/include/pkglist.Ubuntu-14.04 && sudo apt-get -y install ${BASE_PKGS} ${COMPILER_PKGS} ${GOOGLE_PKGS} ${BOOST_PKGS} ${MISC_PKGS} ${HDFS_PKGS}' \
  && apt-get -y install git-core build-essential make && git clone https://github.com/ms705/firmament-experiments /firmament-experiments \
  && apt-get -y --force-yes install hadoop-hdfs-datanode \
  && apt-get clean \
  && wget https://www.cl.cam.ac.uk/~icg27/hadoop/hdfs-site.xml \
  && wget https://www.cl.cam.ac.uk/~icg27/hadoop/core-site.xml \
  && wget https://www.cl.cam.ac.uk/~icg27/hadoop/mapred-site.xml \
  && cp hdfs-site.xml /etc/hadoop/conf/ \
  && cp core-site.xml /etc/hadoop/conf/ \
  && cp mapred-site.xml /etc/hadoop/conf/
