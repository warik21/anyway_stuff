import pandas as pd
import numpy as np


def is_close(waze_lon, waze_lat, redash_lon, redash_lat):
    """

    :param waze_lon:
    :param waze_lat:
    :param redash_lon:
    :param redash_lat:
    :return: bool, deciding whether the points are close enough or not.
    """
    if np.linalg.norm(np.array((float(waze_lon), float(waze_lat))) -
                      np.array((float(redash_lon), float(redash_lat)))) < 0.05:
        return 1
    return 0


def check_compatibility(waze_row, redash_row):
    """
    This function takes a waze row and a redash row and decides how compatible they are by the parameters we have
    :param waze_row: tuple,  the waze row
    :param redash_row: tuple, the redash row
    :return: compatibility(bool): from 0 to 1, deciding how compatible the 2 rows are.
    """
    #Same day will be the condition for everything now, but once everything is in normal date time,
    #there will be an exception for adjacent days.
    #because the objects are generators, we need to take the second element
    waze_row, redash_row = waze_row[1], redash_row[1]
    waze_street = waze_row['street']
    #comparing the day's, and adding a bool to show us which conditions hold
    same_day = (int(redash_row['date'].split('T')[0].split('-')[2]) == int(waze_row['day']))
    same_city = (redash_row['yishuv_name'] == waze_row['city'])
    waze_road = [int(s) for s in str(waze_street).split() if s.isdigit()]
    if waze_road:
        waze_road = waze_road[0]
    same_road = (waze_road == redash_row['road1'])
    #using the street in waze twice is fine because it will ignore something with a number when it's a street,
    #and return no number when it's a road.
    same_street = (waze_street == redash_row['street1_hebrew'])
    same_location = is_close(waze_row['long'], waze_row['lat'], redash_row['lon'], redash_row['lat'])
    if same_day:
        # print('same day')
        if same_city + same_road + same_road + same_location > 2:
            return True


def prediction_creator(redash_dataframe, waze_dataframe):
    """
    This function takes the redash, waze and labeled dataframes and gives us accuracy, precision and recall
    :param redash_dataframe: the redash dataframe for that month
    :param waze_dataframe: the waze dataframe for that month
    :return: compatibles_list, a list of prediction tuples.
    """
    compatibles_list = []
    redash_generator = redash_dataframe.iterrows()
    for i in range(len(redash_dataframe.index)):
        waze_generator = waze_dataframe.iterrows()
        redash_r = redash_generator.__next__()
        for j in range(len(waze_dataframe)):
            waze_r = waze_generator.__next__()
            compatibility = check_compatibility(waze_r, redash_r)
            # print(compatibility)
            if compatibility:
                compatibles_list.append([redash_r[1]['id'], waze_r[1]['uuid']])
    return compatibles_list


def accuracy_statistics(predictions_list, ground_truth):
    """

    :param predictions_list:
    :param ground_truth:
    :return:
    """
    #ground truth is the whole list of true labels, meaning it contains the true positives and the true negatives
    true_positive = []
    false_negative = []
    for i in range(len(ground_truth.index)):
        label = list(ground_truth.loc[i])
        if label in predictions_list:
            true_positive.append(label)
        else:
            false_negative.append(label)
    false_positive_num = len(predictions_list) - len(true_positive)
    true_positive_num = len(true_positive)
    false_negative_num = len(false_negative)

    print('Precision is:', true_positive_num / (true_positive_num + false_positive_num))
    print('Recall is:', true_positive_num / (true_positive_num + false_negative_num))


if __name__ == '__main__':
    redash_df = pd.read_excel(r'redash_jan_updated.xlsx', engine='openpyxl')
    waze_df = pd.read_excel(r'Jan2021.xlsx', engine='openpyxl')
    ground_truth_df = pd.read_excel(r'mapping.xlsx', engine='openpyxl')

    predictions = prediction_creator(redash_df, waze_df)
    print(len(predictions))
    accuracy_statistics(predictions, ground_truth_df)
