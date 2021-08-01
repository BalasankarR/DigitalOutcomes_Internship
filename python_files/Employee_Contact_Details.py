#!/usr/bin/env python
# coding: utf-8

# In[1]:


import ast
import csv
import re
import pandas as pd
import requests
import html
import json


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


# In[4]:


api_url = "https://api.insideview.com/api/v1/target/companies"
index = []
comp = []
for i in range(2):
    response = requests.post(api_url, headers=headers, data = {"fortuneRanking" : "fortune1000","resultsPerPage" : 500,'page' : i+1}).json()
    companies_id_list = response["companies"]
    for j in companies_id_list:
        index.append(int(j['companyId']))
        comp.append(j['name'])


# #### The following code is to get the Contact Details of the Microsoft CEO Satya Nadella

# In[5]:


contact_list_url = "https://api.insideview.com/api/v1/target/contacts"
t = []
n = []
p = []

#for i in range(len(comp)):
for i in range(1):
    title = []
    names = []
    people_id = []
    
    idx = index[i]
    name = comp[i]
    
    r = requests.post(contact_list_url,headers = headers,data = {'jobLevels' : ['1'], 'companyName' : name, 'fortuneRanking' : 'fortune1000', 'resultsPerPage' : 50}).json()
    
    if(int(r['totalResults']) == 0):
        t.append(title)
        n.append(names)
        p.append(people_id)
        continue
    
    for dict in r['contacts']:
        title.append(dict['titles'][0])
        names.append(dict['fullName'])
        people_id.append(dict['id'])

    no = int(r['totalResults'])//50
    
    if(int(r['totalResults'])%50 == 0):
        no = no - 1
        
    if(no == 0):
        t.append(title)
        n.append(names)
        p.append(people_id)
    else:
        for i in range(no):
            r = requests.post(contact_list_url,headers = headers,data = {'jobLevels' : ['1'], 'companyName' : name, 'fortuneRanking' : 'fortune1000', 'resultsPerPage' : 50, 'page' : i+2}).json()
            for dict in r['contacts']:
                title.append(dict['titles'][0])
                names.append(dict['fullName'])
                people_id.append(dict['id'])
        
        t.append(title)
        n.append(names)
        p.append(people_id)

df = pd.DataFrame(list(zip(comp,t,n,p)), columns =['companyName', 'Title', 'Employees', 'InsideView Contact ID'])


# In[6]:


print(len(t[0]))
print(len(n[0]))
print(len(p[0]))


# In[7]:


for i in range(len(n[0])):
    if(n[0][i] == "Satya Nadella"):
        print("{} {}".format(i,p[0][i]))


# In[9]:


new_contact_url = "https://api.insideview.com/api/v1/target/contact/{}"
satya_nadella_id = p[0][22]
satya_nadella_url = new_contact_url.format(satya_nadella_id)


# In[10]:


response = requests.get(satya_nadella_url,headers = headers).json()


# In[11]:


response


# In[12]:


nepctf = []

if('fullName' in response.keys()):
    nepctf.append(response['fullName'])
else:
    nepctf.append("")

if('email' in response.keys()):
    nepctf.append(response['email'])
else:
    nepctf.append("")
    
if('phone' in response.keys()):
    nepctf.append(response['phone'])
else:
    nepctf.append("")
    
if('corporatePhone' in response.keys()):
    nepctf.append(response['corporatePhone'])
else:
    nepctf.append("")
    
if('twitterHandle' in response.keys()):
    nepctf.append(response['twitterHandle'])
else:
    nepctf.append("")

if('facebookHandle' in response.keys()):
    nepctf.append(response['facebookHandle'])
else:
    nepctf.append("")


# In[14]:


nepctf


# ### The following is code to get the contact details for all the employees in the database.

# #### This is to get the name, their title and their "newid" value for all contacts in the Fortune1000 companies.

# In[ ]:


contact_list_url = "https://api.insideview.com/api/v1/target/contacts"
t = []
n = []
p = []

for i in range(len(comp)):
    title = []
    names = []
    people_id = []
    
    idx = index[i]
    name = comp[i]
    
    r = requests.post(contact_list_url,headers = headers,data = {'jobLevels' : ['1'], 'companyName' : name, 'fortuneRanking' : 'fortune1000', 'resultsPerPage' : 50}).json()
    
    if(int(r['totalResults']) == 0):
        t.append(title)
        n.append(names)
        p.append(people_id)
        continue
    
    for dict in r['contacts']:
        title.append(dict['titles'][0])
        names.append(dict['fullName'])
        people_id.append(dict['id'])

    no = int(r['totalResults'])//50
    
    if(int(r['totalResults'])%50 == 0):
        no = no - 1
        
    if(no == 0):
        t.append(title)
        n.append(names)
        p.append(people_id)
    else:
        for i in range(no):
            r = requests.post(contact_list_url,headers = headers,data = {'jobLevels' : ['1'], 'companyName' : name, 'fortuneRanking' : 'fortune1000', 'resultsPerPage' : 50, 'page' : i+2}).json()
            for dict in r['contacts']:
                title.append(dict['titles'][0])
                names.append(dict['fullName'])
                people_id.append(dict['id'])
        
        t.append(title)
        n.append(names)
        p.append(people_id)

