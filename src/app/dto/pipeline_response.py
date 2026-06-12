from pydantic import BaseModel

class PipelineResponse(BaseModel):
    url: str
    status: str
    source: str
    confidence: float