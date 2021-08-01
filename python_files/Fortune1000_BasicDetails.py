#!/usr/bin/env python
# coding: utf-8

# In[1]:


from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import csv
import re
import pandas as pd
from bs4 import BeautifulSoup
import requests
import html


# In[ ]:


driver = webdriver.Chrome(r'C:/Users/DELL-PC/OneDrive/Desktop/chromedriver.exe')  
csv_file = open('fortune2021.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)
writer.writerow(['rank','company','revenues','revenue % change', 'profits','profits % change','assets','market val','change in rank 1000','employees','change in rank 500'])

years_list = [2021]
s = "https://fortune.com/fortune500/{}/search/"


# In[ ]:


for i in years_list:
    url = s.format(i)
    print(url)
    driver.get(url)
    # # Click review button to go to the review section
    # review_button = driver.find_element_by_xpath('//span[@class="padLeft6 cursorPointer"]')
    # review_button.click()


    # Page index used to keep track of where we are.
    index = 1
    while True:
        if index > 100:
            break

        try:
            index = index + 1
            # Find all the rows on the page
            wait_row = WebDriverWait(driver, 30)
            rows = wait_row.until(EC.presence_of_all_elements_located((By.XPATH,
                                        '//div[@class="rt-tr-group"]')))
            for row in rows:
                # Initialize an empty dictionary for each review
                row_dict = {}
                # Use relative xpath to locate the title, text, username, date, rating.
                # Once you locate the element, you can use 'element.text' to return its string.
                # To get the attribute instead of the text of each element, use 'element.get_attribute()'
                try:
                    rank = row.find_element_by_xpath('.//div[@class="rt-td searchResults__cell--2Y7Ce searchResults__rank--1sTfo"]//span').text
                    row_dict['rank'] = rank
                except:
                    rank = None
                try:
                    company = row.find_element_by_xpath('.//div[@class="rt-td searchResults__cell--2Y7Ce searchResults__title--3LyRA"]//span/div').text
                    row_dict['company'] = company
                except:
                    company = None

                try:
                    other_vals = row.find_elements_by_xpath('.//div[@class="rt-td searchResults__cell--2Y7Ce"]//span') 
                    other_vals = [val.text for val in other_vals]  
                    row_dict['revenues'] = other_vals[0]
                    row_dict['revenue % change'] = other_vals[1]
                    row_dict['profits'] = other_vals[2]
                    row_dict['profits % change'] = other_vals[3]
                    row_dict['assets']= other_vals[4]
                    row_dict['market value'] = other_vals[5]
                    row_dict['change in rank 1000'] = other_vals[6]
                    row_dict['employees'] = other_vals[7]
                    row_dict['change in rank 500'] = other_vals[8]
                except:
                    row_dict['revenues'] = None
                    row_dict['revenue % change'] = None
                    row_dict['profits'] = None
                    row_dict['profits % change'] = None
                    row_dict['assets']= None
                    row_dict['market value'] = None
                    row_dict['change in rank 1000'] = None
                    row_dict['employees'] = None
                    row_dict['change in rank 500'] = None


                writer.writerow(row_dict.values())

            # Locate the next button on the page.
            time.sleep(3)
            next_button = driver.find_element_by_xpath('//div[@class="-next"]')
            next_button.click()

        except Exception as e:
            print(e)
            break
csv_file.close()
driver.close()


# In[2]:


headers = {
    "clientID" : "1g0195d428oi204f274g",
    "clientSecret" : "efbr0e5jlpjuj5ibn2ugfmpi7b573uqsn1h6voi1rmn1d5p8t2kk9o2e38aj",
    "grantType" : "cred",
}

api_url = "https://login.insideview.com/Auth/login/v1/token.json"
response = requests.post(api_url, data = {'clientId' : '1g0195d428oi204f274g', 'clientSecret' : 'efbr0e5jlpjuj5ibn2ugfmpi7b573uqsn1h6voi1rmn1d5p8t2kk9o2e38aj','grantType' : 'cred'}).json()
access_token = response["accessTokenDetails"]["accessToken"]


# In[3]:


headers = {
    "Accept": "application/json",
    "accessToken" : access_token,
}


# In[5]:


api_url = "https://api.insideview.com/api/v1/target/companies"
id = []
comp = []
for i in range(2):
    response = requests.post(api_url, headers=headers, data = {"fortuneRanking" : "fortune1000","resultsPerPage" : 500,'page' : i+1}).json()
    companies_id_list = response["companies"]
    for j in companies_id_list:
        id.append(int(j['companyId']))
        comp.append(j['name'])


# ## The following is the code to get the Basic Details of the companies using the InsideView API.

# In[6]:


company_list = "https://api.insideview.com/api/v1/target/companies"
city = []
state = []
industry = []
website = []
fb = []
twitter = []
linkedin = []

for i in range(len(comp)):
    if(i%20 == 0):
        print(i+1)
    r = requests.post(company_list,headers = headers,data = {'companyName' : comp[i], 'fortuneRanking' : 'fortune1000','resultsPerPage' : 50}).json()
    key = r['companies'][0].keys()
    
    if('city' in key):
        city.append(r['companies'][0]['city'])
    else:
        city.append('')
    
    if('state' in key):
        state.append(r['companies'][0]['state'])
    else:
        state.append('')
    
    if('companyFacebookProfile' in key):
        fb.append(r['companies'][0]['companyFacebookProfile'])
    else:
        fb.append('')
        
    if('industry' in key):
        industry.append(r['companies'][0]['industry'])
    else:
        industry.append('')
        
    if('website' in key):
        website.append(r['companies'][0]['website'])
    else:
        website.append('')
        
    if('companyTwitterProfile' in key):
        twitter.append(r['companies'][0]['companyTwitterProfile'])
    else:
        twitter.append('')
        
    if('companyLinkedInProfile' in key):
        linkedin.append(r['companies'][0]['companyLinkedInProfile'])
    else:
        linkedin.append('')


# In[7]:


d = {'Company' : comp, 'Industry' : industry, 'City' : city, 'State' : state, 'Website' : website, 'Facebook' : fb, 'Twitter' : twitter, 'LinkedIn' : linkedin}


# In[8]:


df = pd.DataFrame.from_dict(d)
df


# #### Uses the US_State_Codes.csv file to convert the State code to its name.

# In[9]:


df1 = pd.read_csv('US_State_Codes.csv')
states = df1['States'].to_list()
codes = df1['Codes'].to_list()


# In[10]:


state = df['State']


# In[11]:


s = []
for st in state:
    flag = 0
    for i in range(len(codes)):
        if(codes[i] == st):
            s.append(states[i])
            flag = 1
    if(flag == 0):
        s.append(st)


# In[12]:


df['Headquarters'] = df['City'] + ', ' + s


# In[13]:


df.drop(columns = ['City','State'],inplace = True)
df.head()


# ## Use fortune2021.csv file to include the revenues, FortuneRank of the comapnies and to sort them in the increasing order of their FortuneRank. 

# In[14]:


df1 = pd.read_csv("fortune2021.csv")
c1000 = df['Company'].to_list()
c2021 = df1['company'].to_list()
c1000_copy = df['Company'].to_list()
c2021_copy = df1['company'].to_list()


# In[15]:


for i in range(len(c1000)):
    c1000[i] = ''.join(e for e in c1000[i] if e.isalnum())
for i in range(len(c2021)):
    c2021[i] = ''.join(e for e in c2021[i] if e.isalnum())
for i in range(len(c1000)):
    c1000[i] = c1000[i].lower()
for i in range(len(c2021)):
    c2021[i] = c2021[i].lower()


# In[16]:


missing_companies = []
for i in range(len(c1000)):
    temp = c1000[i]
    flag = 0
    for j in range(len(c2021)):
        if(c2021[j].find(temp) != -1 or temp.find(c2021[j]) != -1):
            flag = 1
            continue
    if(flag == 1):
        continue
    missing_companies.append((c1000_copy[i],i+1)) 
missing_companies


# In[17]:


missing_companies_1 = []
for i in range(len(c2021)):
    temp = c2021[i]
    flag = 0
    for j in range(len(c1000)):
        if(c1000[j].find(temp) != -1 or temp.find(c1000[j]) != -1):
            flag = 1
            continue
    if(flag == 1):
        continue
    missing_companies_1.append((c2021_copy[i],i+1)) 
missing_companies_1 


# In[18]:


print(len(missing_companies))
print(len(missing_companies_1))


# In[19]:


c1000[3] = 'ibm'
c1000[24] = 'automaticdataprocessing'
c1000[54] = 'ups'
c1000[56] = 'aig'
c1000[67] = 'libertymutualinsurancegroup'
c1000[91] =  'statefarminsurance'
c1000[115] = 'usaa'
c1000[145] = 'estéelauder'
c1000[181] = 'tiaa'
c1000[212] = 'ufpindustries'
c1000[238] = 'windstreamholdingsii'
c1000[258] = 'guardianlifeinscoofamerica'
c1000[274] = 'fanniemae'
c1000[303] = 'freddiemac'
c1000[309] = 'academysportsandoutdoors'
c1000[358] = 'mahwahbergenretailgroup'
c1000[424] = 'fmglobal'
c1000[428] = 'molsoncoorsbeverage'
c1000[463] = 'teledyneflir'
c1000[521] = 'erieinsurancegroup'
c1000[540] = 'expeditorsintlofwashington'
c1000[575] = 'americannationalgroup'
c1000[621] = 'servicecorpinternational'
c1000[684] = 'westinghouseairbraketechnologies'
c1000[909] = 'jonesfinancialedwardjones'
c1000[925] = 'sentryinsurancegroup'
c1000[938] = 'countryfinancial'


# In[20]:


revenue = df1['revenues'].to_list()
rank = df1['rank'].to_list()


# In[21]:


rev = []
ra = []
mis = []

for i in range(len(c1000)):
    temp = c1000[i]
    max_len = 0
    j_index = -1
    
    for j in range(len(c2021)):
        temp1 = c2021[j]
        if(temp1.find(temp) != -1 or temp.find(temp1) != -1):
            if(max_len < len(temp1)):
                max_len = len(temp1)
                j_index = j
    
    if(j_index != -1):
        rev.append(revenue[j_index])
        ra.append(rank[j_index])
    else:
        rev.append("")
        ra.append(-1)
        mis.append(i)

df['Revenue (in Millions)'] = rev
df['Fortune1000_Rank'] = ra


# In[22]:


r = []
for s in rev:
    s = s.replace('$','').replace(',','')
    if(s == ''):
        r.append(0)
    else:
        r.append(float(s))


# In[23]:


df['revenue'] = r
df.sort_values('revenue',ascending = False,inplace = True)
df.drop(columns = ['revenue'],inplace = True)
df = df[['Fortune1000_Rank','Company','Revenue (in Millions)','Industry','Website','Headquarters','Facebook','Twitter','LinkedIn']]
df.to_csv("Fortune1000_BasicDetails.csv",index=False)


# In[ ]:




