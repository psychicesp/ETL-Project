# %%
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
for index, row in Full_Ramen.iterrows():
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
    time.sleep(1)
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
                    except:
                        pass
        #    Fourth pass: The earliest trend on the early days of the site is where the <p> of interest begins with 'Click' or ends with 'find it here.'
        # This is very likely to have bycatch so it is near the last.
        if Full_Ramen.loc[index, 'Blurb'] == 'Scrape':
            for i in alphabet_soup:
                try:
                    x = i.text
                    x = x.split(' ')
                    x[-1] = x[-1].replace('.', '')
                    if x[0] == 'Click':
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
#    This ends with few enough rows unsuccessful rows that the remainder can either be ignored or manually scraped
# without much cost of time or lost data.
# %%
Full_Ramen.to_csv('Newfangled_Ramen.csv')