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
#
#     I took this as an opportunity to marry all scrape methods into a single pass with minimal redundant HTML requests.
#
#    These need to be pretty impeccible, however, as the bycatch from any particular method might prevent a later, better method from
# running
Full_Ramen['Blurb'] = ''
for index, row in Full_Ramen.iterrows():
# There are two different URL formats.  We could correct this in the DF but went this route instead.
    try:
        URL = row['URL']
        html = req.get(URL).text
        ramen_soup = bs(html, 'html.parser')
    except:
        URL = 'https://' + row['URL']
            html = req.get(URL).text
            ramen_soup = bs(html, 'html.parser')
#    First pass, tries to find the <p> of interest based on a common opener 'Finished (click to enlarge).
# Simply using parenthesis has some weird bycatch.
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
# Second Pass, exploiting the large portion of pages where the <p> of interest begins with 'Finished (click image to enlarge)'
                try:
                    x = i.text
                    x = x.split('(click image to enlarge)')
                    if x[0] == 'Finished ':
                        Full_Ramen.loc[index,'Blurb'] = i.text
                        print(i.text)
                        break
                except:
#    Third pass - the last-ditch - the <p> of interest often ends with a long barcode, 
# and where there is no barcode it ends with '_ out of 5 stars.'
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
#    This ends with few enough rows unsuccessful rows that the remainder can either be ignored or manually scraped
# without much cost of time or lost data.
# %%
