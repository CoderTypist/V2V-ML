from sklearn.linear_model import LinearRegression
import v2vml.calculations as calc
import v2vml.globals as g
import numpy as np
import pandas as pd
import math
import sys
from typing import List


def get_feature_header():
    return ['Avg Dist', 'Avg Ratio', 'BSM Angle', 'Slope Dif', 'Avg Dif', 'Type']


def features_from_file(file_name, file_path, node_type) -> None:

    print('Extracting features from', file_name)
    raw = pd.read_csv(file_path)
    num_rows = len(raw)

    # do not consider nodes that do not have at least 3 rows
    if num_rows < g.SAMPLE_SIZE:
        return

    # get features
    df = None
    for i in range(0, num_rows//g.SAMPLE_SIZE):

        # make sure that there are at least g.SAMPLE_SIZE rows remaining
        if i > num_rows:
            break

        # get features from sample
        features = features_from_rows(raw.iloc[i*g.SAMPLE_SIZE:(i*g.SAMPLE_SIZE)+g.SAMPLE_SIZE, :], node_type)

        # append row of features to dataframe
        if 0 == i:
            df = features

        else:
            df = pd.concat([df, features], ignore_index=True)

    # print(df)

    # write the features to a file
    with open('./data/processed_data/' + file_name, 'w') as out_file:

        # write column headers to file
        out_file.write(','.join(df.columns) + '\n')

        # write rows to the file one at a time
        for i in range(len(df)):
            row = [str(x) for x in df.iloc[i, :].values.tolist()]
            out_file.write(','.join(row) + '\n')


def features_from_rows(sample: pd.DataFrame, node_type, sample_size=g.SAMPLE_SIZE) -> pd.DataFrame:

    df = pd.DataFrame(0, index=np.arange(1), columns=get_feature_header())

    # FEATURE 1: average distance
    sum_of_distances = 0
    for i in range(sample_size):
        sum_of_distances += calc.distance(sample.iloc[i, 0], sample.iloc[i, 1], sample.iloc[i, 2], sample.iloc[i, 3])

    avg_distance = sum_of_distances / sample_size

    # FEATURE 2: average ratio
    sum_of_ratios = 0
    for i in range(sample_size-1):
        sum_of_ratios += calc.distance(sample.iloc[i, 0], sample.iloc[i, 1], sample.iloc[i+1, 0], sample.iloc[i+1, 1]) \
                         / calc.distance(sample.iloc[i, 2], sample.iloc[i, 3], sample.iloc[i + 1, 2], sample.iloc[i + 1, 3])

    avg_ratio = sum_of_ratios / (sample_size - 1)

    # FEATURE 3: average bsm angle
    sum_of_angles = 0
    for i in range(sample_size-2):

        bsm_a = np.array([sample.iloc[i, 2], sample.iloc[i, 3]])
        bsm_b = np.array([sample.iloc[i+1, 2], sample.iloc[i+1, 3]])
        bsm_c = np.array([sample.iloc[i+2, 2], sample.iloc[i+2, 3]])

        dif_a_b = bsm_a - bsm_b
        dif_c_b = bsm_c - bsm_b

        cos = np.dot(dif_a_b, dif_c_b) / (np.linalg.norm(dif_a_b) * np.linalg.norm(dif_c_b))
        sum_of_angles += np.degrees(np.arccos(cos))

    avg_angle = sum_of_angles / (sample_size - 2)

    # FEATURE 4: slope dif
    actual_x = sample.iloc[:, 0]
    actual_y = sample.iloc[:, 1]

    bsm_x = sample.iloc[:, 2]
    bsm_y = sample.iloc[:, 3]

    # if a line is vertical, make it horizontal before calculating the slope
    # a line if all of x values are the same
    is_vertical = False
    if len(np.unique(actual_x.to_numpy()).tolist()) == 1:
        bsm_x, bsm_y = bsm_y, bsm_x

    # find the best fit line and get the slope
    model = LinearRegression()
    model.fit(np.reshape(bsm_x.to_numpy(), (len(bsm_x), 1)), np.reshape(bsm_y.to_numpy(), (len(bsm_y), 1)))
    slope = abs(model.coef_[0][0])

    # FEATURE 5: Avg Dif
    sum_of_dif = 0
    for i in range(sample_size):
        sum_of_dif += abs(sample.iloc[i, 0] - sample.iloc[i, 2]) + abs(sample.iloc[i, 1] - sample.iloc[i, 3])
    avg_dif = sum_of_dif/(2*sample_size)

    # set df values
    df.iloc[0, 0] = avg_distance
    df.iloc[0, 1] = avg_ratio
    df.iloc[0, 2] = avg_angle
    df.iloc[0, 3] = slope
    df.iloc[0, 4] = avg_dif
    df.iloc[0, 5] = node_type

    return df


# input: a list where each index is a dataframe containing the features for a single node
# returns: a single dataframe with the features from all of the nodes in the list
def condense_features(node_features: List[pd.DataFrame]) -> pd.DataFrame:

    df = node_features[0].copy()

    for features in node_features[1::]:
        df = pd.concat([df, features], ignore_index=True)

    return df
