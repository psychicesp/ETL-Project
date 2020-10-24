#Word freq. 2

import pandas as pd
import numpy as np
#%%

ramen_df = pd.read_csv('../Full_Ramen.csv')
#%%

def word_analysis(x):
    empty = {}
    search_words = ['chewiness', 'spicy', 'fresh', 'flavor', 'like', 'thick', 'tasty', 'surprisingly', 'strong', 'disappointing', 'sour', 'gravy', 'kick', 'onions', 'oil', 'new', 'new', 'sad', 'broth', 'tea', 'full', 'eat', 'good', 'fair']
    for search_word in search_words:
        number_of_occurences = 0
        for word in x.split():
            if word == search_word:
                number_of_occurences += 1
        empty[search_word]= number_of_occurences
    return empty
ramen_df["Blurb_Analysis"]=ramen_df["Blurb"].apply(word_analysis)
ramen_df.head(25)
#%%

