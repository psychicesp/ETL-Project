#%%
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests as req
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
#%%
Ramen2['ID'] = Ramen2['ID'].apply(id_cleaner)
#%% 
Full_Ramen = Ramen2.merge(Ramen1, left_on = 'ID', right_on =  'Review #', how = 'outer')
# %%
Full_Ramen = Full_Ramen.rename({
    'ID': 'Review_ID'
}, axis = 1)
Full_Ramen.drop('Review #', inplace=True, axis=1)

Full_Ramen
#%%
URL = Full_Ramen['URL'][0]
html = req.get(URL).text
ramen_soup = bs(html, 'html.parser')

#   Thought not by initial design, scraping was achieved in multiple passes.
#  
#   This is an inefficient process if scraping from scratch but is 
# more efficient than re-scraping successful rows in an attempt to make one holistic pass.
#
#   If I needed to rescrape from scratch I would marry these scrapes together so that it could be
# achieved in one pass without making redundant HTML requests.
#
#   For our workflow, however, it was most efficient to simply check if a row was finished and make
# additional passes on unfinished rows, because we can't check if a method would fail for any given webpage
# without doing as much work as a manual scrape.

#%%
#First Pass, gets data for about half as it turns out
Full_Ramen['Blurb'] = ''
for index, row in Full_Ramen.iterrows():
    try:
        URL = row['URL']
        html = req.get(URL).text
        ramen_soup = bs(html, 'html.parser')
        for i in ramen_soup.find_all('p'):
            try:
                x = i.text
                x = x.split('(click to enlarge)')
                if x[0] == 'Finished ':
                    Full_Ramen.loc[index,'Blurb'] = i.text
                    print(i.text)
                    break
            except:
                pass
        
    except:
        Full_Ramen.loc[index,'Blurb'] = "Double check URL"
    print(f"finished parsing index# {index}")  
# %%
# Second Pass, will get info from urls input without 'https://'
for index, row in Full_Ramen.iterrows():
    if row['Blurb'] == "Double check URL":
        try:
            URL = 'https://' + row['URL']
            html = req.get(URL).text
            ramen_soup = bs(html, 'html.parser')
            x = 'Some sort of error'
            for i in ramen_soup.find_all('p'):
                try:
                    x = i.text
                    x = x.split(' ')
                    if x[0] == 'Finished':
                        Full_Ramen.loc[index,'Blurb'] = i.text
                        print(i.text)
                        break
                except:
                    pass
        except:
            Full_Ramen.loc[index,'Blurb'] = "Scrape"
    print(f"finished parsing index #{index}")  

#%%
#   This will mark the rows which still need to be Scraped to prevent making redundant requests for 
# rows that successfully scraped
for index, row in Full_Ramen.iterrows():
    try:
        y = len(str(row['Blurb']).split(' '))
        if y < 6:
            Full_Ramen.loc[index, 'Blurb'] = 'Scrape'
    except:
        Full_Ramen.loc[index, 'Blurb'] = 'Scrape'

#%%
#   Third Pass.  This will try and catch those which used a different formatting in the past, based on the fact 
#that a long barcode is often last and when there is no barcode the last word is often 'stars.'
for index, row in Full_Ramen.iterrows():
    if row['Blurb'] == 'Scrape':
        try:
            time.sleep(5)
            URL = row['URL']
            html = req.get(URL).text
            ramen_soup = bs(html, 'html.parser')
            for i in ramen_soup.find_all('p'):
                try:
                    x = i.text
                    x = x.split(' ')
                    x[-1] = x[-1].replace('.','')
                    if x[-1] == 'stars':
                        print(i.text)
                        Full_Ramen.loc[index,'Blurb'] = i.text
                        break
                    x[-1] = int(x[-1])
                    if x[-1]> 100000:
                        print(i.text)
                        Full_Ramen.loc[index,'Blurb'] = i.text
                        break                        
                except:
                    pass
        except:
            Full_Ramen.loc[index,'Blurb'] = "Scrape"
    print(f"finished parsing index #{index}")

#%%
#   Fourth Pass.  If this one doesn't grab the last of them I'll call it a day.
#If making a holistic, single-pass I would probably combine this method with the first
#and the second, ignoring the third.  It appears this net will catch everything caught
#by the third without the baggage of the thirds bycatch.

for index, row in Full_Ramen.iterrows():
    if row['Blurb'] == 'Scrape':
        try:
            time.sleep(5)
            URL = row['URL']
            html = req.get(URL).text
            ramen_soup = bs(html, 'html.parser')
            for i in ramen_soup.find_all('p'):
                try:
                    x = i.text
                    x = x.split('(click image to enlarge)')
                    if x[0] == 'Finished ':
                        Full_Ramen.loc[index,'Blurb'] = i.text
                        print(i.text)
                        break                   
                except:
                    pass
        except:
            Full_Ramen.loc[index,'Blurb'] = "Scrape"
    print(f"finished parsing index #{index}") 
    
Full_Ramen.to_csv('Full_Ramen.csv')
# %%


