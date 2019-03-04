import requests, json, re, random
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
            html = list(soup.children)[9]

            # put all urls into a master list
            for el in soup.findAll("h3", {"class": "teaser-item__title"}):
                ele = el.find('a')
                recipe_urls.append('https://www.bbcgoodfood.com' + ele['href'])


# ============================================ #


def get_recipe_data():
    """
        Request recipe page, parse html and extract data, save into a dict as json
    """

    # store all urls in a master list
    recipe_list = []

    # loop- over list of cuisine url categories
    for url in recipe_urls:

        # make page request - as FireFox
        page = requests.get(url, headers={"User-Agent": "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:47.0) Gecko/20100101 Firefox/47.0"})

        # if status is ok - proceed
        if page.status_code == 200:
            soup = BeautifulSoup(page.content, 'html.parser')
            html = list(soup.children)[9]
            html = list(html.children)[5]



            # set up lists / dicts
            recipe_filters = {}
            recipe_data = {}
            ingredients = []
            methods = []
            nutrition = []
            nLabels = []
            nValues = []



            # extract content of script tag containing filter targets and convert to a dict
            filters = re.findall(r'"environment".*"setPageLevelTargeting":true', str(page.content))
            filters = '{' + filters[0]
            filters = json.loads(filters[:-29])



            # separate single and multiple items for iterating
            filters_single_list = ['planning', 'cuisine', 'mood', 'diet', 'skill_level', 'main_ingredient']
            filters_multiple_list = ['course', 'kw', 'ingred']
            html_data = [
                ['title', "h1", {"class": "recipe-header__title"}],
                ['author', "span", {"class": "author"}],
                ['description', "div", {"class": "field-item even"}],
                ['prep_time', "span", {"class": "recipe-details__cooking-time-prep"}],
                ['cook_time', "span", {"class": "recipe-details__cooking-time-cook"}],
                ['difficulty', "span", {"class": "recipe-details__text"}],
                ['serves', "span", {"itemprop": "recipeYield"}]
            ]


            # check for KeyError and replace - (SINGLE VALUES) - FILTERS
            for i in filters_single_list:
                try:
                    recipe_filters[i] = filters[i][0]['value']
                except KeyError:
                    recipe_filters[i] = ""

            # check for KeyError and replace - (LISTS) - FILTERS
            for i in filters_multiple_list:
                try:
                    recipe_filters[i] = [i['value'] for i in filters[i]]
                except KeyError:
                    recipe_filters[i] = []

            # check for AttributeError and replace - (SINGLE VALUES) - HTML_DATA
            for i in html_data:
                try:
                    recipe_data[i[0]] = soup.find(i[1], i[2]).get_text()
                except AttributeError:
                    recipe_data[i[0]] = ""

            # find image and extract the src/ alt / title into a list - IMAGE_DATA
            image = soup.find('img', {"itemprop": "image"})
            image_details = ['https://' + image['src'][2:], image['alt'], image['title']]



            # put all ingredients into a separated list - (LISTS)
            for el in soup.find_all("li", {"class": "ingredients-list__item"}):
                ingredients.append(el['content'])

            # put all methods into a separated list
            for el in soup.find_all("li", {"class": "method__item"}):
                methods.append(el.get_text())

            # put all labels into a list - (NUTRITION)
            for el in soup.find_all("span", {"class": "nutrition__label"}):
                nLabels.append(el.get_text())

            # put all values into a list
            for el in soup.find_all("span", {"class": "nutrition__value"}):
                nValues.append(el.get_text())

            # join together the labels with their values
            for el in range(6):
                nutrition.append([nLabels[el], nValues[el]])



            # create user specific fields
            users = {
                "likes": random.randint(0, 100),
                "dislikes": random.randint(0, 30)
            }

            # create recipe object - add all values to master dict
            recipe = {
                "recipe_filters": recipe_filters,
                "recipe_data": recipe_data,
                "image_details": image_details,
                "ingredients": ingredients,
                "methods": methods,
                "nutrition": nutrition,
                "users": users
            }

            # append to master recipe list
            recipe_list.append(recipe)

    # write db to json file
    with open('app/data/scraper/db.json', 'w') as db_file:

        # create dict entry and dump into json file
        db['recipes'] = recipe_list
        json.dump(db, db_file)


# ============================================ #


""" 
    run scraper 
"""
get_recipe_urls()
get_recipe_data()