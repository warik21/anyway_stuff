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


def create_matching_row(waze_row, redash_row, ground_truth_row):
    #waze_row = waze_row.iloc[0]
    #redash_row = redash_row.iloc[0]
    waze_street = waze_row['street']
    # comparing the day's, and adding a bool to show us which conditions hold
    same_day = (int(redash_row['date'].split('T')[0].split('-')[2]) == int(waze_row['day']))
    if not same_day:
        return []
    same_city = (redash_row['yishuv_name'] == waze_row['city'])
    waze_road = [int(s) for s in str(waze_street).split() if s.isdigit()]
    if waze_road:
        waze_road = waze_road[0]
    # print(waze_road, waze_street)
    if type(waze_road) == int:
        same_road = (waze_road == redash_row['road1'])
    else:
        same_road = 0
    # using the street in waze twice is fine because it will ignore something with a number when it's a street,
    # and return no number when it's a road.
    same_street = (waze_street == redash_row['street1_hebrew'])
    same_location = is_close(waze_row['long'], waze_row['lat'], redash_row['lon'], redash_row['lat'])
    # time in the day:
    waze_time = pd.to_datetime(waze_row['pubMillis'], unit='ms')
    redash_time = pd.to_datetime(redash_row['date'])
    time_diff = (abs((waze_time - redash_time).seconds) < 3600)

    #print(ground_truth_row)
    if ground_truth_row.empty:
        is_ground_truth = 0
    #elif waze_row['uuid'] == ground_truth_row['waze uuid'][1]:
    #    is_ground_truth = 1
    elif isinstance(ground_truth_row, pd.DataFrame):
        #print(ground_truth_row['waze uuid'].tolist()[0])
        #print(waze_row['uuid'])
        if waze_row['uuid'] == ground_truth_row['waze uuid'].tolist()[0]:
            is_ground_truth = 1
        else:
            is_ground_truth = 0
#    if is_ground_truth == 1:
#        print(is_ground_truth)

    return [int(same_city), int(same_road), int(same_street), int(same_location), int(time_diff), is_ground_truth]


if __name__ == '__main__':
    entries = ["waze uuid", "redash id", "city", "road", "street", "location", "time", "ground_truth"]

    redash_df = pd.read_excel(r'redash_jan_updated.xlsx', engine='openpyxl')
    waze_df = pd.read_excel(r'Jan2021.xlsx', engine='openpyxl')
    ground_truth_df = pd.read_excel(r'mapping.xlsx', engine='openpyxl')

    generator = ground_truth_df.iterrows()
    df = pd.DataFrame(columns=entries)

    redash_generator = redash_df.iterrows()
    #print(len(redash_df.index))
    for i in range(len(redash_df.index)):
        redash_r = redash_generator.__next__()[1]
        #print(redash_r['id'])
        ground_truth_rows = ground_truth_df.loc[ground_truth_df['redash id'] == redash_r['id']]

        if len(ground_truth_rows) > 1:

            ground_truth_rows = ground_truth_rows.reset_index(drop=True)
            #print(ground_truth_rows)

            for k, ground_truth_row in ground_truth_rows.iterrows():
                waze_generator = waze_df.iterrows()
                #print(ground_truth_rows)
                ground_truth_row = ground_truth_rows.loc[[k]]
                print(ground_truth_row, type(ground_truth_row))

                for j in range(len(waze_df.index)):
                    waze_r = waze_generator.__next__()[1]
                    matching_params_row = create_matching_row(waze_r, redash_r, ground_truth_row)
                    if len(matching_params_row) == 6:
                        df_row = [waze_r['uuid'], redash_r['id']]
                        # print(df_row, matching_params_row)
                        df_row = df_row + matching_params_row
                        # print(df_row)
                        df_length = len(df)
                        df.loc[df_length] = df_row
        else:

            waze_generator = waze_df.iterrows()

            ground_truth_row = ground_truth_rows
            for j in range(len(waze_df.index)):
                waze_r = waze_generator.__next__()[1]
                matching_params_row = create_matching_row(waze_r, redash_r, ground_truth_row)
                if len(matching_params_row) == 6:
                    df_row = [waze_r['uuid'], redash_r['id']]
                    #print(df_row, matching_params_row)
                    df_row = df_row + matching_params_row
                    #print(df_row)
                    df_length = len(df)
                    df.loc[df_length] = df_row
    print(df.head())
    df.to_excel('data_to_play_with.xlsx', sheet_name='Sheet1')
