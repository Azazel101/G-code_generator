import streamlit as st
import os
from PIL import Image
import math
from datetime import datetime

st.set_page_config(
    page_title="G-Code Generator : Feedrate Pattern",
    layout="wide",
    page_icon="➕",
)

# Initialize session state for feedrate parameters
if 'feedrate_pattern' not in st.session_state:
    st.session_state.feedrate_pattern = {
        'tool_diameter': 6.0,
        'flutes': 2,
        'tool_material': 'Carbide',
        'workpiece_material': 'Aluminum',
        'depth': 5.0,
        'depth_per_pass': 1.0,
        'pattern_length': 100.0,
        'pattern_width': 20.0,
        'stepover': 5.0,
        'custom_sfm': 0,
        'custom_chipload': 0,
        'safeZ': 5
    }

path = os.path.dirname(__file__)

st.title('G-Code Generator : Feedrate Pattern')

# Material cutting speed chart (SFM - Surface Feet per Minute)
material_speeds = {
    'Aluminum': {'HSS': 300, 'Carbide': 500},
    'Mild Steel': {'HSS': 70, 'Carbide': 150},
    'Stainless Steel': {'HSS': 30, 'Carbide': 100},
    'Brass': {'HSS': 200, 'Carbide': 300},
    'Plastic': {'HSS': 300, 'Carbide': 500},
    'Wood': {'HSS': 400, 'Carbide': 800},
    'Custom': {'HSS': 0, 'Carbide': 0}
}

# Chip load chart (inches per tooth)
chip_loads = {
    'Aluminum': {1: 0.0254, 2: 0.0508, 3: 0.0762, 4: 0.1016, 6: 0.127, 8: 0.1524, 10: 0.1778, 12: 0.2032},
    'Mild Steel': {1: 0.0127, 2: 0.0254, 3: 0.0381, 4: 0.0508, 6: 0.0762, 8: 0.1016, 10: 0.127, 12: 0.1524},
    'Stainless Steel': {1: 0.0076, 2: 0.0178, 3: 0.0254, 4: 0.0381, 6: 0.0508, 8: 0.0762, 10: 0.1016, 12: 0.127},
    'Brass': {1: 0.0254, 2: 0.0508, 3: 0.0762, 4: 0.1016, 6: 0.127, 8: 0.1524, 10: 0.1778, 12: 0.2032},
    'Plastic': {1: 0.0508, 2: 0.0762, 3: 0.1016, 4: 0.127, 6: 0.1524, 8: 0.1778, 10: 0.2032, 12: 0.2286},
    'Wood': {1: 0.0762, 2: 0.1016, 3: 0.127, 4: 0.1524, 6: 0.1778, 8: 0.2032, 10: 0.2286, 12: 0.254},
    'Custom': {1: 0.0254, 2: 0.0254, 3: 0.0254, 4: 0.0254, 6: 0.0254, 8: 0.0254, 10: 0.0254, 12: 0.0254}
}

col1, col2 = st.columns(2)

with col1:
    st.subheader("Tool Parameters")
    tool_diameter = st.number_input('Tool Diameter (mm)', 
                                  min_value=0.5, max_value=25.0, 
                                  value=st.session_state.feedrate_pattern['tool_diameter'], 
                                  step=0.5)
    
    flutes = st.slider('Number of Flutes/Teeth', 
                     min_value=1, max_value=8, 
                     value=st.session_state.feedrate_pattern['flutes'])
    
    tool_material = st.selectbox('Tool Material', 
                               ['HSS', 'Carbide'], 
                               index=['HSS', 'Carbide'].index(st.session_state.feedrate_pattern['tool_material']))
    
    workpiece_material = st.selectbox('Workpiece Material', 
                                     list(material_speeds.keys()),
                                     index=list(material_speeds.keys()).index(st.session_state.feedrate_pattern['workpiece_material']))
    
    if workpiece_material == 'Custom':
        custom_sfm = st.number_input('Custom Surface Speed (SFM)', 
                                   value=st.session_state.feedrate_pattern['custom_sfm'])
        custom_chipload = st.number_input('Custom Chip Load (mm/tooth)', 
                                        value=st.session_state.feedrate_pattern['custom_chipload'],
                                        format="%.4f", step=0.0025)  # 0.0001 inch ≈ 0.0025 mm
    else:
        custom_sfm = 0
        custom_chipload = 0

with col2:
    st.subheader("Cutting Parameters")
    depth = st.number_input('Total Depth (mm)', 
                           min_value=0.1, max_value=50.0, 
                           value=st.session_state.feedrate_pattern['depth'])
    
    depth_per_pass = st.number_input('Depth per Pass (mm)', 
                                    min_value=0.1, max_value=depth, 
                                    value=st.session_state.feedrate_pattern['depth_per_pass'])
    
    pattern_length = st.number_input('Pattern Length (mm)', 
                                    min_value=10.0, max_value=1000.0, 
                                    value=st.session_state.feedrate_pattern['pattern_length'])
    
    pattern_width = st.number_input('Pattern Width (mm)', 
                                   min_value=5.0, max_value=500.0, 
                                   value=st.session_state.feedrate_pattern['pattern_width'])
    
    stepover = st.number_input('Stepover (mm)', 
                              min_value=tool_diameter * 0.1, max_value=tool_diameter * 0.9, 
                              value=st.session_state.feedrate_pattern['stepover'])
    
    safeZ = st.slider('Safe Z Height (mm)', 
                     min_value=1, max_value=50, 
                     value=st.session_state.feedrate_pattern['safeZ'])

