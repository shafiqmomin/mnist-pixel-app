import streamlit as st
import numpy as np
import pandas as pd
from PIL import Image
import io

st.title("🔢 Neural Network Pixel Visualizer")

# Sidebar for Input Method
option = st.sidebar.selectbox("Choose Input Method", ("Upload Image", "Manual Number Entry"))

def process_image(img):
    # Resize to 28x28 and convert to grayscale
    img = img.convert('L').resize((28, 28))
    return np.array(img)

grid_data = np.zeros((28, 28))

if option == "Upload Image":
    uploaded_file = st.file_uploader("Upload a digit image...", type=["jpg", "png", "jpeg"])
    if uploaded_file:
        image = Image.open(uploaded_file)
        grid_data = process_image(image)

else:
    val = st.number_input("Enter a brightness value (0-255) for a sample pattern:", 0, 255, 100)
    # Create a simple diagonal pattern for visualization
    grid_data = np.eye(28) * val

# Pixel Visualization
st.subheader("28 x 28 Pixel Grid")
st.image(grid_data, width=300, caption="Rescaled 28x28 Input")

# Show raw pixel values as a dataframe
if st.checkbox("Show Raw Pixel Data"):
    st.write(pd.DataFrame(grid_data))

# Download Option
df = pd.DataFrame(grid_data)
csv = df.to_csv(index=False).encode('utf-8')
st.download_button(
    label="Download Pixel Data as CSV",
    data=csv,
    file_name='pixel_data.csv',
    mime='text/csv',
)
