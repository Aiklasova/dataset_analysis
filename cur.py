import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Reading from .csv file, which we downloaded from kaggle.com
stat = pd.read_csv("who_suicide_statistics.csv")

# For different colors of plots
color = ['black', 'orange', 'red', 'orange', 'gray', 'yellow']

# This is to indicate age groups by numbers 0-5
age_c = \
    {
            '5-14 years': 0,
            '15-24 years': 1,
            '25-34 years': 2,
            '35-54 years': 3,
            '55-74 years': 4,
            '75+ years': 5
    }
# This is to indicate gender by number
gender_c = \
    {
        'female': 0,
        'male': 1
    }

stat['age_en'] = stat['age'].map(age_c)
stat['sex_en'] = stat['sex'].map(gender_c)

# We fill all fields with suicide numbers with zeros
stat.suicides_no.fillna(0, inplace=True)

en = \
    {
        0: '5-14 years',
        1: '15-24 years',
        2: '25-34 years',
        3: '35-54 years',
        4: '55-74 years',
        5: '75+ years'
    }
gen = \
    {
        0: 'female',
        1: 'male'
    }

# Creating new window (figure) with suicides in different age groups
suicide = stat.groupby('age_en')[['suicides_no']].sum()
plt.figure(figsize=(16, 8))
sns.barplot(x=suicide.index.map(en.get), y=suicide.suicides_no, palette=color)
plt.title("Suicides in different age groups")
plt.ylabel("Suicide")
plt.xlabel("Age group")

# Number of suicides by gender
m_suicide = stat[stat.sex_en == 0]['suicides_no'].values.sum()
f_suicide = stat[stat.sex_en == 1]['suicides_no'].values.sum()
dif = pd.DataFrame([m_suicide, f_suicide], index=['male', 'female'])
dif.head()
dif.plot(kind='pie', subplots=True, title="Suicides in gender")
plt.legend()

# New plot with sorting by age groups and years
suicide_data = stat.groupby(['year', 'age']).sum()['suicides_no'].reset_index()
plt.figure(figsize=(16, 8))
sns.swarmplot(
    x='year',
    y='suicides_no',
    hue='age',
    data=suicide_data,
    palette=color)
plt.title("Suicides in age groups and years")
plt.ylabel("Suicide")

# We show top-20 countries by suicide count
stat.groupby('country').sum().sort_values(
    by='suicides_no',
    ascending=False)[['suicides_no']][:20].plot(
    kind='pie',
    subplots=True,
    shadow=True,
    figsize=(16, 8),
    title='TOP-20 country')

# We group fields by year and suicides count
stat.groupby("year").sum().sort_values(
    by='year',
    ascending=True)[['suicides_no']].plot(
    kind='barh',
    figsize=(16, 8),
    color='green',
    title='Suicide in a year')

plt.show()
