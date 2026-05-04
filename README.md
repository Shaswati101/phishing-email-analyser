# Phishing Email Analyser with Voice Report

This project is a web application that allows users to paste or speak a suspicious email's content. The app analyses the email against a phishing pattern knowledge base using Retrieval-Augmented Generation (RAG). It then assigns a risk score and speaks the verdict back to the user.

## Features

- **Text or Image Input**: Paste the text of an email or upload a screenshot of it.
- **RAG-Powered Analysis**: Uses a custom knowledge base of phishing patterns embedded via `sentence-transformers` and searched using `FAISS`.
- **Advanced LLM**: Leverages Google's Gemini 1.5 Flash to analyze the email against the retrieved context.
- **Risk Assessment**: Provides a color-coded badge, risk score (0-100), and detailed breakdown of indicators found and not found.
- **Voice Verdict**: Reads back the verdict and recommendation using `gTTS`.

## Project Structure

- `app.py`: Main Streamlit app.
- `rag_pipeline.py`: LangChain RAG logic (embed, store, retrieve).
- `asr.py`: SpeechRecognition logic (audio to text).
- `tts.py`: gTTS logic (text to audio).
- `risk_scorer.py`: Risk score display logic.
- `phishing_knowledge_base.txt`: Phishing pattern knowledge base.
- `.env`: Environment variables (API keys).
- `requirements.txt`: Project dependencies.

## Installation & Setup

1. Create a virtual environment and activate it:
   ```bash
   python -m venv .venv
   .\.venv\Scripts\activate
   ```

2. Install the requirements:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up the API key:
   - Edit the `.env` file and replace `your_gemini_api_key_here` with your actual Google Gemini API key.

## Usage

1. Run the Streamlit app:
   ```bash
   streamlit run app.py
   ```

2. Follow the on-screen instructions to paste or speak the suspicious email content.
3. Click **Analyse Email** to view the report and hear the voice verdict.
