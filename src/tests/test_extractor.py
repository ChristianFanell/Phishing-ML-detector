import pytest
import socket
from unittest.mock import patch, MagicMock
from src.app.services.url_feature_checker import FeatureExtractor


@pytest.fixture
def extractor():
    return FeatureExtractor()

@pytest.fixture
def offline_extractor(monkeypatch, extractor):
    """
    No internet traffic for these unit tests
    """
    monkeypatch.setattr(extractor, '_check_dns', lambda domain: 1)
    monkeypatch.setattr(extractor, '_check_ssl', lambda domain: 1)
    return extractor

def get_feature(ext, url, feature_name):
    features_array = ext.extract(url)[0]
    feature_dict = dict(zip(ext.feature_names, features_array))
    return feature_dict[feature_name]


@pytest.mark.parametrize("url, expected", [
    ("http://192.168.1.100/secure-login", -1),
    ("https://bth.se/student", 1)
])
def test_ip_address_detection(offline_extractor, url, expected):
    """IP addresses  (-1)."""
    assert get_feature(offline_extractor, url, 'having_IPhaving_IP_Address') == expected

@pytest.mark.parametrize("url, expected", [
    ("https://google.com", 1),
    ("https://paypal-secure.update-billing.com/login-attempt-verify-account-now", -1) # >= 54 chars
])
def test_url_length_logic(offline_extractor, url, expected):
    """Test the URL length """
    assert get_feature(offline_extractor, url, 'URLURL_Length') == expected

@pytest.mark.parametrize("url, expected", [
    ("https://github.com/christian", 1),
    ("https://legit-site.com@phishing-site.com/login", -1)
])
def test_at_symbol_detection(offline_extractor, url, expected):
    """@ symbol"""
    assert get_feature(offline_extractor, url, 'having_At_Symbol') == expected


@patch("src.app.services.url_feature_checker.socket.gethostbyname")
def test_dns_record_success(mock_gethostbyname, extractor):
    """ DNS resolution."""
    mock_gethostbyname.return_value = "192.168.1.10"
    
    assert extractor._check_dns("legit-site.com") == 1
    mock_gethostbyname.assert_called_once_with("legit-site.com")

@patch("src.app.services.url_feature_checker.socket.gethostbyname")
def test_dns_record_failure(mock_gethostbyname, extractor):
    """failed DNS resolution """
    mock_gethostbyname.side_effect = socket.error("Host not found")
    
    assert extractor._check_dns("fake-phishing-domain.net") == -1

@patch("src.app.services.url_feature_checker.ssl.create_default_context")
@patch("src.app.services.url_feature_checker.socket.create_connection")
def test_ssl_state_success(mock_create_connection, mock_ssl_context, extractor):
    """Simulate a successful SSL handshake."""
    mock_socket = MagicMock()
    mock_create_connection.return_value.__enter__.return_value = mock_socket
    
    mock_context = MagicMock()
    mock_ssl_context.return_value = mock_context
    mock_context.wrap_socket.return_value.__enter__.return_value = MagicMock()
    
    assert extractor._check_ssl("secure-bank.com") == 1
    mock_create_connection.assert_called_once_with(("secure-bank.com", 443), timeout=3)

@patch("src.app.services.url_feature_checker.socket.create_connection")
def test_ssl_state_failure(mock_create_connection, extractor):
    """Simulate an SSL connection failure"""
    mock_create_connection.side_effect = socket.timeout("Connection timed out")
    
    assert extractor._check_ssl("sketchy-site.com") == -1