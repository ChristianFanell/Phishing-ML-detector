from fastapi import FastAPI, HTTPException
from dotenv import load_dotenv

# importera datamodell och request-payload
from src.app.dto.url_request import URLRequest
from src.app.dto.pipeline_response import PipelineResponse


load_dotenv()

from src.app.services.pipeline import run_analysis
from prometheus_fastapi_instrumentator import Instrumentator

app = FastAPI(title="Phishing Detection Pipeline API", version="1.0")

# metrics for observability
Instrumentator().instrument(app).expose(app)


@app.post("/api/checkaphish", response_model=PipelineResponse)
async def analyze_url_endpoint(request: URLRequest):
    try:
        result = run_analysis(request.url)
        return result
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))