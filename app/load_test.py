import requests, concurrent.futures, time

URL = "http://127.0.0.1:8000/users"


def hit(_):
    r = requests.get(URL)
    return r.status_code


start = time.time()
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
    results = list(ex.map(hit, range(30)))
print("done", results.count(200), "OK in", round(time.time() - start, 2), "s")
