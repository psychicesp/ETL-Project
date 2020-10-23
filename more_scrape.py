#%%
from matplotlib import pyplot as plt
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests as req

Full_Ramen = pd.read_csv("Full_Ramen.csv")
for index, row in Full_Ramen.iterrows():
    try:
        y = len(str(row['Blurb']).split(' '))
        if y < 6:
            Full_Ramen.loc[index, 'Blurb'] = 'Scrape'
    except:
        Full_Ramen.loc[index, 'Blurb'] = 'Scrape'


#%%
for index, row in Full_Ramen.iterrows():
    if row['Blurb'] == 'Scrape':
        try:
            URL = 'https://' + row['URL']
            html = req.get(URL).text
            ramen_soup = bs(html, 'html.parser')
            for i in ramen_soup.find_all('p'):
                try:
                    print(i.text)
                    x = i.text
                    print(x)
                    x = x.split(' ')
                    x[-1] = x[-1].replace('.','')
                    print(x[-1])
                    if x[-1] == 'stars':
                        print(i.text)
                        Full_Ramen.loc[index,'Blurb'] = i.text
                        break
                    x[-1] = int(x[-1])
                    if x[-1]> 100:
                        print(i.text)
                        Full_Ramen.loc[index,'Blurb'] = i.text
                        break                        
                except:
                    pass
        except:
            Full_Ramen.loc[index,'Blurb'] = "Scrape"
    print(f"finished parsing index #{index}") 
# %%
Full_Ramen.to_csv('mock_Ramen.csv')