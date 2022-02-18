
USE IMDBmedia;


load data infile '/export/title.akas.tsv' 
    into table `title.akas` 
    fields terminated by '\t' 
    lines terminated by '\n' 
    ignore 1 rows;
    

load data infile '/export/title.basics.tsv' 
    into table `title.basics` 
    fields terminated by '\t' 
    lines terminated by '\n' 
    ignore 1 rows;


load data infile '/export/title.crew.tsv' 
    into table `title.crew` 
    fields terminated by '\t' 
    lines terminated by '\n' 
    ignore 1 rows;

load data infile '/export/title.episode.tsv' 
    into table `title.episode` 
    fields terminated by '\t' 
    lines terminated by '\n' 
    ignore 1 rows;
    

load data infile '/export/title.principals.tsv' 
    into table `title.principals` 
    fields terminated by '\t' 
    lines terminated by '\n' 
    ignore 1 rows;


load data infile '/export/title.ratings.tsv' 
    into table `title.ratings` 
    fields terminated by '\t' 
    lines terminated by '\n' 
    ignore 1 rows;

load data infile '/export/name.basics.tsv' 
    into table `name.basics` 
    fields terminated by '\t' 
    lines terminated by '\n' 
    ignore 1 rows;


--- custom tables ---
load data infile './movies_list.csv' 
    into table `movies_list` 
    fields terminated by ',' 
    lines terminated by '\n' 
    ignore 1 rows;


