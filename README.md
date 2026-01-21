# PhisingDetection
An end-to-end machine learning web application that detects phishing content using a trained AdaBoost classifier, deployed on Streamlit Cloud.
This project demonstrates complete ML ownership — from data processing and feature engineering to model training, persistence, and production deployment.

Problem Statement

Phishing attacks exploit users through malicious links and deceptive content.
Manual detection is unreliable and does not scale.
This system automates phishing detection using machine learning, enabling:
1.Faster identification
2.Consistent predictions
3.Real-time user feedback via a web interface

Live Application

🔗 Live Demo: https://websafe.streamlit.app/

Key Capabilities

End-to-end ML pipeline (not just a notebook)
Real-time inference via web UI
Trained and serialized ML model
Clean separation of concerns (UI, ML, features)
Deployment on Streamlit

System Workflow
User provides input via web interface
Input is converted into engineered features
Features are passed to the trained AdaBoost model
Model predicts:
1.Legitimate
2.Phishing
3.Prediction is displayed instantly on the UI

Model Information

Algorithm: AdaBoost Classifier
Training: Supervised learning on labeled phishing/legitimate data
Model Format: Pickle (.pkl)
Inference: Local, low-latency
