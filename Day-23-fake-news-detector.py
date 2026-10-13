"""
Day 22: Fake News Detector
TF-IDF + Logistic Regression
 
Install:  pip install pandas scikit-learn
Run:      python Day-22-Fake-News-Detector.py
 
Optional (for better accuracy): download the Kaggle dataset
"Fake and Real News Dataset" and keep Fake.csv and True.csv in the same
folder. The script will use them automatically.
"""
 
import os
import re
import string
 
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix
from sklearn.model_selection import train_test_split
 
# ===============================================================
# PART 1: Data, Cleaning, Training, Evaluation
# ===============================================================
 
FAKE_NEWS = [
    "SHOCKING! Scientists reveal drinking tea makes you immortal",
    "You won't believe what this celebrity did, doctors hate him",
    "Aliens have secretly landed and the government is hiding it",
    "Miracle pill melts belly fat in 3 days, no exercise needed",
    "BREAKING: Moon is actually a hologram, NASA insider confesses",
    "Drinking hot water cures all diseases, big pharma hiding truth",
    "This one weird trick makes you a millionaire overnight",
    "Secret document proves world leaders are lizard people",
    "Eating onions under the pillow cures fever instantly, experts stunned",
    "Government puts mind control chips in free vaccines, leaked memo says",
    "Shocking truth about 5G towers that media refuses to tell you",
    "Man lives 200 years by drinking only lemon juice, scientists baffled",
    "Free iPhone giveaway! Click this link now before it's deleted",
    "Famous actor dead? Hoax or truth, what they are hiding from you",
    "Share before they delete this: banks will freeze all accounts tomorrow",
    "Ancient cure for cancer found in kitchen spice, doctors silenced",
    "Earth is flat and satellites are fake, shocking new proof revealed",
    "Politician secretly sold the country to foreign enemies, insiders claim",
    "Magic water from this village cures every illness in one sip",
    "Unbelievable! Cat predicts lottery numbers and wins crores",
    "Scientists confirm chocolate for breakfast makes you lose weight fast",
    "Leaked video shows the election was rigged, media silent",
    "Mobile phones will explode tomorrow due to rare planet alignment",
    "Doctors stunned as grandma reverses aging with kitchen powder",
    "Government hiding free energy machine that big companies fear",
]
 
REAL_NEWS = [
    "Government announces new education budget for the coming fiscal year",
    "Central bank keeps interest rates unchanged amid inflation concerns",
    "Researchers publish study on the effects of exercise on heart health",
    "City council approves new metro rail extension project",
    "Stock markets close higher as technology shares gain",
    "Health ministry launches vaccination drive in rural districts",
    "National cricket team wins the series after a strong bowling display",
    "Parliament passes bill on data protection after lengthy debate",
    "Heavy rain expected in coastal regions, weather department says",
    "Company reports quarterly profit growth driven by cloud services",
    "University introduces new artificial intelligence degree program",
    "Prime minister meets foreign leaders to discuss trade agreements",
    "Engineers complete repairs on the main bridge ahead of schedule",
    "Space agency successfully launches new weather monitoring satellite",
    "Local hospital opens new cancer treatment wing for patients",
    "Unemployment rate falls slightly according to official statistics",
    "Farmers receive higher minimum support price for rice this season",
    "Electric vehicle sales rise as new charging stations open",
    "School board announces updated exam schedule for the next term",
    "Scientists discover new species of frog in the western forests",
    "Police arrest suspect in connection with last week's robbery",
    "Airline adds new direct flights between two major cities",
    "Court delivers verdict in long running land dispute case",
    "Tech firm unveils new smartphone with improved battery life",
    "Ministry releases guidelines to improve road safety in cities",
]
def load_data():
    """use kaggle csv file if available, otherwise use local csv file"""
    if os.path.exists("Fake.csv") and os.path.exists("True.csv"):
        fake = pd.read_csv("Fake.csv").sample(3000, random_state=42)
        true = pd.read_csv("True.csv").sample(3000, random_state=42)

        fake["text_all"] = fake["title"] + " " + fake["text"]
        true["text_all"] = true["title"] + " " + true["text"]

        df = pd.concat([
            pd.DataFrame({"text": fake["text_all"], "label": 0}),
            pd.DataFrame({"text": true["text_all"], "label": 1})
        ])
        print(f"Loaded {len(df)} samples from local CSV files.")

    else:
        df = pd.DataFrame({
            "text": FAKE_NEWS + REAL_NEWS,
            "label": [0] * len(FAKE_NEWS) + [1] * len(REAL_NEWS)
        })
        print(f"Loaded {len(df)} samples from hardcoded data.")
    return df.sample(frac=1, random_state=42).reset_index(drop=True)  # Shuffle the dataset


