import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="28x28 Pixel Lab", layout="wide")

st.title("🔢 28x28 Pixel Visualizer & Flattener")
st.write("Draw or upload to get a **single line** of 784 pixel values.")

# --- Sidebar Configuration ---
st.sidebar.header("Settings")
mode = st.sidebar.radio("Input Mode:", ("Draw a Number", "Upload Image"))

def process_image(img):
    """Convert any PIL image to 28x28 grayscale array."""
    img_gray = img.convert('L').resize((28, 28))
    return np.array(img_gray)

pixel_data = None

# --- Input Section ---
if mode == "Draw a Number":
    st.subheader("Draw on the 280x280 Canvas")
    canvas_result = st_canvas(
        stroke_width=20,
        stroke_color="#FFFFFF",
        background_color="#000000",
        height=280,
        width=280,
        drawing_mode="freedraw",
        key="canvas",
    )
    if canvas_result.image_data is not None:
        raw_img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
        pixel_data = process_image(raw_img)

else:
    st.subheader("Upload Image")
    uploaded_file = st.file_uploader("Choose a file...", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        raw_img = Image.open(uploaded_file)
        pixel_data = process_image(raw_img)

# --- Processing & Output ---
if pixel_data is not None:
    st.divider()
    
    # 1. FLATTEN THE DATA
    # Reshape from (28, 28) to (1, 784)
    flattened_row = pixel_data.reshape(1, -1)
    flattened_df = pd.DataFrame(flattened_row)

    # 2. SHOW THE SINGLE LINE
    st.subheader("Raw Pixel Line (1 x 784)")
    st.write("This single row represents your entire image for a Neural Network:")
    st.dataframe(flattened_df, hide_index=True)

    # 3. VISUALIZATION
    col1, col2 = st.columns([1, 1])
    with col1:
        st.subheader("Heatmap View")
        fig = px.imshow(pixel_data, color_continuous_scale='gray')
        fig.update_layout(coloraxis_showscale=False, margin=dict(l=0, r=0, b=0, t=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Download Options")
        # CSV of the flattened row
        csv_flat = flattened_df.to_csv(index=False, header=False).encode('utf-8')
        st.download_button(
            label="📥 Download Single-Line CSV",
            data=csv_flat,
            file_name='flattened_pixels.csv',
            mime='text/csv',
        )
