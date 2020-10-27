# %%
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests as req
import pymongo
import numpy as np
import time
# %%
Ramen1 = pd.read_csv('Ramen_Ratings_1.csv')
Ramen2 = pd.read_csv('Ramen_Ratings_2.csv')
# %%


def id_cleaner(x):
    try:
        x = x.split('/')
        x = x[0]
        x = int(x)
    except:
        pass
    return x


Ramen1 = Ramen1[['Review #', 'Top Ten']]
Ramen1['Review #'] = Ramen1['Review #'].apply(id_cleaner)
# %%
Ramen2['ID'] = Ramen2['ID'].apply(id_cleaner)
# %%
Full_Ramen = Ramen2.merge(Ramen1, left_on='ID',
                          right_on='Review #', how='outer')
# %%
Full_Ramen = Full_Ramen.rename({
    'ID': 'Review_ID'
}, axis=1)
Full_Ramen.drop('Review #', inplace=True, axis=1)

#    Original scraping was done in about four passes, each one targeting rows which were missed by previous passes.
# I would have stuck with this structure except that some of the methods resulted is some very weird 'bycatch'
# resulting in the necessity to scrape from scratch (ugh).
#
#     I took this as an opportunity to marry all scrape methods into a single pass with minimal redundant HTML requests.
#
#   I looped through one method completely before moving on to the next so that I could arrange them from least to most
# likely to have bycatch. It feels very inefficient to me but is necessary prevent bycatch breaking the loop before it can move onto a
# better method
Full_Ramen['Blurb'] = 'Scrape'
#%%
for index, row in Full_Ramen.iterrows():
    if row['Blurb'] == 'Scrape':
        # There are two different URL formats.  We could correct this in the DF but went this route instead.
        try:
            URL = row['URL']
            html = req.get(URL).text
            ramen_soup = bs(html, 'html.parser')
        except:
            try:
                URL = 'https://' + row['URL']
                html = req.get(URL).text
                ramen_soup = bs(html, 'html.parser')
            except:
                Full_Ramen.loc[index, 'Blurb'] = "Issue with URL"
        alphabet_soup = ramen_soup.find_all('p')
        #    First pass, tries to find the <p> of interest based on a common opener 'Finished (click to enlarge).
        # Simply using '(' has some weird bycatch so I was much more specific.
        try:
            if Full_Ramen.loc[index, 'Blurb'] == 'Scrape':
                for i in alphabet_soup:
                    try:
                        x = i.text
                        x = x.split('(click to enlarge)')
                        if x[0] == 'Finished ':
                            Full_Ramen.loc[index, 'Blurb'] = i.text
                            print('---First Pass FTW!!')
                            print(i.text)
                            break
                    except:
                        pass
            # Second Pass, exploiting the large portion of pages where the <p> of interest begins with 'Finished (click image to enlarge)'
            if Full_Ramen.loc[index, 'Blurb'] == 'Scrape':
                for i in alphabet_soup:
                    try:
                        x = i.text
                        x = x.split('(click image to enlarge)')
                        if x[0] == 'Finished ':
                            Full_Ramen.loc[index, 'Blurb'] = i.text
                            print('---Second pass with the assist!!!')
                            print(i.text)
                            break
                    except:
                        pass
            #    Third pass the <p> of interest often ends with a long barcode,
            # and where there is no barcode it often ends with '_ out of 5 stars.' or '_ stars.'
            if Full_Ramen.loc[index, 'Blurb'] == 'Scrape':
                for i in alphabet_soup:
                        try:
                            x = i.text
                            x = x.split(' ')
                            x[-1] = x[-1].replace('.', '')
                            x[-1] = x[-1].replace('<', '')
                            x[-1] = x[-1].replace('>', '')
                            x[-1] = x[-1].replace(' ', '')
                            if x[-1] == 'stars':
                                print('---Third pass with the spare!!')
                                print(i.text)
                                Full_Ramen.loc[index, 'Blurb'] = i.text
                                break
                            x[-1] = int(x[-1])
                            if x[-1] > 1000000:
                                print('---Third pass with the spare!!')
                                print(i.text)
                                Full_Ramen.loc[index, 'Blurb'] = i.text
                                break
                            if x[0] == "Notes:":
                                print('---Third pass with the spare!!')
                                print(i.text)
                                Full_Ramen.loc[index, 'Blurb'] = i.text
                                break
                        except:
                            pass
            #    Fourth pass: The earliest trend on the early days of the site is where the <p> of interest begins with 'Click' or ends with 'find it here.'
            # This is very likely to have bycatch so it is near the last.
            if Full_Ramen.loc[index, 'Blurb'] == 'Scrape':
                for i in alphabet_soup:
                    try:
                        x = i.text
                        x = x.split(' ')
                        if x[-2] == 'Get' and x[-1] == 'it':
                            print('---Fourth pass to the rescue!!')
                            print(i.text)
                            Full_Ramen.loc[index, 'Blurb'] = i.text
                            break
                        elif x[-2] == 'it' and x[-1] == 'here.':
                            print('---Fourth pass to the rescue!!')
                            print(i.text)
                            Full_Ramen.loc[index, 'Blurb'] = i.text
                            break
                        elif x[-2] == 'it' and x[-1] == 'here':
                            print('---Fourth pass to the rescue!!')
                            print(i.text)
                            Full_Ramen.loc[index, 'Blurb'] = i.text
                            break
                    except:
                        pass
            #    Fifth pass - the last ditch: If the paragraph is long, maybe its the one we're looking for.
            # This is BY FAR the most likely to have bycatch so it is the last one.
            # If this finds the wrong value, we were very unlikely to find the right one in an automated way.
            if Full_Ramen.loc[index, 'Blurb'] == 'Scrape':
                for i in alphabet_soup:
                    try:
                        x = i.text
                        x = x.split(' ')
                        if len(x) > 50:
                            print('ok well... fifth pass got ...something')
                            print(i.text)
                            Full_Ramen.loc[index, 'Blurb'] = i.text
                            break
                    except:
                        print('---We never stood a chance')
                        print(i.text)
                        Full_Ramen.loc[index, 'Blurb'] = "Scrape"

        except:
            print('---We never stood a chance')
            Full_Ramen.loc[index, 'Blurb'] = "Scrape"
        print('---')
        print(f"finished parsing index# {index}")
        print('''
        --------------------
        --------------------
        --------------------''')
    else:
        pass
