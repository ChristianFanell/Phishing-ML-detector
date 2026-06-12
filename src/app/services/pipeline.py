import logging
import json
import sys
import joblib
from pathlib import Path

from src.app.services.safe_api import GoogleSafeBrowsing
from src.app.services.url_feature_checker import FeatureExtractor

google_checker = GoogleSafeBrowsing()
extractor = FeatureExtractor()


MODEL_PATH = Path(__file__).resolve().parent.parent.parent.parent / 'models' / 'model.joblib'

if MODEL_PATH.exists():
    model = joblib.load(MODEL_PATH)
    print(f"Model loaded from: {MODEL_PATH.name}")
else:
    model = None
    print(f"Shit got real! Model not found: {MODEL_PATH}")


# observabilitet
ml_logger = logging.getLogger("ml_payloads")
ml_logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
ml_logger.addHandler(handler)


def log_and_return(response_dict: dict) -> dict:
    compact_json = json.dumps(response_dict, separators=(',', ':'))
    ml_logger.info(compact_json)
    return response_dict


def run_analysis(target_url: str) -> dict:
    """
    Executes the full pipeline: Google API -> Extraction -> ML Inference
    """

    if not google_checker.is_url_safe(target_url):
        return log_and_return({
            "url": target_url,
            "status": "BLOCKED",
            "source": "Google Safe Browsing API",
            "confidence": 1.0
        })

    try:
        feature_vector = extractor.extract(target_url)
    except Exception as e:
        raise RuntimeError(f"Feature extraction failed: {str(e)}")

    # fallback, ch. 15 ML in action, eller "Leveraging Expert Consistency to Improve Algorithmic Decision Support"
    if feature_vector[0][0] == -1:
        return log_and_return({
            "url": target_url,
            "status": "BLOCKED",
            "source": "Heuristic rule: IP based URL",
            "confidence": 1.0
        })

    if model is None:
        raise RuntimeError("ML Model is not loaded into memory. Check the file path.")

    try:
        prediction = model.predict(feature_vector)[0]
        probabilities = model.predict_proba(feature_vector)[0]
        
        is_legit = (prediction == 1)
        confidence_score = round(probabilities[1] if is_legit else probabilities[0], 4)

        return log_and_return({
            "url": target_url,
            "status": "ALLOWED" if is_legit else "BLOCKED",
            "source": "Random Forest Ensemble",
            "confidence": confidence_score,
            "features": feature_vector[0]
        })
        
    except Exception as e:
        raise RuntimeError(f"Model Inference failed: {str(e)}")
    
