from fastapi import FastAPI, File, UploadFile, Form, HTTPException
import os
import uuid
import asyncio
import logging

from crewai import Crew, Process
from agents import doctor
from task import help_patients

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Blood Test Report Analyser")

def run_crew(query: str, file_path: str="data/sample.pdf"):
    """To run the whole crew"""
    medical_crew = Crew(
        agents=[doctor],
        tasks=[help_patients],
        process=Process.sequential,
    )
    
    result = medical_crew.kickoff({
        'query': query,
        'file_path': file_path
    })
    return result

@app.get("/")
async def root():
    """Health check endpoint"""
    return {"message": "Blood Test Report Analyser API is running"}

@app.post("/analyze")
async def analyze_blood_report(
    file: UploadFile = File(...),
    query: str = Form(default="Summarise my Blood Test Report")
):
    """Analyze blood test report and provide comprehensive health recommendations"""
    
    logger.info(f"Received analysis request for file: {file.filename}, query: {query}")
    
    # Validate file type
    if not file.filename.lower().endswith('.pdf'):
        logger.warning(f"Invalid file type uploaded: {file.filename}")
        raise HTTPException(status_code=400, detail="Only PDF files are supported")
    
    # Validate file size (max 10MB)
    MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB
    content = await file.read()
    if len(content) > MAX_FILE_SIZE:
        logger.warning(f"File too large: {file.filename}, size: {len(content)} bytes")
        raise HTTPException(status_code=400, detail="File size too large. Maximum size is 10MB")
    
    # Generate unique filename to avoid conflicts
    file_id = str(uuid.uuid4())
    file_path = f"data/blood_test_report_{file_id}.pdf"
    
    try:
        # Ensure data directory exists
        os.makedirs("data", exist_ok=True)
        
        # Save uploaded file
        with open(file_path, "wb") as f:
            f.write(content)
        
        logger.info(f"File saved successfully: {file_path}")
        
        # Validate query
        if query=="" or query is None:
            query = "Summarise my Blood Test Report"
            
        # Process the blood report with all specialists
        logger.info(f"Starting CrewAI analysis for file: {file_path}")
        response = run_crew(query=query.strip(), file_path=file_path)
        
        logger.info(f"Analysis completed successfully for file: {file.filename}")
        
        return {
            "status": "success",
            "query": query,
            "analysis": str(response),
            "file_processed": file.filename
        }
        
    except Exception as e:
        logger.error(f"Error processing blood report: {str(e)}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Error processing blood report: {str(e)}")
    
    finally:
        # Clean up uploaded file
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                logger.info(f"Cleaned up temporary file: {file_path}")
            except Exception as cleanup_error:
                logger.warning(f"Could not clean up file {file_path}: {cleanup_error}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000, reload=True)