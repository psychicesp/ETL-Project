#Word freq. 2
#%%
import pandas as pd
import numpy as np

ramen_df = pd.read_csv('../Full_Ramen.csv')

#%%

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
    
ramen_df['Blurb_Analysis'] = ramen_df['Blurb'].apply(word_getter)


#%%

def bar_code_getter(x):
    oup_dict = {}
    x = x.split('.')
    for i in x:
        try:
            y = i.split(' ')
            barcode = int(y[-1])
            return
            if len(y[0]) == 3 and y[1] == 'bar' and y[2] == 'code':
                oup_dict[x[0]] = barcode
                return oup_dict
                break
        except:
            pass


ramen_df['Barcode'] = ramen_df['Blurb'].apply(bar_code_getter)
# %%
ramen_df
# %%
