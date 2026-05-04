import os
import streamlit as st
from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate

def init_vector_store():
    # Load knowledge base
    loader = TextLoader("phishing_knowledge_base.txt", encoding="utf-8")
    documents = loader.load()
    
    # Split into chunks
    text_splitter = CharacterTextSplitter(chunk_size=200, chunk_overlap=50, separator="\n")
    docs = text_splitter.split_documents(documents)
    
    # Embeddings
    embeddings = HuggingFaceEmbeddings(model_name="paraphrase-multilingual-MiniLM-L12-v2")
    
    # FAISS vector store
    vector_store = FAISS.from_documents(docs, embeddings)
    return vector_store

def analyze_email(vector_store, email_content):
    # Retrieve top 4 most relevant chunks
    retriever = vector_store.as_retriever(search_kwargs={"k": 4})
    retrieved_docs = retriever.invoke(email_content)
    context = "\n".join([doc.page_content for doc in retrieved_docs])
    
    # Gemini Prompt
    template = """You are a cybersecurity expert specialising in phishing detection. Analyse the email content provided below against the phishing patterns in the context. Identify which phishing indicators are present and which are absent. Assign a risk score between 0 and 100 based on severity. Respond ONLY with a valid JSON object — no preamble, no markdown backticks.

Context (phishing patterns): {context}
Email content to analyse: {email_content}

Return this exact JSON structure:
{{
  "risk_level": "Low" | "Medium" | "High",
  "risk_score": <integer 0-100>,
  "indicators_found": [<list of phishing indicators detected>],
  "indicators_not_found": [<list of safe indicators present>],
  "verdict": "<2-3 sentence plain English verdict>",
  "recommendation": "<1 sentence action recommendation>"
}}"""

    prompt = PromptTemplate(template=template, input_variables=["context", "email_content"])
    
    # LLM
    try:
        api_key = st.secrets.get("GOOGLE_API_KEY")
    except Exception:
        api_key = None
    api_key = api_key or os.getenv("GOOGLE_API_KEY")
    llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash", google_api_key=api_key, temperature=0.0)
    
    chain = prompt | llm
    response = chain.invoke({"context": context, "email_content": email_content})
    return response.content
