import os
import pandas as pd
import pickle
from sklearn.linear_model import LogisticRegression
from sklearn.naive_bayes import GaussianNB
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsClassifier
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.tree import DecisionTreeClassifier
import v2vml.ml.preprocessing as preprocess


# Models are trained and saved as .pkl files
def export_models(dir_path):

    #Ensure path ends with /
    if dir_path[-1] != '/':
        dir_path += '/'

    # delete old models
    for model in os.listdir(dir_path):
        os.remove(dir_path + model)

    # Each index is a dataframe containing the features for a single node
    features = []

    # Load in features from previous data
    for file in os.listdir('./data/processed_data'):
        print('Loading in features for ./data/processed_data/{}'.format(file))
        features.append(pd.read_csv('./data/processed_data/' + file))
    print()

    # Split features between training and testing sets
    training_features, testing_features = train_test_split(features, test_size=0.2)
    scaler = StandardScaler()

    # Preprocess the train and test features
    train = preprocess.condense_features(training_features)
    test = preprocess.condense_features(testing_features)

    # independent features
    unscaled_x_train = train.iloc[:, :-1].to_numpy()
    unscaled_x_test = test.iloc[:, :-1].to_numpy()

    # scaled independent features
    scaled_x_train = scaler.fit_transform(unscaled_x_train)
    scaled_x_test = scaler.transform(unscaled_x_test)

    # dependent features
    y_train = train.iloc[:, -1]
    y_test = test.iloc[:, -1]

    # export models
    # Logistic Regression
    model = LogisticRegression()
    model.fit(scaled_x_train, y_train)
    with open(dir_path + 'Logistic_Regression_Model.pkl', 'wb') as out_file:
        pickle.dump(model, out_file)
    with open(dir_path + 'Logistic_Regression_Model.pkl', 'rb') as in_file:
        print(pickle.load(in_file))
    print()

    # KNN
    model = KNeighborsClassifier(n_neighbors=5, metric='minkowski', p=2)
    model.fit(scaled_x_train, y_train)
    with open(dir_path + 'KNN_Model.pkl', 'wb') as out_file:
        pickle.dump(model, out_file)
    with open(dir_path + 'KNN_Model.pkl', 'rb') as in_file:
        print(pickle.load(in_file))
    print()

    # Decision Tree
    model = DecisionTreeClassifier()
    model.fit(unscaled_x_train, y_train)
    with open(dir_path + 'Decision_Tree_Model.pkl', 'wb') as out_file:
        pickle.dump(model, out_file)
    with open(dir_path + 'Decision_Tree_Model.pkl', 'rb') as in_file:
        print(pickle.load(in_file))
    print()

    # SVM
    model = SVC(kernel='linear')
    model.fit(scaled_x_train, y_train)
    with open(dir_path + 'SVM_Model.pkl', 'wb') as out_file:
        pickle.dump(model, out_file)
    with open(dir_path + 'SVM_Model.pkl', 'rb') as in_file:
        print(pickle.load(in_file))
    print()

    # Naive Bayes
    model = GaussianNB()
    model.fit(scaled_x_train, y_train)
    with open(dir_path + 'Naive_Bayes_Model.pkl', 'wb') as out_file:
        pickle.dump(model, out_file)
    with open(dir_path + 'Naive_Bayes_Model.pkl', 'rb') as in_file:
        print(pickle.load(in_file))
    print()
