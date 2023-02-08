# Import packages
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt 
import corpora
from textblob import TextBlob
# import nltk
from wordcloud import WordCloud
from collections import Counter
import requests 
from streamlit_lottie import st_lottie
import geopandas as gpd
import folium
from streamlit_folium import folium_static
from folium.plugins import FastMarkerCluster

# Cleaning and setting up dataframe
st.set_option('deprecation.showPyplotGlobalUse', False)
df = pd.read_csv("cleansed_listings_dec18.csv", low_memory=False)

selected_columns = ['id', 'listing_url','name','summary','space', 'description', 'neighborhood_overview', 'notes', 'transit',
    'access', 'interaction', 'house_rules', 'neighborhood', 'city',
    'property_type', 'room_type', 'accommodates','bathrooms', 'bedrooms', 'beds', 'price', 'cleaning_fee', 'guests_included', 'extra_people']

cleansed = df[selected_columns].copy()
cleansed = cleansed.set_index('id', drop=False)
cleansed = cleansed[cleansed['price'] != 0]

# Creating select boxes for the pages - this is where the user chooses what page they want to see
pageselector = ['Home', 'I want to learn more about Melbourne', 'Help me choose a neighbourhood', 'Help me choose a property']
page = st.sidebar.selectbox('Choose page:', options = pageselector)
st.sidebar.write('---')

if page == 'Help me choose a property':
    # Sidebar user options
    city = st.sidebar.selectbox('Council Location:', list(sorted(cleansed['city'].unique())))
    neighbourhood = st.sidebar.selectbox('Neighbourhood:', [x for x in cleansed[cleansed['city'] == city]['neighborhood'].unique() if str(x) != 'nan'])
    if not neighbourhood:
        st.caption('Oops, there are no listings here. Please choose another location.')
    prop_type = st.sidebar.selectbox('Property type:', cleansed[cleansed['city'] == city][cleansed['neighborhood']== neighbourhood]['room_type'].unique())

    min_guest_calc = cleansed[cleansed['city'] == city][cleansed['neighborhood'] == neighbourhood][cleansed['room_type'] == prop_type]['guests_included'].min()
    max_guest_calc = cleansed[cleansed['city'] == city][cleansed['neighborhood'] == neighbourhood][cleansed['room_type'] == prop_type]['guests_included'].max()

    if min_guest_calc != max_guest_calc:
        num_of_guests = st.sidebar.slider('Number of guests:', min_value=int(min_guest_calc), max_value=int(max_guest_calc))
    else:
        st.sidebar.write('Maximum number of guests:', max_guest_calc)
        num_of_guests = max_guest_calc

    min_price_calc = cleansed[cleansed['city'] == city][cleansed['neighborhood'] == neighbourhood][cleansed['room_type'] == prop_type][cleansed['guests_included'] == num_of_guests]['price'].min()
    max_price_calc = cleansed[cleansed['city'] == city][cleansed['neighborhood'] == neighbourhood][cleansed['room_type'] == prop_type][cleansed['guests_included'] == num_of_guests]['price'].max()

    if min_price_calc != max_price_calc:
        max_price = st.sidebar.slider('Maximum price per night:', min_value=int(min_price_calc), max_value=int(max_price_calc))
    else: 
        st.sidebar.write('Maximum price per night: $', max_price_calc)
        max_price = max_price_calc

    listing_id_chosen = st.sidebar.selectbox('Select listing to view:', cleansed[cleansed['city'] == city][cleansed['neighborhood'] == neighbourhood][cleansed['room_type'] == prop_type][cleansed['guests_included'] == num_of_guests][cleansed['price'] <= max_price]['id'].unique()) 

    # Sentiment analysis
    st.subheader("Sentiment Analysis of Individual Airbnb Reviews")
    st.write("This page will help you evaluate if you should stay at your chosen Airbnb. The wordclouds will show the most mentioned positive and negative attributes of the property.")

    st.write("This table summarises all the relevant information about the property:")
    st.dataframe(cleansed[cleansed['id'] == listing_id_chosen])

    reviews = pd.read_csv("reviews_dec18.csv")
    reviews['comments'] = reviews['comments'].astype(str)

    # Create subset which has user input
    reviews_subset = reviews.loc[reviews['listing_id'] == listing_id_chosen, :].copy()

    # #If polarity <=0 = negative, >0 positive
    reviews_subset.loc[:, 'polarity'] = reviews_subset['comments'].apply(lambda 
                x: TextBlob(x).sentiment.polarity)
    
    reviews_subset.loc[:, 'subjectivity'] = reviews_subset['comments'].apply(lambda 
                x: TextBlob(x).sentiment.subjectivity)     

    # Count positive and negative comments
    neg_count = reviews_subset[reviews_subset['polarity'] <= 0].shape[0]
    pos_count = reviews_subset[reviews_subset['polarity'] > 0].shape[0]

    st.write("---")
    st.subheader("Reviews Analysis")
    st.write("This property has", pos_count, "positive reviews and", neg_count, "negative reviews.")

    print(reviews_subset['comments'])

    # Extract part-of-speech tags from the 'comments' column
    reviews_subset.loc[:, 'pos_tags'] = reviews_subset['comments'].apply(lambda 
                x: TextBlob(x).pos_tags)

    # Define a function that returns the nouns in a list of tuples
    def get_nouns(tags):
        nouns = [word for word, pos in tags if pos == "NN"]
        return nouns

    # Apply the get_nouns function to the 'pos_tags' column
    reviews_subset.loc[:, 'nouns'] = reviews_subset['pos_tags'].apply(get_nouns)

    # Create a list of the nouns in the 'nouns' column
    noun = [word for tags in reviews_subset['nouns'] for word in tags]

    # Join the nouns into a single string
    text = " ".join(noun)

    # Count and order the frequency of the most popular words
    subset_negative = reviews_subset[reviews_subset['polarity'] <= 0]
    subset_positive = reviews_subset[reviews_subset['polarity'] > 0]

    positive_noun = [word for tags in subset_positive['nouns'] for word in tags]
    negative_noun = [word for tags in subset_negative['nouns'] for word in tags]

    def returnWordCount(wordList) :
        word_counts = Counter(wordList)
        items = list(word_counts.items())
        sorted_items = sorted(items, key=lambda x: x[1], reverse=True)
        word_output = pd.DataFrame(sorted_items, columns=['Word', 'Frequency'])
        return word_output

    st.markdown("**Most frequently mentioned words in the positive reviews:**")
    st.write(returnWordCount(positive_noun))

    # Create positive/negative reviews wordcloud
    st.write("---")
    st.subheader('Having trouble making sense of the information? These wordclouds will summarise it for you.')
    def SentimentWordCloud(emotion):
        noun = [word for tags in emotion['nouns'] for word in tags]
        text = " ".join(noun)

        wordcloud = WordCloud(background_color='white', max_words=100).generate(text)
        wordcloud_array = wordcloud.to_array()
        plt.imshow(wordcloud_array, interpolation='bilinear')
        plt.axis("off")
        plt.show()
        st.pyplot()
    
    try:
        st.write("**Positive Reviews Wordcloud**")
        SentimentWordCloud(subset_positive)

    except: 
        st.caption("There are no positive reviews.")

    try:
        st.write("**Negative Reviews Wordcloud**")
        SentimentWordCloud(subset_negative)

    except: 
        st.caption("There are no negative reviews.")

    # Display reviews table
    st.write("---")
    st.write("Read the reviews left by previous guests:")
    st.dataframe(reviews_subset[['date','reviewer_name','comments']])

# Sidebar for user input depends on the page chosen
if page == 'Help me choose a neighbourhood':
    st.subheader('Explore a neighbourhood!')
    st.write("Don't know where to stay? Choose an area you are curious below and learn more about it!")

    city = st.selectbox('Council Location:', list(cleansed['city'].unique()))
    neighbourhood = st.selectbox('Neighbourhood:', [x for x in cleansed[cleansed['city'] == city]['neighborhood'].unique() if str(x) != 'nan'])
    
    # Main body of neighbourhoods page
    if neighbourhood:
        neighbourhood_count = cleansed[cleansed['neighborhood'] == neighbourhood].shape[0]
        st.write('The', neighbourhood, 'area in', city, 'has', neighbourhood_count, 'properties. See where they are located:')

        # Add map of listings in neighbourhood

        lat = df[df['city'] == city][df['neighborhood'] == neighbourhood]['latitude']
        lon = df[df['city'] == city][df['neighborhood'] == neighbourhood]['longitude']
        locations = list(zip(lat, lon))

        map_mel = folium.Map(location=[-37.815018, 144.946014],tiles='CartoDB Positron',zoom_start=10)
        FastMarkerCluster(data=locations).add_to(map_mel)
        folium_static(map_mel)
        
    if not neighbourhood:
        st.caption('Oops, there are no listings here. Please choose another location.')

    analysis_neighbourhood = st.container()

if page == 'Home':
    st.write('''
    # Welcome to our Melbourne Airbnb Project :sparkles:
    We'll help you choose where to stay on your next visit to Melbourne!
     ''')
    st.write('''----''')

    #url for a lottie file (picture)
    pic_url = 'https://assets8.lottiefiles.com/private_files/lf30_5i5tlydx.json'

    #define a function to load an image: 
    def load_pic(url): 
        r = requests.get(url)
        if r.status_code != 200: 
            return None
        return r.json()

    #loading a pic 
    pic_load = load_pic(pic_url)

    # column for a picture and another column for some info about the project
    with st.container():
        left_col, right_col = st.columns(2)
        with left_col: 
            st.header('More about the project: ')
            st.write('We sourced our AirBnb data from Kaggle. We have analysed and visualised all the information you need to know about all the neighbourhood and properties you can choose from in Melbourne. Above you can navigate to the Neighbourhood page (which shows reviews and details about each specific neighbourhood) and to the Reviews page (to see what other holidaymakers have said about the place. It is important to note that we are working with historical Airbnb listings, with the data last scraped in 2018. It does not represent current property listings and prices.')
            st.write('[You can see our dataset here  >](https://www.kaggle.com/datasets/tylerx/melbourne-airbnb-open-data)')
        with right_col:
            st_lottie(pic_load, height = 300, key = 'coding')

        st.write('---')

        #use css to style the contact form: 
        def load_css(file_name):
            with open(file_name) as f: 
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

        load_css('style.css')

        #Contact form 
        with st.container():
            st.subheader('Please send us your feedback here:')
            contact_form = '''
            <form action="https://formsubmit.co/80243939@fsv.cuni.cz" method="POST">
                 <input type = 'hidden' name = 'captcha_' value = 'false'>
                 <input type="email" name="email" placeholder = 'Email' required>
                 <textarea name = 'message' placeholder = 'Please write your feedback here' required></textarea>
                 <button type="submit">Send</button>
            </form>
            ''' 
            
            left_column, right_column = st.columns(2)
            with left_column: 
                st.markdown(contact_form, unsafe_allow_html = True)
            with right_column: 
                st.empty()

if page == 'I want to learn more about Melbourne':
    st.subheader("Let's explore Melbourne together")
    st.write('Know nothing about Melbourne? This page will show you the breakdown of all the areas in Melbourne - where the cheapest properties are and where you will get the most bang out of your buck.') 
    st.write('Want to know more about a specific area? Go to the "Help me choose a neighbourhood" page.')
    st.write('---')

    #Create map with median value of each region
    median_price_by_city = cleansed.groupby(['city'])['price'].mean().sort_values(ascending=True)

    # Create dataframe containing median prices by city
    median_price_by_city_df = pd.DataFrame(list(median_price_by_city.items()), columns=['neighbourhood', 'Median Price'])
    median_price_by_city_df['Median Price'] = median_price_by_city_df['Median Price'].astype(float)

    # Load json file with coordinates for the city
    melbmap_gdf = gpd.read_file('neighbourhoods.geojson')
    
    # Create map
    st.markdown('**Median price per night sorted by metropolitan council zones**')
    st.caption('This map shows median price of properties as sorted by metropolitan council zones listed by the Victorian Government.')
    map = folium.Map(location = [-37.8136, 144.9631], zoom_start = 10)

    city_layer = folium.Choropleth(
        geo_data = melbmap_gdf,
        name = "Median price per night sorted by metropolitan council",
        data = median_price_by_city_df,
        columns = ['neighbourhood', 'Median Price'],
        key_on = "feature.properties.neighbourhood",
        fill_color = "YlOrRd",
        fill_opacity = 0.7,
        line_opacity = .1,
        legend_name = "Median price per night (AU$)",
    )

    city_layer.add_to(map)
    folium.LayerControl().add_to(map)
    folium_static(map)

    st.write('---')
    st.write('**Median prices per night sorted by neighbourhood**')
    st.caption('This table shows the median price per night as sorted by neighbourhoods. You would most likely know the areas based on these location names.')

    # Create table of median price by neighbourhood
    median_price_by_neighborhood = cleansed.groupby(['neighborhood'])['price'].mean().sort_values(ascending=True)
    median_price_by_neigh_df = pd.DataFrame(list(median_price_by_neighborhood.items()), columns=["Neighbourhood", "Median Price (AU$)"])
    median_price_by_neigh_df['Median Price (AU$)'] = median_price_by_neigh_df['Median Price (AU$)'].astype(float)
    st.write(median_price_by_neigh_df)


