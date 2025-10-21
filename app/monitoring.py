"""
System monitoring routes exposing Prometheus metrics in JSON.
"""

from prometheus_client import REGISTRY
from fastapi import APIRouter, Response
import json

router = APIRouter(prefix="/system", tags=["System"])


@router.get("/metrics", summary="Get Prometheus metrics as JSON")
def get_metrics():
    """
    Collect all Prometheus metrics and return them as a formatted JSON response.
    """
    metrics_data = {}
    for metric in REGISTRY.collect():
        samples = {s.name: s.value for s in metric.samples}
        metrics_data[metric.name] = samples

    return Response(
        content=json.dumps(metrics_data, indent=2),
        media_type="application/json",
    )
