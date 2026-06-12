import pytest
import time
import logging
from unittest.mock import patch
from fastapi.testclient import TestClient

from src.app.main import app 

client = TestClient(app)

class TestPhishingPipelineIntegration:
    
    @patch('src.app.services.safe_api.GoogleSafeBrowsing.is_url_safe')
    def test_stage_1_fast_fail_malicious_url(self, mock_is_url_safe, caplog):
        # Arrange
        mock_is_url_safe.return_value = False
        test_payload = {"url": "http://evil-phishing.com"}
        
        # Act
        start_time = time.perf_counter()
        with caplog.at_level(logging.INFO):
            response = client.post("/api/checkaphish", json=test_payload)
        latency_ms = (time.perf_counter() - start_time) * 1000

        # Assert
        assert response.status_code == 200
        json_response = response.json()
        
        assert "status" in json_response
        assert json_response["status"] == "BLOCKED"
        assert json_response["source"] == "Google Safe Browsing API"
        
        mock_is_url_safe.assert_called_once_with("http://evil-phishing.com")
        assert latency_ms < 500


    @patch('src.app.services.url_feature_checker.FeatureExtractor.extract') 
    @patch('src.app.services.safe_api.GoogleSafeBrowsing.is_url_safe')
    def test_stage_2_full_pipeline_safe_url(self, mock_is_url_safe, mock_extractor, caplog):
        # Arrange
        mock_is_url_safe.return_value = True
        mock_extractor.return_value = [[0, 54, 0, 0, 1, 0, 1, 0, 1, 0, 0]] 
        test_payload = {"url": "https://my-real-bank.com"}

        # Act
        start_time = time.perf_counter()
        response = client.post("/api/checkaphish", json=test_payload)
        latency_ms = (time.perf_counter() - start_time) * 1000

        # Assert 
        assert response.status_code == 200
        json_response = response.json()
        
        assert json_response["status"] in ["BLOCKED", "ALLOWED"]
        assert json_response["source"] == "Random Forest Ensemble"
        assert "confidence" in json_response
        
        mock_is_url_safe.assert_called_once()
        mock_extractor.assert_called_once()
        assert latency_ms < 500