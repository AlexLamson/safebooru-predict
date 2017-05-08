# safebooru-predict
Predict user ratings for anime-style images

## Requirements

### Python
- tqdm
- sklearn

### Other
- GraphViz

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
