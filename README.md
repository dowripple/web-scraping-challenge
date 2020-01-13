# web-scraping-challenge
## by Michael Dowlin
### 1/12/20

#### Description
This is a web application that will go to several Mars mission related sites and return news, images and more.  To read the HTML, I used pandas, splinter and beautiful soup.  I used flask to launch the local service and call a python program to get the latest mars data.  The flask application stores the information into a PyMongo database called mars_data.

#### Directions
To run, start up a Mongo db service (type in mongod), and then run app.py.  This will start the flask service, which run an initial scrape.  When you open the browser to the home page, the information should be displayed.

#### Contents

| File                         | Description                                                                                     |
|------------------------------|-------------------------------------------------------------------------------------------------|
|app.py                        |Notebook that will start the flask app.  Make sure Mongo service is running!                     |
|chromedriver.ext              |Splinter driver for the chrome browser                                                           |
|mission_to_mars_v2.ipynb      |Notebook that comprises the first part of the homework  |
|scrape_mars.py                |Python program version of the notebook scraping.  The function scrape() returns a dictionairy object of all the latest mars news/images/etc. |
|templates\index.html          |HTML template that is used by the flask application.  Will display the Mars info  |
