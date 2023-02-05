# work through the drop down menu for neighbourhoods
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt 
from textblob import TextBlob
import nltk
from wordcloud import WordCloud
from collections import Counter

#Create sidebar
# def app():
    #read files, create dfs for future drop-down list
    df = pd.read_csv("cleansed_listings_dec18.csv", low_memory=False)

    selected_columns = ['id', 'listing_url','name','summary','space', 'description', 'neighborhood_overview', 'notes', 'transit',
        'access', 'interaction', 'house_rules','host_name', 'host_is_superhost', 'neighborhood', 'city', 'latitude', 'longitude',
        'property_type', 'room_type', 'accommodates','bathrooms', 'bedrooms', 'beds', 'bed_type', 'amenities', 'price', 'cleaning_fee', 'guests_included', 'extra_people']

    cleansed = df[selected_columns].copy()
    cleansed = cleansed.set_index('id', drop=False)
    cleansed = cleansed[cleansed['price'] != 0]
    df_city = pd.DataFrame(cleansed['city'].unique())

    st.sidebar.write('---')
    st.sidebar.subheader('Choose from the following options:')

    def user_input_features():
        city = st.sidebar.selectbox('Council Location:', pd.DataFrame(cleansed.city.unique()).unique())
        neighbourhood = st.sidebar.selectbox('Neighbourhood:', cleansed[cleansed['city'] == city]['neighborhood'].unique())
        prop_type = st.sidebar.selectbox('Property type:', cleansed[cleansed['city'] == city][cleansed['neighborhood']== neighbourhood]['room_type'].unique())
        num_of_guests = st.sidebar.slider('Number of guests:', 
                                        cleansed[cleansed['city'] == city][cleansed['neighborhood'] == neighbourhood][cleansed['room_type' ]== prop_type]['guests_included'].min(), 
                                        cleansed[cleansed['city'] == city][cleansed['neighborhood'] == neighbourhood][cleansed['room_type' ]== prop_type]['guests_included'].max())
        max_price = st.sidebar.slider('Maximum price per night:', 
                                       0, 
                                       cleansed[cleansed['city'] == city][cleansed['neighborhood'] == neighbourhood][cleansed['room_type' ]== prop_type][cleansed['guests_included']== num_of_guests]['price'].max(), 
                                       step = 100)
        listing_id_chosen = st.sidebar.selectbox('Select listing to view:', cleansed[cleansed['city'] == city][cleansed['neighborhood'] == neighbourhood][cleansed['room_type' ]== prop_type][cleansed['guests_included']== num_of_guests][cleansed['price'] <= max_price]['id'].unique())
        data = {'City': city, 
                'Neighbourhood':neighbourhood, 
                'Property type': prop_type,
                'Maximum price':max_price,
                'Number of guests':num_of_guests}
        features = pd.DataFrame(data, index = [1])
        return features 
    
    df_selected = user_input_features()

    #Display chosen input parameters

    st.header("Individual Property Reviews")
    st.subheader("Choose from the options on the left panel and we will show your dream vacation property")
    st.write('---')

    st.subheader("Chosen parameters:")
    st.write(df_selected)
    st.write('---')

    # Sentiment analysis

    reviews = pd.read_csv("reviews_dec18.csv")
    reviews['comments'] = reviews['comments'].astype(str)

    # Create subset which has user input
    reviews_subset = df.loc[df['listing_id'] == listing_id_chosen, :].copy()

    # Determine polarity and subjectivity

    # #If polarity <=0 = negative, >0 positive
    reviews_subset.loc[:, 'polarity'] = subset['comments'].apply(lambda 
                x: TextBlob(x).sentiment.polarity)
    reviews_subset.loc[:, 'subjectivity'] = subset['comments'].apply(lambda 
                x: TextBlob(x).sentiment.subjectivity)

    # Extract part-of-speech tags from the 'comments' column
    reviews_subset.loc[:, 'pos_tags'] = subset['comments'].apply(lambda 
                x: TextBlob(x).pos_tags)

    # Define a function that returns the nouns in a list of tuples
    def get_nouns(tags):
        nouns = [word for word, pos in tags if pos == "NN"]
        return nouns

    # Apply the get_nouns function to the 'pos_tags' column
    reviews_subset.loc[:, 'nouns'] = subset['pos_tags'].apply(get_nouns)

    # Create a list of the nouns in the 'nouns' column
    noun = [word for tags in subset['nouns'] for word in tags]

    # Join the nouns into a single string
    text = " ".join(noun)

    # Create wordcloud 
    wordcloud = WordCloud(background_color='white', max_words=100).generate(text)
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis("off")

    # Display reviews table and WordCloud object
    st.dataframe(reviews_subset[['listing_id','date','reviewer_name','comments']])
    st.pyplot(wordcloud)







   






    
