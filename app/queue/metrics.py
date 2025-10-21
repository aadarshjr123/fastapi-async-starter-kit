"""
Prometheus metrics for job queue monitoring.
"""

from prometheus_client import Counter, Gauge
from rq import Queue
from app.queue.worker import redis_conn

# === Counters ===
jobs_created = Counter("jobs_created_total", "Jobs enqueued")
jobs_failed = Counter("jobs_failed_total", "Jobs failed")
jobs_finished = Counter("jobs_finished_total", "Jobs finished")
rate_limited = Counter("rate_limited_total", "Rate-limited requests")

# === Gauges ===
queue_length = Gauge("queue_length", "Current queue length", ["queue"])


def update_queue_metrics() -> dict:
    """
    Refresh queue size metrics for Prometheus.
    """
    q = Queue("default", connection=redis_conn)
    queue_length.labels(queue="default").set(q.count)
    return {"queue_length": q.count}
