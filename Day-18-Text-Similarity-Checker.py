from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

print("="*40)
print("    TEXT SIMILARITY CHECKER")
print("="*40)

text1 = input("\nEnter your first text :")
text2 = input("Enter your second text :")

vectorizer = TfidfVectorizer()
tfidf_matrix = vectorizer.fit_transform([text1,text2])

similarity = cosine_similarity(
    tfidf_matrix[0:1],
    tfidf_matrix[1:2]
    )
similarity_score = similarity[0][0]
similarity_percentage = similarity_score * 100

if similarity_percentage >= 70:
    similarity_level = "High Similarity"

elif similarity_percentage >= 40:
    similarity_level = "Medium Similarity"

else:
    similarity_level = "Low Similarity"

print("\n" + "=" * 40)
print("       TEXT SIMILARITY REPORT")
print("=" * 40)

print("Similarity Score :", round(similarity_percentage, 2), "%")
print("Similarity Level :", similarity_level)

print("=" * 40)
