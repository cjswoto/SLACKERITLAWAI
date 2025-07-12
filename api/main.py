import os
import uuid
import jwt
from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from pydantic import BaseModel

SECRET = os.getenv("JWT_SECRET", "secret")
ALGORITHM = "HS256"  # using HS for simplicity

app = FastAPI(title="Disco API")
security = HTTPBearer()


def verify_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    try:
        jwt.decode(credentials.credentials, SECRET, algorithms=[ALGORITHM])
    except jwt.PyJWTError:
        raise HTTPException(status_code=401, detail="Invalid token")


@app.get("/health")
def health():
    return {"status": "ok"}


class UploadResponse(BaseModel):
    flow_id: str


@app.post("/upload/pst", response_model=UploadResponse)
def upload_pst(file: UploadFile = File(...), token: None = Depends(verify_token)):
    flow_id = str(uuid.uuid4())
    # File processing would occur here
    return {"flow_id": flow_id}


@app.get("/search")
def search(q: str, top_k: int = 5, token: None = Depends(verify_token)):
    return {"results": []}


@app.get("/clusters")
def clusters(token: None = Depends(verify_token)):
    return {"clusters": []}


@app.get("/clusters/{cluster_id}")
def cluster_detail(cluster_id: str, token: None = Depends(verify_token)):
    return {"id": cluster_id, "documents": []}


@app.get("/entities")
def entities(token: None = Depends(verify_token)):
    return {"entities": []}


@app.get("/graph")
def graph(token: None = Depends(verify_token)):
    return {"nodes": [], "edges": []}


@app.get("/timeline")
def timeline(token: None = Depends(verify_token)):
    return {"timeline": []}


@app.get("/alerts")
def alerts(token: None = Depends(verify_token)):
    return {"alerts": []}


@app.post("/review/feedback")
def review_feedback(data: dict, token: None = Depends(verify_token)):
    return {"status": "received"}


@app.post("/chat")
def chat(prompt: dict, token: None = Depends(verify_token)):
    return {"response": "ok"}


@app.post("/review/tag")
def review_tag(tag: dict, token: None = Depends(verify_token)):
    return {"status": "tagged"}
