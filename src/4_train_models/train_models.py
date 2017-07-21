#!/usr/bin/python3
import pickle
import operator
import time
import datetime
from vectorize_data import file_to_xs_ys, load_tag_index_map
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error
import pydotplus
from sklearn import tree

random_state = 1

'''
TODO
----
Choosing what model(s) to train should be controlled by the program flow, rather than messily commenting out code.
'''


filename = "../../res/safebooru/data/head_safebooru.xml"
# filename = "../../res/safebooru/data/sample_safebooru.xml"
tag_index_map = load_tag_index_map("../../res/safebooru/tag_index_map.p")
feature_names = [x[0] for x in sorted(tag_index_map.items(), key=operator.itemgetter(1))]
xs, ys = file_to_xs_ys(filename, tag_index_map)


X_other, X_valid, y_other, y_valid = train_test_split(xs, ys, test_size=10.0/100, random_state=random_state)
X_train, X_test, y_train, y_test = train_test_split(X_other, y_other, test_size=10.0/90, random_state=random_state)

def save_model(filename, regr):
	pickle.dump(regr, open(filename, "wb"))

def load_model(filename):
	regr = pickle.load(open(filename, "rb"))
	return regr

def timestamp():
	return datetime.datetime.fromtimestamp(time.time()).strftime('%Y-%m-%d %H:%M:%S')



from sklearn.decomposition import PCA
pca = PCA(n_components=100)
pca.fit(X_train)
X_train = pca.transform(X_train)
X_test = pca.transform(X_test)





from sklearn.linear_model import LinearRegression
regr = LinearRegression()
print("[{}] training linear regressor".format(timestamp()))
regr.fit(X_train, y_train)
print("[{}] training complete".format(timestamp()))
print("mean_absolute_error:", mean_absolute_error(y_test, regr.predict(X_test)))
save_model("../../res/safebooru/models/linear_regression.p", regr)


#DEBUG
#DEBUG
#DEBUG
exit()
#DEBUG
#DEBUG
#DEBUG

#decision tree regressor
from sklearn.tree import DecisionTreeRegressor
# regr = DecisionTreeRegressor(max_depth=4, min_samples_split=500, min_samples_leaf=25, random_state=random_state)
# regr = DecisionTreeRegressor(max_depth=4, min_samples_split=10000, min_samples_leaf=5000, random_state=random_state)
'''
AREAS OF INTEREST:
"criterion":["mse","mae"]
"max_features":["auto","sqrt","log2",1,2]
"max_depth":[1,3,5,10]
"min_samples_split":[2,4]
"min_samples_leaf":[1,4]
"max_leaf_nodes":[None,10]
"random_state":[random_state]
'''
# print("[{}] training decision tree regressor".format(timestamp()))
# regr.fit(X_train, y_train)
# print("[{}] training complete".format(timestamp()))
# save_model("../../res/safebooru/models/decision_tree.p", regr)

regr = load_model("../../res/safebooru/models/decision_tree.p")

# print("inputs:",X_test)
# print("truth:",y_test)
# print("predictions:",regr.predict(X_test))
# print("mean_absolute_error:", mean_absolute_error(y_test, regr.predict(X_test)))

print("exporting decision tree regressor visualization")
dot_data = tree.export_graphviz(regr, feature_names=feature_names, filled=True, out_file=None)
graph = pydotplus.graph_from_dot_data(dot_data)
graph.write_pdf("../../figures/regression_tree.pdf")



#DEBUG
#DEBUG
#DEBUG
exit()
#DEBUG
#DEBUG
#DEBUG



#random forest of decision trees regressors
from sklearn.ensemble import RandomForestRegressor
regr = RandomForestRegressor(n_estimators=10, max_depth=4, min_samples_split=500, min_samples_leaf=25, random_state=random_state)
'''
AREAS OF INTEREST:
"n_estimators":[10]
"criterion":["mse","mae"]
"max_features":["auto","sqrt","log2",1,2]
"max_depth":[1,3,5,10]
"min_samples_split":[2,4]
"min_samples_leaf":[1,4]
"max_leaf_nodes":[None,10]
"random_state":[random_state]
'''
print("[{}] training random forest regressor".format(timestamp()))
regr.fit(X_train, y_train)
print("[{}] training complete".format(timestamp()))
# print("inputs:",X_test)
# print("truth:",y_test)
# print("predictions:",regr.predict(X_test))
print("mean_absolute_error:", mean_absolute_error(y_test, regr.predict(X_test)))
save_model("../../res/safebooru/models/regression_forest.p", regr)

# print("exporting regression forest visualization")
# dot_data = tree.export_graphviz(regr, feature_names=feature_names, filled=True, out_file=None)
# graph = pydotplus.graph_from_dot_data(dot_data)
# graph.write_pdf("../../figures/regression_forest.pdf")



#PCA(1000->100) features & random forest of decision trees regressors

