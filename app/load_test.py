"""
Simple concurrent load test script for local performance benchmarking.
"""

import time
import requests
import concurrent.futures

URL = "http://127.0.0.1:8000/users"
REQUESTS = 30
WORKERS = 3


def hit(_):
    try:
        r = requests.get(URL)
        return r.status_code
    except Exception:
        return None


def run_load_test():
    start = time.time()
    with concurrent.futures.ThreadPoolExecutor(max_workers=WORKERS) as ex:
        results = list(ex.map(hit, range(REQUESTS)))

    duration = round(time.time() - start, 2)
    success = results.count(200)
    print(f"✅ {success}/{REQUESTS} OK in {duration}s ({WORKERS} workers)")


if __name__ == "__main__":
    run_load_test()
