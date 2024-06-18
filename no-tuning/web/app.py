from flask import Flask, render_template, request
from transformers import logging, T5Tokenizer, T5ForConditionalGeneration
from pypdf import PdfReader
import docx
import torch
from simplify_docx import simplify

logging.set_verbosity_error()

def create_t5_tokenizer(model_name="t5-base"):
    return T5Tokenizer.from_pretrained(model_name)

def create_t5_summarizer(model_name="t5-base", device=None):
    model = T5ForConditionalGeneration.from_pretrained(model_name)
    if device:
        model = model.to(device)
    return model

def break_text_in_sequences(tokenizer, text, max_length_sequence):
    words = text.split()
    current_chunk = 1
    chunks = ['']
    for word in words:
        if len(tokenizer.encode(chunks[current_chunk - 1] + ' ' + word, add_special_tokens=True)) > max_length_sequence:
            current_chunk += 1
            chunks.append(word)
        else:
            chunks[current_chunk - 1] += ' ' + word
    chunks = [chunk.strip() for chunk in chunks]
    return chunks

def concat_summaries(summarizer, text_segments, tokenizer, max_length=512, num_beams=4, early_stopping=True):
    final_summary = ""
    for segment in text_segments:
        input_ids = tokenizer.encode(segment, return_tensors="pt")
        output = summarizer.generate(
            input_ids,
            max_length=max_length,
            num_beams=num_beams,
            early_stopping=early_stopping
        )
        summary = tokenizer.decode(output[0], skip_special_tokens=True)
        final_summary += summary
    return final_summary

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/summarize', methods=['POST'])
def summarize():
    input_text = request.form['input_text']
    max_length = int(request.form['max_length'])

    tokenizer = create_t5_tokenizer()
    processed_text = break_text_in_sequences(tokenizer, input_text, 1024)
    summarizer = create_t5_summarizer(model_name="t5-base", device="cuda" if torch.cuda.is_available() else "cpu")
    final_summary = concat_summaries(summarizer, processed_text, tokenizer, max_length=max_length)

    return final_summary

if __name__ == '__main__':
    app.run(debug=True)