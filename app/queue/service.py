"""
Service layer for RQ job management.
"""

from rq import Retry
from rq.job import Job
from rq import Queue
from app.queue.worker import redis_conn
from app.tasks import process_image
from app.queue.metrics import jobs_created, jobs_finished, jobs_failed


class JobService:
    """
    Handles job enqueueing, monitoring, and status retrieval.
    """

    def __init__(self):
        self.queue = Queue("default", connection=redis_conn)

    def enqueue_image_job(self, filename: str):
        """
        Enqueue a new image processing task with retry logic.
        """
        jobs_created.inc()
        try:
            job = self.queue.enqueue(
                process_image,
                filename,
                retry=Retry(max=3, interval=[5, 10, 20]),
            )
            return job
        except Exception as e:
            jobs_failed.inc()
            raise RuntimeError(f"Failed to enqueue job: {e}")

    def get_job_status(self, job_id: str) -> dict:
        """
        Retrieve the status and result of a queued job.
        """
        try:
            job = Job.fetch(job_id, connection=redis_conn)
            status = job.get_status()
            if status == "finished":
                jobs_finished.inc()
            return {
                "job_id": job.id,
                "status": status,
                "result": job.result,
                "enqueued_at": str(job.enqueued_at),
                "ended_at": str(job.ended_at),
                "retries_left": getattr(job, "retries_left", None),
            }
        except Exception as e:
            jobs_failed.inc()
            raise RuntimeError(f"Error fetching job status: {e}")
