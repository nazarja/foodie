import requests, json, re, random
from bs4 import BeautifulSoup

db = {}
recipe_urls = []
image_urls = []

# ============================================ #

with open('json/urls.json', 'r') as urls_file:
    data = json.load(urls_file)
    recipe_urls = data['urls']


def get_recipe_details():
    """
        Request recipe page, parse html and extract data, save into a dict as json
    """
    for url in recipe_urls:

        # make page request - as FireFox
        page = requests.get(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"})

        # if status is ok - proceed
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            html = list(soup.children)[1]
            html = list(html.children)[1]
            image = []

            try:
                image = soup.findAll('img')[2]
                image = [image['src'], image['title']]
                image_urls.append(image)
            except KeyError:
                image = []

            # print(image)

# ============================================ #


def write_image_urls():
    with open('json/image_urls.json', 'w') as db_file:
        # create dict entry and dump into json file
        db['images'] = image_urls
        json.dump(db, db_file)


# ============================================ #

get_recipe_details()
write_image_urls()