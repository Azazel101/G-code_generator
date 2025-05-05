import streamlit as st
import os
import ezdxf
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="G-Code Generator : DXF Vizualization",
    layout="wide",
    page_icon="🛠️",  # Tool emoji to represent toolpath/machining
)

path = os.path.dirname(__file__)

def plot_dxf(file_path):
    # Načítanie DXF súboru
    doc = ezdxf.readfile(file_path)
    msp = doc.modelspace()

    fig, ax = plt.subplots()
    for e in msp:
        if e.dxftype() == 'LINE':
            start = e.dxf.start
            end = e.dxf.end
            ax.plot([start[0], end[0]], [start[1], end[1]], 'b-')
        elif e.dxftype() == 'CIRCLE':
            center = e.dxf.center
            radius = e.dxf.radius
            circle = plt.Circle((center[0], center[1]), radius, fill=False, color='r')
            ax.add_patch(circle)
        # Pridajte ďalšie typy entít podľa potreby

    ax.set_aspect('equal')
    plt.axis('off')
    return fig

st.title("DXF Vizualization")

uploaded_file = st.file_uploader("Nahrajte DXF súbor", type=["dxf"])
if uploaded_file is not None:
    # Uložíme dočasne súbor, pretože ezdxf vyžaduje cestu k súboru
    with open("temp.dxf", "wb") as f:
        f.write(uploaded_file.getbuffer())

    fig = plot_dxf("temp.dxf")
    st.pyplot(fig)
