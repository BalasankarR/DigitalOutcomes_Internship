#!/usr/bin/env python
# coding: utf-8

# Getting the Company Data from Fortune (We need to know the name of the companies to be able to do the rest of the scraping)

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


# In[2]:


driver = webdriver.Chrome(r'C:/Users/DELL-PC/OneDrive/Desktop/chromedriver.exe')    


# In[3]:


csv_file = open('fortune2021.csv', 'w', encoding='utf-8', newline='')
writer = csv.writer(csv_file)
writer.writerow(['rank','company','revenues','revenue % change', 'profits','profits % change','assets','market val','change in rank 1000','employees','change in rank 500'])

years_list = [2021]
s = "https://fortune.com/fortune500/{}/search/"


# In[4]:


for i in years_list:
    url = s.format(i)
    print(url)
    driver.get(url)

    # Page index used to keep track of where we are.
    index = 1
    while True:
        if index > 50:
            break

        try:
            print("Scraping Page number " + str(index))
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


# Using ForbesAPI to access the Forbes Global 2000 list and then getting the data in the form we need.

# In[5]:


headers = {
    "accept": "application/json, text/plain, */*",
    "referer": "https://www.forbes.com/global2000/",
    "user-agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36",
}

cookies = {
    "notice_behavior": "expressed,eu",
    "notice_gdpr_prefs": "0,1,2:1a8b5228dd7ff0717196863a5d28ce6c",
}

api_url = "https://www.forbes.com/forbesapi/org/global2000/2021/position/true.json?limit=2000"
response = requests.get(api_url, headers=headers, cookies=cookies).json()

sorted_list =  sorted(response["organizationList"]["organizationsLists"], key=lambda k: k["position"])
df = pd.DataFrame(sorted_list)


# In[6]:


df.drop(columns=['name','year','month','description','listUri','organization','visible','timestamp','version','imageExists','image'],inplace = True)
df.drop(columns=['revenueList','assetsList','profitList','employeesList','date','csfDisplayFields','industryLeader','employees','thumbnail'],inplace = True)
df.drop(columns=['squareImage', 'portraitImage','landscapeImage', 'premiumProfile', 'clients', 'ceoCompensations','naturalId'],inplace = True)
df.drop(columns = ['profits','assets','marketValue','profitsRank','assetsRank','marketValueRank','ceoTitle','yearFounded'],inplace = True)


# In[7]:


df.sort_values('revenue',ascending = False,inplace = True)


# In[8]:


df.drop(df[df.country != 'United States'].index,inplace = True)


# In[9]:


df.rename(columns={"organizationName": "Company", "industry": "Industry", "revenue" : "Revenue", "webSite" : "Website", "ceoName" : "CEO"},inplace = True)


# In[10]:


df.drop(columns = ['uri','rank','position','country','revenueRank'],inplace = True)


# In[11]:


df['Headquarters'] = (df['city'] + ', ' + df['state'])
df.drop(columns = ['city','state'],inplace = True)


# In[12]:


df.head()


# The Fortune Company Data is in the file fortune2021.csv, we load that data and we use the forbes data that we have to find the Companies for which the data we need is already in the Forbes data. The Missing Company data will be obtained by scraping their Wikipedia Page.

# In[13]:


df1 = pd.read_csv("fortune2021.csv")


# In[14]:


forbes_comp_list = df['Company'].to_list()
fortune_comp_list = df1['company'].to_list()


# In[15]:


for i in range(len(fortune_comp_list)):
    fortune_comp_list[i] = ''.join(e for e in fortune_comp_list[i] if e.isalnum())
for i in range(len(forbes_comp_list)):
    forbes_comp_list[i] = ''.join(e for e in forbes_comp_list[i] if e.isalnum())
forbes_comp_list = [string.replace("UnitedParcelService","UPS") for string in forbes_comp_list]    


# In[16]:


df['Name'] = forbes_comp_list
df1['Name'] = fortune_comp_list


# Finding the companies that are missing so that we can look at their Wikipedia Pages for the details.

# In[17]:


missing_companies = []
for i in range(len(fortune_comp_list)):
    temp = fortune_comp_list[i]
    flag = 0
    for j in range(len(forbes_comp_list)):
        if(forbes_comp_list[j].find(temp) != -1 or temp.find(forbes_comp_list[j]) != -1):
            flag = 1
            continue
    if(flag == 1):
        continue
    missing_companies.append((temp,i+1))  


# In[18]:


print(missing_companies)


# In[19]:


companies_list = df1['company'].tolist()
comp = []
for string in companies_list:
    new_s = string.replace(" ","_");
    comp.append(new_s)
