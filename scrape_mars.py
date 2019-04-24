from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import numpy as np
import pandas as pd


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # Mars News
    url = "https://mars.nasa.gov/news/"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get title
    results = soup.find('div', class_='content_title')
    title = results.find_all('a')[0].text

    # Get paragraph
    para_results = soup.find('div', class_='article_teaser_body')
    paragraph = para_results.text


    #JPL Mars Space Images
    jpl_url = 'https://www.jpl.nasa.gov/spaceimages/'
    browser.visit(jpl_url) 

    jpl_html = browser.html

    jpl_soup = bs(jpl_html, 'html.parser')

    jpl_results = jpl_soup.find('article', class_='carousel_item')

    featured_image_url = jpl_results.get('style')

    #Mars Weather
    twitter_url = 'https://twitter.com/MarsWxReport/'
    browser.visit(twitter_url)  

    twitter_html = requests.get(twitter_url)

    twitter_soup = bs(twitter_html.text, 'html.parser')

    twitter_results = twitter_soup.find_all('div', class_='js-tweet-text-container')

    mars_weather = twitter_results[0].text
    
    #Mars Facts

    facts_url = 'https://space-facts.com/mars/'

    tables = pd.read_html(facts_url)

    df = tables[0]
    df.columns = ['Diameter', 'Mass']

    html_table = df.to_html()

    html_table.replace('\n', '')

    df.to_html('facts_table.html')

    #Mars Hemisphere

    hemisphere_url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(hemisphere_url)

    hemisphere_html = browser.html

    hemispshere_soup = bs(hemisphere_html, 'html.parser')

    hemisphere_img = hemispshere_soup.find_all('a', class_='itemLink product-item')

    hemisphere_image_urls = []
    for img in hemisphere_img:
        title = img.find('h3')
    
    link = "https://astrogeology.usgs.gov/" + img['href']
    
    hemisphere_image_urls.append({"title": title, "img_url": link})

 
    # Store data in a dictionary
    mars_data = {
        "title": title,
        "paragraph": paragraph,
        "featured_image": featured_image_url,
        "mars_weather": mars_weather,
        "hemisphere_image": hemisphere_image_urls
    }


     

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
