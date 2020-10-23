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

#    Original scraping was done in about four passes, each one targeting rows which were missed by previous passes.
# I would have stuck with this structure except that some of the methods resulted is some very weird 'bycatch'
# resulting in the necessity to scrape from scratch (ugh).
#    I took this as an opportunity to marry all scrape methods into a single pass with minimal redundant HTML requests.
Full_Ramen['Blurb'] = ''
for index, row in Full_Ramen.iterrows():
    try:
        URL = row['URL']
        html = req.get(URL).text
        ramen_soup = bs(html, 'html.parser')
    except:
        URL = 'https://' + row['URL']
            html = req.get(URL).text
            ramen_soup = bs(html, 'html.parser')
    try:
        for i in ramen_soup.find_all('p'):
            try:
                x = i.text
                x = x.split('(click to enlarge)')
                if x[0] == 'Finished ':
                    Full_Ramen.loc[index,'Blurb'] = i.text
                    print(i.text)
                    break
            except:
                try:
                    x = i.text
                    x = x.split('(click image to enlarge)')
                    if x[0] == 'Finished ':
                        Full_Ramen.loc[index,'Blurb'] = i.text
                        print(i.text)
                        break
                except:
                    try: x = i.text
                    x = x.split(' ')
                    x[-1] = x[-1].replace('.','')
                    if x[-1] == 'stars':
                        print(i.text)
                        Full_Ramen.loc[index,'Blurb'] = i.text
                        break
                    x[-1] = int(x[-1])
                    if x[-1]> 1000000:
                        print(i.text)
                        Full_Ramen.loc[index,'Blurb'] = i.text
                        break                        
                    except:
                        pass
    except:
        Full_Ramen.loc[index,'Blurb'] = "Scrape Unsuccessful"
    print(f"finished parsing index# {index}")  
# %%
