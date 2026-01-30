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
#find number of rows and columns, missing values, data types
print("Rows and columns: \n", dt.shape)
print("Missing values: \n", dt.isnull().sum())
print("Data types in the dataset: \n", dt.dtypes)
#summary statistics to show any any anomalies like negative values or extremely high ones
print("Columns: \n",dt.columns)
print("Summary statistics: \n", dt.describe())


#finding outliers 
plt.figure(figsize=(30,20))
quantity_boxplot = plt.boxplot(dt['Quantity'])
plt.title('Boxplot of quantity ')
plt.show()
plt.figure(figsize=(30,20))
unit_price_boxplot = plt.boxplot(dt['UnitPrice'])
plt.title('Boxplot of quantity ')
plt.show()
#barplot with country
plt.figure(figsize=(30,20))
number_of_transcactions = dt['Country'].value_counts()
print("number of transcactions: ", number_of_transcactions)
country_barplot = plt.bar(number_of_transcactions.index, number_of_transcactions.values)
plt.title('Barplot of country ')
country_barplot.xticks(rotate = 90)
plt.show()
