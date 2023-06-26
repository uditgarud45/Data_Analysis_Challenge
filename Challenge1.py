#!/usr/bin/env python
# coding: utf-8

# ### Challenge 
# Which EU countries has the highest average takings per customer?<br> Create and export a chart and a csv/ excel

# In[1]:


# EU countries
eu_countries = ['Austria', 'Belgium', 'Bulgaria', 'Croatia', 'Czech Republic', 'Denmark', 'Estonia', 'Finland', 'France', 
                'Germany', 'Greece', 'Hungary', 'Ireland', 'Italy', 'Latvia', 'Lithuania', 'Luxembourg', 'Malta', 'Netherlands', 
                'Poland', 'Portugal', 'Romania', 'Slovakia', 'Slovenia', 'Spain', 'Sweden']


# In[2]:


import pandas as pd


# In[3]:


payment = pd.read_csv('payment.csv')
payment.head()


# In[4]:


# group payments table by customer_id and sum amount as total_amount
customer_payments = payment[['customer_id', 'amount']].groupby('customer_id').agg(total_sales = ('amount', 'sum'))


# In[5]:


customer_payments.head()


# We will need some other tables to allow us to find out which country each customer is in

# In[6]:


address = pd.read_csv('address.csv')
address.head()


# In[7]:


city = pd.read_csv('city.csv')
city.head()


# In[8]:


country = pd.read_csv('country.csv')
country.head()


# In[9]:


customer = pd.read_csv('customer.csv')


# In[10]:


customer_payment_details_full = customer.merge(right = customer_payments,
                                         how = 'left', left_on = 'customer_id', right_on = 'customer_id'
                                         ).merge(right = address,
                                                how = 'left', left_on = 'address_id', right_on = 'address_id'
                                                ).merge(right = city,
                                                       how = 'left', left_on = 'city_id', right_on = 'city_id'
                                                       ).merge(right = country,
                                                              how = 'left', left_on = 'country_id', right_on = 'country_id')


# In[11]:


customer_payment_details_full.head()


# In[12]:


# column names of new table
customer_payment_details_full.columns


# In[13]:


customer_payment_details = customer_payment_details_full[['customer_id', 'address_id','activebool','total_sales','city_id','city','country_id','country']]
customer_payment_details.head()


# In[14]:


usefull_cols = ['total_sales', 'country', 'country_id']

customer_payment_details_grouped = customer_payment_details[usefull_cols].groupby('country_id')

avg_country_customer = customer_payment_details_grouped.agg({'total_sales':'mean', 'country':'max'})

avg_country_customer.sort_values('total_sales', ascending = False).head()


# In[15]:


# sort values
avg_country_customer = avg_country_customer.sort_values('total_sales')


# In[16]:


# selecting only EU contries 
avg_country_customer_eu = avg_country_customer[avg_country_customer['country'].isin(eu_countries)]


# In[17]:


# plotting Eu hbar
avg_country_customer_eu.plot.barh(x='country', y='total_sales', figsize = (8,8));


# In[18]:


avg_country_customer_eu = avg_country_customer_eu.sort_values('total_sales', ascending = False)
avg_country_customer_eu.head()


# In[19]:


# Export chart
# save the plot

plot = avg_country_customer_eu.plot.barh(x='country', y='total_sales', figsize = (8,8))
plot.set_title('avg_spend_by_eu_customer')
plot.get_figure().savefig('avg_eu_sales.pdf', format='pdf')


# # Export data to a CSV or Excel

# In[20]:


avg_country_customer_eu.to_csv('avg_country_customer_eu.csv', index = False)


# # Excel spreadsheet

# In[21]:


avg_country_customer_eu.to_excel('avg_country_customer_eu.xlsx', sheet_name = 'avg_country_customer_eu')


# In[ ]:




