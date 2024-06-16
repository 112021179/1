import streamlit as st
from PIL import Image


st.set_page_config(
    page_title="Home", 
    layout="wide",
    page_icon=''
)


# --- Header Section ---
header_image = Image.open(r"images\header.png").resize((300, 150))  

with st.container():
    st.image(header_image, width=300, use_column_width=True)  
    st.markdown("<h1 style='text-align: left;'>Welcome to our Final Project!</h1>", unsafe_allow_html=True)
    st.markdown("<h2 style='text-align: left;'>This application provides tools for stock analysis and prediction.</h2>", unsafe_allow_html=True)

st.markdown("---")
st.markdown("<h2>Explore the Features:</h2>", unsafe_allow_html=True)
st.write("- **Stock Charts**: Visualize historical stock data with interactive charts.")
st.write("- **Stock News**: Stay updated with the latest stock news headlines.")
st.write("- **Stock Prediction**: Predict stock price movements using machine learning.")

st.markdown("---")
st.markdown("<h2>Get Started:</h2>", unsafe_allow_html=True)
st.button("Explore Now", key="explore_button")


# --- Sidebar Section ---
st.sidebar.success("Select a page from above")