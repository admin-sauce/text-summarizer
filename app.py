import streamlit as st
from transformers import AutoTokenizer, AutoModelForSeq2SeqLM
from transformers import pipeline

@st.cache_resource
def load_model():
    model_name = "admin-sauce/t5-summerizer"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSeq2SeqLM.from_pretrained(model_name)
    summarizer = pipeline("summarization", model=model, tokenizer=tokenizer)
    return summarizer

summarizer = load_model()

st.title("Text Summarization App")

input_text = st.text_area("Enter text to summarize", height=200)

if st.button("Summarize"):
    prefix = "summarize: "
    input_ids = summarizer.tokenizer.encode(prefix + input_text, return_tensors="pt")
    summary_ids = summarizer.model.generate(input_ids)
    summary = summarizer.tokenizer.decode(summary_ids[0], skip_special_tokens=True)
    st.success(summary)