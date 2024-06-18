document.getElementById('summarizeBtn').addEventListener('click', function() {
    const inputText = document.getElementById('inputText').value;
    const outputText = summarizeText(inputText);
    document.getElementById('outputText').innerText = outputText;
});

document.getElementById('clearBtn').addEventListener('click', function() {
    document.getElementById('inputText').value = '';
    document.getElementById('outputText').innerText = '';
});

function summarizeText(text) {
    // Basic text summarization logic (this should be replaced with a real algorithm)
    const sentences = text.split('. ');
    const summary = sentences.slice(0, Math.ceil(sentences.length / 2)).join('. ') + '.';
    return summary;
}
