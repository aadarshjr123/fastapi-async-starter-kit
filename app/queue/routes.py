"""
Queue-related API routes for job submission, status, and metrics.
"""

from fastapi import APIRouter, HTTPException
from app.queue.service import JobService
from app.queue.metrics import update_queue_metrics

router = APIRouter(prefix="/jobs", tags=["Jobs"])


@router.post("/upload/{filename}", summary="Enqueue image processing job")
def upload_image(filename: str):
    """
    Enqueue a new image processing job.
    """
    try:
        job = JobService().enqueue_image_job(filename)
        return {"job_id": job.id, "status": "queued"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Job enqueue failed: {e}")


@router.get("/status/{job_id}", summary="Get job status by ID")
def job_status(job_id: str):
    """
    Retrieve the status and result of a specific job.
    """
    try:
        return JobService().get_job_status(job_id)
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Job not found: {e}")


@router.get("/metrics/update", summary="Refresh queue length metric")
def refresh_metrics():
    """
    Update Prometheus queue length metric.
    """
    return update_queue_metrics()
