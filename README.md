# PhishingDetection

## Project Overview
An end-to-end machine learning web application that detects phishing content using a trained AdaBoost classifier, deployed on Streamlit Cloud.
This project demonstrates complete machine learning ownership — from data processing and feature engineering to model training and serialization.

## Problem Statement
Phishing attacks exploit users through malicious links and deceptive content.
Manual detection is unreliable, inconsistent, and does not scale.
This system automates phishing detection using machine learning, enabling:
Faster identification of phishing content
Consistent and unbiased predictions
Real-time user feedback through a web interface

## Live Application
🔗 Live Demo: https://websafe.streamlit.app/

Key Capabilities
* End-to-end ML pipeline (not limited to notebooks)
* Real-time inference through a web-based UI
* Trained and serialized machine learning model
* Clean separation of concerns (UI, feature engineering, model logic)
* Deployed and accessible via Streamlit Cloud

System Workflow
* User provides input through the web interface
* Input data is transformed into engineered features
* Features are passed to the trained AdaBoost classifier
* Model predicts one of the following:
* Legitimate
* Phishing
* Prediction is displayed instantly on the UI

## Model Information
* Algorithm: AdaBoost Classifier
* Training Type: Supervised learning
* Dataset: Labeled phishing and legitimate samples
* Model Format: Pickle (.pkl)
* Inference: Local, low-latency prediction
