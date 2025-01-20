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
            background-color: #4CAF50;
            color: white;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
            text-align: center;
            box-sizing: border-box;
        }
        .file-input-btn:hover {
            background-color: #45a049;
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
            margin-bottom: 20px;
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
        }
        .button-container button {
            padding: 12px 24px;
            font-size: 16px;
            border: none;
            border-radius: 8px;
            cursor: pointer;
            width: 100%;
        }
        .write-btn {
            background-color: #4CAF50;
            color: white;
        }
        .write-btn:hover {
            background-color: #45a049;
        }
        .upload-btn {
            background-color: #007bff;
            color: white;
        }
        .upload-btn:hover {
            background-color: #0056b3;
        }
        .summarize-btn {
            background-color: #e74c3c;
            color: white;
        }
        .summarize-btn:hover {
            background-color: #c0392b;
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
        });

        uploadBtn.addEventListener('click', function() {
            textArea.disabled = true;
            fileInput.disabled = false;
            fileLabel.disabled = false;
            uploadBtn.style.backgroundColor = "#0056b3";
            writeBtn.style.backgroundColor = "#4CAF50";
        });
    </script>
</body>
</html>