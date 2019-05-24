from splinter import Browser
from bs4 import BeautifulSoup as bs
import pandas as pd
import time

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "../homework/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

mars_data = {}


def scrape():

    browser = init_browser()

    # Visit website
    nasa = "https://mars.nasa.gov/news/"
    browser.visit(nasa)

    time.sleep(2)

     # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    news_title = soup.find('div', class_='content_title').get_text()

    news_p = soup.find('div', 'article_teaser_body').get_text()

    
    #browser.quit()
#------------------------------------------

    jpl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
    browser.visit(jpl)

    time.sleep(1)

    html = browser.html
    soup = bs(html, "html.parser")

    
    image_url = browser.find_by_id('full_image')

    image_url.click()


    browser.is_element_present_by_text('more info', wait_time=5)
    more_info = browser.find_link_by_partial_text('more info')
    more_info.click()

    img = soup.find('figure', class_='lede')

    main_url = f'https://www.jpl.nasa.gov{img}'


    browser.quit()

      #------------------------------------------

    weather = 'https://twitter.com/marswxreport?lang=en'
    browser.visit(weather)

    time.sleep(2)

    html = browser.html
    soup = bs(html, "html.parser")

    mars_weather = soup.find('div', 'js-tweet-text-container').get_text()
    mars_weather


    browser.quit()

#-----------------------------------------------------------------

    space = 'https://space-facts.com/mars/'
    browser.visit(space)

    time.sleep(2)

    mars_facts = pd.read_html(space)

    mars_df = mars_facts[0]

    table = mars_df.to_html(classes="table table-striped")

    browser.quit()
    #-----------------------------------------------------

    astro = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
    browser.visit(astro)

    time.sleep(2)

    html = browser.html
    soup = bs(html, "html.parser")

    hemisphere_image_urls = []

    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup= bs(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        hemisphere_image_urls.append({"title": title, "img_url": image_url})

        hemisphere_image_urls


    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": main_url,
        "latest_tweet": mars_weather,
        "mars_table": table,
        "Hemispheres": hemisphere_image_urls
        }

    browser.quit()

    return mars_data



 