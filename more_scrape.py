#%%
from matplotlib import pyplot as plt
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests as req
import time

Full_Ramen = pd.read_csv("Full_Ramen.csv")
for index, row in Full_Ramen.iterrows():
    try:
        y = len(str(row['Blurb']).split(' '))
        if y < 6:
            Full_Ramen.loc[index, 'Blurb'] = 'Scrape'
    except:
        Full_Ramen.loc[index, 'Blurb'] = 'Scrape'



#%%
#Third Pass
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
#Fourth Pass
Full_Ramen['Blurb'] = ''
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