import pandas as pd
import numpy as np

df = pd.read_excel(r'redash_jan.xlsx', engine='openpyxl')
list_days = []

for i in range(len(df.index)):
    k = df.at[i, 'date'].split('T')[0].split('-')[2]
    list_days.append(k)

df['day'] = list_days

df.to_excel('redash_jan_updated.xlsx', sheet_name='Sheet1')
