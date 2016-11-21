import json

with open('tmp_data0.json') as json_data:
    d = json.load(json_data)
    print(len(d))
