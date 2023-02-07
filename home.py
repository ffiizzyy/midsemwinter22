import pandas as pd
from textblob import TextBlob
import nltk
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from collections import Counter
import streamlit as st 
import requests 
from streamlit_lottie import st_lottie




def app():
    st.write('''
    # Welcome to our Airbnb Melbourne data science project :sparkles:


    Let us help you pick your dream holiday acccommodation in Melbourne!
     ''')
    st.write('''----''')

    with st.sidebar:
        st.write('----')

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
            st.header('More about the project')
            st.write('We sourced our AirBnb data from Kaggle. We have analysed and visualised all the information you need to know about all the neighbourhood and properties you can choose from in Melbourne. Above you can navigate to the Neighbourhood page (which shows reviews and details about each specific neighbourhood) and to the Reviews page (to see what other holidaymakers have said about the place. It is important to note that we are working with historical Airbnb listings, with the data last scraped in 2018. It does not represent current property listings and prices.')
            st.write('[You can see our dataset here  >](https://www.kaggle.com/datasets/tylerx/melbourne-airbnb-open-data)')
        with right_col:
            st_lottie(pic_load, height = 300, key = 'coding')

        st.write('---')

        #use css to style the contact form: 
        def load_css(file_name):
            with open(file_name) as f: 
                st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html = True)

        load_css('style/style.css')

        #Contact form 
        with st.container():
            st.subheader('Please send us your feedback here:')
            contact_form = '''
            <form action="https://formsubmit.co/80243939@fsv.cuni.cz" method="POST">
                 <input type = 'hidden' name = 'captcha_' value = 'false'>
                 <input type="email" name="email" placeholder = 'Email' required>
                 <textarea name = 'message' placeholder = 'Your feedback here' required></textarea>
                 <button type="submit">Send</button>
            </form>
            ''' 
            
            left_column, right_column = st.columns(2)
            with left_column: 
                st.markdown(contact_form, unsafe_allow_html = True)
            with right_column: 
                st.empty()

    
    

        
    




    


    
    





    

    







































    



