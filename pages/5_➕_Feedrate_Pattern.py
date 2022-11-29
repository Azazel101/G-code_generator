import streamlit as st
import os
from PIL import Image

st.set_page_config(
    page_title="G-Code Generator : Feedrate Pattern",
    layout="wide",
    page_icon="➕",
)

path = os.path.dirname(__file__)

st.title('G-Code Generator : Feedrate Pattern')

spindelspeed = st.slider('Spindel Speed', min_value=100,max_value=30000,value=3100, step=100)
feedrate = st.slider('Feed per tooth', 0.01,1.0,0.1)
numflute = st.slider('Num of flute', 1,10,1)

result = spindelspeed * feedrate * numflute

st.subheader('Feedrate : ' + str(result))
