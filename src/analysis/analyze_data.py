# Reverse engineering VLR player rating
# Purpose: To reverse engineer the VLR.gg player rating calculation using their stat data.
# File: analyze_data.py - trains and tests the scraped data.
# Mark Zhdan | 01-05-2023

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error


df = pd.read_csv("data/clean/champions2023.csv")

# What goes into VLR.gg rating? (https://www.vlr.gg/160667/vlr-gg-player-rating-explained)
# KPR, DPR, Trades (no data), Economy (can't add), post-round (maybe KAST), APR, ADRa, survival rating (DPR & KAST)
# Final features: KPR, APR, DPR, ADRa, SR, KAST
# Could add: K:D, ACS, FK/FD?

featureKeys = ["KPR", "APR", "DPR", "ADRa", "SR", "KAST"]
features = df[featureKeys]
target = df["R"]


X_train, X_test, y_train, y_test = train_test_split(
    features, target, random_state=3, test_size=0.1
)

# Linear Regression Model
model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

# Print metrics
formatted_coefficients = ", ".join(f"{coef:.12f}" for coef in model.coef_)
print(f"Coefficients: [{formatted_coefficients}]")
print(f"Intercept: {model.intercept_}\n")

print(f"R2 score: {r2_score(y_test, predictions)}")
print(f"RMSE: {mean_squared_error(y_test, predictions, squared=False)}")
print(f"MAE: {mean_absolute_error(y_test, predictions)}")
