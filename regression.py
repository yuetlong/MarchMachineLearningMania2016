#!/usr/bin/env python3
from numpy import loadtxt, zeros, ones, mean, std
import pandas as pd


# Code for linear regression
# We did not write these ourselves
# Here is the source and tutorial
# http://aimotion.blogspot.com/2011/10/machine-learning-with-python-linear.html

def feature_normalize(X):
    '''
    Returns a normalized version of X where
    the mean value of each feature is 0 and the standard deviation
    is 1. This is often a good preprocessing step to do when
    working with learning algorithms.
    '''
    mean_r = []
    std_r = []

    X_norm = X

    n_c = X.shape[1]
    for i in range(n_c):
        m = mean(X[:, i])
        s = std(X[:, i])
        mean_r.append(m)
        std_r.append(s)
        X_norm[:, i] = (X_norm[:, i] - m) / s

    return X_norm, mean_r, std_r


def compute_cost(X, y, theta):
    '''
    Comput cost for linear regression
    '''
    #Number of training samples
    m = y.size

    predictions = X.dot(theta)

    sqErrors = (predictions - y)

    J = (1.0 / (2 * m)) * sqErrors.T.dot(sqErrors)

    return J


def gradient_descent(X, y, theta, alpha, num_iters):
    '''
    Performs gradient descent to learn theta
    by taking num_items gradient steps with learning
    rate alpha
    '''
    m = y.size
    J_history = zeros(shape=(num_iters, 1))

    for i in range(num_iters):

        predictions = X.dot(theta)

        theta_size = theta.size

        for it in range(theta_size):

            temp = X[:, it]
            temp.shape = (m, 1)

            errors_x1 = (predictions - y) * temp

            theta[it][0] = theta[it][0] - alpha * (1.0 / m) * errors_x1.sum()

        J_history[i, 0] = compute_cost(X, y, theta)

    return theta, J_history

# We wrote most of the code from here

#Load the training dataset
data = loadtxt('training.txt', delimiter=',')

#Plot the data, commented out for faster production
'''
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
n = 100
for c, m, zl, zh in [('r', 'o', -50, -25)]:
    xs = data[:, 0]
    ys = data[:, 1]
    zs = data[:, 2]
    cs = data[:, 3]
    ax.scatter(xs, ys, zs, c=cs, marker=m)
ax.set_xlabel('WPdiff')
ax.set_ylabel('OWPdiff')
ax.set_zlabel('OOWPdiff')
plt.show()
'''

# this means the right most column of data is the result label
X = data[:, : 3]
y = data[:, 3]

#number of training samples
m = y.size

y.shape = (m, 1)

#Scale features and set them to zero mean
x, mean_r, std_r = feature_normalize(X)

#Add a column of ones to X (interception data)
it = ones(shape=(m, 4))
it[:, 1: 4] = x

#Some gradient descent settings
# We decided that 10000 iterations and 0.001 alpha is optimal
iterations = 10000
alpha = 0.001

#Init Theta and Run Gradient Descent
theta = zeros(shape=(4, 1))

theta, J_history = gradient_descent(it, y, theta, alpha, iterations)

'''
plot(arange(iterations), J_history)
xlabel('Iterations')
ylabel('Cost Function')
show()
'''

print(theta)

submissions = pd.read_csv('testfile.csv')

testX = submissions.ix[:,['WPdiff','OWPdiff','OOWPdiff']].values

ss = pd.read_csv('data/SampleSubmission.csv')

for i in range(len(testX)):
    arr = zeros(shape=(1, 4))
    arr[0][0] = 1.0
    for j in range(1,4):
        arr[0][j] = (testX[i][j-1] - mean_r[j-1]) / std_r[j-1]
    prob = arr.dot(theta)

    if prob[0][0] > 1:
        prob[0][0] = 1
    elif prob[0][0] < 0:
        prob[0][0] = 0

    print(arr,prob[0][0])
    ss.ix[i,'Pred'] = prob[0][0]

ss.to_csv('ourSubmission.csv', index=False)