url = "https://en.wikipedia.org/wiki/{}"
missing_ranks = []
for i in missing_companies:
    missing_ranks.append(i[1])   


# In[20]:


df2 = df[df.Name.isin(df1.Name)]
df2.to_csv("Company_Details.csv",index = False)


# In[21]:


time.sleep(5)
csv_file = open('Company_Details.csv', 'a', encoding='utf-8', newline='')
writer = csv.writer(csv_file)


# In[22]:


companies_list = df1['company'].tolist()
r_list = df1['revenues'].tolist()
revenues_list = []
for i in r_list:
    temp = i.replace('$','')
    revenues_list.append(temp.replace(',',''))
revenues_list = list(map(float,revenues_list))    


# Starting from here I am looking at their Wikipedia pages, there are a few rounds as not all companies have pages as https://en.wikipedia.org/wiki/{Name}. I will first try the name with underscore (i.e _), then with spaces, and then finally if both the above methods fail, i will go the Search page in Wikipedia, use the search phrase as the company name and try to filter out the Company's Page from the different results that we get using keywords like America, Company, Corporation, Inc. and a few others. After each run, we again compute the missing companies so wee can search for those companies alone. 

# In[23]:


url = "https://en.wikipedia.org/wiki/{}"

for i in missing_ranks:
    count = i-1
    comp_url = url.format(comp[i-1]) 
    
    row_dict = {}

    r = requests.get(html.unescape(comp_url).replace(" ",""))  
    soup = BeautifulSoup(r.content, 'html5lib') 
    
    noArticle = soup.findAll("div", attrs = {"class": "noarticletext mw-content-ltr"})
    multiplePages = soup.findAll("div", attrs = {"class": "tocright"})
    if(len(noArticle) != 0 or len(multiplePages) != 0):
        continue 
   
    label = soup.findAll("th", attrs = {"class": "infobox-label"})
    if(len(label) == 0):
        continue
    
    print(comp_url)
    label_list = []
    for j in range(len(label)):
        label_list.append(label[j].text)
    
    table = soup.findAll("td", attrs = {"class": "infobox-data"})
    table_list = []
    for j in range(len(table)):
        table_list.append(table[j].text)
        
    #Company
    row_dict['Company'] = companies_list[count]     
        
    #Industry
    flag = 0
    for j in range(len(label)):
        if(label_list[j] == "Industry" or label_list[j] == "Products"):
            flag = j
            break

    ind = table[j].find_all("a",attrs = {"href":re.compile(r'/wiki/')})    
    ind_list = []
    for j in range(len(ind)):
        ind_list.append(ind[j].text)
    
    if(flag == 0):
        row_dict['Industry'] = ""
    elif(len(ind_list) == 0):
        row_dict['Industry'] = table_list[flag]
    else:
        s = ""
        j = 0
        while(j < len(ind_list) - 1):
            s = s + ind_list[j] + ", "
            j = j + 1
        s = s + ind_list[j]
        row_dict['Industry'] = s    
    
    #Revenue
    row_dict['Revenue'] = revenues_list[count]
    
    #CEO
    for j in range(len(label)):
        if(label_list[j] == "Key people"):
            break
    
    s = ""
    for j in range(len(label)):
        if(label_list[j] == "Key people"):
            s = s + table_list[j]
            break
    lst = []
    lst1 = []
    if(s.find('(') != -1):
        s1 = s.split(')')
        for k in range(len(s1)):
            lst.append(s1[k])
        for k in lst:
            s1 = k.split('(')
            for j in range(len(s1)):
                lst1.append(s1[j])
    else:
        flag = 0
        for j in range(len(label)):
            if(label_list[j] == "Key people"):
                flag = 1
                break
        if(flag == 1):
            key = table_list[j]        
            lst1 = key.split(",")
        
    if(len(lst1) == 0):
        row_dict['CEO'] = "" 
    elif(len(lst1) == 1):
        lst1 = lst1[0].split(" ")
        for k in range(len(lst1)):
            if(lst1[k].find('CEO') != -1):
                break
        j = k-1
        while(1):
            if(lst1[j].find("President") == -1 and lst1[j].find("Chairman") == -1 and lst1[j].find(", ") == -1 and lst1[j].find("& ") == -1 and lst1[j].find("and") == -1):
                break
            elif(j == 0):
                break
            else:    
                j = j - 1;

        s = ""
        for k in range(j+1):
            s = s + lst1[k] + " "    
        row_dict['CEO'] = s
    else:
        for k in range(len(lst1)):
            if(lst1[k].find('CEO') != -1):
                break
        j = k-1
        while(1):
            if(lst1[j].find("President") == -1 and lst1[j].find("Chairman") == -1 and lst1[j].find(", ") == -1 and lst1[j].find("& ") == -1):
                break
            elif(j == 0):
                break
            else:    
                j = j - 1;
        row_dict['CEO'] = lst1[j] 
    
    #Website
    for j in range(len(label)):
        if(label_list[j] == "Website"):
            break
    s = table_list[j]
    s = 'https://' + s
    row_dict['Website'] = s   
    
    #Headquarters
    for j in range(len(label)):
        if(label_list[j] == "Headquarters"):
            break
    row_dict['Headquarters'] = table_list[j]

    writer.writerow(row_dict.values())

