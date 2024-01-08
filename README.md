# Reverse Engineering the VLR Player Rating

[Full in-depth blog post](https://markzhdan.com/blogs/reverse-engineering-vlr-rating)

## TLDR

```python
VLR Rating ≈ 0.898*KPR + 0.228*APR + -0.434*DPR + 0.0025*ADRa + 0.434*SR + 0.313*KAST + 0.175
```

_Full coefficients below_

## Introduction

This project is dedicated to reverse engineering the rating system used by VLR.gg. The purpose is to uncover the underlying formula that calculates a player's rating based on their performance in matches. This analysis is inspired by the approach taken to reverse-engineer the HLTV rating as detailed in a blog post on [flashed.gg](https://flashed.gg/posts/reverse-engineering-hltv-rating/). For an in-depth explanation of the VLR.gg player rating system, refer to their official post [here](https://www.vlr.gg/160667/vlr-gg-player-rating-explained).

## Methodology

VLR rating

```python
KillContribution + DeathContribution + APR + ADRa + SurvivalRating
```

The final model that results in the highest degree of accuracy uses the following metrics derived from players' match data:

- Kills Per Round (KPR)
- Assists Per Round (APR)
- Deaths Per Round (DPR)
- Average Damage Per Round Adjusted (ADRa)
- Survival Rating (SR)
- Kill, Assist, Survived, Traded Rounds (KAST)

These features were fed into a machine learning model to predict player ratings. The model's coefficients and intercept are as follows:

- Coefficients: `[0.898060946867, 0.227872913948, -0.433940698092, 0.002524365390, 0.433940698092, 0.312874869548]`
- Intercept: `0.17492523147187433`

So, **VLR Rating ≈**

```python
0.898060946867*KPR + 0.227872913948*APR + -0.433940698092*DPR + 0.002524365390*ADRa + 0.433940698092*SR + 0.312874869548*KAST + 0.17492523147187433
```

## Model Performance

The model achieved the following metrics on the test set:

- R2 score: `0.9856412843860585`
- RMSE (Root Mean Squared Error): `0.020110865826540265`
- MAE (Mean Absolute Error): `0.015882295992085477`

## Testing

The model was tested with statistics from [VALORANT Champions 2023](https://www.vlr.gg/event/stats/1657/valorant-champions-2023) and resulted in a minor standard deviation of error.

```python
Demon1       | Actual: 1.23, Predicted: 1.23, Error: 0.00
Leo          | Actual: 1.17, Predicted: 1.24, Error: -0.07
Alfajer      | Actual: 1.17, Predicted: 1.19, Error: -0.02
Less         | Actual: 1.16, Predicted: 1.12, Error: 0.04
AAAAY        | Actual: 1.15, Predicted: 1.15, Error: 0.00
aspas        | Actual: 1.15, Predicted: 1.15, Error: 0.00
Cloud        | Actual: 1.14, Predicted: 1.10, Error: 0.04
cauanzin     | Actual: 1.13, Predicted: 1.11, Error: 0.02
s0m          | Actual: 1.08, Predicted: 1.06, Error: 0.02
...
```

## Usage

1. Ensure Python 3 and pip are installed.
2. Install the required dependencies with `pip install -r requirements.txt`.
3. Run the scraping script within the `src/scraping` folder to collect raw data.
4. Execute the cleaning script within the `src/scraping` to process the raw data.
5. Perform analysis using the script in `src/analysis`.

## Conclusion

Even through limitations in data and score calculations, I believe this project successfully reverse-engineered the VLR.gg player rating system to a high degree of accuracy. While VLR rating is calculated by a round-by-round basis and considers economic situation, I believe this offers a close enough representation of what to expect in the rating calculation.

Overall, these insights for player assessment is important to analyze players' performances and I hope to use this with Post-Plant to predict individual VLR ratings.

For any inquiries or contributions, please open an issue or a pull request on the repository.

## Acknowledgements

- VLR.gg for providing comprehensive statistics on player performance.
- The flashed.gg blog for providing a template for this analysis.
