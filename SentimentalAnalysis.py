import re
import pandas as pd
import nltk
import matplotlib.pyplot as plt
from nltk.sentiment.vader import SentimentIntensityAnalyzer
!pip install pandas nltk matplotlib
nltk.download('vader_lexicon')

def clean_and_extract_messages(input_file_path, output_file_path):
    with open(input_file_path, 'r', encoding="utf-8") as input_file:
        with open(output_file_path, 'w', encoding="utf-8") as output_file:
            lines = input_file.readlines()
            for line in lines:
                if re.match(r'^\d+/\d+/\d+, \d+:\d+ [AP]M - ', line):
                    pass
                else:
                    clean_line = re.sub(r'^.*M - ', '', line)
                    output_file.write(clean_line)


def visualize_sentiment_distribution(sentiments):
    sentiment_counts = pd.Series(sentiments).value_counts()
    labels = sentiment_counts.index
    sizes = sentiment_counts.values
    colors = ['red', 'blue', 'green']
    plt.pie(sizes, labels=labels, colors=colors, autopct='%1.1f%%', startangle=140)
    plt.axis('equal')
    plt.title('Sentiment Distribution')
    plt.show()


def calculate_repeated_words(messages):
    words = ' '.join(messages).split()
    word_counts = pd.Series(words).value_counts()
    return word_counts[word_counts > 1]


def count_sentiment(sentiments):
    sentiment_counts = pd.Series(sentiments).value_counts()
    return sentiment_counts


def main():
    input_file_path = 'chat.txt'
    output_file_path = 'clean.txt'
    clean_and_extract_messages(input_file_path, output_file_path)
    with open(output_file_path, 'r', encoding='utf-8') as file:
        whatsapp_messages = file.readlines()

    # Sentiment analysis
    sia = SentimentIntensityAnalyzer()
    sentiments = []
    for message in whatsapp_messages:
        sentiment_score = sia.polarity_scores(message)
        if sentiment_score['compound'] > 0.05:
            sentiment = 'positive'
        elif sentiment_score['compound'] < -0.05:
            sentiment = 'negative'
        else:
            sentiment = 'neutral'
        sentiments.append(sentiment)

    repeated_words = calculate_repeated_words(whatsapp_messages)
    print("Repeated Words:")
    print(repeated_words)

    sentiment_counts = count_sentiment(sentiments)
    sentiment_df = pd.DataFrame({'Sentiment': sentiment_counts.index, 'Count': sentiment_counts.values})

    visualize_sentiment_distribution(sentiments)

    print("\nSentiment Counts:")
    print(sentiment_df)


if __name__ == "__main__":
    main()
