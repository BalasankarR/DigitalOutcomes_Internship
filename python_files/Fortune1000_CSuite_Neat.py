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


# In[ ]:


headers = {
    "clientID" : "1g0195d428oi204f274g",
    "clientSecret" : "efbr0e5jlpjuj5ibn2ugfmpi7b573uqsn1h6voi1rmn1d5p8t2kk9o2e38aj",
    "grantType" : "cred",
}

api_url = "https://login.insideview.com/Auth/login/v1/token.json"
response = requests.post(api_url, data = {'clientId' : '1g0195d428oi204f274g', 'clientSecret' : 'efbr0e5jlpjuj5ibn2ugfmpi7b573uqsn1h6voi1rmn1d5p8t2kk9o2e38aj','grantType' : 'cred'}).json()
access_token = response["accessTokenDetails"]["accessToken"]


# In[ ]:


headers = {
    "Accept": "application/json",
    "accessToken" : access_token,
}


# In[ ]:


api_url = "https://api.insideview.com/api/v1/target/companies"
id = []
comp = []
for i in range(2):
    response = requests.post(api_url, headers=headers, data = {"fortuneRanking" : "fortune1000","resultsPerPage" : 500,'page' : i+1}).json()
    companies_id_list = response["companies"]
    for j in companies_id_list:
        id.append(int(j['companyId']))
        comp.append(j['name'])


# In[ ]:


contact_list_url = "https://api.insideview.com/api/v1/target/contacts"
t = []
n = []

for i in range(len(comp)):
    title = []
    names = []
    
    index = id[i]
    name = comp[i]
    
    r = requests.post(contact_list_url,headers = headers,data = {'jobLevels' : ['1'], 'companyName' : name, 'fortuneRanking' : 'fortune1000', 'resultsPerPage' : 50}).json()
    
    if(int(r['totalResults']) == 0):
        t.append(title)
        n.append(names)
        continue
    
    for dict in r['contacts']:
        title.append(dict['titles'][0])
        names.append(dict['fullName'])

    no = int(r['totalResults'])//50
    
    if(int(r['totalResults'])%50 == 0):
        no = no - 1
        
    if(no == 0):
        t.append(title)
        n.append(names)
    else:
        for i in range(no):
            r = requests.post(contact_list_url,headers = headers,data = {'jobLevels' : ['1'], 'companyName' : name, 'fortuneRanking' : 'fortune1000', 'resultsPerPage' : 50, 'page' : i+2}).json()
            for dict in r['contacts']:
                title.append(dict['titles'][0])
                names.append(dict['fullName'])
        t.append(title)
        n.append(names)

df = pd.DataFrame(list(zip(comp,t,n)), columns =['companyName', 'Title', 'Employees'])


# In[3]:


emp = df['Employees'].to_list()
titles = df['Title'].to_list()
e = []
t = []
for i in range(len(emp)):
    e.append(ast.literal_eval(emp[i]))
    t.append(ast.literal_eval(titles[i])) 


# In[4]:


comp = df['companyName'].to_list()
df1 = pd.read_csv("Fortune1000_BasicDetails.csv")
comp_ranked = df1['Company'].to_list()
rank = []
for s in comp:
    for i in range(len(comp_ranked)):
        if(s == comp_ranked[i]):
            rank.append(i+1)
            break


# In[25]:


ceo = [re.compile(r'.*Chief Executive Officer'), re.compile(r'.*CEO$')]
cfo = [re.compile(r'.*Chief Financial Officer'), re.compile(r'.*CFO$')]
coo = [re.compile(r'.*Chief Operating Officer'), re.compile(r'.*COO$')]
cao = [re.compile(r'.*Chief Accounting Officer'), re.compile(r'.*CAO$')]
cto = [re.compile(r'.*Chief Technical Officer'), re.compile(r'.*CTO$')]
cmo = [re.compile(r'.*Chief Managing Officer'), re.compile(r'.*CMO$')]

clo = [re.compile(r'.*Chief Legal Officer'), re.compile(r'.*CLO$')]
cio = [re.compile(r'.*Chief Information Officer'), re.compile(r'.*CIO$')]
cco = [re.compile(r'.*Chief Communications Officer'), re.compile(r'.*CCO$')]
cdo = [re.compile(r'.*Chief Development Officer'), re.compile(r'.*CDO$')]
ctecho = [re.compile(r'.*Chief Technology Officer')]
cmarko = [re.compile(r'.*Chief Marketing Officer')]
cso = [re.compile(r'.*Chief Sales Officer')]

ciso = [re.compile(r'.*Chief Information Security Officer'), re.compile(r'.*CISO$')]
chro = [re.compile(r'.*Chief Human Resource Officer'), re.compile(r'.*Chief Human Resources Officer'), re.compile(r'.*CHRO$')]
ccompo = [re.compile(r'.*Chief Compliance Officer')]


efo_titles = []
efo_employees = []

