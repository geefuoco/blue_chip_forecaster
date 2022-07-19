# Blue Chip Forecaster

A Data Science project for Lighthouse Labs. The goal of the project was to forecast stock closing prices for the current day.

## Modules
- Data Gathering:
  - module to collect data from sources (yahoo finance, wallstreet journal)
- Crawler
  - a web crawler designed to grab headlines from WSJ
- Data Visualization
  - a group of functions to visualize the data
- Forecast
  - a module that uses facebook's prophet package to forecast
- Preprocessing
  - contains a class that can fully preprocess data for modeling
- Sentiment Analysis
  - a module that makes use of huggingface transformers to perform sentiment analysis
- Model
  - a module that handles creating, predicting, training, and saving of a machine learning model
