#!/usr/bin/env python
# coding: utf-8

# In[1]:


from bs4 import BeautifulSoup as bs
import requests
from splinter import Browser
from bs4 import BeautifulSoup
import time
import pandas as pd


# ## NASA Mars News

# In[2]:


# URL of page to be scraped
url = 'https://mars.nasa.gov/news/'


# In[3]:


# Retrieve page with the requests module
response = requests.get(url)


# In[4]:


# Create BeautifulSoup object; parse with 'lxml'
soup = bs(response.text, 'lxml')


# In[5]:


# Examine the results, then determine element that contains sought info
print(soup.prettify())


# In[6]:


# Retrieve the Latest News Title and paragraph text
news_title = soup.find('div', class_='content_title').text
news_p = soup.find('div', class_='rollover_description').text
print(news_title)
print(news_p)


# ## JPL Mars Space Images - Featured Image

# In[7]:


executable_path = {'executable_path': 'chromedriver.exe'}
browser = Browser('chrome', **executable_path, headless=False)


# In[8]:


url = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
browser.visit(url)


# In[9]:


# Request and parse the HTML
html = browser.html
soup = bs(html,'html.parser')
browser.click_link_by_partial_text('FULL IMAGE')
time.sleep(4)
browser.click_link_by_partial_text('more info')


# In[10]:


# Request and parse again
html_code = browser.html
soup = BeautifulSoup(html_code, "html.parser")
image = soup.find('figure', class_='lede').a['href']
featured_image_url = 'https://www.jpl.nasa.gov'+image
print(featured_image_url)


# In[ ]:





# ## JPL Mars Space Images - Featured Image

# In[11]:


url = 'https://twitter.com/marswxreport?lang=en'
browser.visit(url)


# In[12]:


# Request and parse
html_code = browser.html
soup = BeautifulSoup(html_code, "html.parser")
mars_weather = soup.find('p', class_='TweetTextSize TweetTextSize--normal js-tweet-text tweet-text').text
print(mars_weather)


# ## Mars Facts

# In[13]:


url = 'https://space-facts.com/mars/'
browser.visit(url)


# In[14]:


# Request and parse
html_code = browser.html
soup = BeautifulSoup(html_code, "html.parser")
print(soup.prettify())


# In[15]:


My_table = soup.find('table',{'class':'tablepress tablepress-id-p-mars'})
print(My_table.prettify())


# In[16]:


My_table_rows = My_table.find_all('tr')
col_1 = []
col_2 = []


# In[17]:


for row in My_table_rows:
    rows = row.find_all('td')
    col_1.append(rows[0].text)
    col_2.append(rows[1].text)


# In[18]:


print(col_1)
print(col_2)
facts_df = pd.DataFrame({'facts':col_1, 'values':col_2})
facts_html = facts_df.to_html()
print(facts_html)


# ## Mars Hemispheres

# In[19]:


url = 'https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars'
browser.visit(url)


# In[20]:


# Request and parse the HTML
html = browser.html
soup = bs(html,'html.parser')
#print(soup.prettify())
images = soup.find_all('h3')
#     print(images)
titles = []
for image in images:
    titles.append(image.text)
#     for link in soup.find_all('a'):
#         print(link.get('href'))
for title in titles:
    print(title)


# In[21]:


links = []
for title in titles:
    browser.click_link_by_partial_text(title)
    time.sleep(1)
    html = browser.html
    soup = bs(html,'html.parser')
    link_addr = soup.find('img',class_='wide-image')
    links.append('https://astrogeology.usgs.gov'+link_addr.attrs['src'])
    browser.back()


# In[22]:


print(links)


# In[23]:


hemisphere_image_urls = {}
combine = list(zip(titles, links))
title_link = []
for title,link in combine:
    title_link.append({'title': title, 'img_url':link})

