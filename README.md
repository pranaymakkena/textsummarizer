# Text Summarizer

Text Summarizer summarizes a given text using the Natural Language Toolkit (nltk) in Python.

## Prerequisites

- Python 3.x
- nlkt library

## Installation

1. Clone or download this repository.
2. Install the required libraries using the following command:
~~~bash
pip install -r requirements.txt
~~~
3. Make sure to download the necessary NLTK resources by running the following in a Python shell:
~~~bash
import nltk
nltk.download('punkt')
nltk.download('stopwords')
~~~

## Usage

1.	Place your text file (e.g., your_text_file.txt) in the project folder.
2.	Run the text_summarizer.py script to summarize the content of your file:
~~~bash
python text_summarizer.py <your_text_file.txt>
~~~ 
3. The script will output a summary of the text to the console.