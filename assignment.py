import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from datetime import datetime
#from sklearn.preprocessing import StandardScaler

#load the excel file
excel  = pd.ExcelFile('./online_retail.xlsx')
#read its first sheet of the excel file
df = pd.read_excel(excel, sheet_name=0, header=0)
#convert it to csv 
df.to_csv("online_retail.csv", index=False)
#convert it to a dataframe by reading the csv
dt = pd.read_csv("./online_retail.csv", index_col=False)

#PHASE 2
#find number of rows and columns, missing values, data types
print("Rows and columns: \n", dt.shape)
print("Missing values: \n", dt.isnull().sum())
print("Data types in the dataset: \n", dt.dtypes)
#summary statistics to show any any anomalies like negative values or extremely high ones
print("Columns: \n",dt.columns)
print("Summary statistics: \n", dt.describe().round(2))


#visualizations

#barplot showing trnascactions per country (for countries: Germany, France, Norway, Netherlands, Ireland)
countries  = ['Germany', 'France', 'Norway', 'Netherlands', 'EIRE']
plt.figure(figsize = (18,7))
filtered_dt = dt[dt['Country'].isin(countries)]
number_of_transcactions = filtered_dt['Country'].value_counts()
country_barplot = plt.bar(number_of_transcactions.index, number_of_transcactions.values)
plt.title('Barplot of transcactions per country (Germany, France, Norway, Netherlands, EIRE) ')
plt.xticks(rotation = 90)
plt.show()


#barplot showing number of unique customers per country (Germany, France, Norway, Netherlands, Ireland)
countries  = ['Germany', 'France', 'Norway', 'Netherlands', 'EIRE']
plt.figure(figsize = (18,7))
filtered_dt = dt[dt['Country'].isin(countries)]
number_of_unique_customers = filtered_dt.groupby('Country')['CustomerID'].nunique()
country_barplot = plt.bar(number_of_unique_customers.index, number_of_unique_customers.values)
plt.title('Barplot of number of unique customers per country (Germany, France, Norway, Netherlands, EIRE)')
plt.xticks(rotation = 90)
plt.show()


#barplot showing average quantity per country (Germany, France, Norway, Netherlands, Ireland)
countries  = ['Germany', 'France', 'Norway', 'Netherlands', 'EIRE']
plt.figure(figsize = (18,7))
filtered_dt = dt[dt['Country'].isin(countries)]
average_quantity_per_country = filtered_dt.groupby('Country')['Quantity'].mean()
country_barplot = plt.bar(average_quantity_per_country.index, average_quantity_per_country.values)
plt.title('Barplot of average quantity per country (Germany, France, Norway, Netherlands, EIRE)')
plt.xticks(rotation = 90)
plt.show()



#barplot showing average unit price per country (Germany, France, Norway, Netherlands, Ireland)
countries  = ['Germany', 'France', 'Norway', 'Netherlands', 'EIRE']
plt.figure(figsize = (18,7))
filtered_dt = dt[dt['Country'].isin(countries)]
average_unit_price_per_country = filtered_dt.groupby('Country')['UnitPrice'].mean()
country_barplot = plt.bar(average_unit_price_per_country.index, average_unit_price_per_country.values)
plt.title('Barplot of average unit price per country (Germany, France, Norway, Netherlands, EIRE)')
plt.xticks(rotation = 90)
plt.show()


#boxplot showing unit price per country (Germany, France, Norway, Netherlands, Ireland)
countries  = ['Germany', 'France', 'Norway', 'Netherlands', 'EIRE']
plt.figure(figsize = (18,7))
filtered_dt = dt[dt['Country'].isin(countries)]
sns.boxplot(x='Country', y='UnitPrice', data=filtered_dt)
plt.title('Boxplot of unit price per country (Germany, France, Norway, Netherlands, EIRE)')
plt.xticks(rotation = 90)
plt.show()

