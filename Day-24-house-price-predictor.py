"""
Day 24: House Price Predictor (Chennai Edition)
Regression: Linear Regression vs Random Forest

NOTE: The dataset below is SYNTHETIC (generated with realistic-looking
price-per-sqft values per locality). Prices are for learning purposes only,
not real market rates. You can replace it with a real Kaggle CSV later.

Install:  pip install pandas numpy matplotlib scikit-learn
Run:      python Day-24-House-Price-Predictor.py
Charts are saved in the 'charts' folder.
"""

import os

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
from sklearn.model_selection import train_test_split

os.makedirs("charts", exist_ok=True)

# ===============================================================
# PART 1: Data Creation + EDA (Exploratory Data Analysis)
# ===============================================================

# Approx price per sqft (in Rs) for each locality (illustrative values)
LOCALITY_RATE = {
    "Avadi": 4500,
    "Ambattur": 5200,
    "Tambaram": 5600,
    "Porur": 6500,
    "OMR": 7200,
    "Velachery": 8500,
    "Anna Nagar": 11000,
    "T Nagar": 13000,
}


def create_dataset(n=600, seed=42):
    rng = np.random.default_rng(seed)
    localities = rng.choice(list(LOCALITY_RATE.keys()), n)
    area = rng.integers(500, 2600, n)
    bedrooms = np.clip(np.round(area / 600) + rng.integers(-1, 2, n), 1, 5).astype(int)
    bathrooms = np.clip(bedrooms - rng.integers(0, 2, n), 1, 5).astype(int)
    age = rng.integers(0, 26, n)

    rate = np.array([LOCALITY_RATE[loc] for loc in localities])
    base = area * rate / 100000                      # price in Lakhs
    base = base * (1 - 0.012 * age)                  # older = cheaper
    base = base + bathrooms * 1.5                    # small bonus per bathroom
    noise = rng.normal(0, 0.06 * base)               # ~6% random variation
    price = np.round(base + noise, 2)

    return pd.DataFrame({
        "area_sqft": area,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "age_years": age,
        "locality": localities,
        "price_lakhs": price,
    })


df = create_dataset()
print("Dataset shape:", df.shape)
print("\nFirst 5 rows:")
print(df.head())
print("\nStatistical summary:")
print(df.describe().round(2))
print("\nMissing values:", int(df.isnull().sum().sum()))

# --- Chart 1: Correlation heatmap ---
numeric = df.select_dtypes(include="number")
corr = numeric.corr()
fig, ax = plt.subplots(figsize=(7, 5))
im = ax.imshow(corr, cmap="coolwarm", vmin=-1, vmax=1)
ax.set_xticks(range(len(corr)))
ax.set_yticks(range(len(corr)))
ax.set_xticklabels(corr.columns, rotation=45, ha="right")
ax.set_yticklabels(corr.columns)
for i in range(len(corr)):
    for j in range(len(corr)):
        ax.text(j, i, f"{corr.iloc[i, j]:.2f}", ha="center", va="center", fontsize=9)
fig.colorbar(im)
ax.set_title("Correlation Heatmap")
plt.tight_layout()
plt.savefig("charts/1_correlation_heatmap.png", dpi=150)
plt.close()

# --- Chart 2: Area vs Price scatter with trend line ---
fig, ax = plt.subplots(figsize=(7, 5))
ax.scatter(df["area_sqft"], df["price_lakhs"], alpha=0.5, color="#3b82f6")
slope, intercept = np.polyfit(df["area_sqft"], df["price_lakhs"], 1)
xs = np.linspace(df["area_sqft"].min(), df["area_sqft"].max(), 100)
ax.plot(xs, slope * xs + intercept, color="red", linewidth=2, label="Trend line")
ax.set_xlabel("Area (sqft)")
ax.set_ylabel("Price (Lakhs)")
ax.set_title("Area vs Price")
ax.legend()
plt.tight_layout()
plt.savefig("charts/2_area_vs_price.png", dpi=150)
plt.close()

# --- Chart 3: Average price per sqft by locality ---
df["price_per_sqft"] = df["price_lakhs"] * 100000 / df["area_sqft"]
avg_rate = df.groupby("locality")["price_per_sqft"].mean().sort_values()
fig, ax = plt.subplots(figsize=(7, 5))
ax.barh(avg_rate.index, avg_rate.values, color="#10b981")
ax.set_xlabel("Average Price per sqft (Rs)")
ax.set_title("Price per sqft by Locality")
plt.tight_layout()
plt.savefig("charts/3_price_by_locality.png", dpi=150)
plt.close()

