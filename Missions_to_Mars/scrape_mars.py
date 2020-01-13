# Declare Dependencies 
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
import pymongo

# function to scrape all the sites and return everything in 1 dictionairy
def scrape ():
    
    # setup the browser for splinter
    browser = Browser('chrome')

    # Defining the url for the mars website
    url = 'https://mars.nasa.gov/news/'

    # return the rendered html
    response = requests.get(url)

    # create the bs object
    space_bs = bs(response.text, 'html.parser')

    # return the first article div
    title_div = space_bs.find('div', class_='content_title')

    # grab the text from the only anchor (a) tag in the div, stripping the new line
    article_title = title_div.a.text.strip('\n')    

    # div containing the paragraph, found by looking for the class "rollover_description_inner"
    p_div = space_bs.find('div',class_='rollover_description_inner')

    # grab the text from the div, stripping out the new line
    article_p = p_div.text.strip('\n')

    # featured image
    
    # navigate to image page
    browser.visit('https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars')

    # parse the html with some bs
    image_bs = bs(browser.html, 'html.parser')

    # grab the image div
    img_div = image_bs.find('div', class_="img")

    # find the img object
    img = img_div.find('img')

    # get the image object's source
    img_src = img['src']

    # setting up the image base url
    base_url = 'https://www.jpl.nasa.gov'

    # setting the featured image url (base + image_id)
    featured_image_url = base_url + img_src

    # grabbing the image title too, it may come in handy later
    featured_image_title = img['title']

    # MARS FACTS

    # navigate to image page
    browser.visit('https://space-facts.com/mars/')

    # parse the html with some bs
    facts_bs = bs(browser.html, 'html.parser')

    # return the div that contains the facts
    facts_div = facts_bs.find('div', id='facts')

    # grab the factrs unordered list
    facts_ul = facts_div.find('ul')

    # create a list of list items in the ul
    facts_li = facts_ul.find_all('li')

    # list to store the facts
    mars_facts = []
    # dummy id
    fact_id = 0

    # loop through the facts, creating a dictionairy for each row, and appending to the facts list
    for fact_li in facts_li:
        # the fact title is in the stron tag, so grab that text
        fact_title = fact_li.find('strong').text
        
        # make a dictionary of the object
        fact = {
            'fact_id': fact_id,
            'fact_title': fact_title,
            'fact': fact_li.text.strip('\n')
        }
        
        # add to list
        mars_facts.append(fact)
        
        # increment the id counter
        fact_id +=1
        
    # convert list of dictionairies to a dataframe
    facts_df = pd.DataFrame(mars_facts)

    # create the html string for the table of facts, adding the bootstrap table classes
    facts_table = facts_df.to_html(classes='table table-striped')

    # HEMISPHERES

    # navigate to image page
    browser.visit('https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars')

    # parse the html with some bs
    hemi_bs = bs(browser.html, 'html.parser')

    # find the four anchor tags for each hemisphere
    hemi_as = hemi_bs.find_all('a', class_='itemLink')

    # counter for id
    hemi_id = 0

    # base url for hemisphere page
    base_url = 'https://astrogeology.usgs.gov'

    # list to store dicitonaries (rows)
    hemispheres = []

    len(hemi_as)

    # there are two links per hemisphere, i only want to grab one
    hemi_link_cntr = 0

    # list to store the hemisphere stuff
    hemispheres = []

    # loop through the 4 hemis
    for hemi_a in hemi_as:
        
        if hemi_link_cntr == 1:
            
            # grab this hemisphere's href (link)
            img_url = hemi_a['href']
        
            # go to the hemi page
            hemi_url = base_url + img_url
        
            # going to page
            browser.visit(hemi_url)
            
            # bs on the hemisphere page
            single_hemi_bs = bs(browser.html, 'html.parser')
            
            # find the a-tags, loop through until the one with 'original' is found
            a_tags = single_hemi_bs.find_all('a','')
            for a_tag in a_tags:
                
                a_text = a_tag.text
                
                if a_text == 'Original':
                    
                    img_url = a_tag['href']
                    
        
            # get the h2 tag with the class of "title"
            title_tag = single_hemi_bs.find('h2', class_='title')

            # get the text
            title = title_tag.text
            
            # create the dictionary
            hemisphere = {
                'hemi_id': hemi_id,
                'title': title,
                'img_url': img_url,
            }
            
            hemispheres.append(hemisphere)
            
            # increment the counter
            hemi_id += 1
            
            # reset the counter
            hemi_link_cntr = 0
        
        else:
            
            # increment the counter
            hemi_link_cntr = 1

    mars_updates = {
        'latest_news_title': article_title,
        'latest_news_desc': article_p,
        'featured_image_url': featured_image_url,
        'featured_image_title': featured_image_title,
        'facts_table': facts_table,
        'hemispheres' : hemispheres
    }

    # close the browser
    browser.quit()

    return mars_updates