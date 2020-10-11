import requests, json
from bs4 import BeautifulSoup


"""
    This file scrapes bbc good food for recipes and recipe data,
    a list of base category urls are provided which will be scraped,
    recipe urls extracted, recipe url requested and data scraped.
    all data will then be saved in a json file for transfer to mongodb.
"""


db = {}
recipe_urls = []

base_urls = [
    'https://www.bbcgoodfood.com/recipes/collection/american',
    'https://www.bbcgoodfood.com/recipes/collection/british',
    'https://www.bbcgoodfood.com/recipes/collection/caribbean',
    'https://www.bbcgoodfood.com/recipes/collection/chinese',
    'https://www.bbcgoodfood.com/recipes/collection/french',
    'https://www.bbcgoodfood.com/recipes/collection/greek',
    'https://www.bbcgoodfood.com/recipes/collection/indian',
    'https://www.bbcgoodfood.com/recipes/collection/italian',
    'https://www.bbcgoodfood.com/recipes/collection/japanese',
    'https://www.bbcgoodfood.com/recipes/collection/mediterranean',
    'https://www.bbcgoodfood.com/recipes/collection/mexican',
    'https://www.bbcgoodfood.com/recipes/collection/moroccan',
    'https://www.bbcgoodfood.com/recipes/collection/spanish',
    'https://www.bbcgoodfood.com/recipes/collection/thai',
    'https://www.bbcgoodfood.com/recipes/collection/turkish',
    'https://www.bbcgoodfood.com/recipes/collection/vietnamese',
]


# ============================================ #


def get_recipe_urls():

    """
        Request collection page, parse html and extract the url link
    """

    # iterate over urls
    for url in base_urls:

        # make page request - as FireFox
        page = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"})

        # if status is ok - proceed
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            html = list(soup.children)[2]

            # put all urls into a master list
            for el in soup.findAll("a", {"class": "img-container img-container--square-thumbnail"}):
                recipe_urls.append(el['href'])


# ============================================ #

# write db to json file
    with open('json/urls.json', 'w') as db_file:

        # create dict entry and dump into json file
        db['urls'] = recipe_urls
        json.dump(db, db_file)


get_recipe_urls()