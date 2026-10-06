"""
Day 20: Movie Recommendation System
Content-Based Filtering using TF-IDF + Cosine Similarity

Install:  pip install pandas scikit-learn
Run:      python Day-20-Movie-Recommendation-System.py
"""

import difflib

import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

# ---------------------------------------------------------------
# 1. Dataset (small built-in dataset, no download needed)
#    Later you can replace this with a CSV (e.g. TMDB / MovieLens)
# ---------------------------------------------------------------
MOVIES = [
    ("Inception", "Sci-Fi Thriller", "A thief enters dreams to steal secrets and plant an idea in a mind"),
    ("Interstellar", "Sci-Fi Drama", "Astronauts travel through a wormhole in space to save humanity"),
    ("The Matrix", "Sci-Fi Action", "A hacker discovers reality is a simulation controlled by machines"),
    ("The Dark Knight", "Action Crime", "Batman fights the Joker, a criminal mastermind terrorizing Gotham city"),
    ("Joker", "Crime Drama", "A failed comedian turns into a criminal mastermind in Gotham city"),
    ("Avengers Endgame", "Action Superhero", "Superheroes unite to defeat Thanos and restore the universe"),
    ("Iron Man", "Action Superhero", "A billionaire builds a powerful armored suit to fight evil"),
    ("Titanic", "Romance Drama", "A love story between two passengers on a doomed ocean ship"),
    ("The Notebook", "Romance Drama", "A couple falls in love and their romance lasts through the years"),
    ("Toy Story", "Animation Family", "Toys come alive and go on adventures with friendship and humor"),
    ("Finding Nemo", "Animation Family", "A clownfish searches the ocean to find his lost son"),
    ("Mad Max Fury Road", "Action Adventure", "A road war across the desert to escape a tyrant ruler"),
    ("Gravity", "Sci-Fi Thriller", "Two astronauts struggle to survive after their shuttle is destroyed in space"),
    ("Shutter Island", "Mystery Thriller", "A detective investigates a disappearance at a mental hospital on an island"),
    ("Se7en", "Crime Thriller", "Two detectives hunt a serial killer who uses seven deadly sins"),
]


# ---------------------------------------------------------------
# 2. Build the recommender
# ---------------------------------------------------------------
class MovieRecommender:
    def __init__(self, movies):
        self.df = pd.DataFrame(movies, columns=["title", "genre", "description"])
        # Genre is repeated so it gets more weight than the description
        self.df["features"] = (self.df["genre"] + " ") * 3 + self.df["description"]

        vectorizer = TfidfVectorizer(stop_words="english")
        tfidf_matrix = vectorizer.fit_transform(self.df["features"])
        self.similarity = cosine_similarity(tfidf_matrix)

    def find_title(self, query):
        """Handle typos / lowercase input using fuzzy matching."""
        titles = self.df["title"].tolist()
        lookup = {t.lower(): t for t in titles}
        match = difflib.get_close_matches(query.lower(), lookup.keys(), n=1, cutoff=0.5)
        return lookup[match[0]] if match else None

    def recommend(self, query, top_n=3):
        title = self.find_title(query)
        if title is None:
            return None, []

        idx = self.df.index[self.df["title"] == title][0]
        scores = sorted(enumerate(self.similarity[idx]), key=lambda x: x[1], reverse=True)
        scores = [s for s in scores if s[0] != idx][:top_n]

        results = [(self.df.iloc[i]["title"], self.df.iloc[i]["genre"], round(score * 100, 1))
                   for i, score in scores]
        return title, results


# ---------------------------------------------------------------
# 3. Command line interface
# ---------------------------------------------------------------
def main():
    rec = MovieRecommender(MOVIES)

    print("=" * 50)
    print("   MOVIE RECOMMENDATION SYSTEM")
    print("=" * 50)
    print("Available movies:")
    for title in rec.df["title"]:
        print(f"  - {title}")
    print("\nType 'exit' to quit.\n")

    while True:
        query = input("Enter a movie you like: ").strip()
        if query.lower() == "exit":
            print("Thanks for using the recommender!")
            break
        if not query:
            continue

        matched, results = rec.recommend(query)
        if matched is None:
            print("Movie not found. Try another one.\n")
            continue

        print(f"\nBecause you liked '{matched}', you may also like:")
        for rank, (title, genre, score) in enumerate(results, start=1):
            print(f"  {rank}. {title} ({genre}) - {score}% match")
        print()


if __name__ == "__main__":
    main()