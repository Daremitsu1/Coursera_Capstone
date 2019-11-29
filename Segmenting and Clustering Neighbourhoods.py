#!/usr/bin/env python
# coding: utf-8

# # Applied Data Science Capstone Assignment 2 :Segmenting and Clustering Neighborhoods in Toronto - Part 1
# 
# ## For this assignment, you will be required to explore and cluster the neighborhoods in Toronto.
# 1.Start by creating a new Notebook for this assignment.
# 2.Use the Notebook to build the code to scrape the following Wikipedia page, https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M, in order to obtain the data that is in the table of postal codes and to transform the data into a pandas dataframe like the one shown below:

# In[1]:


# Import necessary libraries

import requests
import lxml.html as lh
import pandas as pd


# In[2]:


url='https://en.wikipedia.org/wiki/List_of_postal_codes_of_Canada:_M'

#Create a handle, page, to handle the contents of the website
page = requests.get(url)

#Store the contents of the website under doc
doc = lh.fromstring(page.content)

#Parse data that are stored between <tr>..</tr> of HTML
tr_elements = doc.xpath('//tr')


# In[3]:


#Check the length of the first 12 rows
[len(T) for T in tr_elements[:12]]


# ### This means that there are 3 columns per row

# In[4]:


tr_elements = doc.xpath('//tr')

#Create empty list
col=[]
i=0

#For each row, store each first element (header) and an empty list
for t in tr_elements[0]:
    i+=1
    name=t.text_content()
    print ('%d:"%s"'%(i,name))
    col.append((name,[]))


# ### Creating Pandas DataFrame
# Each header is appended to a tuple along with an empty list.

# In[5]:


#Since out first row is the header, data is stored on the second row onwards
for j in range(1,len(tr_elements)):
    #T is our j'th row
    T=tr_elements[j]
    
    #If row is not of size 3, the //tr data is not from our table 
    if len(T)!=3:
        break
    
    #i is the index of our column
    i=0
    
    #Iterate through each element of the row
    for t in T.iterchildren():
        data=t.text_content() 
        #Check if row is empty
        if i>0:
        #Convert any numerical value to integers
            try:
                data=int(data)
            except:
                pass
        #Append the data to the empty list of the i'th column
        col[i][1].append(data)
        #Increment i for the next column
        i+=1


# In[6]:


# Check the length of each column. Ideally, they should all be the same
[len(C) for (title,C) in col]


# Creating the pandas data frame

# In[7]:


Dict={title:column for (title,column) in col}
df=pd.DataFrame(Dict)


# 3.To create the above dataframe:
# 
# The dataframe will consist of three columns: PostalCode, Borough, and Neighborhood
# 
# Only process the cells that have an assigned borough. Ignore cells with a borough that is Not assigned.
# 
# More than one neighborhood can exist in one postal code area. For example, in the table on the Wikipedia page, you will notice that M5A is listed twice and has two neighborhoods: Harbourfront and Regent Park. These two rows will be combined into one row with the neighborhoods separated with a comma as shown in row 11 in the above table.
# 
# If a cell has a borough but a Not assigned neighborhood, then the neighborhood will be the same as the borough. So for the 9th cell in the table on the Wikipedia page, the value of the Borough and the Neighborhood columns will be Queen's Park.
# 
# Clean your Notebook and add Markdown cells to explain your work and any assumptions you are making.
# In the last cell of your notebook, use the .shape method to print the number of rows of your dataframe.
# 4.Submit a link to your Notebook on your Github repository. (10 marks)
# 
# Note: There are different website scraping libraries and packages in Python. One of the most common packages is BeautifulSoup. Here is the package's main documentation page: http://beautiful-soup-4.readthedocs.io/en/latest/
# 
# The package is so popular that there is a plethora of tutorials and examples of how to use it. Here is a very good Youtube video on how to use the BeautifulSoup package: https://www.youtube.com/watch?v=ng2o98k983k
# 
# Use the BeautifulSoup package or any other way you are comfortable with to transform the data in the table on the Wikipedia page into the above pandas dataframe

# In[8]:


# Access the top 5 rows of the data frame 
df.head()


# Rearranging and renaming the columns

# In[9]:


df.columns = ['Borough', 'Neighbourhood','Postcode']

cols = df.columns.tolist()
cols

cols = cols[-1:] + cols[:-1]

df = df[cols]

df.head()


# Cleaning the messy string in the Borough column

# In[10]:


df = df.replace('\n',' ', regex=True)
df.head()


# Dropping all cells with a borough that is Not assigned

# In[11]:


df.drop(df.index[df['Borough'] == 'Not assigned'], inplace = True)

# Reset the index and dropping the previous index
df = df.reset_index(drop=True)

df.head(10)


# Combining Neighbourhoods based on similar Postcode and Borough

# In[12]:


df = df.groupby(['Postcode', 'Borough'])['Neighbourhood'].apply(','.join).reset_index()
df.columns = ['Postcode','Borough','Neighbourhood']
df.head(10)


# Removing any space in the start of the string

# In[13]:


df['Neighbourhood'] = df['Neighbourhood'].str.strip()


# Assigning Borough values to the Neignbourhood where vlaue is "Not assigned"

# In[14]:


df.loc[df['Neighbourhood'] == 'Not assigned', 'Neighbourhood'] = df['Borough']


# In[15]:


# Check if the Neighbourhood for Queen's Park changed 
df[df['Borough'] == 'Queen\'s Park']


# In[16]:


# Check the shape of the data frame
df.shape


# Save this file to a csv

# In[17]:


df.to_csv(r'df_can.csv')

