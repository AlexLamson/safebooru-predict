# safebooru-predict
Predict user ratings for anime-style images

## Requirements

### Python
See requirements.txt

### Other
- GraphViz


## Getting Started
### Downloading & Preprocessing
- `python download/download_booru.py`
- `python download/xml_to_csv.py`
- `python preprocess/preprocess_all_data.py`

### Initializing the database
- `pg_ctl initdb -D "safebooru-predict2/res/safebooru/sql_data"`
- `pg_ctl start -D "safebooru-predict/res/safebooru/sql_data" -l logfile`

### Starting the webserver
- `set FLASK_APP=src/recommend/webserver.py`


## To Do
- parameterize number of images instead of hardcoding it
- convert the XML into CSV to make it accessible to pandas and (maybe?) easier to parse


## Pipeline
- download all metadata
- sample from that xml file so that amount of data is reasonable
- select features
- machine learn it up
  - regression tree
  - random forest of regression trees
  - PCA and K-means
  - naive bayes maybe
- choose optimal regressor based on testing set
- report accuracy found in validation set


## General notes
- It took 5 hours and 12 minutes to download all the metadata
- It took 59 minutes to count the number of occurrences of each score
- Only about 28.9% of images have a score greater than 0.
- It took 1 hour and 5 minutes to count the number of occurrences of each tag
- Setting criterion="mae" makes the classifier train too slowly to be useable
- Look into this: http://scikit-learn.org/stable/auto_examples/ensemble/plot_adaboost_multiclass.html
