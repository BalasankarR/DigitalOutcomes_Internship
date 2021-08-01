# Sales Intelligence Application

This project focuses on helping the salespersons to sell the products to the right clients at the right time using various pieces of data (it could include the financial data, news articles on the client to gauge if they would be willing to buy our product, the persona of the person to whom we sell, etc.) about the clients. 

## Collecting the Data

In this project, we focus on Companies that appear in the Fortune 500 list (you can look at the companies at https://fortune.com/fortune500/). For these companies, we initially collect their basic details like their Name, their Industry, their Revenue, CEO of the company, the company website, their social media handles and the Headquarters of the Company.  The free sources for this data include their Wikipedia Page, Forbes Global 2000 list 2021 which has free API access but we will only be able to use these data sources for the really big and well-known companies as not all companies have the data that we are interested in in their Wikipedia Webpages. And so, we make use of the InsideView API (which is a paid subscription) to get these details for the 1000 companies in the Fortune 500 list. Using the InsideView API, we will also be able to get the details about the Employees of the company (and so much more) which will be useful to us when we are trying to build up a contact list for these companies. This data is stored as a JSON object in our MongoDB database Fortune1000.

The next step was to get the details of the company employees so as to be able to build up the contact list. Our initial focus was on the Top-level Employees (i.e., the 
C-Suite officers). As we were using only a trial account of InsideView API, their personal details like phone numbers, email addresses and social media handles were redacted and thus we just compiled their names and their titles for the companies in a JSON file and stored it in our MongoDB database. We also have another collection CSuite_Neat that includes only a few of the well-known Positions like CEO, CFO, COO, etc. Also, we see that in the data available with InsideView, there are a few corner cases that needs attention, for example, we have that for different companies the same position is phrased differently (for ex., CEO, Chief Executive Officer, Executive Chairman and CEO are some of the different variations for the Title CEO), and sometimes we have 2 or more persons for the same Position in the same company. These cases have also been taken care of in the collection CSuite_Neat. 
 
The next step is to get the latest News Articles about the different companies and for this the Data Source that we use is the EventRegistry Website. It has all the news articles written all over the world since 2014, moreover it also has a simple API access and is thus a really good source for news articles. We can create a document in MongoDB for each company, loop for every 2 hrs (say) and get the articles written in the last 2 hrs and add it to the document corresponding to the company. In this way, we will be able to build our own database of news articles about our different companies and we can then be able to make use of this data to be able to find out the companies that satisfy certain triggers like CXO Changes or Mergers/Acquisitions in the last 6 months and others like this.

As a small example, we have collected the Titles of the 100 latest news articles for the different companies and stored it in our MongoDB database. We have also collected the data of the Top 100 Keywords used in a collection of 5000 news articles for the Top 10 companies in our list. The Top Keywords is a good indicator of what the company is all about and it could also be of use to the Salesperson (as these are sort of the buzz words to keep in mind about the client). We can also create visualization models like Wordcloud of the Top Keywords, which tells us at a glance the words and their importance. We also make use of these news titles to cluster our companies into a few buckets with the idea being that similar companies will fall in the same bucket and thus from a salesperson point of view, a sales strategy that works for one company in Bucket 0 is also highly likely to work for other companies in Bucket 0. The clustering Algorithm that we use is the KMeans Algorithm.

## API Access to the data

Now that we have collected the data for the companies, our task is then to make the data available to the Salesperson through the medium of APIs. We create the APIs using the flask library in Python. As we have a lot of companies in the database, we have a unique ID for each company which is used for all the other API calls and thus we firstly need an API that returns the ID of the input company / industry. There is another API that helps us query for the basic details of the company given its ID. It is also necessary for us to be able to filter the companies on the basis of either Industries or their revenues or their geographies (in this case since all companies are US based it is not useful but in general it maybe necessary). Therefore, we have also designed an API that enables. There is also an API that allows us to get the Employee details for the input company, the parameters are the Position and the ID of the company. We also need to be able to access the news articles that are available in our database. To enable this, we have an API that takes as parameter the ID of the company and returns the news articles that we have stored for that company. And finally, we need an API to access the Top Keywords associated with the different companies, this takes as parameters the ID of the company and the number of words that we want as input (10 is default and 100 is maximum). 


 


