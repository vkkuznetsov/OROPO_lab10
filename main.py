import os
import psutil
from prometheus_client import Gauge, generate_latest
from fastapi import FastAPI, Response
from fastapi.responses import PlainTextResponse

app = FastAPI()

CPU_USAGE = Gauge('cpu_usage_percent', 'CPU usage percent', ['core'])
MEMORY_TOTAL = Gauge('memory_total_bytes', 'Total memory in bytes')
MEMORY_USED = Gauge('memory_used_bytes', 'Used memory in bytes')
DISK_TOTAL = Gauge('disk_total_bytes', 'Total disk space in bytes', ['partition'])
DISK_USED = Gauge('disk_used_bytes', 'Used disk space in bytes', ['partition'])


def collect_metrics():

    for i, percentage in enumerate(psutil.cpu_percent(percpu=True)):
        CPU_USAGE.labels(core=f'core_{i}').set(percentage)

    memory = psutil.virtual_memory()
    MEMORY_TOTAL.set(memory.total)
    MEMORY_USED.set(memory.used)

    for partition in psutil.disk_partitions():
        usage = psutil.disk_usage(partition.mountpoint)
        DISK_TOTAL.labels(partition=partition.mountpoint).set(usage.total)
        DISK_USED.labels(partition=partition.mountpoint).set(usage.used)


@app.get("/", response_class=PlainTextResponse)
def metrics():
    collect_metrics()
    return Response(content=generate_latest(), media_type="text/plain")


if __name__ == '__main__':
    import uvicorn

    host = os.getenv('EXPORTER_HOST', '127.0.0.1')
    port = int(os.getenv('EXPORTER_PORT', '8080'))

    uvicorn.run(app, host=host, port=port)
