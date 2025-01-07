from flask import Flask, request, render_template_string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Download required nltk data files
nltk.download('punkt')
nltk.download('stopwords')

# Flask app setup
app = Flask(__name__)

# HTML template for file upload
UPLOAD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Text Summarizer</title>
</head>
<body>
    <h1>Upload Your Text File for Summarization</h1>
    <form action="/" method="POST" enctype="multipart/form-data">
        <input type="file" name="file" accept=".txt" required>
        <button type="submit">Summarize</button>
    </form>
    {% if summary %}
    <h2>Summary:</h2>
    <p>{{ summary }}</p>
    {% endif %}
</body>
</html>
"""

def summarize_text(text):
    # Tokenize text into sentences
    sentences = sent_tokenize(text)

    # Tokenize text into words and remove stopwords
    stop_words = set(stopwords.words('english'))
    words = word_tokenize(text.lower())
    filtered_words = [word for word in words if word.isalnum() and word not in stop_words]

    # Calculate word frequencies
    word_frequencies = {}
    for word in filtered_words:
        if word not in word_frequencies:
            word_frequencies[word] = 1
        else:
            word_frequencies[word] += 1

    # Calculate sentence scores based on word frequencies
    sentence_scores = {}
    for sentence in sentences:
        sentence_tokens = word_tokenize(sentence.lower())
        sentence_score = 0
        for word in sentence_tokens:
            if word in word_frequencies:
                sentence_score += word_frequencies[word]
        sentence_scores[sentence] = sentence_score

    # Sort sentences based on scores
    sorted_sentences = sorted(sentence_scores, key=sentence_scores.get, reverse=True)

    # Select top 3 sentences for summary
    summary = ' '.join(sorted_sentences[:3])

    return summary

@app.route("/", methods=["GET", "POST"])
def upload_file():
    summary = None
    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file.filename.endswith(".txt"):
            # Read the file content
            text = uploaded_file.read().decode("utf-8")
            # Generate summary
            summary = summarize_text(text)
        else:
            summary = "Error: Please upload a valid .txt file."

    return render_template_string(UPLOAD_HTML, summary=summary)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)