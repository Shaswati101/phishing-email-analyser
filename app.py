import streamlit as st
from dotenv import load_dotenv
import os
import time

from rag_pipeline import init_vector_store, analyze_email
from image_ocr import extract_text_from_image
from tts import generate_audio_base64
from risk_scorer import parse_and_display_risk

# Load environment variables
load_dotenv()

# Streamlit config
st.set_page_config(page_title="Phishing Email Analyser", page_icon="🎣")

# Sidebar
st.sidebar.title("Phishing Email Analyser")
st.sidebar.markdown("""
A cybersecurity tool to analyze suspicious emails and detect phishing patterns.

**How to use:**
1. Choose to either **Paste** or **Upload Screenshot** of your email content.
2. Provide the email text or record audio.
3. Click **Analyse Email** to get a risk assessment and voice verdict.
""")

# Initialize FAISS vector store in session state
if "vector_store" not in st.session_state:
    try:
        st.session_state.vector_store = init_vector_store()
    except Exception as e:
        st.error(f"Error initializing knowledge base: {e}")
        st.stop()

# Main area - 4 clear sections
st.title("Phishing Email Analyser")

# 1. Email Input
st.header("1. Email Input")
input_mode = st.radio("Choose input mode:", ["Paste Email", "Upload Screenshot"])

email_content = ""

if input_mode == "Paste Email":
    email_content = st.text_area("Paste the suspicious email content here:", height=200)
else:
    st.write("Upload a screenshot of the email:")
    uploaded_file = st.file_uploader("Choose an image", type=["png", "jpg", "jpeg"])
    
    if uploaded_file is not None:
        st.image(uploaded_file, caption="Uploaded Screenshot", use_container_width=True)
        with st.spinner("Extracting text from image..."):
            extracted_text = extract_text_from_image(uploaded_file.getvalue())
            
        if extracted_text.startswith("Error"):
            st.error(extracted_text)
        else:
            st.success("Text extraction complete!")
            st.write("**Extracted Text:**")
            st.write(extracted_text)
            email_content = extracted_text

# 2. Analysis
st.header("2. Analysis")
if st.button("Analyse Email"):
    if not email_content.strip():
        st.warning("Please provide an email to analyse.")
    else:
        with st.spinner("Analysing email for phishing indicators..."):
            try:
                # 3. Risk Assessment
                json_response = analyze_email(st.session_state.vector_store, email_content)
                
                st.header("3. Risk Assessment")
                parsed_data = parse_and_display_risk(json_response)
                
                # 4. Voice Verdict
                if parsed_data:
                    st.header("4. Voice Verdict")
                    verdict_text = f"{parsed_data.get('verdict', '')} {parsed_data.get('recommendation', '')}"
                    
                    audio_b64 = generate_audio_base64(verdict_text)
                    if audio_b64:
                        st.markdown(
                            f'<audio autoplay="true" controls="true"><source src="data:audio/mp3;base64,{audio_b64}" type="audio/mp3"></audio>',
                            unsafe_allow_html=True,
                        )
                    else:
                        st.write("*(Voice verdict could not be generated)*")
                        
            except Exception as e:
                st.error("Analysis failed. Please try again.")
                st.write(f"Error details: {e}")
