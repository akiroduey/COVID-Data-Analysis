#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Mar 27 23:11:34 2020

@author: Akiro
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np

confirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
deaths = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
recovered = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
population = pd.read_csv('worldometers_population.csv')

confirmed_new = pd.concat([confirmed['Country/Region'], confirmed.iloc[:, -1]], axis = 1)
confirmed_new.columns = ['country', 'confirmed']
confirmed_new = confirmed_new.groupby('country').sum()
deaths_new = pd.concat([deaths['Country/Region'], deaths.iloc[:, -1]], axis = 1)
deaths_new.columns = ['country', 'deaths']
deaths_new = deaths_new.groupby('country').sum()
recovered_new = pd.concat([recovered['Country/Region'], recovered.iloc[:, -1]], axis = 1)
recovered_new.columns = ['country', 'recovered']
recovered_new = recovered_new.groupby('country').sum()

combined = pd.merge(confirmed_new, deaths_new, on = 'country')
combined = pd.merge(combined, recovered_new, on = 'country')
combined['active'] = combined['confirmed'] - combined['deaths'] - combined['recovered']
combined = combined.rename(index = {'US': 'United States', 'Korea, South': 'South Korea', 'Czechia': 'Czech Republic (Czechia)', 'Taiwan*': 'Taiwan', "Cote d'Ivoire": "Côte d'Ivoire"})
combined = pd.merge(combined, population, how = 'inner', on = 'country')
combined['percentage_confirmed'] = combined['confirmed'] / combined['population'] * 100
combined['percentage_active'] = combined['active'] / combined['population'] * 100
combined['percentage_deaths'] = combined['deaths'] / combined['population'] * 100
combined = combined.sort_values('country')
combined = combined.set_index('country')

plt.style.use('default')
fig, ax = plt.subplots(2, 3, dpi = 300)
fig.set_size_inches([11, 8.5])
plt.autoscale()
plt.tight_layout(7)

combined = combined.sort_values('confirmed')
combined_new = combined.tail(10)
ax[0,0].barh(combined_new.index, combined_new['confirmed'])
ax[0,0].set_xlabel('Confirmed Coronavirus Cases')

combined = combined.sort_values('active')
combined_new = combined.tail(10)
ax[0,1].barh(combined_new.index, combined_new['active'])
ax[0,1].set_xlabel('Active Coronavirus Cases')

combined = combined.sort_values('deaths')
combined_new = combined.tail(10)
ax[0,2].barh(combined_new.index, combined_new['deaths'])
ax[0,2].set_xlabel('Coronavirus Deaths')

combined = combined.sort_values('confirmed')
combined_new = combined.tail(10)
combined_new = combined_new.sort_values('percentage_confirmed')
ax[1,0].barh(combined_new.index, combined_new['percentage_confirmed'])
ax[1,0].set_xlabel('Total Coronavirus Cases as a' + '\n' + 'Percentage of the Total Population')

combined_new = combined_new.sort_values('percentage_active')
ax[1,1].barh(combined_new.index, combined_new['percentage_active'])
ax[1,1].set_xlabel('Active Coronavirus Cases as a' + '\n' + 'Percentage of the Total Population')

combined_new = combined_new.sort_values('percentage_deaths')
ax[1,2].barh(combined_new.index, combined_new['percentage_deaths'])
ax[1,2].set_xlabel('Coronavirus Deaths as a' + '\n' + 'Percentage of the Total Population')

fig.savefig('subplots.jpg')
plt.show()

combined_new['confirmed_millions'] = combined_new['confirmed'] / 1000000
combined_new['active_millions'] = combined_new['active'] / 1000000
combined_new['deaths_thousands'] = combined_new['deaths'] / 1000

fig2, ax2 = plt.subplots(2, 3, dpi = 300)
fig2.set_size_inches([11, 8.5])
plt.tight_layout(7)
sns.despine()

combined_new = combined_new.sort_values('confirmed', ascending = False)
sns.catplot(x = 'confirmed_millions', y = 'country', data = combined_new.reset_index(), kind = 'bar', palette = "Blues_r", ax = ax2[0,0])
ax2[0,0].set_xlabel('Confirmed Coronavirus Cases' + '\n' + '(Millions)')
ax2[0,0].set_ylabel('')
ax2[0,0].tick_params(axis='y', which='both',length=0)
plt.close(2)

combined_new = combined_new.sort_values('active', ascending = False)
sns.catplot(x = 'active_millions', y = 'country', data = combined_new.reset_index(), kind = 'bar', palette = "Blues_r", ax = ax2[0,1])
ax2[0,1].set_xlabel('Active Coronavirus Cases' + '\n' + '(Millions)')
ax2[0,1].set_ylabel('')
ax2[0,1].tick_params(axis='y', which='both',length=0)
plt.close(2)

