from abc import ABC, abstractmethod
from dataclasses import dataclass
from datetime import datetime
from typing import BinaryIO, Generator


class StorageError(Exception):
    """
    StorageError is the base class for all storage errors.
    """


class NoSuchBucketError(StorageError):
    """
    NoSuchBucketError is raised when a bucket does not exist.
    """


class NoSuchFileError(StorageError):
    """
    NoSuchFileError is raised when a file does not exist.
    """


class BucketAlreadyExistsError(StorageError):
    """
    BucketAlreadyExistsError is raised when a bucket already exists.
    """


@dataclass
class FileData:
    """
    FileData is the data of a file.
    """

    name: str
    size: int
    modified: datetime


class Storage(ABC):
    """
    Storage is the interface for the storage backend.
    """

    @abstractmethod
    def create_bucket(self, name: str) -> None:
        """
        Create a new bucket.
        """
        pass

    @abstractmethod
    def delete_bucket(self, name: str) -> None:
        """
        Delete a bucket.
        """
        pass

    @abstractmethod
    def list_buckets(self, start: int = 0, limit: int = 100) -> list[str]:
        """
        Get a bucket.
        """
        pass

    @abstractmethod
    def list_files(
        self, bucket: str, start: int = 0, limit: int = 100
    ) -> list[FileData]:
        """
        List all files in a bucket.
        """
        pass

    @abstractmethod
    def open_read(self, bucket: str, file: str) -> Generator[BinaryIO, None, None]:
        """
        Open a file for reading.
        """
        pass

    @abstractmethod
    def open_write(self, bucket: str, file: str) -> Generator[BinaryIO, None, None]:
        """
        Open a file for writing, maybe creating. If not create a new version.
        """
        pass

    @abstractmethod
    def delete_file(self, bucket: str, file: str) -> None:
        """
        Delete a file.
        """
        pass

    @abstractmethod
    def stat(self, bucket: str, file: str) -> FileData:
        """
        Get the data of a file.
        """
        pass