#    This ends with few enough rows unsuccessful rows that the remainder can either be ignored or manually scraped
# without much cost of time or lost data.
# %%
#This part adds a 'Continents' Column and corrects some mistakes with country names.

corrections = {
   'Country': {
      'USA': 'United States',
      'UK': 'United Kingdom',
      'Souh Korea': 'South Korea',
      'Dubai':'United Arab Emirates',
      'Sarawak':'Malaysia'}
}

Full_Ramen.replace(corrections, regex=True, inplace=True)

#Set Continent List Manually
North_America = ['United States','Canada','Mexico']
South_America = ['Brazil','Peru','Colombia']
Australia = ['Australia']
Oceania = ['Fiji','New Zealand']
Africa = ['Ghana','Nigeria']
Europe = ['Finland','France','Germany','Holland','Italy','Poland','Spain','Sweden','United Kingdom','Portugal','Hungary','Netherlands','Estonia','Ukraine']
Asia = ['Bangladesh','Cambodia','China','India','Indonesia','Israel','Japan','Malaysia','Myanmar','Nepal','Pakistan','Philippines','Phlippines','Singapore','South Korea','Taiwan','Thailand','Hong Kong','Russia','Vietnam']

# Add Continent column
Full_Ramen = Full_Ramen.copy()
Full_Ramen['Continent'] = ''

for i in Full_Ramen.index:
    
    if Full_Ramen['Country'][i] in North_America:
        Full_Ramen.loc[i,'Continent'] = 'North America'
        
    if Full_Ramen['Country'][i] in South_America:
        Full_Ramen.loc[i,'Continent'] = 'South America'
    
    if Full_Ramen['Country'][i] in Australia:
        Full_Ramen.loc[i,'Continent'] = 'Australia'
        
    if Full_Ramen['Country'][i] in Oceania:
        Full_Ramen.loc[i,'Continent'] = 'Oceania'
        
    if Full_Ramen['Country'][i] in Africa:
        Full_Ramen.loc[i,'Continent'] = 'Africa'
        
    if Full_Ramen['Country'][i] in Europe:
        Full_Ramen.loc[i,'Continent'] = 'Europe'
    
    if Full_Ramen['Country'][i] in Asia:
        Full_Ramen.loc[i,'Continent'] = 'Asia'

#%%
#This will add 'Comment Length' columns

Full_Ramen['Comment_Length'] = ''

for index, row in Full_Ramen.iterrows():
    Full_Ramen.loc[index, "Comment_Length"]= len(row["Blurb"].split(" "))

#%%
#This is to analyze the 'Blurb'

def word_getter(x):
    search_words = ['chewiness', 'spicy', 'fresh', 'flavor', 'like', 'thick', 'tasty', 'surprisingly', 'strong', 'disappointing', 'sour', 'gravy', 'kick', 'onions', 'oil', 'new', 'new', 'sad', 'broth', 'tea', 'full', 'eat', 'good', 'fair']
    ramen_dict = {}
    for search_word in search_words:
        number_of_occurences = 0
        for word in x.split():
            if word == search_word:
                number_of_occurences += 1
        ramen_dict[search_word] = number_of_occurences
    return ramen_dict
    
Full_Ramen['Blurb_Analysis'] = Full_Ramen['Blurb'].apply(word_getter)

#%%
#This will get the barcode and add it to its own column

def bar_code_getter(x):
    oup_dict = {}
    x = x.split('.')
    for i in x:
        try:
            y = i.split(' ')
            barcode = int(y[-1])
            if y[-2] == 'code' and y[-3] == 'bar':
                if 'EAN' in y[1] or 'EAN' in y[0]:
                    oup_dict['EAN'] = barcode
                if 'JAN' in y[1] or 'JAN' in y[0]:
                    oup_dict['JAN'] = barcode
                if 'UPC' in y[1] or 'UPC' in y[0]:
                    oup_dict['UPC'] = barcode
                return oup_dict
                break
        except:
            pass


Full_Ramen['Barcode'] = Full_Ramen['Blurb'].apply(bar_code_getter)

#%%
#This will chop up the DataFrame and feed it into MongoDB
conn = 'mongodb://localhost:27017'
client = pymongo.MongoClient(conn)
db = client.RamenDB
ramen_list = Full_Ramen.columns.tolist()

for index, row in Full_Ramen.iterrows():
    list_dict= {}
    for column in ramen_list:
        if pd.isnull(row[column])== False:
            list_dict[column]=row[column]
    db.RamenDB.insert_one(list_dict)
#%%
Full_Ramen.to_csv('Full_Ramen.csv')