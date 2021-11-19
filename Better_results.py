import pandas as pd
import numpy as np
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report, confusion_matrix
import matplotlib.pyplot as plt

df = pd.read_excel(r'data_to_play_with.xlsx', engine='openpyxl', sheet_name='only_data')
X = df.loc[:, ['city', 'road', 'street', 'location', 'time']]
Y = df.loc[:, 'ground_truth']

lists = []
counters = []
number_of_ones = []
number_of_zeros = []

for i in range(len(df.index)):

    curr_row = list(X.loc[i])
    curr_y = Y[i]

    if curr_row not in lists:
        lists.append(curr_row)
        counters.append(1)
        number_of_ones.append(0)
        number_of_zeros.append(0)

    else:
        k = lists.index(curr_row)
        counters[k] = counters[k] + 1

    b = lists.index(curr_row)
    if curr_y == 1:
        number_of_ones[b] = number_of_ones[b] + 1
    else:
        number_of_zeros[b] = number_of_zeros[b] + 1

with open('stats.txt', 'w') as f:
    for j in range(len(counters)):
        f.write(str(lists[j]))
        f.write('\t')
        f.write('number of occurences: ')
        f.write(str(counters[j]))
        f.write('\t')
        f.write('number of zeros: ')
        f.write(str(number_of_zeros[j]))
        f.write('\t')
        f.write('number of ones: ')
        f.write(str(number_of_ones[j]))
        f.write('\n')

print(sum(counters))



def logreg(X, Y):
    model = LogisticRegression(solver='liblinear', random_state=0)
    model.fit(X, Y)

    model.classes_

    predictions = model.predict(X)
    model.score(X, Y)

    cm = confusion_matrix(Y, model.predict(X))

    fig, ax = plt.subplots(figsize=(8, 8))
    ax.imshow(cm)
    ax.grid(False)
    ax.xaxis.set(ticks=(0, 1), ticklabels=('Predicted 0s', 'Predicted 1s'))
    ax.yaxis.set(ticks=(0, 1), ticklabels=('Actual 0s', 'Actual 1s'))
    ax.set_ylim(1.5, -0.5)
    for i in range(2):
        for j in range(2):
            ax.text(j, i, cm[i, j], ha='center', va='center', color='red')
    plt.show()