csv_file.close()


# In[24]:


df = pd.read_csv("Company_Details.csv")
df1 = pd.read_csv("fortune2021.csv")


# In[25]:


comp_list = df['Company'].to_list()
fortune_comp_list = df1['company'].to_list()
for i in range(len(fortune_comp_list)):
    fortune_comp_list[i] = ''.join(e for e in fortune_comp_list[i] if e.isalnum())
for i in range(len(comp_list)):
    comp_list[i] = ''.join(e for e in comp_list[i] if e.isalnum())
comp_list = [string.replace("UnitedParcelService","UPS") for string in comp_list] 


# In[26]:


missing_companies = []
for i in range(len(fortune_comp_list)):
    temp = fortune_comp_list[i]
    flag = 0
    for j in range(len(comp_list)):
        if(comp_list[j].find(temp) != -1 or temp.find(comp_list[j]) != -1):
            flag = 1
            continue
    if(flag == 1):
        continue
    missing_companies.append((temp,i+1))  


# In[27]:


print(missing_companies)


# In[28]:


csv_file = open('Company_Details.csv', 'a', encoding='utf-8', newline='')
writer = csv.writer(csv_file)


# In[29]:


missing_ranks = []
missing_ranks_copy = []
missing_companies_list = []
for i in missing_companies:
    missing_ranks.append(i[1])
    missing_ranks_copy.append(i[1])
    missing_companies_list.append(i[0])


# In[30]:


companies_list = df1['company'].tolist()
r_list = df1['revenues'].tolist()
revenues_list = []
for i in r_list:
    temp = i.replace('$','')
    revenues_list.append(temp.replace(',',''))
revenues_list = list(map(float,revenues_list)) 

url = "https://en.wikipedia.org/wiki/{}"

for a in range(len(missing_ranks)):
    i = missing_ranks[a]
    count = i-1
    comp_url = url.format(companies_list[i-1]) 
    
    row_dict = {}

    r = requests.get(html.unescape(comp_url).replace(" ","_"))  
    soup = BeautifulSoup(r.content, 'html5lib') 
    
    noArticle = soup.findAll("div", attrs = {"class": "noarticletext mw-content-ltr"})
    multiplePages = soup.findAll("div", attrs = {"class": "tocright"})
    if(len(noArticle) != 0 or len(multiplePages) != 0):
        continue    
    
    label = soup.findAll("th", attrs = {"class": "infobox-label"})
    if(len(label) == 0):
        continue
    
    print(comp_url)
    label_list = []
    for j in range(len(label)):
        label_list.append(label[j].text)
    
    table = soup.findAll("td", attrs = {"class": "infobox-data"})
    table_list = []
    for j in range(len(table)):
        table_list.append(table[j].text)
        
    #Company
    row_dict['Company'] = companies_list[count]     
        
    #Industry
    flag = 0
    for j in range(len(label)):
        if(label_list[j] == "Industry" or label_list[j] == "Products"):
            flag = j
            break

    ind = table[j].find_all("a",attrs = {"href":re.compile(r'/wiki/')})    
    ind_list = []
    for j in range(len(ind)):
        ind_list.append(ind[j].text)
    
    if(flag == 0):
        row_dict['Industry'] = ""
    elif(len(ind_list) == 0):
        row_dict['Industry'] = table_list[flag]
    else:
        s = ""
        j = 0
        while(j < len(ind_list) - 1):
            s = s + ind_list[j] + ", "
            j = j + 1
        s = s + ind_list[j]
        row_dict['Industry'] = s    
    
    #Revenue
    row_dict['Revenue'] = revenues_list[count]
    
    #CEO
    for j in range(len(label)):
        if(label_list[j] == "Key people"):
            break
    
    s = ""
    for j in range(len(label)):
        if(label_list[j] == "Key people"):
            s = s + table_list[j]
            break
    lst = []
    lst1 = []
    if(s.find('(') != -1):
        s1 = s.split(')')
        for k in range(len(s1)):
            lst.append(s1[k])
        for k in lst:
            s1 = k.split('(')
            for j in range(len(s1)):
                lst1.append(s1[j])
    else:
        flag = 0
        for j in range(len(label)):
            if(label_list[j] == "Key people"):
                flag = 1
                break
        if(flag == 1):
            key = table_list[j]        
            lst1 = key.split(",")
        
    if(len(lst1) == 0):
        row_dict['CEO'] = "" 
    elif(len(lst1) == 1):
        lst1 = lst1[0].split(" ")
        for k in range(len(lst1)):
            if(lst1[k].find('CEO') != -1):
                break
        j = k-1
        while(1):
            if(lst1[j].find("President") == -1 and lst1[j].find("Chairman") == -1 and lst1[j].find(", ") == -1 and lst1[j].find("& ") == -1 and lst1[j].find("and") == -1):
                break
            elif(j == 0):
                break
            else:    
                j = j - 1;

        s = ""
        for k in range(j+1):
            s = s + lst1[k] + " "    
        row_dict['CEO'] = s
    else:
        for k in range(len(lst1)):
            if(lst1[k].find('CEO') != -1):
                break
        j = k-1
        while(1):
            if(lst1[j].find("President") == -1 and lst1[j].find("Chairman") == -1 and lst1[j].find(", ") == -1 and lst1[j].find("& ") == -1):
                break
            elif(j == 0):
                break
            else:    
                j = j - 1;
        row_dict['CEO'] = lst1[j] 
    
    #Website
    for j in range(len(label)):
        if(label_list[j] == "Website"):
            break
    s = table_list[j]
    s = 'https://' + s
    row_dict['Website'] = s   
    
    #Headquarters
    for j in range(len(label)):
        if(label_list[j] == "Headquarters"):
            break
    row_dict['Headquarters'] = table_list[j]

    writer.writerow(row_dict.values())
    missing_ranks_copy.remove(missing_ranks[a])
    