for j in range(len(e)):
    eo = []
    ename = []

    fo = []
    fname = []

    oo = []
    oname = []

    ao = []
    aname = []

    to = []
    tname = []

    mo = []
    mname = []
    
    lo = []
    lname = []

    io = []
    iname = []

    co = []
    cname = []

    do = []
    dname = []

    techo = []
    techname = []

    marko = []
    markname = []
    
    so = []
    sname = []
    
    iso = []
    isname = []

    hro = []
    hrname = []
    
    compo = []
    compname = []
    
    t_0 = t[j]
    e_0 = e[j]

    for i in range(len(t_0)):
        title = t_0[i]
        for s in ceo:
            if(s.match(title)):
                eo.append(title)
                ename.append(e_0[i])
        
        for s in cfo:
            if(s.match(title)):
                fo.append(title)
                fname.append(e_0[i])
        
        for s in coo:
            if(s.match(title)):
                oo.append(title)
                oname.append(e_0[i])
                
        for s in cao:
            if(s.match(title)):
                ao.append(title)
                aname.append(e_0[i])
                
        for s in cto:
            if(s.match(title)):
                to.append(title)
                tname.append(e_0[i])
        
        for s in cmo:
            if(s.match(title)):
                mo.append(title)
                mname.append(e_0[i])
                
        for s in clo:
            if(s.match(title)):
                lo.append(title)
                lname.append(e_0[i])
        
        for s in cio:
            if(s.match(title)):
                io.append(title)
                iname.append(e_0[i])
        
        for s in cco:
            if(s.match(title)):
                co.append(title)
                cname.append(e_0[i])
                
        for s in cdo:
            if(s.match(title)):
                do.append(title)
                dname.append(e_0[i])
                
        for s in ctecho:
            if(s.match(title)):
                techo.append(title)
                techname.append(e_0[i])
        
        for s in cmarko:
            if(s.match(title)):
                marko.append(title)
                markname.append(e_0[i])
                
        for s in cso:
            if(s.match(title)):
                so.append(title)
                sname.append(e_0[i])
                
        for s in ciso:
            if(s.match(title)):
                iso.append(title)
                isname.append(e_0[i])
        
        for s in chro:
            if(s.match(title)):
                hro.append(title)
                hrname.append(e_0[i])
                
        for s in ccompo:
            if(s.match(title)):
                compo.append(title)
                compname.append(e_0[i])
                
    ti = [i for i in eo]
    em = [i for i in ename]
    
    for i in range(len(fo)):
        ti.append(fo[i])
        em.append(fname[i])
        
    for i in range(len(oo)):
        ti.append(oo[i])
        em.append(oname[i])
    
    for i in range(len(ao)):
        ti.append(ao[i])
        em.append(aname[i])
        
    for i in range(len(to)):
        ti.append(to[i])
        em.append(tname[i])
        
    for i in range(len(mo)):
        ti.append(mo[i])
        em.append(mname[i])
        
    for i in range(len(lo)):
        ti.append(lo[i])
        em.append(lname[i])
        
    for i in range(len(io)):
        ti.append(io[i])
        em.append(iname[i])
        
    for i in range(len(co)):
        ti.append(co[i])
        em.append(cname[i])
    
    for i in range(len(do)):
        ti.append(do[i])
        em.append(dname[i])
        
    for i in range(len(techo)):
        ti.append(techo[i])
        em.append(techname[i])
        
    for i in range(len(marko)):
        ti.append(marko[i])
        em.append(markname[i])
        
    for i in range(len(so)):
        ti.append(so[i])
        em.append(sname[i])
        
    for i in range(len(iso)):
        ti.append(iso[i])
        em.append(isname[i])
        
    for i in range(len(hro)):
        ti.append(hro[i])
        em.append(hrname[i])
        
    for i in range(len(compo)):
        ti.append(compo[i])
        em.append(compname[i])
    
    efo_titles.append(ti)
    efo_employees.append(em)


# In[26]:


from collections import defaultdict

dict1 = defaultdict(list)

details_1 = []
for i in range(1000):
    l_1 = efo_titles[i]
    l_2 = efo_employees[i]
    
    dict1 = {}
    
    for j in range(len(efo_titles[i])):
        a = l_1[j].replace('.','')
        
        if(not(a in dict1.keys())):
            dict1[a] = []
        if(not(l_2[j] in dict1[a])):
            dict1[a].append(l_2[j])

    dict1['Rank'] = rank[i]
    dict1['Name'] = comp[i]
    details_1.append(dict1)

out_file = open("CSuite_Neat.json", "w") 
json.dump(details_1, out_file, indent = 6) 
out_file.close()


# ### This is to have all the Details of the different Job Titles we have obtained from InsideView in a json file (as a dictionary of {Title : Employee_Name, 'Rank' : Fortune1000_rank, 'Name' : Company_Name})

# In[27]:


details = []
for i in range(1000):
    dict1 = {t[i][j] : e[i][j] for j in range(len(t[i]))}
    dict1['Rank'] = rank[i]
    dict1['Name'] = comp[i]
    details.append(dict1)

out_file = open("CSuite_All.json", "w") 
json.dump(details, out_file, indent = 6) 
out_file.close()

