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
            font-family: Arial, sans-serif;
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
            color: #5e5e5e;
            margin-bottom: 20px;
            text-align: center;
        }
        .container {
            width: 80%;
            max-width: 600px;
            margin-top: 30px;
            padding: 30px;
            background-color: #fff;
            border-radius: 8px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        form {
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        /* Custom file upload button */
        .file-input-container {
            position: relative;
            margin-bottom: 20px;
            width: 100%;
            display: flex;
            flex-direction: column;
            align-items: center;
        }
        .file-input-container input[type="file"] {
            display: none;
        }
        .file-input-btn {
            padding: 12px 24px;
            font-size: 16px;
            background-color: #007bff;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
            text-align: center;
            box-sizing: border-box;
        }
        .file-input-btn:hover {
            background-color: #0056b3;
        }
        .file-name {
            display: block;
            margin-top: 10px;
            color: #666;
            text-align: center;
        }
        /* Textarea */
        .text-area {
            width: 100%;
            height: 200px;
            padding: 10px;
            margin: 10px 0;
            border-radius: 8px;
            border: 1px solid #ccc;
            font-size: 16px;
            resize: vertical;
        }
        /* Button Container */
        .button-container {
            display: flex;
            gap: 10px;
            margin-bottom: 20px;
            justify-content: center;
        }
        .button-container button {
            padding: 12px 24px;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
            transition: background-color 0.3s ease;
        }
        .write-btn, .upload-btn {
            background-color: #4CAF50;
            color: white;
        }
        .write-btn:hover, .upload-btn:hover {
            background-color: #8e24aa;
        }
        .summarize-btn {
            background-color: #ff9800;
            color: white;
            font-size: 18px;
            padding: 14px 28px;
            width: 50%;
            border-radius: 10px;
            border: none;
            margin-top: 20px;
        }
        .summarize-btn:hover {
            background-color: #f57c00;
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
        .or-divider {
            margin: 20px 0;
            font-size: 18px;
            color: #888;
        }
        /* Responsive design */
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
            <div class="button-container">
                <button type="button" id="write-text" class="write-btn">Write Text</button>
                <span class="or-divider">OR</span>
                <button type="button" id="upload-file" class="upload-btn">Upload File</button>
            </div>
            <div class="file-input-container">
                <input type="file" name="file" accept=".txt" id="file-upload" disabled required>
                <label for="file-upload" class="file-input-btn" id="file-label">Choose File</label>
                <span class="file-name" id="file-name">No file selected</span>
            </div>
            <textarea class="text-area" name="text" id="text-input" placeholder="Write your text here" disabled></textarea>
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
        // Update file name label when a file is selected
        const fileInput = document.getElementById('file-upload');
        const fileNameLabel = document.getElementById('file-name');
        const textArea = document.getElementById('text-input');
        const writeBtn = document.getElementById('write-text');
        const uploadBtn = document.getElementById('upload-file');
        const fileLabel = document.getElementById('file-label');
        
        fileInput.addEventListener('change', function() {
            const fileName = this.files.length ? this.files[0].name : 'No file selected';
            fileNameLabel.textContent = fileName;
        });

        // Toggle between write text and upload file options
        writeBtn.addEventListener('click', function() {
            textArea.disabled = false;
            fileInput.disabled = true;
            fileLabel.disabled = true;
            writeBtn.style.backgroundColor = "#45a049";
            uploadBtn.style.backgroundColor = "#007bff";
            uploadBtn.style.opacity = 0.5;
        });

        uploadBtn.addEventListener('click', function() {
            textArea.disabled = true;
            fileInput.disabled = false;
            fileLabel.disabled = false;
            uploadBtn.style.backgroundColor = "#45a049";
            writeBtn.style.backgroundColor = "#4CAF50";
            writeBtn.style.opacity = 0.5;
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
        uploaded_file = request.files.get("file")
        if uploaded_file and uploaded_file.filename.endswith(".txt"):
            # Read the file content
            text = uploaded_file.read().decode("utf-8")
            # Generate summary
            summary = summarize_text(text)
        elif request.form.get("text"):
            text = request.form.get("text")
            summary = summarize_text(text)
        else:
            summary = "Error: Please upload a valid .txt file or enter text."

    return render_template_string(UPLOAD_HTML, summary=summary)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)