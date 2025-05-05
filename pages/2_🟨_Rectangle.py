import streamlit as st
import os
from PIL import Image
from datetime import datetime

st.set_page_config(
    page_title="G-Code Generator : Rectangle",
    layout="wide",
    page_icon="🟨",
)

# Initialize session state for rectangle parameters
if 'rectangle' not in st.session_state:
    st.session_state.rectangle = {
        'spindelspeed': 3100,
        'feedrate': 70,
        'safeZ': 5,
        'deep': 5.0,
        'deep_pass': 5.0,
        'tool': 'On',
        'tool_diameter': 1.0,
        'sideA': 5.0,
        'sideB': 10.0
    }

path = os.path.dirname(__file__)

image1 = Image.open(path+'/rectengle.JPG')
image2 = Image.open(path+'/spindel.JPG')

st.title('G-Code Generator : Rectangle')

col1, col2 = st.columns(2)

with col1:
    st.image(image2)
    spindelspeed = st.slider(
        'Spindel Speed', min_value=100, max_value=30000,
        value=st.session_state.rectangle['spindelspeed'], step=10
    )
    feedrate = st.slider(
        'Feedrate', min_value=10, max_value=1000,
        value=st.session_state.rectangle['feedrate'], step=10
    )
    safeZ = st.slider(
        'Safe Z', 1, 100,
        value=st.session_state.rectangle['safeZ']
    )
    deep = st.number_input(
        'Depth of cutting', min_value=0.05, max_value=200.0,
        value=st.session_state.rectangle['deep']
    )
    deep_pass = st.number_input(
        'Depth of cutting per pass', min_value=0.05, max_value=deep,
        value=st.session_state.rectangle['deep_pass']
    )
with col2:
    st.image(image1)
    tool = st.selectbox(
        'Tool movement', ('On', 'Outside', 'Inside'),
        index=['On', 'Outside', 'Inside'].index(st.session_state.rectangle['tool'])
    )
    if tool != 'On':
        tool_diameter = st.number_input(
            'Tool Diameter', min_value=1.0, max_value=200.0,
            value=st.session_state.rectangle['tool_diameter'], step=0.5
        )
    else:
        tool_diameter = st.session_state.rectangle['tool_diameter']
    sideA = st.number_input(
        'Side - A', min_value=1.0, max_value=200.0,
        value=st.session_state.rectangle['sideA']
    )
    sideB = st.number_input(
        'Side - B', min_value=1.0, max_value=200.0,
        value=st.session_state.rectangle['sideB']
    )
    #st.markdown("***")

# Update session state with current values
st.session_state.rectangle['spindelspeed'] = spindelspeed
st.session_state.rectangle['feedrate'] = feedrate
st.session_state.rectangle['safeZ'] = safeZ
st.session_state.rectangle['deep'] = deep
st.session_state.rectangle['deep_pass'] = deep_pass
st.session_state.rectangle['tool'] = tool
st.session_state.rectangle['tool_diameter'] = tool_diameter
st.session_state.rectangle['sideA'] = sideA
st.session_state.rectangle['sideB'] = sideB
st.session_state.rectangle['deep'] = deep
st.session_state.rectangle['deep_pass'] = deep_pass
# Calculate the adjusted radius based on tool movement
deep = round(deep, 2)
deep_pass = round(deep_pass, 2)

#cycle_pass = round(deep - deep_pass,2)
cycle_pass = deep_pass
next_pass = deep_pass

deep_cycle = 1

text = "G90\nM3 S" + str(spindelspeed) + "\n"
text += "G0 Z+" + str(safeZ) + "\nG0 X0 Y0"

while next_pass < deep:
    text += "\n(Deep cycle " + str(deep_cycle) + ")"
    text += "\nG1 Z-" + str(next_pass) + " F" + str(feedrate)
    text += "\nG1 X0 Y"+ str(sideA) + " F" + str(feedrate)
    text += "\nG1 X" + str(sideB) + " Y"+ str(sideA)
    text += "\nG1 X" + str(sideB) + " Y0"
    text += "\nG1 X0 Y0"

    cycle_pass -= deep_pass
    next_pass += deep_pass
    deep_cycle += 1
    
if deep >= deep_pass:
    text += "\n(Deep cycle " + str(deep_cycle) + ")"
    text += "\nG1 Z-" + str(deep) + " F" + str(feedrate)
    text += "\nG1 X0 Y"+ str(sideA) + " F" + str(feedrate)
    text += "\nG1 X" + str(sideB) + " Y"+ str(sideA)
    text += "\nG1 X" + str(sideB) + " Y0"
    text += "\nG1 X0 Y0"

text += "\nG00 Z+" + str(safeZ) + "\nM5\nM30"

st.code(text)

filename = f"rectangle_{datetime.now().strftime('%Y%m%d_%H%M%S')}.nc"
st.download_button('Download G-Code', data=text, file_name=filename)
