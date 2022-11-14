import streamlit as st

st.set_page_config(layout="wide")

st.title('CNC - G-Code Generator : Rectangle')

col1, col2, col3 = st.columns(3)
with col1:
    spindelspeed = st.slider('Spindel Speed', 100,30000,3100)
    feedrate = st.slider('Feedrate', 10,1000,70)
with col2:
    sideA = st.number_input('Side A', min_value = 1.0, max_value = 200.0, value = 5.0)
    sideB = st.number_input('Side B', min_value = 1.0, max_value = 200.0, value = 5.0)
    #st.markdown("***")

with col3:
    deep = st.number_input('Depth of cutting', min_value = 1.0, max_value = 200.0, value = 5.0)
    deep_pass = st.number_input('Depth of cutting per pass', min_value = 1.0, max_value = 200.0, value = 5.0)

text = "G90\nM3 S" + str(spindelspeed) + "\n"

text += "G0 Z+5\nG0 " + "+" + "\nG0 Z-1.604\nG1 Z-" + str(deep) + " F" + str(feedrate) + "\n"

text += "M5\nG0 X+0 Y+0\nM30"

st.code(text)

st.download_button('Download G-Code', data = text)

#G00 Z0.5 (raise the tool to the clearance height)
#G00 X0 Y0 (the movement of the tool to the start point of the milling (point 5))
#G01 Z-1 F50 (lower the tool to the desired cutting depth)
#G01 X0 Y20 F50 (milling side a)
#G01 X30 Y20 (milling side b)
#G01 X30 Y0 (milling side a)
#G01 X0 Y0 (milling side b, return to the start point for milling) G00 Z0.5 F70 (raise the tool to the clearance height)
#M30 (end of the control program)