# Day 15 - Extractive Text Summarizer
import string

print("-"*30)
print("  EXTRACTIVE TEXT SUMMARIZER")
print("-"*30)
print("\nEnter the text you want to summarize :")
text = input(">> ")
sentences = text.split(".")
clean_text = text.lower()
clean_text = clean_text.translate(
    str.maketrans(" "," ",string.punctuation)
    )
words = clean_text.split()
stop_words = [
    "is", "the", "a", "an", "and", "are",
    "to", "in", "of", "for", "on", "with"
]
filtered_words = []

for word in words :
    if word not in stop_words :
        filtered_words.append(word)

word_frequency = {}

for word in filtered_words :
    if word in word_frequency :
        word_frequency[word] = word_frequency[word] + 1
    else :
        word_frequency[word] = 1

sentence_scores = {}

for sentence in sentences :
    sentence_words = sentence.lower().split()
    score = 0
    for word in sentence_words :
        if word in word_frequency :
            score = score + word_frequency[word]
    sentence_scores[sentence]=score


sorted_sentences = sorted(
    sentence_scores,
    key = sentence_scores.get,
    reverse = True
    )

top_sentences = sorted_sentences[:2]
summary = ".".join(top_sentences)

print("\n" + "-" * 60)
print("          SUMMARY")
print("-" * 60)

print(summary)

print("-" * 60)

