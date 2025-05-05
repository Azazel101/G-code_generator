from datetime import datetime
import streamlit as st
import os
from PIL import Image
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="G-Code Generator : Round Contour",
    layout="wide",
    page_icon="🛠️",  # Tool emoji to represent toolpath/machining
)
path = os.path.dirname(__file__)

st.title("Visualization toolpath from G-codu")

def parse_gcode(file_content):
    import re
    import numpy as np
    coords = []
    current_x, current_y, current_z = 0, 0, 0
    
    for line in file_content.splitlines():
        line = line.strip().upper()
        
        # Extract X, Y, Z coordinates
        x_match = re.search(r'X([-+]?[0-9]*\.?[0-9]+)', line)
        y_match = re.search(r'Y([-+]?[0-9]*\.?[0-9]+)', line)
        z_match = re.search(r'Z([-+]?[0-9]*\.?[0-9]+)', line)
        i_match = re.search(r'I([-+]?[0-9]*\.?[0-9]+)', line)
        j_match = re.search(r'J([-+]?[0-9]*\.?[0-9]+)', line)
        
        # Update current position if coordinates are specified
        if x_match: current_x = float(x_match.group(1))
        if y_match: current_y = float(y_match.group(1))
        if z_match: current_z = float(z_match.group(1))
        
        # Linear move (G0/G1)
        if line.startswith(('G0', 'G1')):
            coords.append((current_x, current_y, current_z))
            
        # Circular move (G02/G03)
        elif line.startswith(('G2', 'G02', 'G3', 'G03')):
            # Get center offset
            center_x = current_x + float(i_match.group(1)) if i_match else current_x
            center_y = current_y + float(j_match.group(1)) if j_match else current_y
            
            # Calculate radius and angles
            radius = np.sqrt((current_x - center_x)**2 + (current_y - center_y)**2)
            start_angle = np.arctan2(current_y - center_y, current_x - center_x)
            end_x = float(x_match.group(1)) if x_match else current_x
            end_y = float(y_match.group(1)) if y_match else current_y
            end_angle = np.arctan2(end_y - center_y, end_x - center_x)
            
            # For full circle without specified endpoint
            if not x_match and not y_match:
                end_angle = start_angle + 2 * np.pi
            
            # Adjust for clockwise/counterclockwise
            if line.startswith(('G3', 'G03')):  # CCW
                if end_angle <= start_angle:
                    end_angle += 2 * np.pi
            else:  # CW (G2/G02)
                if end_angle >= start_angle:
                    end_angle -= 2 * np.pi
            
            # Generate points along the arc (approx. every 5 degrees)
            angle_step = 0.09  # radians (~5 degrees)
            if line.startswith(('G3', 'G03')):  # CCW
                angles = np.arange(start_angle, end_angle, angle_step)
            else:  # CW
                angles = np.arange(start_angle, end_angle, -angle_step)
                
            for angle in angles:
                arc_x = center_x + radius * np.cos(angle)
                arc_y = center_y + radius * np.sin(angle)
                coords.append((arc_x, arc_y, current_z))
            
            # Add final point
            coords.append((end_x, end_y, current_z))
            current_x, current_y = end_x, end_y
            
    return coords

uploaded_file = st.file_uploader("Nahrajte G-code súbor", type=["gcode", "nc", "txt"])
if uploaded_file is not None:
    content = uploaded_file.read().decode("utf-8")
    coords = parse_gcode(content)
    if coords:
        # Display coordinates in a table with improved styling
        st.subheader("Toolpath Coordinates (X, Y, Z)")
            
        # Create a dataframe with coordinates for better display
        df_coords = pd.DataFrame(coords, columns=['X (mm)', 'Y (mm)', 'Z (mm)'])

        # Add row numbers
        df_coords.index = df_coords.index + 1
        df_coords.index.name = 'Point'

        # Show the coordinates table with scrolling for large datasets
        st.dataframe(df_coords, height=300, use_container_width=True)

        # Show summary statistics
        st.subheader("Toolpath Statistics")
        col1, col2, col3 = st.columns(3)
        col1.metric("Number of points", len(coords))
        col2.metric("X Range", f"{min(x):.2f} to {max(x):.2f} mm")
        col3.metric("Y Range", f"{min(y):.2f} to {max(y):.2f} mm")
        x, y, z = zip(*coords)
        
        # Create figure with white theme
        fig, ax = plt.subplots(figsize=(10, 8), facecolor='white')
        ax.set_facecolor('white')
        
        # Plot the toolpath with better styling
        ax.plot(x, y, color='#0066cc', linewidth=2, marker=None)
        
        # Starting point marker
        ax.scatter(x[0], y[0], color='#00aa00', s=100, marker='o', 
                   label='Start point', zorder=5)
        
        # Ending point marker
        ax.scatter(x[-1], y[-1], color='#cc0000', s=100, marker='x', 
                  label='End point', zorder=5)
        
        # Grid styling
        ax.grid(True, linestyle='--', alpha=0.5, color='#aaaaaa')
        
        # Labels and title styling
        ax.set_xlabel('X (mm)', color='black', fontsize=12)
        ax.set_ylabel('Y (mm)', color='black', fontsize=12)
        ax.set_title('Toolpath Visualization', color='black', fontsize=14, fontweight='bold')
        
        # Set equal aspect ratio to ensure circles look circular
        ax.set_aspect('equal')
        
        # Style tick labels
        ax.tick_params(colors='black', labelsize=10)
        
        # Add legend
        ax.legend(loc='upper right', facecolor='white', edgecolor='#aaaaaa')
        
        # Add coordinate system indicator
        ax.annotate('', xy=(1, 0), xytext=(0, 0), 
                   arrowprops=dict(facecolor='red', shrink=0, width=1.5, headwidth=8))
        ax.annotate('', xy=(0, 1), xytext=(0, 0), 
                   arrowprops=dict(facecolor='green', shrink=0, width=1.5, headwidth=8))
        ax.text(1.05, 0, 'X', color='red')
        ax.text(0, 1.05, 'Y', color='green')

        # Adjust layout
        plt.tight_layout()
        st.pyplot(fig)
    else:
        st.write("V súbore neboli nájdené žiadne pohyby G0/G1.")