import streamlit as st
import os
from PIL import Image

st.set_page_config(
    page_title="G-Code Generator : Face Milling",
    layout="wide",
    page_icon="🚧",
)

path = os.path.dirname(__file__)

image1 = Image.open(path+'/face.jpg')
image2 = Image.open(path+'/spindel.JPG')

st.title('G-Code Generator : Face Milling')

 

col1, col2 = st.columns(2)
with col1:
    st.image(image2)
    spindelspeed = st.slider('Spindel Speed', 100,30000,3100)
    feedrate = st.slider('Feedrate', 10,1000,70)
    safeZ = st.slider('Safe Z', 1,100,5)
    deep = st.number_input('Depth of cutting', min_value = 0.05, max_value = 200.0, value = 5.0)
    deep_pass = st.number_input('Depth of cutting per pass', min_value = 0.05, max_value = deep, value = deep)
with col2:
    st.image(image1)
    tool_diameter = st.number_input('Tool Diameter', min_value = 1.0, max_value = 200.0, value = 2.0)
    overlapY = st.number_input('Y Overlap %', min_value = 1, max_value = 100, value = 90)
    overlapX = st.checkbox('Pass Extension')
    sideA = st.number_input('Side - A', min_value = 1.0, max_value = 200.0, value = 10.0)
    sideB = st.number_input('Side - B', min_value = 1.0, max_value = 200.0, value = 20.0)


deep = round(deep,2)
deep_pass = round(deep_pass,2)
next_pass = deep_pass
sideA_phase = 0
deep_cycle = 1
if overlapX:
    startX = -abs(round(tool_diameter/2,2))
    sideB += round(tool_diameter/2,2)
else: startX = 0


text = "G90\nM3 S" + str(spindelspeed) + "\n"
text += "G0 Z+" + str(safeZ) + "\nG0 X0 Y0"

text += "\nG1 Z-" + str(next_pass) + " F" + str(feedrate)

while sideA_phase < sideA:

    text += "\n(Phase cycle " + str(deep_cycle) + ")"
    text += "\nG1 X" + str(sideB) + " Y" + str(round(sideA_phase,2))    
    sideA_phase += round(tool_diameter * overlapY / 100,2)
    if sideA_phase > sideA: sideA_phase = sideA
    text += "\nG1 X" + str(sideB) + " Y" + str(round(sideA_phase,2))
    text += "\nG1 X" + str(startX) +" Y" + str(round(sideA_phase,2))
    sideA_phase += round(tool_diameter * overlapY / 100,2)
    if sideA_phase > sideA: sideA_phase = sideA
    if sideA_phase < sideA:text += "\nG1 X" + str(startX) +" Y" + str(round(sideA_phase,2))

    next_pass += deep_pass
    deep_cycle += 1
    
#if deep >= deep_pass:

#    text += "\n(Deep cycle " + str(deep_cycle) + ")"
#    text += "\nG1 Z-" + str(deep) + " F" + str(feedrate)
#    text += "\nG1 X0 Y"+ str(sideA) + " F" + str(feedrate)
#    text += "\nG1 X" + str(sideB) + " Y"+ str(sideA)
#    text += "\nG1 X" + str(sideB) + " Y0"
#    text += "\nG1 X0 Y0"

text += "\nG00 Z+" + str(safeZ)
text += "\nG1 X0 Y0"
text += "\nM5\nM30"

st.code(text)

st.download_button('Download G-Code', data = text)
