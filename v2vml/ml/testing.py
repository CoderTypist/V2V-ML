import numpy as np
import os
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
import v2vml.configuration as conf
from v2vml.ml.metrics import StatSuite
import v2vml.ml.preprocessing as pre


def test_models():

    # each index is a dataframe containing the features for a single node
    node_features = []

    # load in features
    for file in os.listdir('./data/processed_data'):
        print('Loading in features for ./data/processed_data/{}'.format(file))
        node_features.append(pd.read_csv('./data/processed_data/' + file))

    index = ['Good', 'Faulty', 'Malicious']

    # various different stats
    logistic_regression_stat_suite = StatSuite(index=index)
    knn_stat_suite = StatSuite(index=index)
    decision_tree_stat_suite = StatSuite(index=index)
    svm_stat_suite = StatSuite(index=index)
    naive_bayes_stat_suite = StatSuite(index=index)

    for i in np.arange(conf.TRAIN_MODELS_NUM_TESTS):

        print('Iteration', i+1)

        training_node_features, testing_node_features = train_test_split(node_features, test_size=0.2)
        scaler = StandardScaler()

        train = pre.condense_features(training_node_features)
        test = pre.condense_features(testing_node_features)

        # print('DROPPING DATA!!!!!!!!!!!!!!!!')
        # train = train.drop(columns=['Avg Dist', 'Avg Ratio', 'BSM Angle'])
        # test = test.drop(columns=['Avg Dist', 'Avg Ratio', 'BSM Angle'])

        # independent features
        unscaled_x_train = train.iloc[:, :-1].to_numpy()
        unscaled_x_test = test.iloc[:, :-1].to_numpy()

        # scaled independent features
        scaled_x_train = scaler.fit_transform(unscaled_x_train)
        scaled_x_test = scaler.transform(unscaled_x_test)

        # dependent features
        y_train = train.iloc[:, -1]
        y_test = test.iloc[:, -1]

        # Logistic Regression
        model = LogisticRegression()
        model.fit(scaled_x_train, y_train)
        predictions = model.predict(scaled_x_test)
        logistic_regression_stat_suite.add(y_test, predictions)

        # KNN
        model = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2)
        model.fit(scaled_x_train, y_train)
        predictions = model.predict(scaled_x_test)
        knn_stat_suite.add(y_test, predictions)

        # Decision Tree
        model = DecisionTreeClassifier()
        model.fit(unscaled_x_train, y_train)
        predictions = model.predict(unscaled_x_test)
        decision_tree_stat_suite.add(y_test, predictions)

        # SVM
        model = SVC(kernel='linear')
        model.fit(scaled_x_train, y_train)
        predictions = model.predict(scaled_x_test)
        svm_stat_suite.add(y_test, predictions)

        # Naive Bayes
        model = GaussianNB()
        model.fit(scaled_x_train, y_train)
        predictions = model.predict(scaled_x_test)
        naive_bayes_stat_suite.add(y_test, predictions)

    # update percentages
    logistic_regression_stat_suite.finalize()
    knn_stat_suite.finalize()
    decision_tree_stat_suite.finalize()
    svm_stat_suite.finalize()
    naive_bayes_stat_suite.finalize()

    # print custom stats
    print('\n-------------------------------------------------------------------------------------------------------')
    print('Logistic Regression Stats\n')
    print(logistic_regression_stat_suite, '\n')
    print('-------------------------------------------------------------------------------------------------------\n')
    print('KNN Stats\n')
    print(knn_stat_suite, '\n')
    print('-------------------------------------------------------------------------------------------------------\n')
    print('Decision Tree Stats\n')
    print(decision_tree_stat_suite, '\n')
    print('-------------------------------------------------------------------------------------------------------\n')
    print('SVM Stats\n')
    print(svm_stat_suite, '\n')
    print('-------------------------------------------------------------------------------------------------------\n')
    print('Naive Bayes Stats\n')
    print(naive_bayes_stat_suite, '\n')
    print('-------------------------------------------------------------------------------------------------------\n')