combined_new = combined_new.sort_values('deaths', ascending = False)
sns.catplot(x = 'deaths_thousands', y = 'country', data = combined_new.reset_index(), kind = 'bar', palette = "Blues_r", ax = ax2[0,2])
ax2[0,2].set_xlabel('Coronavirus Deaths' + '\n' + '(Thousands)')
ax2[0,2].set_ylabel('')
ax2[0,2].tick_params(axis='y', which='both',length=0)
plt.close(2)

combined_new = combined_new.sort_values('percentage_confirmed', ascending = False)
sns.catplot(x = 'percentage_confirmed', y = 'country', data = combined_new.reset_index(), kind = 'bar', palette = "Blues_r", ax = ax2[1,0])
ax2[1,0].set_xlabel('Confirmed Coronavirus Cases as a' '\n' 'Percentage of Total Population (%)')
ax2[1,0].set_ylabel('')
ax2[1,0].tick_params(axis='y', which='both',length=0)
plt.close(2)

combined_new = combined_new.sort_values('percentage_active', ascending = False)
sns.catplot(x = 'percentage_active', y = 'country', data = combined_new.reset_index(), kind = 'bar', palette = "Blues_r", ax = ax2[1,1])
ax2[1,1].set_xlabel('Active Coronavirus Cases as a' '\n' 'Percentage of Total Population (%)')
ax2[1,1].set_ylabel('')
ax2[1,1].tick_params(axis='y', which='both',length=0)
plt.close(2)

combined_new = combined_new.sort_values('percentage_deaths', ascending = False)
sns.catplot(x = 'percentage_deaths', y = 'country', data = combined_new.reset_index(), kind = 'bar', palette = "Blues_r", ax = ax2[1,2])
ax2[1,2].set_xlabel('Coronavirus Deaths as a' '\n' 'Percentage of Total Population (%)')
ax2[1,2].set_ylabel('')
ax2[1,2].tick_params(axis='y', which='both',length=0)
plt.close(2)

fig2.savefig('subplots_seaborn.jpg')
plt.show()

combined_new = combined_new.sort_values('active', ascending = False)
combined = combined.sort_values('confirmed', ascending = False)

confirmed_new_2 = pd.concat([confirmed['Country/Region'], confirmed.iloc[:, -1]], axis = 1)
for i in np.arange(2, 8, 1):
    confirmed_new_2 = pd.concat([confirmed_new_2, confirmed.iloc[:, -i]], axis = 1)
confirmed_new_2.columns = ['country', 'confirmed -0', 'confirmed -1', 'confirmed -2', 'confirmed -3', 'confirmed -4', 'confirmed - 5', 'confirmed -6']
confirmed_new_2 = confirmed_new_2.groupby('country').sum()
confirmed_new_2 = confirmed_new_2.rename(index = {'US': 'United States', 'Korea, South': 'South Korea', 'Czechia': 'Czech Republic (Czechia)', 'Taiwan*': 'Taiwan', "Cote d'Ivoire": "Côte d'Ivoire"})
confirmed_new_2 = pd.merge(confirmed_new_2, population, how = 'inner', on = 'country')
change_names = ['change 1', 'change 2', 'change 3', 'change 4', 'change 5', 'change 6']
growth_names = ['growth 1', 'growth 2', 'growth 3', 'growth 4', 'growth 5', 'growth 6']
for i in range(6):
    confirmed_new_2[change_names[i]] = confirmed_new_2.iloc[:, i + 1] - confirmed_new_2.iloc[:, i + 2]
    confirmed_new_2[growth_names[i]] = confirmed_new_2[change_names[i]] /confirmed_new_2.iloc[:, i + 2] * 100
confirmed_new_2['growth average'] = confirmed_new_2[growth_names].mean(axis = 1)
confirmed_new_3 = confirmed_new_2.sort_values('confirmed -0').tail(10)
confirmed_new_3 = confirmed_new_3[['country', 'confirmed -0', 'growth 1', 'growth 2', 'growth 3', 'growth 4', 'growth 5', 'growth 6', 'growth average']]
confirmed_new_3.columns = ['country', 'confirmed', 'growth 1', 'growth 2', 'growth 3', 'growth 4', 'growth 5', 'growth 6', 'growth average']
confirmed_new_3 = confirmed_new_3.sort_values('growth average', ascending = False)

fig3, ax3 = plt.subplots(dpi = 300)
sns.despine()
sns.catplot(x = 'growth average', y = 'country', data = confirmed_new_3, kind = 'bar', palette = "Purples_r", ax = ax3)
ax3.set_xlabel('Average Daily Growth Rate %')
ax3.set_ylabel('')
ax3.set_title('Average Daily Growth Rate of Confirmed' + '\n' + 'Coronavirus Cases Over the Last 7 Days')
ax3.tick_params(axis='y', which='both',length=0)
plt.close(2)
plt.tight_layout()
fig3.savefig('growth_rate.jpg')
plt.show()