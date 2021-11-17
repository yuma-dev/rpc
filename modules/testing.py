import json


with open('data/database.json', 'w') as f:
    data = [
        {
            "testing" : 1
        }
    ]
    json.dump(data, f, ensure_ascii=False, indent=4,sort_keys=True)