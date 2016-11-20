# safebooru-predict
Predict user ratings for anime-style images

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
It took 5 hours and 12 minutes to download all the metadata


