# Day 11 - Keyword Extractor

import string

print("================================")
print("       KEYWORD EXTRACTOR")
print("================================")

# Get text from the user
print("\nEnter the text you want to analyze:")
text = input(">> ")

clean_text = text.lower()
clean_text = clean_text.translate(
    str.maketrans("", "", string.punctuation)
)

words = clean_text.split()

# Common words to ignore
stop_words = [
    "is", "the", "a", "an", "and", "are",
    "to", "in", "of", "for", "on", "with"
]
filtered_words = []

for word in words:
    if word not in stop_words:
        filtered_words.append(word)

# Count keyword frequency
word_frequency = {}

for word in filtered_words:
    if word in word_frequency:
        word_frequency[word] = word_frequency[word] + 1
    else:
        word_frequency[word] = 1

# Sort keywords by frequency
sorted_keywords = sorted(
    word_frequency.items(),
    key=lambda item: item[1],
    reverse=True
)

# Select top 5 keywords
top_keywords = sorted_keywords[:5]

# Display the keyword report
print("\n================================")
print("       KEYWORD EXTRACTOR")
print("================================")

print("\nTop 5 Keywords:\n")

for i, item in enumerate(top_keywords, start=1):
    print(i, ".", item[0], ":", item[1])

print("\n================================")



















