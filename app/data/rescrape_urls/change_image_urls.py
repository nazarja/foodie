import json

db = {}
newDB = {'recipes': []}
image_urls = {}

# ============================================ #

with open('json/db.json', 'r') as db_file:
    db = json.load(db_file)

# ============================================ #

with open('json/image_urls.json', 'r') as image_urls_file:
    image_urls = json.load(image_urls_file)

# ============================================ #

for i in image_urls['images']:
    for j in db['recipes']:
        if i[1].lower() == j['details']['title'].lower():
            j['image'][0] = i[0]
            newDB['recipes'].append(j)

# ============================================ #

with open('json/newDB.json', 'w') as new_db_file:
    json.dump(newDB, new_db_file)
