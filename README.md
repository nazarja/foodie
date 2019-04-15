## Build a Recipe App - Foodie 
---

Python & Flask - Data Centric Development  - Milestone Project 4 for Code Institute by Sean Murphy

---

## Project Summary

Foodie is a full recipe website built on *Flask* as the backend and incorporates *MongoDB* as the Database, *UIKit* as a CSS Framework, Vanilla JavaScript and *PyGal* for charting with Python.

The concept and usage of the website is based on world cuisines that users have the ability to view, search, filter, search and filter, edit, delete, create, leave comments and much more.

I wanted the website to closely represent a real world website of the same nature and have tried to include as many features as possible that makes the site both user friendly and encourages the user to stay on the site and make use of all the features (Which are documented in the [Features](#Features) section of the README). 

The website on launch contains 398 recipes sourced from [BBC Good Food](https://bbcgoodfood.co.uk). To include this vast amount of recipes I built a web scaper with [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/), and built another python script to *insert_many* to my MongoDB Database.

I hope you enjoy viewing and using this site as much as I have had building it!


---

## UX

The User Interface is built completely around two important elements of the database, the users profile, and the recipes filters.

When designing the menu system I needed to have a way to quickly navigate through the sites recipes based on a major recipe filter, such as cuisine or diet, and the main dropdown menu allows you to do this.

The other side of the menu is all about user actions, being able to see your profile page, with saved recipes, recent comments and site statistics. And logging in and out of the site quickly.

Wherever you on on the site you will be able to navigate easily around the site just from the navbar alone.

#### Colours, Design & UX  

Browsing online at various recipe and food websites I studied the general layout patterns and common color tones being used, I decided upon using a css framework that would allow me to quickly create a reusable and appeasing grid system and slider system for displaying multiple recipes.

This would mean creates lots  of small html partials and using jinja to insert the html into any page that needed it. These partials are reused multiple times and makes the site really modular and cut down on code size immensely. Partials have been created for a number of items such as *comments*, *grid*, *slider*, *pagination*, *menu*, *icon navs* and much more.

After researching a number of CSS Frameworks I decided upon [UIKit](https://getuikit.com) as it looked extremely modern, was very easy to implement, responsiveness is second to none and contained so many features that I could easily include on the site such as notifications, off canvas menu, dropdown menus, sliders and grid systems that are better and more intuitive than bootstraps. At times the html code can look slighty messy with *uikits* attributes and classes, but overall less code is needed compared to bootstrap. This framework was the perfect choice for the project type.

The logo was created by myself using [PIXLR PRO](https://pixlr.com/pro/) and upon scrolling down the page the menu resizing and a small logo is displayed. As the original logo used *url_for*, I was presented with an issue in JavaScript when trying to set the new images url, the solution was to build an absolute url using `window.location.protocol + '//' + window.location.host + '/';` which solved the `src` problem, simply using `window.location.href` would duplicate the current endpoint and result in the image not being found.

Responsiveness was extremely important and I was alway testing and aware of how the elements reacted to different screen widths and my aim was to make the site the same experience on mobile as desktop. 


#### User Stories

- As a user ... I am immediately aware what the nature of the site is and its purpose.
- As a user ... I can navigate through the recipes by various main filters.
- As a user ... I can filter recipes based on multiple queries.
- As a user ... I can search for a recipe, and further filter my results.
- As a user ... I can create a user profile, and log in and out.
- As a user ... I access the site on mobile and have close to the same experience as a desktop device.
- As a user ... I can select a remember me feature so I can close my browser and return later without logging in again.
- As a user ... I can like, dislike, comment on, create, edit and delete recipes and see those recipes on my profile page if they exist.


--- 

## Database

I choose to use [BBC Good Food](https://bbcgoodfood.co.uk) as the source of data for all the recipes and images. 

The json files which are  used as a template for a new recipe , a new user and the menu can be found in `/app/data/schemas`.

The web scraper and python script to add the recipes to the database can be found in `/app/data/scraper`.

### Designing the Database

The site was firstly going to need a a filter system to used as both a menu and recipe filters, so decided upon a few categories found on bbcgoodfood. After viewing what recipe information was available, I looked at the source code of each recipe and noticed a few patterns between all recipes that would help me get the data I needed. 

To gather the vast amount of recipes to create the site, I used [Beautiful Soup](https://www.crummy.com/software/BeautifulSoup/bs4/doc/) to scrape for the recipes. 

Firstly I started with a list of urls to scrape and then scraped each categories recipe urls, usually about 20 for each category. Now with a large list of categories and recipe urls I could begin scraping each recipe for its data and ultimately saving each recipe as an object in a json file. This would be my database.

Much data was simply imbedded in tags with ids or classes and was relatively easy to parse,  but there was extra metadata that was being served to each page within a `script` tag with an object inside which contained data in key, value pairs. This data contained filters information that I could use for a menu system and apply to each recipe. I needed to use a regular expression to extract the data and then converted it back to an object. This object would serve as my recipe filters.

To add the database to mongodb I created a small python script inserting a first user, menu filters, and recipes. The `insert_many` method was used for recipes, and `insert_one` for the others. 

To simulate already liked / disliked recipe count, I generated random numbers with `random.randint(0, 100)` for example.

**Default recipe.json**
```
{
    "filters": {
        "planning": "",
        "cuisine": "",
        "mood": "",
        "diet": "",
        "skill": "",
        "main_ingredient": "",
        "course": [],
        "kw": [],
        "ingred": []
    },
    "details": {
        "title": "",
        "author": "",
        "description": "",
        "prep_time": "",
        "cook_time": "",
        "difficulty": "",
        "serves": ""
    },
    "image": [],
    "ingredients": [],
    "methods": [],
    "nutrition": [
        ["kcal", ""],
        ["fat", ""],
        ["saturates", ""],
        ["carbs", ""],
        ["sugars", ""],
        ["fibre", ""]
    ],
    "users": {
        "likes": 0,
        "dislikes": 0,
        "comments": []
    }
}
```

**Default user.json**

The User object was going to small, and only needed to store a few essential keys. 

```
{
    "username": "",
    "password": "",
    "recipes": [],
    "likes": [],
    "dislikes": [],
    "comments": []
}
```

**Default filters.json**

To create the menu system, I iterated over the recipes db.json file as for each filter check for unique values and added to a manually created dictionary. Some filters contained odd results which I removed after it was created and sorted alphabetically.

```
{
    "cuisine": ["american", "british", "caribbean", "chinese", "french", "greek", "indian", "italian", "japanese", "mediterranean", "mexican", "moroccan", "spanish", "thai", "turkish", "vietnamese"],
    "course": ["afternoon-tea", "breakfast", "brunch", "buffet", "canapes", "cocktails", "condiment", "dessert", "dinner", "drink", "fish-course", "lunch", "main-course", "pasta-course", "side-dish", "snack", "soup-course", "starter", "supper", "treat", "vegetable-course"],
    "planning": ["10-minute-supper", "beginners", "easily-doubled", "easily-halved", "everyday-food", "freezable", "in-season", "make-ahead", "make-it-tonight", "ultimate"],
    "mood": ["budget", "casual", "comfort", "family-friendly", "formal", "hearty", "indulgent", "light", "quick", "romantic"],
    "diet": ["dairy-free", "gluten-free", "healthy", "low-calorie", "low-fat", "low-salt", "vegetarian"],
    "skill": ["easy", "medium", "hard"]
}
```

---  

## Project Layout

The main goal during development was to seperate the code to make it as modular as possible. The main application code is contained in `/app`., with sub directories for `/data, /models, /routes, /static, /templates`.

The idea behind this structure is that I could create smaller functions which could be reusable, better readabilty and tracing back errors was simplified. The pattern is generally that the routes.py called a helper function from the `/models` dir, the code was processed, sent back and a route was rendered with new data. 

To categorize functions better, a class was created for each main operation in `/models` such as `Recipes`, `Users`, `Forms` and `Graphs`. Although there is python logic in routes function, its keep to a minimum when possible.

---

## Features  


**Navigation**

The Navigation is the core of the site, it not only provides the navigation, but also the basis for filtering recipes. When creating the initial database, a seperate collection was created that could be used solely for the menu and filter systems. To make this available to all templates, I used `@app.context_processor ` which opens the filters schema, converts to dictionary and is now available to jinja without needing to be passed directly on each route.  

**Filters**

The filters page / function initally shows the top liked recipes. Results can be filtered using a form of dropdown selects menus. The default value for the selects is 'all'. Pagination is achieved by returning a limit of items selected by the user. Results can be sorted using different values. If any filter needs to be applied, it is placed into a list in which we can then use the `$or`, `$in` and `$and` methods to get multiple results returned.

**Search**

Users can search for a recipe through the search icon in the navigation bar. Upon recieving the search term, a redirect to the filters page takes place. The keywords array is search for a matching keyword and the title is also searched for any matches contained the title.

After a search has taken place, results can be further refined with the filters bar / form.

**URL Slugs**

When passing long recipe titles, the url did not look very friendly. No jinja filters appeared to exist to combat this as I was passing the title in a link, I needed to create a custom filter that replaces spaces and non word chars with something such as _ . I created the function `slug_friendly` which can be used as a jinja filter with `|resub`. To make it available as a filter I could assign the new function with `app.jinja_env.filters['resub'] = slug_friendly`

**Recipe CRUD**

Recipes can only be edited, created and deleted by a logged in user. For the simpllicity of the site, any user can edit or delete any recipe, not just those that they have created themselves. Most recipe crud functions can be found in the `/models/recipes` class. 

1. For the Index page I gather random recipes from the database with `aggregate` and `"$sample"`. 

2. For the Category Pages I find all recipes by cuisine type and return a list limited by 12 and sorted by default by likes. Although the can be sorted differently by using the sort menu on the page. Pagination is implemted by counting the number of documents and dividing by 12 to get the nuumber of pages avaible. Pagination logic is written int he category route. The find function skips a number of document depending on the page * 12 which is passed to the `get_categories` function.

3. Recipes can be created by clicking on the + icon on the screen, this will load a new form that when submitted, is processed and assigned to the recipe schema's dictionary before being inserted to the database. Additional Fields may be added to both ingredients and instructions.

4. Recipes can be edited by clicking the first icon in the icon nav, a request to get the recipe details from the database is sent, before being returned to the jinja template which at that point the values are used as the default values in the input fields. Fields can be removed or added via buttons for the ingredients and instructions fields.

- One issue I had was creating multiple fields with the same name such as ingredients, the solution was to append a number to the end of the name in line with the index number of the loop such as `ingredient-1`. Which when turning back to a list to be stored, I used a regex to find all keys with ingredient, and then put them into a list together.  

5. Recipes can be deleted, a `delete_one` request is sent with the recipe id, and any comments that exist should also be removed from all users profiles.


**Comments**

A user can comment on a recipe, to save page refresh, a event listener captures the submitted form and updates the html before sending a xhr request to the backend to update the users profile and the recipe with the new comment.

Captured is the time, the user, recipe_id, title and the reply. This is converted to a dictionary before being inserted to the database. The new comment contains a link to the recipe, so when on the profile page with comments you can go directly to that recipe.  

**Likes / Dislikes**

Recipes can be liked or disliked by a logged in user, by never liked and disliked at the same time. Nor can you like or dislike an item more than once. For the sake a limiting page refreshes, when a like/dislike is clicked a JavaScript event listener is fired, a xhr request is sent to the `/update_favourites` route with the recipe id and opinion, and the page is updated to reflect the updated like/dislike.

An issue I encountered during this was that the like/dislike icons were made with svg and changing the color of the event.target did not work properly, nor did changing the inner Text as it would remove the icon as well.

The solution was to rely on Event Bubling to captue the click and identify the childNodes, which then I could cahnge the colorr of the entire svg and change the textContent of the count.

**Profile**

The profile page serves as both a hub for a user to see the recipes that they have either created or edited, their recent comments that they have made and some site statistics.

Recent comments are limited to 8 results, for recipes I have limited the initial results to 8, pagination can be achieved with dynamic buttons which will increase or decrease the results by 4 recipes. This particular pagination style was achieved with JavaScript.

On deleting a recipe, making a comment or editing/creating a recipe. The profile page should be immediatly updated.


**Login**    

Login authentication logic is wrote in the `/sign/<url>` route, but the user session is handled by Flask-Login. After confirming a successful username/password login or sign up, the user profile is given to Flask Login which uses mongo to find the user and loads the users object through the `User` Class.

A number of methods are then available to you in python and jinja such as `is_authenticated`, and more importantly the `current_user` object, which I can update by calling a written method `User.getData`. If a profile should be updated, then the `current_user` object should also.


**Graphs**   

The graphs were created will PyGal, this easy to use and simple charting library was perfect for my needs. Two graphs were created. A Bar chart and a Pie Chart.

1. The Bar Chart shows the average likes and dislikes from each cuisine in the database. To get the average of each I used the `aggregate` method to group all cuisine types and I used `$avg` to get the average from the likes and dislikes category. To make the bar chart a little more interesting I inverted the dislikes by mulitpling the final sum by -1. This creates upside down dislike bars.

2. The Pie Chart shows the average nutritional kcal (calories) from each cuisine in the database, tis was a lot trickier. As the kcal were stored in a 2d array, and as strings. After much trial and error, I performed two `projection` operations in combination with `$arrayElemAt` to select the correct index. Finally I needed to sum the average and convert to an interger with `$toInt` which I would later find out is only supported in Mongo Shell 4+.


---

**Bugs:**


1. (Resolved) The last `ul` on the menu needed a seperate class from the rest as there was only 3 items in the menu, using `flex-wrap: nowrap` ensured that the was not a single item that looked out of place in the dropdown menu.

2. (Resolved) Original I had intended to use mlab, but had to use mongo atlas instead as mlab's current version of mongo shell is 3.6 and I need version 4.0. I discovered after a test deployment to heroku that my profile page would cause a 500 server not found error. Tracing the error is the logs I discovered that the mongo method `$toInt` was only introduced in version 4.0. The `kcal` values were all saved as strings, so when I was making my graphs and calculating the `$avg` I need to convert the string to an int.

3. (Resolved) Adding a edited recipe to the users profile, if that recipe already existed, it was duplicated, this was solved with `$addToSet`. When a recipe was deleted, the comments for that recipe remained in the users profile. Solved with  removing the recipe from all users profiles.

4. (Resolved) Creating or editing a recipe would sometimes add unused fields to a recipe.

5. Main Menu tends to re-adjust itself with scrolling back to the top of the page. Causing a small visual but nothing offputting.

6. Tooltips cause minor JavaScript Reflow, Also on mobile, when clicking on a like the tooltip does not dissapear until the next screen touch.


---

### Features Left to Implement

- The comments section on recipes does not currently allow for a comment to be deleted.
- Extra graphs showing the users personally most liked category etc ...
- Additional form elements to be created for adding additonal course or cuisines to the same recipe. I find the edit recipe form was getting very large so I restricted the feature to  a single item per selection.
- A feature for users to able to follow other users.
- Users can only edit or delete a recipe that they  have created themselves.

---
## Technologies Used

> *Python, Flask, Jinja, Flask-WTF, SSLify, PyGal, PyMongo, BeautifulSoup, Flask-Login, JavaScipt, JSON, CSS, UIKIT, Git, Heroku*  
 
- Python  
https://docs.python.org/3/  
*time, math, json, random, shuffle, datetime, os*  
Python is used as the backend language for created helper functions, logic and routes  
Various modules were used to assist with parsing, math, json operations and file manipulation


- Flask  
http://flask.pocoo.org/  
*render_template, redirect, url_for, session, request, flash*  
Flask was used as a micro framework for constructing a backend.   
It also provided useful functions that I could use to help with routing, errors and messages.

- Jinja  
http://jinja.pocoo.org/  
Jinja is the templating language used by flask. I made a lot of use of jinjas if statements, loops and ability to construct partial templates.

- Flask-WTForms  
https://flask-wtf.readthedocs.io/en/stable/  
*werkzeug.security, generate_password_hash, check_password_hash , wtforms, wtforms.validators*  
I have used flask-wtf to perform only the sign in / up form creation, partial clien-side validation, and similarly realted - `werkzeug.security` to created and validate hashed passwords.

- SSLify  
[https://github.com/kennethreitz/flask-sslify](https://github.com/kennethreitz/flask-sslify "SSLify")  
SSLify was used to correct and ensure that all requests were carried out over secure `https`, as on signing in, heroku switches to http some some unknown reason.


- JavaScript  
https://www.ecma-international.org/  
I have used vanilla JavaScript to perform some aesthetic changes to the DOM, as per guidelines, no logic has been performed withh JavaScript. Most post request are posted directed to the backend with the exception of commentsand likes / dislikes, Instead I have used an XMLHttpRequest to prevent unnecessary page refresh.
JavaScript was also used to listen for clicks on certian elements and show notifications when the user is not logged in, JavaScript is used by UIKit for some elements, and I have used JavaScript for dynamic creation and deletion of inputs on the edit / create recipe form. 

- JSON  
https://www.ecma-international.org/  
JSON is used as the primary data structure that is used to create a new recipe or user. It initially contained the first database before transfering to mongodb.


- CSS, UIKit  
http://www.w3.org/Style/CSS/members  
https://getuikit.com  
I have mainly used UIKit to style most elements with my own code usually reinforcing and applying sublte overwrites to the default styling being applied. Some styles and media queries are used without uikit and are usually a positional or width percentage based style being applied.

- PyGal    
http://pygal.org/en/stable/
I used PyGal for charting two graphs visible on the users profile page. Although not incredible interactive, the speed and simplicity of creating charts with PyGal mad it an easy choice.

- PyMongo    
https://api.mongodb.com/python/current/    
I used the official PyMongo to work with MongoDB with Python, frequently referencing the API documentation for operations I needed to perform with mongodb.

- Flask-Login    
https://flask-login.readthedocs.io/en/latest/    
Flask-Login was used to handle user session management. It handles logging in, logging out, and remembering your useers sessions even after the browser has been closed.

- BeautifulSoup4    
https://www.crummy.com/software/BeautifulSoup/bs4/doc/         
Beautiful Soup was used to scrape content and parse the return html data from bbcgoodfood. It main use was aiding in creating a large database programatically.



---

## Testing

Testing was performed in 3 different ways.  
2. Automated written tests
1. Manual Browser Testing during develoment  
3. User testing

The test file can be found in `/tests`, an issue I had was running the file from tests directory, I was unable to import `app` and the solution seemed long winded, so I resorted to running the test file from the projects root directory.

####  Automated written tests

I used pythons built-in Unit Test Framework  [UnitTest](https://docs.python.org/3/library/unittest.html), and making reference to this page https://rallion.bitbucket.io/explorations/flask_tutorial/api/flask.Response.html  which clearly highlights many methods that are availible on the Flask Response Object.

My UnitTests were seperated into two main Test Suites being, those that required a logged in user and those that did not.
Each suite is started with a `setUp` and `TearDown` with is performed before and after each test. 

After import all required modules, I configured the database and set the correct app.config variables for testing.

For pattern of my test generally followed the following style:
    - get a route, or in the case of a route that expects a form, post to a route with a dictionary of simulated data  
    - decode the response.data object to utf-8
    - test a fail situation to make sure the test is functional correctly
    - assert that the expected data exists in the data that is returned
    - if writing to the database, assert that the new data did not exist before and afterwards that it has been updated  

Using automated testing I have tested and successfully asserted:
    - all routes get as expected including either a 200 ok, 302 redirect or 404 unknown
    - Sign In and Sign Up functions correctly for failed and successful attempts
    - Post request to the filters , search and search with filters return correct data
    - comments can be posted and are sucessfully written to the database
    - likes / dislikes can be added / removed. Values are checked before and after the test to compare interger increases and descreases.
    - recipe edits are tested to ensure data has been successfully updated
    - recipe creation is tested to ensure a new recipe with id has been added to the database, a regex was need to get the recipe id from the return data
    - recipe deleteion, a recipe cannot be found int the database after the test


#### Browser Testing

While my main choice of browser for development is google chrome, I regularly checked the performance on firefox and opera browsers. 
Making use of browser resizing and dev tools device toolbars on each browser to test responsiveness and how how the grid, fonts and media queries were performing and the consistency between each. Adjusting to find a happy medium for all three. 

After I had test deployed the site to heroku I was able to see the real life versions which I was able to test on android phone, amazon fire tablet and different orientations. Unfortunitely, I have no safari devices which I am able test on.

The css framework in use, uikit, and the few media queries I wrote were quite sufficent and only twice did I need to  make a few changes a once to correct any elements out of place. Most of the time it was a case of changing an element to a `display: block` to force it to the next line.


####  User testing

I have asked multiple friends to test the website on their devices and recieved very little feedback on errors indicating that there was not many issues to be found. I am satisfied with the outcome.

---

## GIT

Git was used on project foundation and throughout at regular intervals during development. Not as many commits were performed as previous projects, but they were performed and pushed when needed or a particular feature has been completed.

I created two seperated branches, one branch was for testing the creation of graphs with pygal, and the other was for testing the app on heroku. This allowed me to keep some different files to my locally ran master branch which I was using with mongodb locally, as well as not needing to change debug variables each time.

I have made use of the .gitignore file to exclude my env vars, pycache, venv and vscode files and folders.

---

## Deployment 

Before I fully deployed my finalized project to heroku I created a branch in git called 'heroku', this was only a test deployment to see how the site functioned using a remote database, let other people test the site and to test the site on mobile and tablet. The currently deployment branch is master.

#### Deployment to Heroku

In order the deploy my project to Heroku I have completed the following steps:

- Created a `Procfile` with the command `echo web: python run.py > Procfile`.
- Created a requirement.txt file so Heroku know what python modules it will need to run my application with the command `pip freeze > requirements.txt`
- Created a new branch to test deployment to heroku changing  MONGO_URI  from local to mongo atlas, changed app.run() to set debug to false.
- Created a new project on heroku and in the deploy section linked my github repositiory with heroku in order to deploy straight from the source.
- Configured any enviornment variables in Heroku App Settings > Config Vars such as my Secret Key, IP PORT and MONGO_URI.
- After reviewing the test branch, I noted changes to made locally and applied them.
- Finalised all code, and made sure that it was production ready and ensured that my `.gitignore` was not uploading any `__pycache__`, `.env` files  or `venv` folders.
- Made a final commit / push to github.
- Deployed the application from heroku admin page using linked repository and master branch.
- The application was now fully deployed


#### Setting the project up in a local development environment

Should you wish the run a local copy of this application of your local machine, you will need to follow the instructions listed below:

**Tools you may need:**   

Python 3 installed on your machine https://www.python.org/downloads/  
PIP installed on your machine https://pip.pypa.io/en/stable/installing/  
Git installed on your machine: https://gist.github.com/derhuerst/1b15ff4652a867391f03  
A text editor such as https://code.visualstudio.com/ Visual Studio Code  
An account at  https://www.mongodb.com/cloud/atlas MongoDB Atlas or MongoDB running locally on your machine

**Instructions**

- Obtain a copy of the github repository located at https://github.com/nazarja/foodie by clicking the download zip button and extracting the zip file to a chosen folder. Should you have git installed on your system you can clone the repository with the command `git clone https://github.com/nazarja/foodie.git`.
- If possible open a termial session in the unzip folder or `cd` to the correct location
- Next your need to install a virtual environment for the python interpreter, I recommend using pythons built in virtual environment. Enter the command `python -m venv venv` . NOTE: Your python command may differ, such as `python3` or `py`.
- Activate the venv with the command `source venv/bin/activate`, again this may differ depending on your operating system, please check https://docs.python.org/3/library/venv.html for further instructions.
- If needed, Upgrade pip locally by `pip install --upgrade pip`.
- Install all required modules withh the command `pip -r requirements.txt`.
- Its now time to open your text editor and create a file called `.flaskenv`.
- Inside this file you will need to create a SECRET_KEY variable and a MONGO_URI  to link to your own database. Please make sure to call your database 'foodie', with 3 collections called recipes, users, filters. You will find the source for these collections in `/app/data`.
- Lastly, open run.py and on replace line 10 to ` app.run(host=os.getenv('IP'), port=os.getenv('PORT'), debug=True)` and save the file
- You can now run the application with the command `python run.py`
- You can visit the website at `http://127.0.0.1:5000`

---

## Credits

###  Content and Media

- All Code is my own work, referencing and making use of official documentation when needed.  
- All site recipes and images are sourced from [BBC Good Food](https://bbcgoodfood.co.uk)




