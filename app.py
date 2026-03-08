import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="28x28 Pixel Lab", layout="wide")

st.title("🔢 28x28 Pixel Visualizer")
st.write("Upload an image or draw a number to see its pixel matrix.")

# --- Sidebar Configuration ---
st.sidebar.header("Input Settings")
mode = st.sidebar.radio("Select Input Mode:", ("Draw a Number", "Upload Image"))

def process_image(img):
    """Convert any PIL image to 28x28 grayscale array."""
    img_gray = img.convert('L').resize((28, 28))
    return np.array(img_gray)

pixel_data = None

# --- Input Section ---
if mode == "Draw a Number":
    st.subheader("Draw on the canvas")
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
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
    st.subheader("Upload your image")
    uploaded_file = st.file_uploader("Choose a file...", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        raw_img = Image.open(uploaded_file)
        st.image(raw_img, caption="Original Uploaded Image", width=200)
        pixel_data = process_image(raw_img)

# --- Visualization Section ---
if pixel_data is not None:
    st.divider()
    col1, col2 = st.columns([1, 1])

    with col1:
        st.subheader("Heatmap Visualization")
        # px.imshow makes the 28x28 grid large and interactive
        fig = px.imshow(
            pixel_data, 
            color_continuous_scale='gray',
            labels=dict(x="Pixel X", y="Pixel Y", color="Brightness")
        )
        fig.update_layout(coloraxis_showscale=False, margin=dict(l=0, r=0, b=0, t=0))
        st.plotly_chart(fig, use_container_width=True)

    with col2:
        st.subheader("Raw Pixel Data (0-255)")
        df = pd.DataFrame(pixel_data)
        st.dataframe(df, height=350)

        # Download Logic
        csv = df.to_csv(index=False).encode('utf-8')
        st.download_button(
            label="📥 Download Pixel CSV",
            data=csv,
            file_name='pixel_data.csv',
            mime='text/csv',
        )
