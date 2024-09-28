# Phishing Link Scanner ✈️🔍

## Overview
The Phishing Link Scanner is a Python-based application designed to detect malicious URLs and provide users with insights into the safety of websites. Using machine learning and heuristic methods, this tool aims to protect users from phishing attempts and unsafe web content.

## Project Details
- **Model**: The scanner utilizes a Naive Bayes model trained on a dataset of URLs labeled as safe or malicious.
- **Features**:
  - Checks if a website is safe or malicious based on machine learning predictions.
  - Performs heuristic checks to identify suspicious URLs.
  - Resolves domain names to IP addresses.
  - Logs all checks and results for future reference.

## How to Use
1. **Clone the repository** or download the files.
2. **Install required libraries**:
   pip install requests pandas scikit-learn joblib
Prepare the dataset: Ensure you have a CSV file named url_dataset.csv with two columns: url and label.
Train the model: Run the training script:

python train.py
This will create url_classifier_model.pkl and vectorizer.pkl files needed for the scanner.
Run the phishing scanner:
python phishing_scanner.py

Follow the on-screen menu to check URLs or get the IP address of a domain.
Author
👤 Dharmpreet Singh

Stay safe online! 🌐✨
