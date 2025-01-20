from flask import Flask, request, render_template_string
import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Download required nltk data files
nltk.download('punkt')
nltk.download('stopwords')

# Flask app setup
app = Flask(__name__)

# HTML template for file upload with stylish components
UPLOAD_HTML = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Text Summarizer</title>
    <style>
        body {
            font-family: 'Arial', sans-serif;
            background-color: #f4f7fc;
            color: #333;
            margin: 0;
            padding: 0;
            height: 100%;
            display: flex;
            justify-content: center;
            align-items: center;
        }
        h1 {
            color: #333;
            margin-bottom: 20px;
            font-size: 28px;
        }
        .container {
            width: 80%;
            max-width: 600px;
            margin-top: 30px;
            padding: 30px;
            background-color: #fff;
            border-radius: 12px;
            box-shadow: 0 6px 12px rgba(0, 0, 0, 0.1);
            text-align: center;
        }
        form {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        /* Curvy border buttons */
        .curvy-btn {
            padding: 14px 28px;
            font-size: 16px;
            background-color: #5C6BC0;
            color: white;
            border: none;
            border-radius: 30px;
            cursor: pointer;
            width: 100%;
            box-sizing: border-box;
            transition: background-color 0.3s ease;
            margin: 10px 0;
        }
        .curvy-btn:hover {
            background-color: #3f4b8a;
        }
        /* File upload container */
        .file-input-container {
            position: relative;
            margin-bottom: 20px;
            width: 100%;
        }
        .file-input-container input[type="file"] {
            display: none;
        }
        .file-input-btn {
            padding: 14px 28px;
            font-size: 16px;
            background-color: #FF8A65;
            color: white;
            border: none;
            border-radius: 30px;
            cursor: pointer;
            width: 100%;
            box-sizing: border-box;
            text-align: center;
            transition: background-color 0.3s ease;
        }
        .file-input-btn:hover {
            background-color: #FF7043;
        }
        .file-name {
            display: block;
            margin-top: 10px;
            color: #666;
            font-size: 14px;
        }
        h2 {
            color: #333;
            margin-top: 20px;
        }
        p {
            font-size: 18px;
            line-height: 1.6;
            color: #444;
        }
        .error {
            color: red;
            font-size: 16px;
        }
        /* Textarea styling */
        textarea {
            width: 100%;
            padding: 12px;
            border-radius: 10px;
            border: 1px solid #ddd;
            font-size: 16px;
            box-sizing: border-box;
            margin-top: 10px;
        }
        /* Responsive design */
        @media (max-width: 768px) {
            .container {
                width: 90%;
                padding: 25px;
            }
            h1 {
                font-size: 26px;
            }
        }
        @media (max-width: 480px) {
            .container {
                width: 95%;
                padding: 20px;
            }
            h1 {
                font-size: 22px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Text Summarizer</h1>
        <form action="/" method="POST" enctype="multipart/form-data">
            <!-- Option Buttons to choose between writing text or uploading file -->
            <div class="option-buttons" style="width: 100%;">
                <button type="button" class="curvy-btn" onclick="showTextInput()">Write Text</button>
                <button type="button" class="curvy-btn" onclick="showFileInput()">Upload File</button>
            </div>

            <!-- Text input field (initially hidden) -->
            <div id="text-input-container" style="display:none; width: 100%; margin-top: 20px;">
                <textarea name="text" id="text-input" rows="6" placeholder="Write your text here..."></textarea>
            </div>

            <!-- File upload input (initially hidden) -->
            <div id="file-input-container" style="display:none; width: 100%; margin-top: 20px;">
                <div class="file-input-container">
                    <input type="file" name="file" accept=".txt" id="file-upload" required>
                    <label for="file-upload" class="file-input-btn">Choose File</label>
                    <span class="file-name" id="file-name">No file selected</span>
                </div>
            </div>

            <!-- Summarize button -->
            <button type="submit" class="curvy-btn">Summarize</button>
        </form>

        <!-- Display summary or error -->
        {% if summary %}
        <h2>Summary:</h2>
        <p>{{ summary }}</p>
        {% elif summary == "Error: Please upload a valid .txt file." %}
        <p class="error">{{ summary }}</p>
        {% endif %}
    </div>

    <script>
        function showTextInput() {
            document.getElementById('text-input-container').style.display = 'block';
            document.getElementById('file-input-container').style.display = 'none';
        }

        function showFileInput() {
            document.getElementById('file-input-container').style.display = 'block';
            document.getElementById('text-input-container').style.display = 'none';
        }

        // Update file name label when a file is selected
        const fileInput = document.getElementById('file-upload');
        const fileNameLabel = document.getElementById('file-name');
        
        fileInput.addEventListener('change', function() {
            const fileName = this.files.length ? this.files[0].name : 'No file selected';
            fileNameLabel.textContent = fileName;
        });
    </script>
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
        if "text" in request.form:
            text = request.form["text"]
            summary = summarize_text(text)
        elif "file" in request.files:
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