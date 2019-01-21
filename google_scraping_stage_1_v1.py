#!/usr/bin/env python
# coding: utf-8

# ## Importing library

# In[1]:


import time
from time import sleep
import requests
from bs4 import BeautifulSoup
import pandas as pd
import numpy as np
import os


# ## Setting up keywords

# In[2]:


keyword_df = pd.read_csv('00_keywords.csv')
keyword_list = keyword_df['Keywords'].values.tolist()
number_of_results_list = keyword_df['Number of results'].values.tolist()
language_code_list = keyword_df['Language Code'].values.tolist()


# ## Searchpage scrapping

# In[3]:


def get_random_ua():
    random_ua = ''
    ua_file = 'ua_file.txt'
    try:
        with open(ua_file) as f:
            lines = f.readlines()
        if len(lines) > 0:
            prng = np.random.RandomState()
            index = prng.permutation(len(lines) - 1)
            idx = np.asarray(index, dtype=np.integer)[0]
            random_proxy = lines[int(idx)]
            random_ua = random_proxy.rstrip()
    except Exception as ex:
        print('Exception in random_ua')
        print(str(ex))
    finally:
        return random_ua


# In[4]:


def request_link():
    user_agent = get_random_ua()
    search_term = keyword_list[number_inputs]
    number_results = number_of_results_list[number_inputs]
    language_code = language_code_list[number_inputs]
    headers = {
            'user-agent': user_agent,
             'referrer': 'https://google.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Pragma': 'no-cache',
        }
    escaped_search_term = search_term.replace(' ', '+')
    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results, language_code)
    delays = [7, 4, 6, 2, 10, 19]
    delay = np.random.choice(delays)
    time.sleep(delay)
    response = requests.get(google_url)
    google_url
    response.raise_for_status()
    response_text = response.text 
    text_list = response_text.split('</a>') 
    text_df = pd.DataFrame({'col':text_list})
    if not os.path.exists('results'):
        os.makedirs('results')
    return text_df


# In[5]:


def test_link():
    user_agent = get_random_ua()
    search_term = keyword_list[number_inputs]
    number_results = number_of_results_list[number_inputs]
    language_code = language_code_list[number_inputs]
    headers = {
            'user-agent': user_agent,
             'referrer': 'https://google.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Pragma': 'no-cache',
        }
    escaped_search_term = search_term.replace(' ', '+')
    google_url = 'https://www.google.com/search?q={}&num={}&hl={}'.format(escaped_search_term, number_results, language_code)
    print (google_url)


# In[6]:


def normal_result():
    search_term = keyword_list[number_inputs]
    text_df = request_link_list[number_inputs]
    escaped_search_term = search_term.replace(' ', '+')
    # Non-ad & Non-table link & with cached
    text_df_set = text_df[text_df['col'].str.contains("</h3>")]
    if len(text_df_set) > 0:
        text_df_set = text_df[text_df['col'].str.contains("</h3>")]
        text_df_set_2 = text_df_set['col'].str.split("http://webcache.googleusercontent.com/", n = 1, expand = True)
        text_df_set_2.columns = ['a', 'b']
        text_df_set_3 = text_df_set_2['b'].str.split(":", n = 1, expand = True)
        text_df_set_3.columns = ['a', 'b']
        text_df_set_4 = text_df_set_3['b'].str.split(":", n = 1, expand = True)
        text_df_set_4.columns = ['a', 'b']
        text_df_set_5 = text_df_set_4['b'].str.split("%", n = 1, expand = True)
        text_df_set_5.columns = ['full link', 'b']
        text_df_set_5 = text_df_set_5.drop(['b'], axis=1)
        text_df_set_5 = text_df_set_5.reset_index(drop=True)
        text_df_set_5['search term'] = search_term
    else:
        col_names =  ['full link', 'search term']
        text_df_set_5  = pd.DataFrame(columns = col_names)
        text_df_set_5.loc[len(text_df_set_5)] = ['result not found',search_term]
        
    # Non-ad & Non-table link & with cached    
    text_df_wo_cache = text_df[text_df['col'].str.contains("q=related")]
    if len(text_df_wo_cache) > 0: 
        text_df_wo_cache.head()
        text_df_wo_cache_2 = text_df_wo_cache['col'].str.split('q=related:', n = 1, expand = True)
        text_df_wo_cache_2.columns = ['a', 'b']
        text_df_wo_cache_3 = text_df_wo_cache_2['b'].str.split('+', n = 1, expand = True)
        text_df_wo_cache_3.columns = ['full link', 'b']
        text_df_wo_cache_3 = text_df_wo_cache_3.drop(['b'], axis=1)
        text_df_wo_cache_3 = text_df_wo_cache_3.reset_index(drop=True)
        text_df_wo_cache_3['search term'] = search_term
    else:
        col_names = ['full link', 'search term']
        text_df_wo_cache_3  = pd.DataFrame(columns = col_names)
        text_df_wo_cache_3.loc[len(text_df_wo_cache_3)] = ['result not found',search_term]
    
    #concating cached and similar result
    frames = [text_df_set_5, text_df_wo_cache_3]
    normal_result = pd.concat(frames)

    #combining 
    normal_result = normal_result.drop_duplicates(subset=['full link'], keep="first")
    normal_result = normal_result.reset_index(drop = True)
    normal_result = normal_result.dropna()
    normal_result
    normal_result_file_name = 'results\\' + escaped_search_term + '-normal+result.csv'
    normal_result.to_csv(normal_result_file_name)


