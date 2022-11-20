import streamlit as st
import os
from PIL import Image

path = os.path.dirname(__file__)


image2 = Image.open(path+'/spindel.JPG')

st.title('G-Code Generator : Drill hole')

col1, col2 = st.columns(2)
with col1:
    st.image(image2)
    spindelspeed = st.slider('Spindel Speed', 100,30000,3100)
    feedrate = st.slider('Feedrate', 10,1000,70)
    safeZ = st.slider('Safe Z', 1,100,5)
    deep = st.number_input('Depth of cutting', min_value = 1.0, max_value = 200.0, value = 5.0)

with col2:
    direction = st.selectbox('Select direction',('X','Y'))
    #st.markdown("***")
    offset = st.number_input('Offset first hole', min_value = 0.0, max_value = 300.0, value = 25.0)
    num_hole = st.slider('How many hole', 1,100,1)

offset = round(offset,2)

text = "G90\nM3 S" + str(spindelspeed) + "\n"

text += "(Hole 1)\nG0 Z+" + str(safeZ) + "\nG0 " + direction + "+" + str(offset) + "\nG0 Z-1.604\nG1 Z-" + str(deep) + " F" + str(feedrate) + "\n"

if num_hole > 1:
    with col3: distanc = st.number_input('Distance between hole', min_value = 0.0, max_value = 300.0, value = 25.0)

    acc_dist = offset + distanc

    for x in range(num_hole):
        text += "(Hole " + str(x + 2) + ")\nG0 Z+" + str(safeZ) + "\nG0 " + direction + "+" + str(acc_dist) + "\nG0 Z-1.604\nG1 Z-" + str(deep) + " F" + str(feedrate) + "\n"
        acc_dist += distanc

text += "G0 Z+" + str(safeZ) + "\nM5\nG0 X+0 Y+0\nM30"

st.code(text)

st.download_button('Download G-Code', data = text)