import os
from fastapi import FastAPI, UploadFile, File
from pypdf import PdfReader
from io import BytesIO
from agent.job_graph import job_app
from dotenv import load_dotenv

load_dotenv()

app = FastAPI()

@app.get("/")
def home():
    return {"message": "Vantage AI - Agentic Engine is running"}

@app.post("/find-jobs")
async def find_jobs(
    file: UploadFile = File(...), 
    
    location: str = "India", 
    min_salary: str = "Any",
    refresh_id: int = 0,
    seen_urls: str = "" # Comma separated
):
    # 1. Read PDF
    pdf_content = await file.read()
    text = ""
    try:
        reader = PdfReader(BytesIO(pdf_content))
        for page in reader.pages:
            text += page.extract_text() or ""
    except Exception as e:
        from fastapi import HTTPException
        raise HTTPException(status_code=400, detail="Invalid or unreadable PDF file.")
    
    try:
        # 2. Run Graph
        url_list = [u.strip() for u in seen_urls.split(",") if u.strip()]
        initial_state = {
            "resume_text": text,
            "location": location,
            "min_salary": min_salary,
            "extract_data": {},
            "jobs": [],
            "final_report": {},
            "seen_urls": url_list
        }
        
        final_state = job_app.invoke(initial_state)
        final_report = final_state.get("final_report", {})
        
        # Safety Check
        if isinstance(final_report, str):
            final_report = {
                "match": "80%",
                "match_label": "Compatible",
                "insights": [{"icon": "◈", "label": "Analysis", "text": final_report}]
            }
        
        return {
            "skills": final_state.get("extract_data", {}).get("skills", []),
            "jobs_found": final_state.get("jobs", []),
            "report": final_report
        }
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(error_details)  # Log to console
        raise HTTPException(status_code=500, detail=f"Graph Execution Error: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)