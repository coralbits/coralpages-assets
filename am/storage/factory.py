from am.storage.types import Storage
from am.storage.disk import DiskStorage
from am.config import config, StorageConfig
import logging

logger = logging.getLogger(__name__)


def create_storage(config: StorageConfig) -> Storage:
    """
    Create a storage backend from the config.
    """
    logger.debug(f"Creating storage backend: {config and config.name}")
    if config.type == "disk":
        return DiskStorage(config)
    raise ValueError(f"Unknown storage type: {config.type}")


def get_storage(name: str) -> Storage:
    """
    Get a storage backend from the config.

    TODO: there needs to be a map in db for bucket to storage backend.
    """
    logger.debug(f"Getting storage backend for bucket={name}")
    storage_config = config.storage.get("default")
    if storage_config is None:
        raise ValueError(f"Storage backend for bucket={name} not found")
    return create_storage(storage_config)
