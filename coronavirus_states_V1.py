#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 19:28:46 2020

@author: Akiro
"""

# import packages
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from matplotlib.dates import DateFormatter

# read csv files
data1 = pd.read_csv('https://raw.githubusercontent.com/nytimes/covid-19-data/master/us-states.csv', parse_dates = ['date'])
data2 = pd.read_csv('population_data_us.csv') 

#extract most recent date
data3 = data1.sort_values('date', ascending = False)
data3 = data3.groupby('state').head(1)

#sort and extract coronavirus columns
data3 = data3.sort_values('cases')
data3 = data3[['state', 'cases', 'deaths']]

# extract population columns and rename
data4 = data2[['State', 'Pop']]
data4.columns = ['state', 'population']

#merge coronavirus dataframe with population dataframe and calculate percentage infected
data5 = pd.merge(data3, data4, on = 'state')
data5['percentage'] = data5['cases'] / data5['population'] * 100

#sort by number of coronavirus cases
data5 = data5.sort_values('cases')

##create a plot for all states based on coronavirus cases
#fig, ax = plt.subplots(dpi = 300)
#fig.set_size_inches([11, 8.5])
#ax.barh(data5['state'], data5['cases'])
#ax.set_xlabel('Total Number of Coronavirus Cases')
#ax.set_title('Coronavirus Cases in the United States')
#plt.tight_layout()
#fig.savefig('cases_us.jpg')
#plt.show()

#sort by percentage infected
data5 = data5.sort_values('percentage')

##create a plot for all states based on percentage infected
#fig2, ax2 = plt.subplots(dpi = 300)
#fig2.set_size_inches([11, 8.5])
#ax2.barh(data5['state'], data5['percentage'])
#ax2.set_xlabel('Percentage of Total Population (%)')
#ax2.set_title('Coronavirus Cases in the United States by Percentage of Total Population')
#plt.tight_layout()
#fig2.savefig('percentage_us.jpg')
#plt.show()

#extract massachusetts data and sort by date
data8 = data1[data1.state == 'Massachusetts']
data8 = data8.sort_values('date')
data8['new'] = data8['cases'].diff()

#create a plot for massachusetts
#fig4, ax4 = plt.subplots(dpi = 300)
#plt.plot(data8['date'], data8['cases'], linewidth = 3)
#ax4.set_xlabel('Date')
#ax4.set_ylabel('Confirmed Coronavirus Cases')
#ax4.set_title('Confirmed Coronavirus Cases in Massachusetts')
#plt.xticks(rotation = 45)
#plt.close(2)
#plt.tight_layout()
#fig4.savefig('massachusetts.png')
#plt.show()

fig6, ax6 = plt.subplots(dpi = 300)
ax6.bar(data8['date'].tail(30), data8['new'].tail(30), color = '#34ACCD')
ax6.set_ylabel('Daily Coronavirus Cases')
ax6.set_title('Daily Coronavirus Cases in Massachusetts')
ax6.xaxis.set_major_formatter(DateFormatter('%m/%d'))
plt.close(2)
plt.tight_layout()
fig6.savefig('massachusetts_daily.jpg')
plt.show()

#sort by coronavirus cases and filter the top 10
data5 = data5.sort_values('cases', ascending = False)
data6 = data5.head(10)

#sort by date and extract the last 7 days for each state
data9 = data1.sort_values('date', ascending = False)
data9 = data9.groupby('state').head(7)
data9 = data9.sort_values('cases')
data9 = data9[['date', 'state', 'cases']]
data9 = pd.merge(data9, data4, on = 'state')

#make each date into a new column and relabel the columns
data9 = data9.pivot(index = 'state', columns = 'date', values = 'cases')
data9 = data9.reset_index()
data9.columns = ['state', 'confirmed -6', 'confirmed -5', 'confirmed -4', 'confirmed -3', 'confirmed -2', 'confirmed - 1', 'confirmed -0']
change_names = ['change 1', 'change 2', 'change 3', 'change 4', 'change 5', 'change 6']
growth_names = ['growth 1', 'growth 2', 'growth 3', 'growth 4', 'growth 5', 'growth 6']

#calculate the daily growth rate for each of the past 7 days
for i in range(6):
    data9[change_names[i]] = data9.iloc[:, 7-i] - data9.iloc[:, 6-i]
    data9[growth_names[i]] = data9[change_names[i]] /data9.iloc[:, 6-i] * 100

#calculate the average growth rate over the past week
data9['growth average'] = data9[growth_names].mean(axis = 1)
data9 = pd.merge(data9, data4, on = 'state')

#calculate the percentage of coronavirus cases and sort by total cases
data9['percentage'] = data9['confirmed -0'] / data9['population'] * 100
data9 = data9.sort_values('confirmed -0', ascending = False)

#extract the top 10 cases and sort by growth rate
data9 = data9.head(10)
data9 = data9.sort_values('growth average', ascending = False)


#create a plot for top 10 coronavirus cases and growth rate
fig3, ax3 = plt.subplots(2, 1, dpi = 300)
fig3.set_size_inches([8.5, 11])
sns.despine()

data6['cases_thousands'] = data6['cases'] / 1000

#plot for coronavirus cases
sns.catplot(y = 'state', x = 'cases_thousands', data = data6, kind = 'bar', palette = "Blues_r", ax = ax3[0])
ax3[0].set_xlabel('Confirmed Coronavirus Cases (Thousands)')
ax3[0].set_ylabel('')
ax3[0].set_title('Top 10 States Based on Total Coronavirus Cases')
ax3[0].tick_params(axis='y', which='both',length=0)
plt.close(2)

#plot for growth rate
sns.catplot(x = 'growth average', y = 'state', data = data9, kind = 'bar', palette = "Purples_r", ax = ax3[1])
ax3[1].set_xlabel('Average Daily Growth Rate %')
ax3[1].set_ylabel('')
ax3[1].set_title('Average Daily Growth Rate of Confirmed' + '\n' + 'Coronavirus Cases Over the Last 7 Days')
ax3[1].tick_params(axis='y', which='both',length=0)
plt.close(2)

#save plot
plt.tight_layout(3)
fig3.savefig('subplots.jpg')
plt.show()

#calculate deaths per capita
data10 = data5.copy()
data10['percentage_deaths'] = data5['deaths'] / data5['population'] * 1000
data10 = data10.sort_values('percentage_deaths', ascending = False)
data10 = data10.head(10)

#sort by percentage and filter for top 10
data5 = data5.sort_values('percentage', ascending = False)
data7 = data5.head(10)

#create plot for percentage infected and deaths per capita
fig5, ax5 = plt.subplots(2, 1, dpi = 300, figsize = (8.5, 11))
sns.despine()

#plot for percentage infected
sns.catplot(y = 'state', x = 'percentage', data = data7, kind = 'bar', palette = "Greens_r", ax = ax5[0])
ax5[0].set_xlabel('Percentage of Population Infected (%)')
ax5[0].set_ylabel('')
ax5[0].set_title('Top 10 States Based on Percentage ' + '\n' + 'of Population Infected with Coronavirus')
ax5[0].tick_params(axis='y', which='both',length=0)
plt.close(2)

#plot for deaths per capita
sns.catplot(x = 'percentage_deaths', y = 'state', data = data10, kind = 'bar', palette = "Reds_r", ax = ax5[1])
ax5[1].set_xlabel('Deaths Per 1,000 People')
ax5[1].set_ylabel('')
ax5[1].set_title('Deaths Per 1,000 People in the United States')
ax5[1].tick_params(axis='y', which='both',length=0)
plt.close(2)

#save plot
plt.tight_layout(3)
fig5.savefig('deaths_per_capita.jpg')
plt.show()

##print data table
#print(data5)