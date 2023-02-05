import pandas as pd 
import streamlit as st 
import matplotlib.pyplot as plt 
import geopandas as gpd
import folium 
from reviews import cleansed

def app():
    # Load and cleaned df
    

    #Create df of coordinates 
    listing_location = cleansed[['latitude','longitude']]
    listing_location.head(5)
    
    #Create map with median value of each region

   median_price_by_city = cleansed.groupby(['city'])['price'].mean().sort_values(ascending=True)
   median_price_by_neighborhood = cleansed.groupby(['neighborhood'])['price'].mean().sort_values(ascending=True)

   # Create dataframe containing median prices by city

   median_price_by_city_df = pd.DataFrame(list(median_price_by_city.items()), columns=['neighbourhood', 'Median Price'])

   median_price_by_city_df['Median Price'] = median_price_by_city_df['Median Price'].astype(float)

   #load json file with coordinates for the city

   melbmap_gdf = gpd.read_file('neighbourhoods.geojson')

   #Add some design text to the page 

   st.sidebar.subheader('Choose from options')
   def user_input_map():
      

   #Create a map 

   map = folium.Map(location = [-37.8136, 144.9631], zoom_start = 10)

   folium.Choropleth(
      geo_data = melbmap_gdf,
      name = "Median price per night sorted by metropolitan council",
      data = median_price_by_city_df,
      columns = ['neighbourhood', 'Median Price'],
      key_on = "feature.properties.neighbourhood",
      fill_color = "YlOrRd",
      fill_opacity = 0.7,
      line_opacity = .1,
      legend_name = "Median price per night (AU$)",
   ).add_to(map)

   folium.LayerControl().add_to(map)




   

    





