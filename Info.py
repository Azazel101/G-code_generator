import streamlit as st
from streamlit.components.v1 import html

st.set_page_config(
    page_title="Welcome to G-Code Generator!",
    layout="wide",
    page_icon="👋",
)

st.write("# Welcome to G-Code Generator! 👋")

my_js = """<script type="text/javascript" src="https://cdnjs.buymeacoffee.com/1.0.0/button.prod.min.js" data-name="bmc-button" data-slug="romanslov" data-color="#FFDD00" data-emoji="" data-font="Cookie" data-text="Buy me a coffee" data-outline-color="#000000" data-font-color="#000000" data-coffee-color="#ffffff" ></script>"""

st.markdown(
    """
    G-Code Generator is an open-source app to create
    Fast and Easy basic G-code for Milling Maschine.
"""
)

html(my_js)