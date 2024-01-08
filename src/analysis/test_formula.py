# Reverse engineering VLR player rating
# Purpose: To reverse engineer the VLR.gg player rating calculation using their stat data.
# File: check_forumal.py - tests formula on csv file to validate results.
# Mark Zhdan | 01-05-2023

import pandas as pd


def calculate_vlr_rating(*stats):
    coefficients = [
        0.467584759836,
        0.312158631682,
        -1.153682762595,
        0.003942697956,
        -0.000725869108,
        -0.063496102738,
        0.204588665932,
    ]
    intercept = 1.0013936330345852

    rating = sum(coef * stat for coef, stat in zip(coefficients, stats)) + intercept
    return rating


# "KPR", "APR", "DPR", "ADR", "ACS", "FDPR", "FKPR"
stats = [1.25, 0.1875, 0.65625, 227, 358, 0.0625, 0.1875]
predicted_rating = calculate_vlr_rating(*stats)

print(f"Cuft | Predicted: {predicted_rating:.2f}")
