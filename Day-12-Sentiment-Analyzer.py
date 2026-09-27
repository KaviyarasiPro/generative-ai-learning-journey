import string

print("================================")
print("       SENTIMENT ANALYZER")
print("================================")

# Get text from the user
print("\nEnter the text you want to analyze:")
text = input(">> ")
# Clean the text
clean_text = text.lower()

clean_text = clean_text.translate(
    str.maketrans("", "", string.punctuation)
)
words = clean_text.split()
# Sentiment word lists
positive_words = [
    "good", "great", "happy", "love", "excellent",
    "useful", "amazing", "enjoyed", "interesting", "wonderful"
]

negative_words = [
    "bad", "sad", "hate", "poor", "terrible",
    "difficult", "boring", "disappointed", "worst", "awful"
]
positive_count = 0
negative_count = 0

for word in words:
    if word in positive_words:
        positive_count = positive_count + 1

    elif word in negative_words:
        negative_count = negative_count + 1

# Determine the sentiment
if positive_count > negative_count:
    sentiment = "Positive 😊"

elif negative_count > positive_count:
    sentiment = "Negative 😞"

else:
    sentiment = "Neutral 😐"

# Display the sentiment report
print("\n================================")
print("       SENTIMENT ANALYZER")
print("================================")

print("\nPositive Words :", positive_count)
print("Negative Words :", negative_count)
print("Sentiment      :", sentiment)

print("\n================================")


