CREATE TABLE rankings (pageRank INT, pageURL STRING, avgDuration INT);
LOAD DATA LOCAL INPATH '/home/icg27/Rankings.dat' INTO TABLE rankings;
CREATE TABLE rankings_select ( pageRank INT, pageURL STRING );
quit;