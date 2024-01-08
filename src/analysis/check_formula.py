# Reverse engineering VLR player rating
# Purpose: To reverse engineer the VLR.gg player rating calculation using their stat data.
# File: check_forumal.py - tests formula on csv file to validate results.
# Mark Zhdan | 01-05-2023

import pandas as pd


def calculate_vlr_rating(*stats):
    coefficients = [
        0.898060946867,
        0.227872913948,
        -0.433940698092,
        0.002524365390,
        0.433940698092,
        0.312874869548,
    ]
    intercept = 0.17492523147187433

    rating = sum(coef * stat for coef, stat in zip(coefficients, stats)) + intercept
    return rating


df = pd.read_csv("data/clean/champions2023.csv")

featureKeys = ["KPR", "APR", "DPR", "ADRa", "SR", "KAST"]

player_name_width = max(len(row["Player"]) for index, row in df.iterrows()) + 2

# Iterate through each row and calculate the rating
for index, row in df.iterrows():
    # Extract the stats
    stats = row[featureKeys]

    # Compare with actual rating
    actual_rating = row["R"]
    predicted_rating = calculate_vlr_rating(*stats)
    error = actual_rating - predicted_rating

    player_name = row["Player"].ljust(player_name_width)
    print(
        f"{player_name} | Actual: {actual_rating:.2f}, Predicted: {predicted_rating:.2f}, Error: {error:.2f}"
    )
