# safebooru-predict
Predict user ratings for anime-style images


## Getting Started
1. Install the required python packages with `pip install -r requirements.txt`
2. [Download the data](https://www.kaggle.com/alamson/safebooru) and place `all_data.csv` into `res/safebooru/data`


### Generate statistics
Enter the `src/preprocess` directory and run `python preprocess_all_data.py`
Cost: 2.5 GB RAM, 16 minutes


### Find correlations between tags
Enter the `src/correlate` directory and run `python compute_cooccurrence_matrix.py`
Cost: 5.5 GB RAM, 35 minutes

Run `python query.py` and explore tags.


<!--
### To initialize the database
- `pg_ctl initdb -D "safebooru-predict2/res/safebooru/sql_data"`
- `pg_ctl start -D "safebooru-predict/res/safebooru/sql_data" -l logfile`


### To start the webserver
- `set FLASK_APP=src/recommend/webserver.py`
 -->
