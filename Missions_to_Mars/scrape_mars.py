from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import re
import pandas as pd

mars_info = {}

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape():

  browser = init_browser()
  url = 'https://mars.nasa.gov/news/'
  jpl_url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
  mars_facts_url = 'https://space-facts.com/mars/'
  hemisphere_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"

  mars_info = {}

# Mars News

  browser.visit(url)

  browser.is_element_present_by_value('article_teaser_body', wait_time=5)

  html = browser.html
  soup = bs(html, 'html.parser')

  title = soup.find('div', attrs={'class': 'content_title'}).text
  paragraph = soup.find('div', attrs={'class': 'article_teaser_body'}).text

  mars_info['title'] = title
  mars_info['paragraph'] = paragraph


  # JPL Mars Space Images

  browser.visit(jpl_url)

  jpl_html = browser.html
  jpl_soup = bs(jpl_html, 'html.parser')

  jpl_image = jpl_soup.find('article', attrs={'class': 'carousel_item'})
  jpl_string = jpl_image['style']
  jpl_image_link = re.findall(r"'(.*?)'", jpl_string)
  featured_image_url = 'https://www.jpl.nasa.gov' + jpl_image_link[0]

  mars_info['featured_image_url'] = featured_image_url


  # Mars Facts

  mars_facts_table = pd.read_html(mars_facts_url)
  mars_facts_df = mars_facts_table[0]
  mars_facts_df.columns = ['Description', 'Value']
  mars_facts_df.set_index('Description', inplace=True)
  mars_facts_html = mars_facts_df.to_htmls()

  mars_info['facts'] = mars_facts_html


  # Mars Hemisphere

  browser.visit(hemisphere_url)
  hemisphere_html = browser.html
  hemisphere_soup = bs(hemisphere_html, 'html.parser')

  hemisphere_items = hemisphere_soup.find_all('div', class_='item')
  hemisphere_image_urls = []
  hemisphere_home_url = "https://astrogeology.usgs.gov"

  for i in hemisphere_items:
      title = i.find('h3').text
      img_url = i.find('a')['href']
      hemisphere_url_equation = hemisphere_home_url + img_url

      browser.visit(hemisphere_url_equation)
      hemisphere_html = browser.html
      hemisphere_soup = bs(hemisphere_html, 'html.parser')
      hemisphere_img = hemisphere_soup.find('div', class_='downloads')
      hemisphere_image_url = hemisphere_img.find('a')['href']
      
      print(hemisphere_image_url)
      img_dict=dict({'title': title, 'img_url': img_url})    
      hemisphere_image_urls.append(img_dict)
  mars_info['hemisphere_image_urls'] = hemisphere_image_urls
  browser.quit()
  return mars_info