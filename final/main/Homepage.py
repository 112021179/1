import streamlit as st

st.set_page_config(
    page_title="Home", 
    layout="wide",
    page_icon='')

# --- Header Section ---
with st.container():
    st.title("Final Project")
    st.subheader(
        "Overview"
    )
    st.write(
        "Our Final Project consists of:\n - Stock Charts\n - Stock News\n - Stock Prediction"
    )

# --- Sidebar ---
st.sidebar.success("Select a page from above")