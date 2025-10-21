"""
Middleware that profiles request execution using cProfile.
Activated only when PROFILE=1.
"""

import os
import time
import cProfile
from pathlib import Path
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response

logger = logging.getLogger("app.utils.profiler")


class RequestProfilerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, dump_dir: str = "/app/profiles"):
        super().__init__(app)
        self.dump_dir = Path(dump_dir)
        self.dump_dir.mkdir(parents=True, exist_ok=True)

    async def dispatch(self, request: Request, call_next):
        """
        Profiles a request if PROFILE=1 is set in the environment.
        Saves the profiling report in .prof files under /app/profiles.
        """
        if os.getenv("PROFILE", "0") != "1":
            return await call_next(request)

        profiler = cProfile.Profile()
        start = time.perf_counter()
        profiler.enable()

        try:
            response: Response = await call_next(request)
        finally:
            profiler.disable()

        elapsed_ms = (time.perf_counter() - start) * 1000
        path = request.url.path.strip("/").replace("/", "_") or "root"
        fname = f"{request.method}_{path}_{int(elapsed_ms)}ms.prof"
        fpath = self.dump_dir / fname
        profiler.dump_stats(str(fpath))

        logger.info(f"Profile saved: {fpath} ({elapsed_ms:.2f} ms)")
        return response
