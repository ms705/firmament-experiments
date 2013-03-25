INSERT OVERWRITE TABLE rankings_select SELECT pageRank, pageURL FROM rankings WHERE pageRank > 10;
INSERT OVERWRITE TABLE rankings_select SELECT pageRank, pageURL FROM rankings WHERE pageRank > 10;
quit;