#!/usr/bin/env -S uv run --script

import logging
import sys
from pathlib import Path
from unittest import TestCase
import unittest


logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.DEBUG)


sys.path.append(str(Path(__file__).parent.parent))

from am.storage.types import NoSuchBucketError
from am.storage.factory import create_storage


class TestDiskStorage(TestCase):
    """
    TestDiskStorage is a test case for the DiskStorage class.
    """

    def test_disk_storage(self):
        """
        Test the DiskStorage class.
        """
        storage = create_storage({"type": "disk", "path": "./data"})
        storage.create_bucket("test")
        with storage.open_write("test", "test.txt") as f:
            f.write(b"test")

        with storage.open_read("test", "test.txt") as f:
            assert f.read() == b"test"

        assert storage.stat("test", "test.txt").size == 4
        assert storage.stat("test", "test.txt").modified is not None

        files = storage.list_files("test")
        logger.debug("Files: %s", files)
        assert len(files) == 1
        assert files[0].name == "test.txt"
        assert files[0].size == 4
        assert files[0].modified is not None

        assert storage.list_buckets() == ["test"]

        storage.delete_bucket("test")
        assert storage.list_buckets() == []
        with self.assertRaises(NoSuchBucketError):
            storage.list_files("test")

        storage.create_bucket("test")
        assert storage.list_buckets() == ["test"]


if __name__ == "__main__":
    unittest.main()
