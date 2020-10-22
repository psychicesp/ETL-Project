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
Full_Ramen = Ramen2.merge(Ramen1, left_on = 'ID', right_on =  'Review #')
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

#%%
Full_Ramen['Blurb'] = ''
for index, row in Full_Ramen.iterrows():
    try:
        URL = row['URL']
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
        Full_Ramen.loc[index,'Blurb'] = "Double check URL"
    print(f"finished parsing index# {index}")  
# %%
Full_Ramen.to_csv('Full_Ramen.csv')