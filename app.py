import streamlit as st

st.set_page_config(page_title="My IT & AI Portfolio", layout="wide")

st.title("Main Project Hub")
st.write("Welcome! Use the **sidebar on the left** to switch between my different tools.")

st.sidebar.success("Select a tool above.")

st.markdown("""
### 🛠️ Featured Tools:
* **Pixel Visualizer**: Interactive 28x28 grid for Neural Network inputs.
* **Infra Dashboard**: Automated analysis of IT Incident dumps (Link, Agent, Storage).
""")