csv_file.close()
missing_ranks = missing_ranks_copy
#missing_ranks.remove(151)


# In[31]:


df1 = pd.read_csv("fortune2021.csv")
companies = df1['company'].to_list()
companies = [s.replace(" ","+") for s in companies]


# In[32]:


csv_file = open('Company_Details.csv', 'a', encoding='utf-8', newline='')
writer = csv.writer(csv_file)


# In[33]:


l = []

URL = "https://en.wikipedia.org/w/index.php?search={}&title=Special%3ASearch&fulltext=1&ns0=1"
for i in missing_ranks:
    url = URL.format(companies[i-1])
    r = requests.get(url)

    soup = BeautifulSoup(r.content, 'html5lib')
    multiplePages = soup.findAll("div", attrs = {"class": "mw-search-result-heading"})
    
    res = soup.findAll("div", attrs = {"class": "searchresult"})
    res_list = []
    for i in range(len(res)):
        res_list.append(res[i].text)
    
    k = 21
    for j in range(len(res_list)):
        a = res_list[j].lower()
        lst = ['usa','america','corporation','inc.','company','firm','division']
        for c in lst:
            if(a.find(c) != -1):
                k = j
                break
        if(k == j):
            break
    s = multiplePages[k].find_all("a",attrs = {"href":re.compile(r'/wiki/')})
    s1 = s[0]['href'].split('/')
    l.append(s1[len(s1)-1])  


# In[34]:


companies_list = df1['company'].tolist()
r_list = df1['revenues'].tolist()
revenues_list = []
for i in r_list:
    temp = i.replace('$','')
    revenues_list.append(temp.replace(',',''))
revenues_list = list(map(float,revenues_list)) 

url = "https://en.wikipedia.org/wiki/{}"

