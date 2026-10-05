# Day 19 - Spam Message Classifier
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import MultinomialNB
messages = [
    "Win a free iPhone now",
    "Claim your cash prize today",
    "Congratulations you won a lottery",
    "Click here to get free money",
    "Limited offer claim your reward",
    "Meeting is scheduled at 5 PM",
    "Can you send me the document",
    "Let's have lunch tomorrow",
    "Please complete the project report",
    "Your appointment is confirmed"
]
labels = ["spam", "spam", "spam", "spam", "spam", "not spam", "not spam", "not spam", "not spam", "not spam"]
vectorizer = TfidfVectorizer()
message_vectors = vectorizer.fit_transform(messages)
model = MultinomialNB()
model.fit(message_vectors, labels)
user_message = input("Enter a message to classify: ")
user_message_vector = vectorizer.transform([user_message])
prediction = model.predict(user_message_vector)
print(f"The message is classified as: {prediction[0]}")
if prediction[0] == "spam":
    print("Warning: This message is likely to be spam.")
else:
    print("This message is not spam.")