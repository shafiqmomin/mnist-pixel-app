import streamlit as st
from streamlit_drawable_canvas import st_canvas
from PIL import Image
import numpy as np
import pandas as pd
import io

st.set_page_config(page_title="28x28 Pixel Lab", layout="centered")
st.title("🔢 28x28 Image & Drawing Processor")

# 1. Sidebar Selection
option = st.sidebar.radio("Input Method", ("Draw Number", "Upload Image"))

def process_to_28x28(img_input):
    """Resizes and converts any image input to a 28x28 grayscale array."""
    # Convert to grayscale ('L' mode) and resize
    img_resized = img_input.convert('L').resize((28, 28))
    return np.array(img_resized)

# 2. Input Logic
pixel_data = None

if option == "Draw Number":
    st.subheader("Draw a digit (0-9)")
    canvas_result = st_canvas(
        stroke_width=18,
        stroke_color="#FFFFFF",
        background_color="#000000",
        height=280,
        width=280,
        drawing_mode="freedraw",
        key="canvas",
    )
    if canvas_result.image_data is not None:
        # Canvas data is RGBA, convert to PIL
        raw_img = Image.fromarray(canvas_result.image_data.astype('uint8'), 'RGBA')
        pixel_data = process_to_28x28(raw_img)

else:
    st.subheader("Upload an image")
    uploaded_file = st.file_uploader("Choose a file...", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        raw_img = Image.open(uploaded_file)
        pixel_data = process_to_28x28(raw_img)
        st.image(raw_img, caption="Original Upload", width=200)

# 3. Visualization & Download
if pixel_data is not None:
    st.divider()
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Processed 28x28 View**")
        # Upscale slightly for visibility in browser
        st.image(pixel_data, width=150)
        
    with col2:
        st.write("**Pixel Matrix**")
        df = pd.DataFrame(pixel_data)
        st.dataframe(df, height=150)

    # Download Button
    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="📥 Download 28x28 Pixel CSV",
        data=csv,
        file_name='digit_data.csv',
        mime='text/csv',
    )
