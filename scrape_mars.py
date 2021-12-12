from splinter import Browser
from bs4 import BeautifulSoup
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd


def scrape():
    # browser = init_browser()
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=True)

    # Code block to scrape top news story from replanetscience.com

    url = "https://redplanetscience.com"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")


    news_title = soup.find('div', class_='content_title').get_text()
    news_p = soup.find('div', class_='article_teaser_body').get_text()

    # Code block to scrape featured mars image from spaceimages-mars.com

    url = "https://spaceimages-mars.com"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    temp = soup.find('a', class_='showimg fancybox-thumbs')

    featured_image_url = 'https://spaceimages-mars.com/'+temp['href']  
    
    # Code block to scrape tabular mars data from galaxyfacts-mars.com and convert it
    # into an html table

    url = "https://galaxyfacts-mars.com"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    fact_rows = soup.findAll('tr')

    first = True

    for x in range(7):
        fact = fact_rows[x]
        col1 = fact.find('th').get_text()
        temp = fact.findAll('td')
        col2 = temp[0].get_text()
        col3 = temp[1].get_text()
        col3 = col3.strip('\t')
        if first:
            h1 = col1
            h2 = col2
            h3 = col3
            mars_df = pd.DataFrame(columns = [h1, h2, h3])
            first = False
        else:
            mars_df = mars_df.append([{h1:col1, h2:col2, h3:col3}], ignore_index = True)   
    
    mars_facts_html = mars_df.to_html(classes='table table-striped', index=False)

    
    # Code block to scrape images of martian hemispheres from marshemispheres.com and store 
    # them in a list of dictionaries

    url = "https://marshemispheres.com"
    browser.visit(url)

    html = browser.html
    soup = BeautifulSoup(html, "html.parser")

    item_list = soup.findAll('div', class_='item')

    hemisphere_image_urls = []

    for item in item_list:
        title = item.find('h3').get_text()
        temp2 = item.find('a', class_='itemLink product-item')
        url = "https://marshemispheres.com/"+temp2['href']
        browser.visit(url)
        html = browser.html
        soup = BeautifulSoup(html, "html.parser")
        temp = soup.find('img', class_='wide-image')
        full_img_url = "https://marshemispheres.com/"+temp['src']
        hemisphere_image_urls.append({'title': title, 'img_url': full_img_url})


    mars_data = {}

    mars_data["marsNewsTitle"] = news_title
    mars_data["marsNewsP"] = news_p
    mars_data["marsFeaturedImage"] = featured_image_url
    mars_data["marsFacts"] = mars_facts_html
    mars_data["marsHemispheres"] = hemisphere_image_urls

    # Quit the browser
    browser.quit()

    return mars_data
