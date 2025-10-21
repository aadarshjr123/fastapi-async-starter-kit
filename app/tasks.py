"""
RQ background job definitions.
"""

import time
import random
import logging
from rq.job import Job
from rq.registry import FinishedJobRegistry
from app.queue_setup import queue, redis_conn

logger = logging.getLogger("app.tasks")


def process_image(filename: str):
    """
    Simulate an image processing task.
    Randomly fails to simulate retry logic.
    """
    logger.info(f"🟢 Processing {filename}...")
    time.sleep(3)

    if random.random() < 0.3:
        logger.error(f"❌ Failed to process {filename} (simulated error).")
        raise Exception("Random simulated failure")

    logger.info(f"✅ Finished processing {filename}")
    return f"Processed {filename}"


def clean_old_jobs():
    """
    Clean finished jobs from Redis registry to keep it lightweight.
    """
    registry = FinishedJobRegistry(queue=queue)
    count = 0
    for job_id in registry.get_job_ids():
        job = Job.fetch(job_id, connection=redis_conn)
        job.delete()
        count += 1
    logger.info(f"🧹 Cleaned {count} finished jobs from registry.")
    return f"Cleaned {count} jobs"
