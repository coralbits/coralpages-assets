"""
DiskStorage is a storage backend that uses the local filesystem.

It is used to store the data of the application.

It is a simple storage backend that uses the local filesystem.
"""

from datetime import datetime
import os
import shutil
import logging
from contextlib import contextmanager
from itertools import islice
from pathlib import Path
from typing import BinaryIO, Generator
from am.storage.types import NoSuchBucketError, NoSuchFileError, Storage, FileData

logger = logging.getLogger(__name__)


class DiskStorage(Storage):
    """
    DiskStorage is a storage backend that uses the local filesystem.
    """

    def __init__(self, config: dict):
        self.path = config["path"]

    def create_bucket(self, name: str) -> None:
        logger.debug("Creating bucket=%s", name)
        os.makedirs(os.path.join(self.path, name), exist_ok=True)

    def delete_bucket(self, name: str) -> None:
        logger.debug("Deleting bucket=%s", name)
        shutil.rmtree(os.path.join(self.path, name))

    def list_buckets(self, start: int = 0, limit: int = 100) -> list[str]:
        logger.debug("Listing buckets: start=%s limit=%s", start, limit)
        return os.listdir(self.path)[start : start + limit]

    def list_files(
        self, bucket: str, start: int = 0, limit: int = 100
    ) -> list[FileData]:
        logger.debug(
            "Listing files: bucket=%s start=%s limit=%s path=%s",
            bucket,
            start,
            limit,
            self.path,
        )

        def list_recursive(path: str, prefix: str) -> Generator[FileData, None, None]:
            files = os.listdir(path)
            # first list plain files
            for file in files:
                if not os.path.isdir(os.path.join(path, file)):
                    yield FileData(
                        name=os.path.join(prefix, file),
                        size=os.path.getsize(os.path.join(path, file)),
                        modified=os.path.getmtime(os.path.join(path, file)),
                    )
            # then list directories
            for file in files:
                if os.path.isdir(os.path.join(path, file)):
                    yield from list_recursive(
                        os.path.join(path, file), os.path.join(prefix, file)
                    )

        bucket_path = Path(self.path) / bucket
        if not bucket_path.exists():
            raise NoSuchBucketError(f"Bucket {bucket} does not exist")

        ret = list(
            islice(
                list_recursive(bucket_path, ""),
                start,
                start + limit,
            )
        )
        logger.debug("Found files count=%s", ret)
        return ret

    @contextmanager
    def open_read(self, bucket: str, file: str) -> Generator[BinaryIO, None, None]:
        filepath = Path(self.path) / bucket / file
        if not filepath.exists():
            raise NoSuchFileError(f"File {file} does not exist")
        logger.debug("Opening file for reading: bucket=%s file=%s", bucket, file)
        with open(filepath, "rb") as f:
            yield f

    @contextmanager
    def open_write(self, bucket: str, file: str) -> Generator[BinaryIO, None, None]:
        filepath = Path(self.path) / bucket / file
        filepath.parent.mkdir(parents=True, exist_ok=True)
        logger.debug("Opening file for writing: bucket=%s file=%s", bucket, file)
        with open(filepath, "wb") as f:
            yield f

    def delete_file(self, bucket: str, file: str) -> None:
        logger.debug("Deleting file: bucket=%s file=%s", bucket, file)
        filepath = Path(self.path) / bucket / file
        if not filepath.exists():
            raise NoSuchFileError(f"File {file} does not exist")
        filepath.unlink()

    def stat(self, bucket: str, file: str) -> FileData:
        logger.debug("Statting file: bucket=%s file=%s", bucket, file)
        filepath = Path(self.path) / bucket / file
        if not filepath.exists():
            raise NoSuchFileError(f"File {file} does not exist")

        statdata = filepath.stat()
        return FileData(
            name=file,
            size=statdata.st_size,
            modified=datetime.fromtimestamp(statdata.st_mtime),
        )
