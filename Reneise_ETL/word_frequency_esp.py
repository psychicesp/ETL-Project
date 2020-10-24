#Word freq. 2
#%%
import pandas as pd
import numpy as np

ramen_df = pd.read_csv('../Newfangled_ramen.csv')

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
    


# %%