for a in range(len(missing_ranks)):
    i = missing_ranks[a]-1
    count = i
    comp_url = url.format(l[a]) 
    
    row_dict = {}

    r = requests.get(comp_url)  
    soup = BeautifulSoup(r.content, 'html5lib') 
    
    noArticle = soup.findAll("div", attrs = {"class": "noarticletext mw-content-ltr"})
    multiplePages = soup.findAll("div", attrs = {"class": "tocright"})
    if(len(noArticle) != 0 or len(multiplePages) != 0):
        continue    
    
    label = soup.findAll("th", attrs = {"class": "infobox-label"})
    if(len(label) == 0):
        continue
    
    print(comp_url)
    label_list = []
    for j in range(len(label)):
        label_list.append(label[j].text)
    
    table = soup.findAll("td", attrs = {"class": "infobox-data"})
    table_list = []
    for j in range(len(table)):
        table_list.append(table[j].text)
        
    #Company
    row_dict['Company'] = companies_list[count]     
        
    #Industry
    flag = 0
    for j in range(len(label)):
        if(label_list[j] == "Industry" or label_list[j] == "Products"):
            flag = j
            break

    ind = table[j].find_all("a",attrs = {"href":re.compile(r'/wiki/')})    
    ind_list = []
    for j in range(len(ind)):
        ind_list.append(ind[j].text)
    
    if(flag == 0):
        row_dict['Industry'] = ""
    elif(len(ind_list) == 0):
        row_dict['Industry'] = table_list[flag]
    else:
        s = ""
        j = 0
        while(j < len(ind_list) - 1):
            s = s + ind_list[j] + ", "
            j = j + 1
        s = s + ind_list[j]
        row_dict['Industry'] = s    
    
    #Revenue
    row_dict['Revenue'] = revenues_list[count]
    
    #CEO
    for j in range(len(label)):
        if(label_list[j] == "Key people"):
            break
    
    s = ""
    for j in range(len(label)):
        if(label_list[j] == "Key people"):
            s = s + table_list[j]
            break
    lst = []
    lst1 = []
    if(s.find('(') != -1):
        s1 = s.split(')')
        for k in range(len(s1)):
            lst.append(s1[k])
        for k in lst:
            s1 = k.split('(')
            for j in range(len(s1)):
                lst1.append(s1[j])
    else:
        flag = 0
        for j in range(len(label)):
            if(label_list[j] == "Key people"):
                flag = 1
                break
        if(flag == 1):
            key = table_list[j]        
            lst1 = key.split(",")
        
    if(len(lst1) == 0):
        row_dict['CEO'] = "" 
    elif(len(lst1) == 1):
        lst1 = lst1[0].split(" ")
        for k in range(len(lst1)):
            if(lst1[k].find('CEO') != -1):
                break
        j = k-1
        while(1):
            if(lst1[j].find("President") == -1 and lst1[j].find("Chairman") == -1 and lst1[j].find(", ") == -1 and lst1[j].find("& ") == -1 and lst1[j].find("and") == -1):
                break
            elif(j == 0):
                break
            else:    
                j = j - 1;

        s = ""
        for k in range(j+1):
            s = s + lst1[k] + " "    
        row_dict['CEO'] = s
    else:
        for k in range(len(lst1)):
            if(lst1[k].find('CEO') != -1):
                break
        j = k-1
        while(1):
            if(lst1[j].find("President") == -1 and lst1[j].find("Chairman") == -1 and lst1[j].find(", ") == -1 and lst1[j].find("& ") == -1):
                break
            elif(j == 0):
                break
            else:    
                j = j - 1;
        row_dict['CEO'] = lst1[j] 
    
    #Website
    for j in range(len(label)):
        if(label_list[j] == "Website"):
            break
    s = table_list[j]
    s = 'https://' + s
    row_dict['Website'] = s   
    
    #Headquarters
    for j in range(len(label)):
        if(label_list[j] == "Headquarters"):
            break
    row_dict['Headquarters'] = table_list[j]

    writer.writerow(row_dict.values())
    
csv_file.close()


# In[35]:


df = pd.read_csv("Company_Details.csv")
df1 = pd.read_csv("fortune2021.csv")
forbes_comp_list = df['Company'].to_list()
fortune_comp_list = df1['company'].to_list()
for i in range(len(fortune_comp_list)):
    fortune_comp_list[i] = ''.join(e for e in fortune_comp_list[i] if e.isalnum())
for i in range(len(forbes_comp_list)):
    forbes_comp_list[i] = ''.join(e for e in forbes_comp_list[i] if e.isalnum())
forbes_comp_list = [string.replace("UnitedParcelService","UPS") for string in forbes_comp_list]


# In[36]:


df1['Name'] = fortune_comp_list
df['Name'] = forbes_comp_list
Fortune_Rev = df1['revenues'].to_list()
Fortune_Rank = df1['rank'].to_list()

revenue_list = []
rank_list = []
for i in forbes_comp_list:
    for j in range(len(fortune_comp_list)):
        if(fortune_comp_list[j] == i):
            revenue_list.append(Fortune_Rev[j])
            rank_list.append(Fortune_Rank[j])


# In[37]:


df['rev'] = revenue_list
df['rank'] = rank_list
df.sort_values('rank',inplace = True)
df.drop(columns = ['Revenue','Name'],inplace = True)
df.rename(columns={"rev": "Revenue (in Millions)", "rank": "Rank"},inplace = True)
df = df[['Rank','Company','Revenue (in Millions)','Industry','CEO','Website','Headquarters']]
df.to_csv("Company_Details.csv",index = False)

