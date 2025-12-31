import streamlit as st
import google.generativeai as genai
from PIL import Image
import os

# 1. Configuration - Using Streamlit Secrets for security
# When running locally, this looks for a .streamlit/secrets.toml file
# When on the web, you'll enter this in the Streamlit Cloud dashboard
if "GOOGLE_API_KEY" in st.secrets:
    genai.configure(api_key=st.secrets["GOOGLE_API_KEY"])
else:
    # Fallback for local testing if you haven't set up secrets yet
    os.environ["GOOGLE_API_KEY"] = "YOUR_ACTUAL_API_KEY_HERE"
    genai.configure(api_key=os.environ["GOOGLE_API_KEY"])

# 2. Folder Setup - Ensure 'data' exists so the app doesn't crash
SAVE_DIR = "data"
if not os.path.exists(SAVE_DIR):
    os.makedirs(SAVE_DIR)

TCM_SYSTEM_PROMPT = """
You are an expert Traditional Chinese Medicine (TCM) practitioner. 
Analyze the provided tongue image step-by-step:
1. Tongue Color: (e.g., Pale, Red, Purple)
2. Coating Color & Thickness: (e.g., White, Yellow, Thin, Thick)
3. Shape/Features: (e.g., Swollen, Teeth marks, Cracks)

Based on this, provide a TCM Syndrome differentiation and recommend 
a standard herbal formula.
"""

BOILING_INSTRUCTIONS = """
---
**Standard Boiling Instructions:**
1. Soak herbs in cold water for 30 minutes.
2. Bring to a boil, then simmer for 40 minutes.
3. Strain and drink while warm.
"""

st.title("TCM Tongue Analysis Portal")
st.write("Please upload a clear photo of your tongue for analysis.")

uploaded_file = st.file_uploader("Choose a photo...", type=["jpg", "jpeg", "png"])

if uploaded_file is not None:
    image = Image.open(uploaded_file)
    st.image(image, caption='Uploaded Image', use_container_width=True)
    
    if st.button('Analyze and Prescribe'):
        with st.spinner('Analyzing tongue features...'):
            try:
                model = genai.GenerativeModel('gemini-1.5-flash')
                response = model.generate_content([TCM_SYSTEM_PROMPT, image])
                
                st.subheader("Analysis Results")
                st.markdown(response.text)
                
                st.subheader("Prescription & Instructions")
                st.info(BOILING_INSTRUCTIONS)
                
                # 3. Saving the file correctly
                save_path = os.path.join(SAVE_DIR, f"patient_{uploaded_file.name}")
                image.save(save_path)
                st.success(f"Record saved for doctor review.")
                
            except Exception as e:
                st.error(f"An error occurred: {e}")