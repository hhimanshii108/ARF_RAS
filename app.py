import streamlit as st
import utils as utl
from views import home
from views import about
from views import analysis

# Set Streamlit page configuration
st.set_page_config(layout="wide", page_title='Navbar sample')
st.set_option('deprecation.showPyplotGlobalUse', False)

# Inject custom CSS and navbar component
utl.inject_custom_css()
utl.navbar_component()

def navigation():
    route = utl.get_current_route()
    if route == "home":
        home.load_view()
    elif route == "about":
        about.load_view()
    elif route == "analysis":
        analysis.load_view()
    elif route is None:
        home.load_view()

# Call the navigation function
navigation()