# In[7]:


def result_with_map():
    search_term = keyword_list[number_inputs]
    text_df = request_link_list[number_inputs]
    escaped_search_term = search_term.replace(' ', '+')
    # Table link
    text_df_tab = text_df[text_df['col'].str.contains("<span>")]
    if len(text_df_tab) > 0:
        text_df_tab_2 = text_df_tab['col'].str.split("<span>", n = 1, expand = True)
        text_df_tab_2.columns = ['a', 'b']
        text_df_tab_3 = text_df_tab_2['b'].str.split("</span>", n = 1, expand = True)
        text_df_tab_3.columns = ['organization name', 'b']
        text_df_tab_3 = text_df_tab_3.drop(['b'], axis=1)
        text_df_tab_3 = text_df_tab_3.reset_index(drop=True)
        text_df_tab_3['search term'] = search_term
        text_df_tab_file_name = 'results\\' +escaped_search_term + '-with+map+result.csv'
        text_df_tab_3.to_csv(text_df_tab_file_name)
    else:
        print('')


# In[8]:


def result_with_adwords():
    search_term = keyword_list[number_inputs]
    text_df = request_link_list[number_inputs]
    escaped_search_term = search_term.replace(' ', '+')
    # Adwords Link 
    text_df_ad = text_df[text_df['col'].str.contains('<div class="ads-visurl">')]
    if len(text_df_ad) > 0:
        text_df_ad_2 = text_df_ad['col'].str.split('<cite class="UdQCqe">', n = 1, expand = True)
        text_df_ad_2.columns = ['a', 'b']
        text_df_ad_3 = text_df_ad_2['b'].str.split('</cite>', n = 1, expand = True)
        text_df_ad_3.columns = ['a', 'b']
        text_df_ad_3['a'] = text_df_ad_3['a'].str.replace('<b>','')
        text_df_ad_3['a'] = text_df_ad_3['a'].str.replace('</b>','')
        text_df_ad_3 = text_df_ad_3.drop(['b'], axis=1)
        text_df_ad_3.columns = ['website with adword']
        text_df_ad_3['search term'] = search_term
        text_df_ad_3 = text_df_ad_3.reset_index(drop=True)
        text_df_ad_file_name = 'results\\' +escaped_search_term + '-with+adwords+result.csv'
        text_df_ad_3.to_csv(text_df_ad_file_name)
    else:
        print('')


# In[9]:


request_link_list =[]
for number_inputs in range(0,len(keyword_df)):
    request_link()
    request_link_list.append(request_link()) 
    normal_result()
    result_with_map()
    result_with_adwords()
    test_link()
   

