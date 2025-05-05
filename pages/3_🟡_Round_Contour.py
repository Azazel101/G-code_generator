from datetime import datetime
import streamlit as st
import os
from PIL import Image

st.set_page_config(
    page_title="G-Code Generator : Round Contour",
    layout="wide",
    page_icon="🟡",
)

# Initialize session state for saving parameters
if 'round_contour' not in st.session_state:
    st.session_state.round_contour = {
        'spindelspeed': 20000,
        'feedrate': 70,
        'safeZ': 5,
        'deep': 5.0,
        'deep_pass': 5.0,
        'tool': 'On',
        'tool_diameter': 1.0,
        'diameter': 5.0
    }

path = os.path.dirname(__file__)

image1 = Image.open(path+'/round.JPG')
image2 = Image.open(path+'/spindel.JPG')

st.title('G-Code Generator : Round Contour')

col1, col2 = st.columns(2)
with col1:
    st.image(image2)
    spindelspeed = st.slider('Spindel Speed', min_value=100, max_value=30000, 
                            value=st.session_state.round_contour['spindelspeed'], step=10)
    feedrate = st.slider('Feedrate', min_value=10, max_value=1000, 
                        value=st.session_state.round_contour['feedrate'], step=10)
    safeZ = st.slider('Safe Z', 1, 100, 
                     value=st.session_state.round_contour['safeZ'])
    deep = st.number_input('Depth of cutting', min_value=0.05, max_value=200.0, 
                          value=st.session_state.round_contour['deep'])
    deep_pass = st.number_input('Depth of cutting per pass', min_value=0.05, max_value=deep, 
                               value=st.session_state.round_contour['deep_pass'])
with col2:
    st.image(image1)
    tool = st.selectbox('Tool movement', ('On', 'Outside', 'Inside'), 
                       index=['On', 'Outside', 'Inside'].index(st.session_state.round_contour['tool']))
    if tool != 'On': 
        tool_diameter = st.number_input('Tool Diameter', min_value=1.0, max_value=200.0, 
                                       value=st.session_state.round_contour['tool_diameter'], step=0.5)
    else:
        tool_diameter = st.session_state.round_contour['tool_diameter']
    diameter = st.number_input('Diameter of a circle D', min_value=1.0, max_value=200.0, 
                              value=st.session_state.round_contour['diameter'])

# Update session state with current values
st.session_state.round_contour['spindelspeed'] = spindelspeed
st.session_state.round_contour['feedrate'] = feedrate
st.session_state.round_contour['safeZ'] = safeZ
st.session_state.round_contour['deep'] = deep
st.session_state.round_contour['deep_pass'] = deep_pass
st.session_state.round_contour['tool'] = tool
st.session_state.round_contour['tool_diameter'] = tool_diameter
st.session_state.round_contour['diameter'] = diameter

diameter_r = diameter / 2

if tool == 'Outside':
    diameter_r = diameter_r + round(tool_diameter / 2, 3)
elif tool == 'Inside':
    diameter_r = diameter_r - round(tool_diameter / 2, 3)

deep = round(deep, 2)
deep_pass = round(deep_pass, 2)

cycle_pass = deep_pass
next_pass = deep_pass

text = "G90\nM3 S" + str(spindelspeed) + "\n"
text += "G00 Z+" + str(safeZ) + "\nG0 X0 Y0"

deep_cycle = 1

while next_pass < deep:
    text += "\n(Deep cycle " + str(deep_cycle) + ")"
    text += "\nG01 Z-" + str(next_pass) + " F" + str(feedrate)
    text += "\nG02 I" + str(diameter_r)
    cycle_pass -= deep_pass
    next_pass += deep_pass
    deep_cycle += 1
    
if deep >= deep_pass:
    text += "\n(Deep cycle " + str(deep_cycle) + ")"
    if deep == deep_pass:text += "\nG00 X-"+ str(diameter_r) + " Y0"
    text += "\nG01 Z-" + str(deep) + " F" + str(feedrate)
    text += "\nG02 I" + str(diameter_r)

text += "\nG00 Z+" + str(safeZ) + "\nG00 X0 Y0"
text += "\nM5\nM30"

st.code(text)

filename = f"round_contour_{datetime.now().strftime('%Y%m%d_%H%M%S')}.nc"
st.download_button('Download G-Code', data=text, file_name=filename)
