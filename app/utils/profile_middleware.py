# app/utils/profile_middleware.py
import cProfile, pstats, io, os, time
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from starlette.responses import Response
from pathlib import Path


class RequestProfilerMiddleware(BaseHTTPMiddleware):
    def __init__(self, app, dump_dir: str = "/app/profiles"):
        super().__init__(app)
        self.dump_dir = Path(dump_dir)
        self.dump_dir.mkdir(parents=True, exist_ok=True)

    async def dispatch(self, request: Request, call_next):
        # Only profile when explicitly enabled
        if os.getenv("PROFILE", "0") != "1":
            return await call_next(request)

        pr = cProfile.Profile()
        start = time.time()
        pr.enable()
        try:
            response: Response = await call_next(request)
        finally:
            pr.disable()
        elapsed = (time.time() - start) * 1000

        # File name: method_path_timestamp.prof (sanitize slashes)
        path = request.url.path.strip("/").replace("/", "_") or "root"
        fname = f"{request.method}_{path}_{int(time.time())}_{int(elapsed)}ms.prof"
        fpath = self.dump_dir / fname
        pr.dump_stats(str(fpath))
        return response
