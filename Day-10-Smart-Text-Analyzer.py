# Day 10 - Smart Text Analyzer

import string

print("================================")
print("       SMART TEXT ANALYZER")
print("================================")

# Get text from the user
print("\nPaste or type the text you want to analyze:")
text = input(">> ")


# Clean and prepare the text
clean_text = text.lower()
clean_text = clean_text.translate(
    str.maketrans("", "", string.punctuation)
)

words = clean_text.split()


# Calculate basic text statistics
total_characters = len(text)
total_words = len(words)
total_sentences = text.count(".") + text.count("!") + text.count("?")

unique_words = set(words)
total_unique_words = len(unique_words)


# Calculate word frequency
word_frequency = {}

for word in words:
    word_frequency[word] = words.count(word)


# Find the most frequent word
most_frequent_word = max(word_frequency, key=word_frequency.get)
highest_frequency = word_frequency[most_frequent_word]


# Find the longest word
longest_word = max(words, key=len)
longest_word_length = len(longest_word)


# Display the analysis report
print("\n================================")
print("       TEXT ANALYSIS REPORT")
print("================================")

print("Total Characters    :", total_characters)
print("Total Words         :", total_words)
print("Total Sentences     :", total_sentences)
print("Unique Words        :", total_unique_words)
print("Most Frequent Word  :", most_frequent_word)
print("Word Frequency      :", highest_frequency)
print("Longest Word        :", longest_word)
print("Longest Word Length :", longest_word_length)

print("================================")
