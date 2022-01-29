#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd

import requests
from bs4 import BeautifulSoup


# In[2]:


res= requests.get("https://victoria.craigslist.org/search/apa")


# In[6]:


bs= BeautifulSoup(res.content,"lxml")


# In[15]:


all_ads = bs.find_all("ul", attrs={"id":"search-results"})[0]


# In[21]:


all_ads = all_ads.find_all('li', attrs ={ "class": "result-row"})


# In[96]:


df= pd.DataFrame(columns = ['URL','date','Title', 'Price', 'Home Property', 'Hood','latitude', 'longitude', 'tags','Description'])
for ad in all_ads :
    add_info= ad.find_all('div')[0]
    
    #extract Date
    ad_date = add_info.find_all('time')[0]['datetime']
    
    #extract title
    title = add_info.find_all('h3')[0].find_all('a')[0].text
    
    #extract URL
    URL = add_info.find_all('h3')[0].find_all('a')[0]['href']
    
    #extract price
    price = add_info.find_all('span', attrs = {"class":'result-price'})[0].text
    
    #extract home property
    home_prop = add_info.find_all('span', attrs = {"class":'housing'})
    if home_prop:
        home_prop=home_prop[0].text.strip().replace('\n',',')
    else:
        home_prop = None

    #extract hood
    hood = add_info.find_all('span', attrs = {"class":'result-hood'})[0].text
    
    
    res = requests.get(URL)
    ad_page= BeautifulSoup(res.content,"lxml")
    
    # extract Description
    description =ad_page.find_all("section", attrs = {'id': 'postingbody'})[0].text
    
    # extract map location
    latitude =ad_page.find_all("div", attrs = {'id': 'map'})[0]['data-latitude']
    longitude =ad_page.find_all("div", attrs = {'id': 'map'})[0]['data-longitude']
    
    tags = ad_page.find_all("p", attrs = {'class': 'attrgroup'})
    
    tag_list = []
    for tag in tags:
        for span in tag.find_all('span'):
            tag_list.append(span.text)
        
    df = df.append({'URL': URL, 'date': ad_date,'Title': title, 'Price': price, 'Home Property': home_prop, 'Hood': hood, 'Description': description , 'latitude':latitude , 'longitude':longitude , 'tags': ','.join(tag_list)}, ignore_index=True)
    
df


# In[ ]:




