import nltk
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize, sent_tokenize

# Download required nltk data files
nltk.download('punkt')
nltk.download('stopwords')

def summarize_text(file_path):
    # Read the input file
    with open(file_path, 'r') as file:
        text = file.read()

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

if __name__ == "__main__":
    # Replace command-line argument with user input
    file_path = input("Enter the path to your text file (e.g., sample_text.txt): ")

    try:
        summary = summarize_text(file_path)
        print("\nSummary:")
        print(summary)
    except FileNotFoundError:
        print("Error: File not found. Please check the file path and try again.")