df = df.drop(columns=["price_per_sqft"])
print("\nPart 1 charts saved in 'charts' folder.")

# ===============================================================
# PART 2: Model Training, Comparison, Live Prediction
# ===============================================================

# One-Hot Encoding: locality (text) -> numeric columns
X = pd.get_dummies(df.drop(columns=["price_lakhs"]), columns=["locality"])
y = df["price_lakhs"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.2, random_state=42
)

models = {
    "Linear Regression": LinearRegression(),
    "Random Forest": RandomForestRegressor(n_estimators=200, random_state=42),
}

print("\n" + "=" * 55)
print("MODEL COMPARISON")
print("=" * 55)
results = {}
for name, model in models.items():
    model.fit(X_train, y_train)
    pred = model.predict(X_test)
    r2 = r2_score(y_test, pred)
    mae = mean_absolute_error(y_test, pred)
    rmse = np.sqrt(mean_squared_error(y_test, pred))
    results[name] = (r2, mae, rmse, pred)
    print(f"{name:<18} R2: {r2:.3f} | MAE: {mae:.2f} Lakhs | RMSE: {rmse:.2f} Lakhs")

best_name = max(results, key=lambda k: results[k][0])
best_model = models[best_name]
print(f"\nBest model: {best_name}")

# --- Chart 4: Actual vs Predicted (best model) ---
fig, ax = plt.subplots(figsize=(6, 6))
ax.scatter(y_test, results[best_name][3], alpha=0.6, color="#8b5cf6")
lims = [y_test.min(), y_test.max()]
ax.plot(lims, lims, "r--", label="Perfect prediction")
ax.set_xlabel("Actual Price (Lakhs)")
ax.set_ylabel("Predicted Price (Lakhs)")
ax.set_title(f"Actual vs Predicted ({best_name})")
ax.legend()
plt.tight_layout()
plt.savefig("charts/4_actual_vs_predicted.png", dpi=150)
plt.close()

# --- Chart 5: Feature importance (Random Forest) ---
rf = models["Random Forest"]
importance = pd.Series(rf.feature_importances_, index=X.columns).sort_values().tail(8)
fig, ax = plt.subplots(figsize=(7, 5))
ax.barh(importance.index, importance.values, color="#f59e0b")
ax.set_xlabel("Importance")
ax.set_title("What affects house price the most?")
plt.tight_layout()
plt.savefig("charts/5_feature_importance.png", dpi=150)
plt.close()

print("\nTop factors affecting price:")
for feat, val in importance.sort_values(ascending=False).head(5).items():
    print(f"  {feat:<22} {val * 100:.1f}%")
print("Part 2 charts saved in 'charts' folder.")


def predict_price(area, bedrooms, bathrooms, age, locality):
    row = pd.DataFrame([{
        "area_sqft": area,
        "bedrooms": bedrooms,
        "bathrooms": bathrooms,
        "age_years": age,
        f"locality_{locality}": 1,
    }])
    row = row.reindex(columns=X.columns, fill_value=0)
    return float(best_model.predict(row)[0])


def ask_number(prompt, cast=int):
    while True:
        try:
            return cast(input(prompt))
        except ValueError:
            print("Please enter a valid number.")


def main():
    names = {k.lower(): k for k in LOCALITY_RATE}
    print("\n" + "=" * 55)
    print("   HOUSE PRICE PREDICTOR (type 'exit' as locality to quit)")
    print("=" * 55)
    print("Localities:", ", ".join(LOCALITY_RATE))

    while True:
        loc = input("\nEnter locality: ").strip().lower()
        if loc == "exit":
            print("Thanks for using the predictor!")
            break
        if loc not in names:
            print("Locality not in dataset. Choose from the list above.")
            continue
        area = ask_number("Enter area (sqft): ")
        beds = ask_number("Enter bedrooms: ")
        baths = ask_number("Enter bathrooms: ")
        age = ask_number("Enter age of property (years): ")

        price = predict_price(area, beds, baths, age, names[loc])
        print(f"\nPredicted Price: Rs {price:.1f} Lakhs 🏠 ({names[loc]}, {area} sqft)")


if __name__ == "__main__":
    main()