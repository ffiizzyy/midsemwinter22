import pandas as pd
from textblob import TextBlob
import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import streamlit as st 
import requests 
from streamlit_lottie import st_lottie


st.set_page_config(page_title = 'Python project', page_icon = ':snake:')

st.write('''
# Welcome to our Airbnb Melbourne data science project :sparkles:


We aim to help you consciously pick your stay
''')
st.write('''----''')

# Load CSV
df = pd.read_csv("reviews_dec18.csv")
df['comments'] = df['comments'].astype(str)

# List how many unique places are reviewed
num_unique_values = df['listing_id'].nunique()
unique_values = df['listing_id'].unique()

# user input here
listing_id_chosen = 12936
subset = df.loc[df['listing_id'] == listing_id_chosen, :].copy()

# Determine polarity

#If polarity <0 = negative, =0 means neutral, >0 positive
subset.loc[:, 'polarity'] = subset['comments'].apply(lambda 
                x: TextBlob(x).sentiment.polarity)

# Determine subjectivity
subset.loc[:, 'subjectivity'] = subset['comments'].apply(lambda 
                x: TextBlob(x).sentiment.subjectivity)

# Extract part-of-speech tags from the 'comments' column
subset.loc[:, 'pos_tags'] = subset['comments'].apply(lambda 
                x: TextBlob(x).pos_tags)

# Define a function that returns the nouns in a list of tuples
def get_nouns(tags):
    nouns = [word for word, pos in tags if pos == "NN"]
    return nouns

# Apply the get_nouns function to the 'pos_tags' column
subset.loc[:, 'nouns'] = subset['pos_tags'].apply(get_nouns)


## stopped to display sth onto the website
st.sidebar.header('Specify listing ID')
def user_input_features():     #working on TEXT_INPUT
    SUBURB = st.sidebar.text_input()
    data = {'listing':LISTING}
    features = pd.DataFrame(data, index = [0])
    return features 
side_panel = user_input_features()


#code for a lottie file (picture)
pic_url = 'https://assets8.lottiefiles.com/private_files/lf30_5i5tlydx.json'

#define a function to load an image: 
def load_pic(url): 
    r = requests.get(url)
    if r.status_code != 200: 
        return None
    return r.json()

pic_loaded = load_pic(pic_url)


# column for a picture and another column for some info about the project
with st.container():
    left_col, right_col = st.columns(2)
    with left_col: 
        st.header('More about the project')
        st.write('add sth about the source of data etc')
        st.write('[You can see our dataset here  >](https://www.kaggle.com/datasets/tylerx/melbourne-airbnb-open-data)')
    with right_col: 
        st_lottie(pic_loaded, height = 300, key = 'coding')



    



