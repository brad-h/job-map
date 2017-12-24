
# coding: utf-8

# In[1]:


get_ipython().magic('matplotlib inline')
import csv
import pandas as pd
import matplotlib.pyplot as plt

job_path = 'jobs.csv'
with open(job_path, 'r') as csvfile:
    csvreader = csv.reader(csvfile, dialect='excel')
    data = [{ 'zip': postal_code, 'company': company, 'position': position}
            for (postal_code, company, position) in csvreader]

jobs = pd.DataFrame(data)

zip_path = 'free-zipcode-database-Primary.csv'
with open(zip_path, 'r') as csvfile:
    csvreader = csv.DictReader(csvfile, dialect='excel')
    data = list(csvreader)
    zips = pd.DataFrame(data)

zips['Lat'] = pd.to_numeric(zips['Lat'])
zips['Long'] = pd.to_numeric(zips['Long'])
zips.head()

# Merge jobs.csv from JobMap.py and ZIP code database found online
data = pd.merge(jobs, zips, left_on='zip', right_on='Zipcode')
data.head()


# In[2]:

# Group jobs by surrounding cities/suburbs
data.groupby('City').describe()


# In[3]:

# Show average longitude and latitude for all jobs
data['Lat'].mean(), data['Long'].mean()

# In[4]:

# scatter plot all jobs in list grouped and sized by ZIP code
plt.scatter(data['Long'], data['Lat'], s=data.groupby('zip').count(), cmap='viridis')
