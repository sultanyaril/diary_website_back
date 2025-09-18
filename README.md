# Diary Website Backend

This project is the backend for a Diary Website, designed to support user authentication, diary entry management, and advanced emotion detection from diary entries. Built with Python and Flask, it is structured for scalability and clarity.

## Features

- **User Authentication**: Secure registration and login endpoints.
- **Diary Entry Management**: Create, read, update, and delete diary entries.
- **Emotion Detection**: Analyze diary entries to predict the emotional tone using machine learning models.
- **Evaluation Endpoints**: Assess and validate emotion predictions.

## Emotion Detection (Highlight)

The core data science feature of this project is the emotion detection service, implemented in `app/services/emotion_predictor.py`. This module leverages NLP techniques and machine learning models to classify the emotional content of diary entries. The pipeline can be easily extended or replaced with custom models, making it ideal for experimentation and showcasing your data science skills.

- **Modular Design**: The emotion predictor is decoupled from the main app logic, allowing for rapid prototyping and integration of new models.
- **Customizable**: Swap in your own models or feature extraction methods to improve accuracy or adapt to new datasets.
- **API Integration**: The emotion detection service is exposed via RESTful endpoints, enabling easy integration with frontends or other applications.

## Project Structure

```
app/
  __init__.py
  config.py
  models.py
  utilities.py
  routes/
    auth_routes.py
    emotion_routes.py
    entry_routes.py
    evaluate_routes.py
  services/
    emotion_predictor.py
instance/
  diary.db
requirements.txt
run.py
```

## Getting Started

1. **Clone the repository**
2. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Run the application**:
   ```bash
   python run.py
   ```

## API Endpoints

- `/auth/*` — User authentication
- `/entries/*` — Diary entry CRUD
- `/emotions/predict` — Predict emotion from text
- `/evaluate/*` — Evaluate emotion predictions

## Customizing Emotion Detection

To use your own emotion detection model:
1. Replace or extend the logic in `app/services/emotion_predictor.py`.
2. Update dependencies in `requirements.txt` as needed.
3. Test via the `/emotions/predict` endpoint.
