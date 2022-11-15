import streamlit as st
#from PIL import Image
#image = Image.open('rectengle.JPG')

#st.set_page_config(layout="wide")

st.title('G-Code Generator : Round Contour')

#st.image(image, caption='Sunrise by the mountains')

col1, col2, col3 = st.columns(3)
with col1:
    spindelspeed = st.slider('Spindel Speed', 100,30000,3100)
    feedrate = st.slider('Feedrate', 10,1000,70)
    safeZ = st.slider('Safe Z', 1,100,5)
with col2:
    tool = st.selectbox('Tool movement',('On','Outside','Inside'))
    if tool != 'On': tool_diameter = st.number_input('Tool Diameter', min_value = 1.0, max_value = 200.0, value = 1.0)
    diameter = st.number_input('Diameter of a circle D', min_value = 1.0, max_value = 200.0, value = 5.0)
    #st.markdown("***")

with col3:
    deep = st.number_input('Depth of cutting', min_value = 1.0, max_value = 200.0, value = 5.0)
    deep_pass = st.number_input('Depth of cutting per pass', min_value = 1.0, max_value = deep, value = deep)

diameter_r = diameter / 2

if tool == 'Outside':
    diameter_r = diameter_r + round(tool_diameter / 2,3)
elif tool == 'Inside':
    diameter_r = diameter_r - round(tool_diameter / 2,3)


deep = round(deep,2)
deep_pass = round(deep_pass,2)

cycle_pass = round(deep - deep_pass,2)
next_pass = deep_pass

text = "G90\nM3 S" + str(spindelspeed) + "\n"
text += "G00 Z+" + str(safeZ) + "\nG0 X0 Y0"

if deep >= deep_pass:

    text += "\nG00 X-"+ str(diameter_r) + " Y0"
    text += "\nG01 Z-" + str(next_pass) + " F" + str(feedrate)
    text += "\nG02 I" + str(diameter_r)


while deep_pass < cycle_pass:

    text += "\nG01 Z-" + str(next_pass) + " F" + str(feedrate)
    text += "\nG02 I" + str(diameter_r)

    cycle_pass -= deep_pass
    next_pass += deep_pass

if deep_pass > cycle_pass and not cycle_pass == 0:
    text += "\nG01 Z-" + str(cycle_pass) + " F" + str(feedrate)
    text += "\nG02 I" + str(diameter_r)

if deep_pass == cycle_pass and not cycle_pass == 0:
    text += "\nG01 Z-" + str(deep) + " F" + str(feedrate)
    text += "\nG02 I" + str(diameter_r)


text += "\nG00 Z+" + str(safeZ) + "\nG00 X0 Y0"
text += "\nM5\nM30"

#st.write(tool[inde])

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