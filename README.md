# IMDB Data Analysis Notebooks

This is where I will be uploading my Kaggle notebooks, I have abandoned the MySQL part of the project in favor of using pandas (or polaris in future) for working with the IMDB Datasets.  Pandas does have a to_sql() function for loading a DataFrame into a RDBMS like MySQL, PostgreSQL, Oracle later on.  


## IMDB Non-Commercial Datasets
Subsets of IMDB data are available for access to customers for personal and non-commercial use. You can hold local copies of this data, and it is subject to our terms and conditions. Please refer to the [Non-Commercial Licensing](https://help.imdb.com/article/imdb/general-information/can-i-use-imdb-data-in-my-software/G5JTRESSHJBBHTGX?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=1ed1aea6-d2ad-4705-95fd-ba13f1b5014f&pf_rd_r=XRE3QWF2G5YWTD2SGT0V&pf_rd_s=center-1&pf_rd_t=60601&pf_rd_i=interfaces&ref_=fea_mn_lk1) and [copyright/license](http://www.imdb.com/Copyright?pf_rd_m=A2FGELUUNOQJNL&pf_rd_p=1ed1aea6-d2ad-4705-95fd-ba13f1b5014f&pf_rd_r=XRE3QWF2G5YWTD2SGT0V&pf_rd_s=center-1&pf_rd_t=60601&pf_rd_i=interfaces&ref_=fea_mn_lk2) and verify compliance.

## Data Location
The dataset files can be accessed and downloaded from [https://datasets.imdbws.com/](https://datasets.imdbws.com/). The data is refreshed daily.

## IMDB Dataset Details
Each dataset is contained in a gzipped, tab-separated-values (TSV) formatted file in the UTF-8 character set. The first line in each file contains headers that describe what is in each column. A ‘\N’ is used to denote that a particular field is missing or null for that title/name.

### some files get very big!

* 1.4G	title.akas.tsv
* 676M	title.basics.tsv
* 256M	title.crew.tsv
* 150M	title.episode.tsv
* 2.0G	title.principals.tsv
* 20M	title.ratings.tsv
* 640M	name.basics.tsv

### MediaProc.py

This will contain my Python code for extracting and ploting data in the IMDB datasets. This will be used in both Kaggle and JetBrains DataSpell.
