import os
import base64
import streamlit as st
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage

def extract_text_from_image(image_bytes):
    """
    Uses Gemini 1.5 Flash to extract text from an uploaded image.
    """
    image_b64 = base64.b64encode(image_bytes).decode('utf-8')
    
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY")
    except Exception:
        api_key = None
    api_key = api_key or os.getenv("GOOGLE_API_KEY")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key, temperature=0.0)
    
    message = HumanMessage(
        content=[
            {"type": "text", "text": "Extract all the text from this email screenshot exactly as it appears. Do not add any extra commentary or markdown blocks. Just return the raw text."},
            {"type": "image_url", "image_url": f"data:image/jpeg;base64,{image_b64}"}
        ]
    )
    
    try:
        response = llm.invoke([message])
        return response.content
    except Exception as e:
        return f"Error extracting text: {e}"