df = pd.DataFrame(list(zip(comp,t,n,p)), columns =['companyName', 'Title', 'Employees', 'InsideView Contact ID'])


# In[ ]:


df.to_csv("CSuite_with_newid.csv")


# #### Now we use the "newid" value to get their email, and phone numbers.

# In[ ]:


company_name = []
emp_name = []
email = []
phone = []
corp_phone = []
twitter = []
facebook = []

for i in range(len(n)):
    name_list = n[i]
    index_list = p[i]
    
    for j in range(len(name_list)):
        name = name_list[j]
        new_contact_url = "https://api.insideview.com/api/v1/target/contact/{}"
        name_url = new_contact_url.format(index_list[j])
        response = requests.get(name_url,headers = headers).json()
        
        company_name.append(comp[i])
        
        if('fullName' in response.keys()):
            emp_name.append(response['fullName'])
        else:
            emp_name.append("")

        if('email' in response.keys()):
            email.append(response['email'])
        else:
            email.append("")
    
        if('phone' in response.keys()):
            phone.append(response['phone'])
        else:
            phone.append("")
    
        if('corporatePhone' in response.keys()):
            corp_phone.append(response['corporatePhone'])
        else:
            corp_phone.append("")
            
        if('twitterHandle' in response.keys()):
            twitter.append(response['twitterHandle'])
        else:
            twitter.append("")

        if('facebookHandle' in response.keys()):
            facebook.append(response['facebookHandle'])
        else:
            facebook.append("")
            
df1 = pd.DataFrame(list(zip(company_name,emp_name,email,phone,corp_phone,twitter,facebook)), columns =['companyName', 'Name', 'emailId', 'phoneNo', 'corporatePhoneNo', 'twitterHandle', 'facebookHandle'])


# In[ ]:


df1.to_csv("ContactDetailsOfEmployees.csv")


# #### We will check if the code is correct by testing it out on a small company (I use the company with the index 944).

# In[15]:


contact_list_url = "https://api.insideview.com/api/v1/target/contacts"
t = []
n = []
p = []

for i in range(1):
#for i in range(len(comp)):
    i = 944
    title = []
    names = []
    people_id = []
    
    idx = index[i]
    name = comp[i]
    
    r = requests.post(contact_list_url,headers = headers,data = {'jobLevels' : ['1'], 'companyName' : name, 'fortuneRanking' : 'fortune1000', 'resultsPerPage' : 50}).json()
    
    if(int(r['totalResults']) == 0):
        t.append(title)
        n.append(names)
        p.append(people_id)
        continue
    
    for dict in r['contacts']:
        title.append(dict['titles'][0])
        names.append(dict['fullName'])
        people_id.append(dict['id'])

    no = int(r['totalResults'])//50
    
    if(int(r['totalResults'])%50 == 0):
        no = no - 1
        
    if(no == 0):
        t.append(title)
        n.append(names)
        p.append(people_id)
    else:
        for i in range(no):
            r = requests.post(contact_list_url,headers = headers,data = {'jobLevels' : ['1'], 'companyName' : name, 'fortuneRanking' : 'fortune1000', 'resultsPerPage' : 50, 'page' : i+2}).json()
            for dict in r['contacts']:
                title.append(dict['titles'][0])
                names.append(dict['fullName'])
                people_id.append(dict['id'])
        
        t.append(title)
        n.append(names)
        p.append(people_id)

df = pd.DataFrame(list(zip(comp[944],t,n,p)), columns =['companyName', 'Title', 'Employees', 'InsideView Contact ID'])


# In[16]:


df


# In[24]:


comp[944]


# In[22]:


company_name = []
emp_name = []
email = []
phone = []
corp_phone = []
twitter = []
facebook = []

for i in range(len(n)):
    name_list = n[i]
    index_list = p[i]
    
    for j in range(len(name_list)):
        name = name_list[j]
        new_contact_url = "https://api.insideview.com/api/v1/target/contact/{}"
        name_url = new_contact_url.format(index_list[j])
        response = requests.get(name_url,headers = headers).json()
        
        company_name.append(comp[944])
        
        if('fullName' in response.keys()):
            emp_name.append(response['fullName'])
        else:
            emp_name.append("")

        if('email' in response.keys()):
            email.append(response['email'])
        else:
            email.append("")
    
        if('phone' in response.keys()):
            phone.append(response['phone'])
        else:
            phone.append("")
    
        if('corporatePhone' in response.keys()):
            corp_phone.append(response['corporatePhone'])
        else:
            corp_phone.append("")
            
        if('twitterHandle' in response.keys()):
            twitter.append(response['twitterHandle'])
        else:
            twitter.append("")

        if('facebookHandle' in response.keys()):
            facebook.append(response['facebookHandle'])
        else:
            facebook.append("")
            
df1 = pd.DataFrame(list(zip(company_name,emp_name,email,phone,corp_phone,twitter,facebook)), columns =['companyName', 'Name', 'emailId', 'phoneNo', 'corporatePhoneNo', 'twitterHandle', 'facebookHandle'])


# In[23]:


df1


# In[ ]:




