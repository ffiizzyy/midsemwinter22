# work through the drop down menu for neighbourhoods
import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt 

#create a side drop down menu to pick a neighbourhood
def app():

    #read files, create dfs for future drop-down list
    df_neigh = pd.read_csv('neighbourhoods.csv')
    df = pd.read_csv("cleansed_listings_dec18.csv", low_memory=False)

    selected_columns = ['id', 'listing_url','name','summary','space', 'description', 'neighborhood_overview', 'notes', 'transit',
        'access', 'interaction', 'house_rules','host_name', 'host_is_superhost', 'neighborhood', 'city', 'latitude', 'longitude',
        'property_type', 'room_type', 'accommodates','bathrooms', 'bedrooms', 'beds', 'bed_type', 'amenities', 'price', 'cleaning_fee', 'guests_included', 'extra_people']

    cleansed = df[selected_columns].copy()
    cleansed = cleansed.set_index('id', drop=False)
    cleansed = cleansed[cleansed['price'] != 0]
    df_city = pd.DataFrame(cleansed['city'].unique())

    st.sidebar.write('---')
    st.sidebar.subheader('Choose from options')

    def user_input_features():
        neighbourhood = st.sidebar.selectbox('Neighbourhood', df_neigh['neighbourhood'])
        city = st.sidebar.selectbox('City', df_city[0])
        prop_type = st.sidebar.selectbox('Property type', pd.DataFrame(cleansed.property_type.unique()))
        num_of_guests = st.sidebar.slider('Number of guests', 
                                        cleansed['guests_included'].min(), 
                                        cleansed['guests_included'].max())
        max_price = st.sidebar.slider('Maximum price', 
                                       0, 
                                       cleansed['price'].max(), 
                                       step = 100)
        num_of_bedrooms = st.sidebar.slider('Number of bedrooms', 
                                        int(cleansed['bedrooms'].min()), 
                                        int(cleansed['bedrooms'].max()),
                                        step = 1)
        data = {'City': city, 
                'Neighbourhood':neighbourhood, 
                'Property type': prop_type,
                'Maximum price':max_price,
                'Number of guests':num_of_guests,
                'Number of bedrooms':num_of_bedrooms}
        features = pd.DataFrame(data, index = [1])
        return features 
    
    df_selected = user_input_features()

    #Display chosen input parameters

    st.header('Let`s explore reviews')
    st.subheader('Choose from options on the left panel and we`ll take care of the rest')
    st.write('---')

    st.subheader('Chosen parameters')
    st.write(df_selected)
    st.write('---')

    #Let`s now find which listing ids correspond to df_selected



   






    
