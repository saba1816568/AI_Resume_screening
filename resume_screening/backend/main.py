# FastAPI main file
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from ranking import rank_resumes
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware  # ✅ Import this
from pydantic import BaseModel
from typing import List

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow requests from any origin
    allow_credentials=True,
    allow_methods=["*"],  # Allow all HTTP methods (GET, POST, OPTIONS, etc.)
    allow_headers=["*"],  # Allow all headers
)
# Define request body format
class ResumeRequest(BaseModel):
    resumes: list[str]
    job_description: str

@app.post("/rank_resumes/")
async def rank_resumes_api(request: ResumeRequest):
    """
    API Endpoint to rank resumes based on job description.
    """
    if not request.resumes or not request.job_description:
        raise HTTPException(status_code=400, detail="Resumes and job description cannot be empty.")
    print(request)
    
    ranked_results = rank_resumes(request.resumes, request.job_description)

    # Return ranked results in JSON format
    return {"ranked_resumes": ranked_results}
    

@app.get("/")
async def root():
    return {"message": "AI-Based Resume Screening System is running!"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
