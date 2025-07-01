#!/usr/bin/env -S uv run --script

"""
Serve the application.
"""

import logging
import sys
from pathlib import Path
from am.storage.factory import get_storage
import fastapi
import uvicorn


sys.path.append(str(Path(__file__).parent))


logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)

app = fastapi.FastAPI()


@app.get("/")
def list_buckets():
    return {"buckets": ["test"]}


@app.get("/{bucket}/")
def list_files(bucket: str):
    storage = get_storage(bucket)
    return {"files": storage.list_files(bucket)}


@app.put("/{bucket}/")
def create_bucket(bucket: str):
    storage = get_storage(bucket)
    storage.create_bucket(bucket)
    return {"bucket": bucket}


@app.get("/{bucket}/{file:path}")
def get_file(bucket: str, file: str):
    storage = get_storage(bucket)
    with storage.open_read(bucket, file) as f:
        return f.read()


@app.put("/{bucket}/{file:path}")
async def create_file(request: fastapi.Request, bucket: str, file: str):
    storage = get_storage(bucket)
    with storage.open_write(bucket, file) as f:
        f.write(await request.body())
    return {"file": file}


if __name__ == "__main__":
    uvicorn.run("serve:app", host="0.0.0.0", port=8000, reload=True)
