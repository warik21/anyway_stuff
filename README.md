# anyway_stuff
A playground to improve the anyway algorithm of linking redash and waze accidents

redash__jan_updated is the january redash with the day in a seperate column, created by redash_date_extraction.py
mapping is the file of my labels, which I created by comparing the Jan2021 excel file (WAZE) and the redash_jan_updated excel file (REDASH)
comparing is the code which creates predictions and outputs 3 things:
1. The number of predictions we got
2. Precision - true positive / total positive
3. Recall - true positive / (true positive + false negative)
