# NFL Win Predictor (Homework 1)

Start here: open the live app at https://mlbahwk1nfl.streamlit.app/ and upload `standings.csv` from this repo.

A small Streamlit app that fits a straight-line (linear regression) model on a CSV file you upload. Pick two input columns and a target, and the app shows what the line predicts for values you type in.

## What the app does

1. Upload a CSV file and see a preview of the first rows.
2. Pick a numeric column and a chart type (line, scatter, or histogram) and see the chart.
3. Pick two input columns and one target column. The app fits a linear regression and shows how much the target changes for each extra unit of each input, plus R2 on the uploaded data.
4. Type a value for each input to see the model's prediction. If a value is outside the range the model learned from, the app shows a warning.

The page also states what the model is for and what happens when it is wrong: it gives a rough estimate of a team's wins from the points it scores and allows, and when it is wrong a team can look stronger or weaker than it really is.

## Try it with the sample data

This repository includes `standings.csv`, one row per NFL team per regular season, 2002 through 2025 (768 rows).

1. Click `standings.csv` in this repository, then click the download icon.
2. Open the live app and upload the file.
3. The app starts on `scored` and `allowed` as inputs and `wins` as the target. With these choices, R2 on this data is 0.83.

Columns: `season`, `conf`, `division`, `team`, `wins`, `losses`, `ties`, `pct`, `div_rank`, `scored`, `allowed`, `net`, `sov`, `sos`, `seed`, `playoff`.

The app works with any CSV that has at least three numeric columns.

## Data source

`standings.csv` comes from the `nfldata` repository by Lee Sharpe, part of the nflverse project (https://github.com/nflverse/nfldata). Attribution: nflverse (https://nflverse.com). nflverse data is generally released under CC-BY 4.0; see the nflverse repositories for the license that applies to each dataset.

- Accessed: October 25, 2026.
- The source file also contains the 2026 season, which is still in progress (teams had played only 5 to 7 games), so those rows were removed. No other changes were made.

## Limits of the model

- It is a straight line fitted to all of the uploaded rows. R2 is measured on those same rows, not on held-out data, so it describes how well the line fits this data and not how well it would predict new seasons.
- It uses only the two inputs you choose. Injuries, schedule strength, and many other things that affect wins are not included.
- Predictions for values outside the range of the data are extrapolations and should be treated with caution.

## Files

- `app.py`: the Streamlit app
- `requirements.txt`: the libraries Streamlit Cloud installs (streamlit, pandas, plotly, scikit-learn)
- `standings.csv`: sample data
- `README.md`: this file

## Run it locally

    pip install -r requirements.txt
    streamlit run app.py
