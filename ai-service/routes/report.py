from fastapi import APIRouter
from pydantic import BaseModel
from services.job_service import start_job

router = APIRouter()


class ReportRequest(BaseModel):
    data: str


@router.post("/generate-report")
def generate_report(req: ReportRequest):
    job_id = start_job(req.data)

    return {
        "job_id": job_id,
        "status": "processing"
    }