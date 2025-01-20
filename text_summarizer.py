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
            border-radius: 25px;
            cursor: pointer;
            width: 100%;
            box-sizing: border-box;
            margin: 10px 0;
            transition: background-color 0.3s;
        }
        .curvy-btn:hover {
            background-color: #3f4c9d;
        }
        /* Disabled button */
        .disabled-btn {
            background-color: #B0BEC5;
            cursor: not-allowed;
        }
        /* Separator with "OR" */
        .separator {
            margin: 10px 0;
            color: #777;
            font-size: 18px;
        }
        /* Custom file upload */
        .file-input-container {
            position: relative;
            margin-bottom: 20px;
            width: 100%;
            text-align: left;
        }
        .file-input-container input[type="file"] {
            display: none;
        }
        .file-input-btn {
            padding: 12px 24px;
            font-size: 16px;
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            width: 100%;
            text-align: center;
        }
        .file-input-btn:hover {
            background-color: #45a049;
        }
        .file-name {
            display: block;
            margin-top: 10px;
            color: #666;
            font-size: 16px;
        }
        /* Summarize button color (red) */
        .summarize-btn {
            padding: 14px 28px;
            font-size: 16px;
            background-color: #E57373;
            color: white;
            border: none;
            border-radius: 25px;
            cursor: pointer;
            margin-top: 20px;
        }
        .summarize-btn:hover {
            background-color: #EF5350;
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
        @media (max-width: 768px) {
            .container {
                width: 90%;
                padding: 20px;
            }
            h1 {
                font-size: 24px;
            }
        }
        @media (max-width: 480px) {
            .container {
                width: 95%;
                padding: 15px;
            }
            h1 {
                font-size: 20px;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>Text Summarizer</h1>
        <form action="/" method="POST" enctype="multipart/form-data">
            <div>
                <button type="button" class="curvy-btn" id="write-text-btn" onclick="selectOption('write')">Write Text</button>
                <span class="separator">OR</span>
                <button type="button" class="curvy-btn" id="upload-file-btn" onclick="selectOption('upload')">Upload File</button>
            </div>
            <div id="write-text-container" style="display:none;">
                <textarea name="text" rows="6" placeholder="Write your text here..."></textarea>
            </div>
            <div id="upload-file-container" style="display:none;">
                <div class="file-input-container">
                    <input type="file" name="file" accept=".txt" id="file-upload" required>
                    <label for="file-upload" class="file-input-btn">Choose File</label>
                    <span class="file-name" id="file-name">No file selected</span>
                </div>
            </div>
            <button type="submit" class="summarize-btn">Summarize</button>
        </form>
        {% if summary %}
        <h2>Summary:</h2>
        <p>{{ summary }}</p>
        {% elif summary == "Error: Please upload a valid .txt file." %}
        <p class="error">{{ summary }}</p>
        {% endif %}
    </div>

    <script>
        let selectedOption = null;

        function selectOption(option) {
            if (option === 'write') {
                document.getElementById('write-text-btn').classList.add('disabled-btn');
                document.getElementById('upload-file-btn').classList.remove('disabled-btn');
                document.getElementById('write-text-container').style.display = 'block';
                document.getElementById('upload-file-container').style.display = 'none';
                selectedOption = 'write';
            } else if (option === 'upload') {
                document.getElementById('upload-file-btn').classList.add('disabled-btn');
                document.getElementById('write-text-btn').classList.remove('disabled-btn');
                document.getElementById('upload-file-container').style.display = 'block';
                document.getElementById('write-text-container').style.display = 'none';
                selectedOption = 'upload';
            }
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
        if 'text' in request.form:
            # Process written text
            text = request.form['text']
            summary = summarize_text(text)
        elif 'file' in request.files:
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