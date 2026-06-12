# Machine Learning Engineering Project

Project assignment for the course "Machine learning engineering" via Blekinge tekniska högskola. This repository contains a machine learning pipeline and REST API designed to detect phishing URLs.

## Prerequisites

* **Google Safe Browsing API Key:** The system relies on Google's threat intelligence API for its initial validation stage. 
* *Note:* If you do not have a valid API key, you must comment out lines 9-10 in `safe_api.py` to bypass this check before running the application.

If you want to train the model, you need the dataset. This is not included in this repo.

## Setup
Activate your Python virtual environment:

```bash
source .venv/bin/activate
```

## Run it

```
docker compose up -d --build
```

## Try it out
```
curl -X POST "http://localhost:8000/api/checkaphish" \
     -H "Content-Type: application/json" \
     -d '{"url": "[https://192.1.1.1/evil-website"}'
```

## Run tests 
```
docker compose run --rm test 
```