# Update session state
st.session_state.feedrate_pattern['tool_diameter'] = tool_diameter
st.session_state.feedrate_pattern['flutes'] = flutes
st.session_state.feedrate_pattern['tool_material'] = tool_material
st.session_state.feedrate_pattern['workpiece_material'] = workpiece_material
st.session_state.feedrate_pattern['depth'] = depth
st.session_state.feedrate_pattern['depth_per_pass'] = depth_per_pass
st.session_state.feedrate_pattern['pattern_length'] = pattern_length
st.session_state.feedrate_pattern['pattern_width'] = pattern_width
st.session_state.feedrate_pattern['stepover'] = stepover
st.session_state.feedrate_pattern['custom_sfm'] = custom_sfm
st.session_state.feedrate_pattern['custom_chipload'] = custom_chipload
st.session_state.feedrate_pattern['safeZ'] = safeZ

# Calculate cutting parameters
tool_diameter_inch = tool_diameter / 25.4  # Convert mm to inch for calculations

# Get surface speed
if workpiece_material == 'Custom':
    sfm = custom_sfm
else:
    sfm = material_speeds[workpiece_material][tool_material]

# Calculate RPM: RPM = (SFM × 12) / (π × diameter in inches)
rpm = int((sfm * 12) / (math.pi * tool_diameter_inch))

# Limit RPM to reasonable maximum
rpm = min(rpm, 30000)

# Get chip load (mm per tooth)
if workpiece_material == 'Custom':
    chip_load = custom_chipload
else:
    # Find the closest diameter in the chip load chart
    diameters = sorted(chip_loads[workpiece_material].keys())
    closest_dia = min(diameters, key=lambda x: abs(x - tool_diameter))
    chip_load = chip_loads[workpiece_material][closest_dia]

# Calculate feed rate: Feed Rate = RPM × Number of Flutes × Chip Load (mm/min)
feed_rate_mm = rpm * flutes * chip_load

# Display calculation results
st.subheader("Calculated Values")
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("Spindle Speed (RPM)", f"{rpm:,}")
with col2:
    st.metric("Chip Load", f"{chip_load:.4f} mm/tooth")
with col3:
    st.metric("Feed Rate", f"{int(feed_rate_mm)} mm/min")

# Generate G-code for feedrate pattern test
st.subheader("G-Code for Feedrate Pattern Test")

# Generate a pattern that varies feed rate along the length
num_passes = max(1, int(depth / depth_per_pass))
num_stepover = max(1, int(pattern_width / stepover))

g_code = []
g_code.append("G90")  # Absolute positioning
g_code.append(f"M3 S{rpm}")  # Start spindle at calculated RPM
g_code.append(f"G0 Z{safeZ}")  # Move to safe height
g_code.append("G0 X0 Y0")  # Move to start position

current_depth = 0
for pass_num in range(num_passes):
    current_depth += depth_per_pass
    if current_depth > depth:
        current_depth = depth
    
    g_code.append(f"(Pass {pass_num + 1} - Depth: {current_depth}mm)")
    g_code.append(f"G1 Z-{current_depth} F{int(feed_rate_mm/2)}")  # Plunge at half feed rate
    
    for step in range(num_stepover):
        y_pos = step * stepover
        
        # Calculate varied feed rates along the length
        feed_min = int(feed_rate_mm * 0.5)  # 50% of calculated
        feed_max = int(feed_rate_mm * 1.5)  # 150% of calculated
        
        # Move to start of current line with rapid move
        g_code.append(f"G0 X0 Y{y_pos}")
        
        # Cut with increasing feed rate
        g_code.append(f"G1 X{pattern_length/3} F{feed_min}")
        g_code.append(f"G1 X{pattern_length*2/3} F{int(feed_rate_mm)}")
        g_code.append(f"G1 X{pattern_length} F{feed_max}")
    
    # Return to safe Z after each depth pass
    g_code.append(f"G0 Z{safeZ}")

# End program
g_code.append("G0 X0 Y0")
g_code.append("M5")  # Stop spindle
g_code.append("M30")  # End program

# Display G-code
g_code_text = "\n".join(g_code)

# Download button for G-code
filename = f"feedrate_pattern_{datetime.now().strftime('%Y%m%d_%H%M%S')}.nc"
st.download_button('Download G-Code', data=g_code_text, file_name=filename)

# Display G-code in a code block
st.code(g_code_text)

# Display information about the feedrate pattern
st.subheader("Pattern Description")
st.write("""
This pattern creates a series of parallel lines with varying feed rates:
- First third: 50% of calculated feed rate ({} mm/min)
- Middle third: 100% of calculated feed rate ({} mm/min) 
- Last third: 150% of calculated feed rate ({} mm/min)

Observe the cut quality across different sections to determine the optimal feed rate for your specific tool and material combination.
""".format(int(feed_rate_mm * 0.5), int(feed_rate_mm), int(feed_rate_mm * 1.5)))

# Add reference tables
with st.expander("Material Cutting Speed Reference"):
    speed_df = {
        "Material": list(material_speeds.keys())[:-1],  # Exclude 'Custom'
        "HSS (SFM)": [material_speeds[m]['HSS'] for m in material_speeds if m != 'Custom'],
        "Carbide (SFM)": [material_speeds[m]['Carbide'] for m in material_speeds if m != 'Custom']
    }
    st.table(speed_df)

with st.expander("Chip Load Reference (mm per tooth)"):
    st.write("Recommended chip loads vary by tool diameter and material:")
    for material in list(chip_loads.keys())[:-1]:  # Exclude 'Custom'
        st.write(f"**{material}**")
        chip_df = {
            "Diameter (mm)": [f"{d}" for d in sorted(chip_loads[material].keys())],
            "Chip Load (mm/tooth)": [f"{chip_loads[material][d]:.4f}" for d in sorted(chip_loads[material].keys())]
        }
        st.table(chip_df)