import pandas as pd
import numpy as np
test = pd.read_csv('joint_all.csv')
test=test[(test.DX == 0) | (test.DX == 1)]
data=test.as_matrix()
#X=data[:, np.arange(2,data.shape[1])]
X=data[:, np.append(np.array((2,3)),np.arange(4010,data.shape[1]))]
y=data[:,1]
X[np.isnan(X)]=0
randsort=np.argsort(np.random.rand(y.size))
X=X[randsort]
y=y[randsort]

from sklearn.cross_validation import StratifiedKFold
from sklearn.feature_selection import RFECV
from sklearn.svm import SVC

X_new = X

# Create the RFE object and compute a cross-validated score.
svc = SVC(kernel="linear")
# The "accuracy" scoring is proportional to the number of correct
# classifications
rfecv = RFECV(estimator=svc, step=1, cv=StratifiedKFold(y, 5),
              scoring='accuracy')

rfecv.fit(X_new, y)
print("Optimal number of features : %d" % rfecv.n_features_)
print("max score: %f" % np.max(rfecv.grid_scores_))