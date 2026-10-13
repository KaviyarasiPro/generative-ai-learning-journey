"""
Day 27: Customer Churn Predictor
Classification: Logistic Regression vs Random Forest

NOTE: The dataset below is SYNTHETIC (generated with realistic patterns,
e.g. month-to-month customers churn more). It is for learning purposes only.
You can replace it with the real Kaggle "Telco Customer Churn" CSV later.

Install:  pip install pandas numpy matplotlib scikit-learn
Run:      python Day-27-Customer-Churn-Predictor.py
Charts are saved in the 'charts' folder.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (accuracy_score, confusion_matrix, f1_score,
                             precision_score, recall_score)
from sklearn.model_selection import train_test_split
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler

os.makedirs("charts", exist_ok=True)

# ===============================================================
# PART 1: Data Creation + EDA
# ===============================================================


def create_dataset(n=2000, seed=42):
    rng = np.random.default_rng(seed)
    contract = rng.choice(["Month-to-month", "One year", "Two year"], n, p=[0.55, 0.25, 0.20])
    internet = rng.choice(["DSL", "Fiber", "None"], n, p=[0.35, 0.45, 0.20])
    payment = rng.choice(["Auto-pay", "Manual"], n, p=[0.5, 0.5])
    tenure = rng.integers(1, 73, n)
    support_calls = np.clip(rng.poisson(1.8, n), 0, 8)

    base_charge = np.select([internet == "None", internet == "DSL"], [25, 55], default=85)
    monthly = np.round(base_charge + rng.normal(0, 8, n), 2).clip(15, 130)

    # Churn probability (logistic formula with realistic patterns)
    score = (
        -2.4
        + 1.3 * (contract == "Month-to-month")
        - 1.2 * (contract == "Two year")
        - 0.035 * tenure
        + 0.45 * (internet == "Fiber")
        + 0.30 * support_calls
        + 0.012 * monthly
        + 0.35 * (payment == "Manual")
    )
    prob = 1 / (1 + np.exp(-score))
    churn = (rng.random(n) < prob).astype(int)

    return pd.DataFrame({
        "tenure_months": tenure,
        "contract": contract,
        "monthly_charges": monthly,
        "internet_service": internet,
        "support_calls": support_calls,
        "payment_method": payment,
        "churn": churn,
    })


df = create_dataset()
print("Dataset shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())
print(f"\nOverall churn rate: {df['churn'].mean() * 100:.1f}%")
print("\nChurn rate by contract type:")
print((df.groupby("contract")["churn"].mean() * 100).round(1).astype(str) + "%")

# --- Chart 1: Churn rate by contract ---
rate = (df.groupby("contract")["churn"].mean() * 100).sort_values()
fig, ax = plt.subplots(figsize=(7, 5))
bars = ax.bar(rate.index, rate.values, color=["#10b981", "#f59e0b", "#ef4444"])
for b, v in zip(bars, rate.values):
    ax.text(b.get_x() + b.get_width() / 2, v + 0.8, f"{v:.1f}%", ha="center")
ax.set_ylabel("Churn Rate (%)")
ax.set_title("Churn Rate by Contract Type")
plt.tight_layout()
plt.savefig("charts/1_churn_by_contract.png", dpi=150)
plt.close()

# --- Chart 2: Churn rate by support calls ---
calls = df.groupby("support_calls")["churn"].mean() * 100
fig, ax = plt.subplots(figsize=(7, 5))
ax.plot(calls.index, calls.values, marker="o", color="#3b82f6", linewidth=2)
ax.set_xlabel("Support Calls")
ax.set_ylabel("Churn Rate (%)")
ax.set_title("More Support Calls = More Churn?")
ax.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("charts/2_churn_by_support_calls.png", dpi=150)
plt.close()

print("\nPart 1 charts saved in 'charts' folder.")

# ===============================================================
# PART 2: Model Training, Evaluation, Risk Prediction
# ===============================================================

X = pd.get_dummies(df.drop(columns=["churn"]), drop_first=False)
y = df["churn"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42, stratify=y
)

models = {
    "Logistic Regression": make_pipeline(
        StandardScaler(), LogisticRegression(class_weight="balanced", max_iter=1000)
    ),
    "Random Forest": RandomForestClassifier(
        n_estimators=200, max_depth=8, class_weight="balanced", random_state=42
    ),
}

print("\n" + "=" * 70)
print("MODEL COMPARISON")
print("=" * 70)
print(f"{'Model':<20}{'Accuracy':>10}{'Precision':>11}{'Recall':>9}{'F1':>8}")
results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    acc = accuracy_score(y_test, pred)
    prec = precision_score(y_test, pred)
    rec = recall_score(y_test, pred)
    f1 = f1_score(y_test, pred)
    results[name] = {"f1": f1, "pred": pred}
    print(f"{name:<20}{acc:>10.3f}{prec:>11.3f}{rec:>9.3f}{f1:>8.3f}")

best_name = max(results, key=lambda k: results[k]["f1"])
best_model = models[best_name]
print(f"\nBest model (by F1): {best_name}")
print("Note: In churn problems, RECALL matters, because missing a customer "
      "who will leave costs more than a false alarm.")

# --- Chart 3: Confusion matrix heatmap ---
cm = confusion_matrix(y_test, results[best_name]["pred"])
fig, ax = plt.subplots(figsize=(5.5, 5))
ax.imshow(cm, cmap="Blues")
labels = ["Stayed", "Churned"]
ax.set_xticks([0, 1])
ax.set_yticks([0, 1])
ax.set_xticklabels(labels)
ax.set_yticklabels(labels)
ax.set_xlabel("Predicted")
ax.set_ylabel("Actual")
ax.set_title(f"Confusion Matrix ({best_name})")
for i in range(2):
    for j in range(2):
        ax.text(j, i, cm[i, j], ha="center", va="center", fontsize=16,
                color="white" if cm[i, j] > cm.max() / 2 else "black")
plt.tight_layout()
plt.savefig("charts/3_confusion_matrix.png", dpi=150)
plt.close()

# --- Chart 4: Feature importance (Random Forest) ---
rf = models["Random Forest"]
importance = pd.Series(rf.feature_importances_, index=X.columns).sort_values().tail(8)
fig, ax = plt.subplots(figsize=(7, 5))
ax.barh(importance.index, importance.values, color="#8b5cf6")
ax.set_xlabel("Importance")
ax.set_title("Why do customers leave?")
plt.tight_layout()
plt.savefig("charts/4_feature_importance.png", dpi=150)
plt.close()

print("\nTop reasons customers leave:")
for feat, val in importance.sort_values(ascending=False).head(5).items():
    print(f"  {feat:<30} {val * 100:.1f}%")

# --- High-risk customers (from test set) ---
risk = best_model.predict_proba(X_test)[:, 1]
top = X_test.copy()
top["churn_risk_%"] = (risk * 100).round(1)
top = top.sort_values("churn_risk_%", ascending=False).head(5)
print("\nTop 5 highest-risk customers in the test set:")
for idx, row in top.iterrows():
    original = df.loc[idx]
    print(f"  Customer #{idx}: {original['contract']}, {original['tenure_months']} months, "
          f"{original['support_calls']} support calls -> Risk {row['churn_risk_%']}%")
print("Part 2 charts saved in 'charts' folder.")


def retention_tips(contract, tenure, monthly, internet, calls, payment):
    tips = []
    if contract == "Month-to-month":
        tips.append("Offer a discount for switching to a yearly plan")
    if calls >= 4:
        tips.append("Call the customer personally, support issues are unresolved")
    if internet == "Fiber" and monthly > 80:
        tips.append("Give a loyalty discount on the Fiber plan")
    if payment == "Manual":
        tips.append("Encourage auto-pay with a small cashback")
    if tenure < 12:
        tips.append("Run a new-customer onboarding follow-up")
    return tips or ["Customer looks stable, keep the service quality high"]


def predict_churn(contract, tenure, monthly, internet, calls, payment):
    row = pd.DataFrame([{
        "tenure_months": tenure,
        "monthly_charges": monthly,
        "support_calls": calls,
        f"contract_{contract}": 1,
        f"internet_service_{internet}": 1,
        f"payment_method_{payment}": 1,
    }])
    row = row.reindex(columns=X.columns, fill_value=0)
    return float(best_model.predict_proba(row)[0][1])


def choose(prompt, options):
    lookup = {o.lower(): o for o in options}
    while True:
        value = input(f"{prompt} ({'/'.join(options)}): ").strip().lower()
        if value in lookup:
            return lookup[value]
        print("Invalid choice, try again.")


def ask_number(prompt, cast=int):
    while True:
        try:
            return cast(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def main():
    print("\n" + "=" * 70)
    print("   CUSTOMER CHURN PREDICTOR (type 'exit' at the first question to quit)")
    print("=" * 70)
    while True:
        first = input("\nPress Enter to check a customer (or type 'exit'): ").strip().lower()
        if first == "exit":
            print("Thanks for using the predictor!")
            break
        contract = choose("Contract", ["Month-to-month", "One year", "Two year"])
        tenure = ask_number("Tenure (months): ")
        monthly = ask_number("Monthly charges: ", float)
        internet = choose("Internet service", ["DSL", "Fiber", "None"])
        calls = ask_number("Support calls in last 3 months: ")
        payment = choose("Payment method", ["Auto-pay", "Manual"])

        prob = predict_churn(contract, tenure, monthly, internet, calls, payment)
        level = "HIGH ⚠️" if prob >= 0.6 else "MEDIUM 🟡" if prob >= 0.35 else "LOW ✅"
        print(f"\nChurn Risk: {prob * 100:.0f}% ({level})")
        print("Suggested actions:")
        for tip in retention_tips(contract, tenure, monthly, internet, calls, payment):
            print(f"  - {tip}")


if __name__ == "__main__":
    main()