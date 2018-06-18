from lib.execute import daily_reporting, transaction_reporting
import json
import csv

with open('trans.json') as json_data:
    trans = json.load(json_data)
    results = transaction_reporting(**trans)
    # print(results)
    if results:
        keys = results[0].keys()
        with open('trans.csv', 'w') as csv_file:
            c = csv.writer(csv_file)
            c.writerow(keys)
            for result in results:
                c.writerow(result.values())


# with open('daily.json') as json_data:
#     daily = json.load(json_data)
#     results = daily_reporting(**daily)
#     if results:
#         keys = results[0].keys()
#         with open('daily.csv', 'w') as csv_file:
#             c = csv.writer(csv_file)
#             c.writerow(keys)
#             for result in results:
#                 c.writerow(result.values())
