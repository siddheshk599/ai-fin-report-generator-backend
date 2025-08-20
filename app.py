import json, logging
from datetime import datetime
from typing import Dict, List, Optional
from fastapi import FastAPI, HTTPException, Depends
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from sqlalchemy.orm import Session

from database import get_db, init_db
from models import Report
from ai_service import generate_financial_report
from pdf_generator import generate_pdf_report

# Configure logging
logging.basicConfig(level=logging.DEBUG)

app = FastAPI(title="AI Financial Report Generator", version="1.0.0")

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database
init_db()

# Pydantic models
class CompanyData(BaseModel):
    revenue: float
    profit: float
    growth_percentage: float
    sector_trends: str
    key_metrics: str
    risks: str
    recommendations: str
    company_name: Optional[str] = "Company"
    executive_name: Optional[str] = "Executive"
    report_title: Optional[str] = "Financial Report"

class ReportResponse(BaseModel):
    id: str
    executive_summary: str
    key_trends: str
    risks: str
    recommendations: str
    top_risks: List[str]
    top_recommendations: List[str]

class SaveReportRequest(BaseModel):
    title: str
    content: Dict
    company_name: str

@app.post("/api/generate-report", response_model=ReportResponse)
async def generate_report(data: CompanyData, db: Session = Depends(get_db)):
    """Generate an AI-powered financial report"""
    try:
        logging.info(f"Generating report for company: {data.company_name}")
        
        # Generate report using AI service
        report_content = await generate_financial_report(data)
        
        # Create response with generated ID
        report_id = f"report_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        response = ReportResponse(
            id=report_id,
            executive_summary=report_content["executive_summary"],
            key_trends=report_content["key_trends"],
            risks=report_content["risks"],
            recommendations=report_content["recommendations"],
            top_risks=report_content["top_risks"],
            top_recommendations=report_content["top_recommendations"]
        )
        
        logging.info("Report generated successfully")
        return response
        
    except Exception as e:
        logging.error(f"Error generating report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to generate report: {str(e)}")

@app.post("/api/export-report")
async def export_report(data: Dict):
    """Export report as PDF"""
    try:
        logging.info("Exporting report as PDF")
        
        # Generate PDF
        pdf_path = generate_pdf_report(data)
        
        return FileResponse(
            pdf_path,
            media_type="application/pdf",
            filename=f"{data.get('company_name', 'report')}_{datetime.now().strftime('%Y%m%d')}.pdf"
        )
        
    except Exception as e:
        logging.error(f"Error exporting report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to export report: {str(e)}")

@app.post("/api/reports")
async def save_report(request: SaveReportRequest, db: Session = Depends(get_db)):
    """Save a report to the database"""
    try:
        logging.info(f"Saving report: {request.title}")
        
        report = Report(
            title=request.title,
            content_json=json.dumps(request.content),
            company_name=request.company_name,
            created_at=datetime.utcnow()
        )
        
        db.add(report)
        db.commit()
        db.refresh(report)
        
        return {"id": report.id, "message": "Report saved successfully"}
        
    except Exception as e:
        logging.error(f"Error saving report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to save report: {str(e)}")

@app.get("/api/reports")
async def get_reports(db: Session = Depends(get_db)):
    """Get all saved reports"""
    try:
        reports = db.query(Report).order_by(Report.created_at.desc()).all()
        
        return [
            {
                "id": report.id,
                "title": report.title,
                "company_name": report.company_name,
                "created_at": report.created_at.isoformat(),
                "content": json.loads(str(report.content_json) if report.content_json else '{}')
            }
            for report in reports
        ]
        
    except Exception as e:
        logging.error(f"Error fetching reports: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch reports: {str(e)}")

@app.get("/api/reports/{report_id}")
async def get_report(report_id: int, db: Session = Depends(get_db)):
    """Get a specific report by ID"""
    try:
        report = db.query(Report).filter(Report.id == report_id).first()
        
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        return {
            "id": report.id,
            "title": report.title,
            "company_name": report.company_name,
            "created_at": report.created_at.isoformat(),
            "content": json.loads(str(report.content_json) if report.content_json else '{}')
        }
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error fetching report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to fetch report: {str(e)}")

@app.delete("/api/reports/{report_id}")
async def delete_report(report_id: int, db: Session = Depends(get_db)):
    """Delete a report"""
    try:
        report = db.query(Report).filter(Report.id == report_id).first()
        
        if not report:
            raise HTTPException(status_code=404, detail="Report not found")
        
        db.delete(report)
        db.commit()
        
        return {"message": "Report deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        logging.error(f"Error deleting report: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Failed to delete report: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}
