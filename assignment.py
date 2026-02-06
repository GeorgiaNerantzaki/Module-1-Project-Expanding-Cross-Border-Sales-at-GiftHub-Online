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

#PHASE 3
#subplots showing quantity accross time per country (Germany, France, Norway, Netherlands, Ireland)
dt['InvoiceDate']= pd.to_datetime(dt['InvoiceDate']).dt.normalize()
all_dates = pd.date_range(start = dt['InvoiceDate'].min(),end = dt['InvoiceDate'].max(), freq= 'D' )
fig, axes = plt.subplots(nrows=5, ncols=1, sharex=True, figsize = (18,20))
fig.suptitle('Cancellations across tie by Country (Germany, France, Norway, Netherlands, Ireland)', fontsize=16)
for ax,country in zip(axes, countries):
    country_dt = dt[dt['Country'] == country]
    ts = country_dt.groupby('InvoiceDate')['Quantity'].sum().reindex(all_dates, fill_value=0)
    time_series_plot = ax.plot(ts.index, ts.values)
    ax.set_ylabel('Cancellations')
    ax.set_title(country)
plt.show()

#heatmap showing sales by country and category (using Description as category)
countries  = ['Germany', 'France', 'Norway', 'Netherlands', 'EIRE']
dt['Sales'] = dt['Quantity'] * dt['UnitPrice']
filtered_dt = dt[dt['Country'].isin(countries)]
top_categories = filtered_dt.groupby('Description')['Sales'].sum().nlargest(10).index
heatmap_data = filtered_dt[filtered_dt['Description'].isin(top_categories)]
plt.figure(figsize = (18,7))
pivot_table = heatmap_data.pivot_table(values='Sales', index='Description', columns='Country', aggfunc='sum', fill_value=0)
sns.heatmap(pivot_table, annot=True, fmt=".1f", cmap="YlGnBu")
plt.title('Heatmap of Sales by Country and Category (Top 10 Products)')
plt.show()


#scatter plot for cancellation frequency by country
countries  = ['Germany', 'France', 'Norway', 'Netherlands', 'EIRE']
filtered_dt = dt[dt['Country'].isin(countries)].copy()
filtered_dt['Sales'] = filtered_dt['Quantity'] * filtered_dt['UnitPrice']
filtered_dt['InvoiceNo'] = filtered_dt['InvoiceNo'].astype(str)

stats = filtered_dt.groupby('Country').agg(
    TotalRevenue=('Sales', 'sum'),
    TotalInvoices=('InvoiceNo', 'nunique'),
    CancelledInvoices=('InvoiceNo', lambda x: x[x.str.startswith('C')].nunique()),
    SuccessfulInvoices=('InvoiceNo', lambda x: x[~x.str.startswith('C')].nunique())
).reset_index()
stats['CancellationRate'] = stats['CancelledInvoices'] / stats['TotalInvoices']

plt.figure(figsize = (18,7))
sizes = (stats['TotalRevenue'] / stats['TotalRevenue'].max()) * 2000 + 100
plt.scatter(stats['SuccessfulInvoices'], stats['CancellationRate'], s=sizes, color='purple', alpha=0.6)
for i, row in stats.iterrows():
    plt.text(row['SuccessfulInvoices'], row['CancellationRate'], row['Country'], fontsize=12)
plt.axvline(x=stats['SuccessfulInvoices'].mean(), color='blue', linestyle='--', label='Avg Order Volume')
plt.axhline(y=stats['CancellationRate'].mean(), color='red', linestyle='--', label='Avg Cancellation Rate')
plt.title('Scatter plot of cancellation frequency vs order volume (Size = Revenue)')
plt.xlabel('Total unique successful InvoiceNo')
plt.ylabel('% of InvoiceNo starting with \'C\'')
plt.legend()
plt.show()
