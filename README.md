# Reverse Engineering the VLR Player Rating

[Full in-depth blog post](https://markzhdan.com/blogs/reverse-engineering-vlr-rating)

## TLDR

```python
VLR Rating ≈ 0.468*KPR + 0.312*APR + -1.154*DPR + 0.004*ADR + -0.0007*ACS + -0.063*FDPR + 0.205*FKPR + 1.001
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
- Average Damage Per Round (ADR)
- Average Combat Score (ACS)
- First Death Per Round (FDPR)
- First Kill Per Round (FKPR)

These features were fed into a machine learning model to predict player ratings. The model's coefficients and intercept are as follows:

- Coefficients: `[0.467584759836, 0.312158631682, -1.153682762595, 0.003942697956, -0.000725869108, -0.063496102738, 0.204588665932]`
- Intercept: `1.0013936330345852`

So, **VLR Rating ≈**

```python
0.467584759836*KPR + 0.312158631682*APR + -1.153682762595*DPR + 0.003942697956*ADR + -0.000725869108*ACS + -0.063496102738*FDPR + 0.204588665932*FKPR + 1.0013936330345852
```

## Model Performance

The model achieved the following metrics on the test set:

- R2 score: `0.9662357787569015`
- RMSE (Root Mean Squared Error): `0.015609055720644964`
- MAE (Mean Absolute Error): `0.011419627259488604`

## Testing

The model was tested with statistics from [VALORANT Champions 2023](https://www.vlr.gg/event/stats/1657/valorant-champions-2023) and resulted in a minor standard deviation of error.

```python
Demon1       | Actual: 1.23, Predicted: 1.23, Error: 0.00
Less         | Actual: 1.16, Predicted: 1.11, Error: 0.05
aspas        | Actual: 1.15, Predicted: 1.13, Error: 0.03
cauanzin     | Actual: 1.13, Predicted: 1.10, Error: 0.03
SUYGETSU     | Actual: 1.10, Predicted: 1.09, Error: 0.01
jawgemo      | Actual: 1.10, Predicted: 1.09, Error: 0.01
d4v41        | Actual: 1.08, Predicted: 1.09, Error: -0.01
cNed         | Actual: 1.08, Predicted: 1.09, Error: -0.01
something    | Actual: 1.08, Predicted: 1.03, Error: 0.05
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
