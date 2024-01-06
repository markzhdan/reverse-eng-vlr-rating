# Reverse engineering VLR player rating
# Purpose: To reverse engineer the VLR.gg player rating calculation using their stat data.
# File: analyze_data.py - trains and tests the scraped data.
# Mark Zhdan | 01-05-2023

import pandas as pd
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score, mean_squared_error


# What goes into VLR.gg rating? (https://www.vlr.gg/160667/vlr-gg-player-rating-explained)
# KPR, DPR, Trades, Economy (can't add), post-round (maybe kast), apr, ADRa (adr for us), survival (dpr & kast)
# Final features: KPR, APR, DPR, ADR, KAST
# Could add: K:D, ACS, fk/fd?
featureKeys = ["KPR", "APR", "DPR", "ADR", "ACS", "FDPR", "FKPR"]

df = pd.read_csv("data/clean/stats_recent.csv")

target = df["R"]
features = df[featureKeys]

X_train, X_test, y_train, y_test = train_test_split(
    features, target, random_state=42, test_size=0.1
)

# Linear Regression Model
model = LinearRegression()
model.fit(X_train, y_train)

predictions = model.predict(X_test)

# Print metrics
formatted_coefficients = ", ".join(f"{coef:.12f}" for coef in model.coef_)
print(f"Coefficients: [{formatted_coefficients}]")
print(f"Intercept: {model.intercept_}\n")

print(f"R2 score:{r2_score(y_test, predictions)}")
print(f"RMSE:{mean_squared_error(y_test, predictions, squared=False)}")
print(f"MAE:{mean_absolute_error(y_test, predictions)}")
