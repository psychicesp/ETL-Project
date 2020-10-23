#%%
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests as req

Full_Ramen = pd.read_csv("Full_Ramen.csv")
# %%
for index, row in Full_Ramen.iterrows():
    row_blurb = str(row['Blurb'])
    if len(row_blurb) == '':
        try:
            URL = 'https://' + row['URL']
            html = req.get(URL).text
            ramen_soup = bs(html, 'html.parser')
            x = 'Some sort of error'
            for i in ramen_soup.find_all('p'):
                try:
                    x = i.text
                    x = x.split('.')
                    isBlurb == False
                    print(x[-1])
                    try:
                        x[-1] = x[-1].replace('.','')
                        int(x[-1])
                        isBlurb = True
                    except:
                        pass
                    if x[-1] == 'Finished' or isBlurb == True or x[-1] == 'here.':
                        Full_Ramen.loc[index,'Blurb'] = i.text
                        print(i.text)
                        break
                except:
                    pass
            
        except:
            Full_Ramen.loc[index,'Blurb'] = "Some weird issue"
    print(f"finished parsing index #{index}") 
# %%
