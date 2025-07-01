#!/usr/bin/env -S uv run --script

"""
Serve the application.
"""

import json
import logging
import argparse
import mimetypes
import sys
from pathlib import Path
from am.storage.types import NoSuchBucketError
from am.storage.factory import get_storage
from am.config import load_config, config
import fastapi
import uvicorn


sys.path.append(str(Path(__file__).parent))


logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)

app = fastapi.FastAPI()


@app.get("/")
def list_buckets():
    storage = get_storage("default")
    buckets = storage.list_buckets()
    logger.debug("Buckets: %s", buckets)
    return {
        "owner": "test",
        "buckets": [
            {
                "name": bucket.name,
                "creation_date": bucket.creation_date.isoformat(),
            }
            for bucket in buckets
        ],
    }


@app.get("/{bucket}/")
def list_files(bucket: str):
    try:
        storage = get_storage(bucket)
        return {
            "contents": [
                {
                    "key": file.key,
                    "size": file.size,
                    "last_modified": file.last_modified.isoformat(),
                }
                for file in storage.list_files(bucket)
            ]
        }
    except NoSuchBucketError:
        return fastapi.Response(
            status_code=404,
            media_type="application/json",
            content=json.dumps({"details": f"Bucket {bucket} not found"}),
        )


@app.put("/{bucket}/")
def create_bucket(bucket: str):
    storage = get_storage(bucket)
    storage.create_bucket(bucket)
    return {"bucket": bucket}


@app.head("/{bucket}/{file:path}")
def head_file(bucket: str, file: str):
    storage = get_storage(bucket)
    stat = storage.stat(bucket, file)
    return fastapi.Response(
        status_code=200,
        media_type=mimetypes.guess_type(file)[0] or "application/octet-stream",
        headers={
            "Last-Modified": stat.last_modified.isoformat(),
        },
    )


@app.get("/{bucket}/{file:path}")
def get_file(request: fastapi.Request, bucket: str, file: str):
    storage = get_storage(bucket)
    mime_type = mimetypes.guess_type(file)[0] or "application/octet-stream"
    stat = storage.stat(bucket, file)
    with storage.open_read(bucket, file) as f:
        content = f.read()

    if request.headers.get("If-Modified-Since") == stat.last_modified.isoformat():
        return fastapi.Response(
            status_code=304,
            headers={
                "Last-Modified": stat.last_modified.isoformat(),
            },
        )
    return fastapi.Response(
        content=content,
        media_type=mime_type,
        headers={
            "Last-Modified": stat.last_modified.isoformat(),
        },
    )


@app.put("/{bucket}/{file:path}")
async def create_file(request: fastapi.Request, bucket: str, file: str):
    storage = get_storage(bucket)
    with storage.open_write(bucket, file) as f:
        f.write(await request.body())
    return {"file": file}


def load_args():
    """
    Load the arguments.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("other", nargs="*", help="Other arguments are ignored")
    parser.add_argument("--config", type=str, default="config.yaml")
    parser.add_argument("--port", type=int, default=None)
    parser.add_argument("--host", type=str, default=None)
    parser.add_argument("--reload", action="store_true", default=None)
    return parser.parse_args()


try:
    args = load_args()
    load_config(args.config)
except Exception as e:
    logger.error("Error loading config: %s", e)
    sys.exit(1)

if __name__ == "__main__":

    uvicorn.run(
        "serve:app",
        host=args.host or config.server.host,
        port=args.port or config.server.port,
        reload=args.reload or config.server.reload,
    )
