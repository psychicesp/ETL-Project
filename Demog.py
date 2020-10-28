#%%
import pandas as pd
from bs4 import BeautifulSoup as bs
import requests as req
#import pymongo
import numpy as np
import time

df = pd.read_csv('Full_Ramen.csv')

def numify(x):
    try:
        x = float(x)
        return x
    except:
        pass


df['Stars'] = df['Stars'].apply(numify)
df.groupby('Continent').agg({
    "Stars":"mean",
    "Review_ID":"count"
})
# %%
df.groupby('Country').agg({
    "Stars":"mean",
    "Review_ID":"count"
})
#%%
df.groupby('Style').agg({
    "Stars":"mean",
    "Review_ID":"count"
})
# %%
df['Stars'].hist(bins = 20)

# %%