def clean_text(text):
    """Clean the text by removing unwanted characters and formatting."""
    # Implement text cleaning logic here (e.g., remove punctuation, lowercase, etc.)
    text = text.lower()  # Convert to lowercase
    text = re.sub(r"http\S+|www\S+|https\S+", " ", text)  # Remove URLs
    text = text.replace("\n", " ")  # Remove newlines
    text = text.translate(str.maketrans("", "", string.punctuation))
    text = re.sub(r"\d+", " ", text)  # Remove digits
    return re.sub(r"\s+", " ", text).strip()  # Remove extra whitespace

df = load_data()
df["clean"] = df["text"].apply(clean_text)

X_train, X_test, y_train, y_test = train_test_split(
    df["clean"], df["label"], test_size=0.25, random_state=42, stratify=df["label"]
)

vectorizer = TfidfVectorizer(stop_words="english", sublinear_tf=True)
X_train_vec = vectorizer.fit_transform(X_train)
X_test_vec = vectorizer.transform(X_test)

model = LogisticRegression(C=10, max_iter=1000)
model.fit(X_train_vec, y_train)

y_pred = model.predict(X_test_vec)
print(f"\nAccuracy: {accuracy_score(y_test, y_pred) * 100:.1f}%")
print("\nConfusion Matrix (rows = actual, cols = predicted):")
print(pd.DataFrame(
    confusion_matrix(y_test, y_pred),
    index=["Actual REAL", "Actual FAKE"],
    columns=["Pred REAL", "Pred FAKE"],
))
print("\nClassification Report:")
print(classification_report(y_test, y_pred, target_names=["REAL", "FAKE"]))

# ===============================================================
# PART 2: Top Words + Live Prediction
# ===============================================================

def show_top_words(n=8):
    words = vectorizer.get_feature_names_out()
    coefs = model.coef_[0]
    order = coefs.argsort()
    print(f"\nTop {n} words for FAKE news:")
    for i in order[::-1][:n]:
        print(f"{words[i]:<22} {coefs[i]:+.2f}")
    print(f"\nTop {n} words for REAL news:")
    for i in order[:n]:
        print(f"{words[i]:<22} {coefs[i]:+.2f}")

def predict_news(text):
    """Predict whether the given news text is REAL or FAKE."""
    vec = vectorizer.transform([clean_text(text)])
    fake_prob = model.predict_proba(vec)[0][0]
    if fake_prob > 0.5:
        return "FAKE", fake_prob
    return "REAL", 1 - fake_prob

def main():
    show_top_words()
    print("\n" + "=" * 55)
    print("   FAKE NEWS DETECTOR  (type 'exit' to quit)")
    print("=" * 55)
    while True:
        text = input("\nEnter news headline: ").strip()
        if text.lower() == "exit":
            print("Stay informed, verify before you share!")
            break
        if not text:
            continue
        label, confidence = predict_news(text)
        print(f"Prediction: {label} (confidence: {confidence * 100:.0f}%)")
 
 
if __name__ == "__main__":
    main()
 