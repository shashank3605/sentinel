import time
import statistics
import requests

URL = "http://127.0.0.1:8000/score"
NUM_REQUESTS = 100

payload = {
    "transaction_id": "bench_txn",
    "user_id": "bench_user",
    "amount": 4500,
    "currency": "INR",
    "timestamp": "2026-09-04T10:15:00",
    "channel": "UPI",
}

latencies_ms = []

for i in range(NUM_REQUESTS):
    start = time.perf_counter()
    response = requests.post(URL, json=payload)
    end = time.perf_counter()

    if response.status_code != 200:
        print(f"Request {i} failed: {response.status_code} {response.text}")
        continue

    latencies_ms.append((end - start) * 1000)  # convert seconds to ms

latencies_ms.sort()

def percentile(data, pct):
    index = int(len(data) * pct / 100)
    return data[min(index, len(data) - 1)]

print(f"Requests completed: {len(latencies_ms)}/{NUM_REQUESTS}")
print(f"Min:    {min(latencies_ms):.2f} ms")
print(f"p50:    {percentile(latencies_ms, 50):.2f} ms")
print(f"p95:    {percentile(latencies_ms, 95):.2f} ms")
print(f"p99:    {percentile(latencies_ms, 99):.2f} ms")
print(f"Max:    {max(latencies_ms):.2f} ms")
print(f"Mean:   {statistics.mean(latencies_ms):.2f} ms")