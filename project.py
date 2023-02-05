import streamlit as st
from multiapp import MultiApp
from apps import home, reviews # import your app modules here

app = MultiApp()



# Add all your application here
app.add_app("Home", home.app)
app.add_app("Reviews", reviews.app)
# The main app
app.run()