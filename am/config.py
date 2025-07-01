from dataclasses import dataclass, field
import yaml


@dataclass
class StorageConfig:
    name: str
    type: str
    config: dict

    @classmethod
    def from_dict(cls, config: dict):
        return cls(
            name=config["name"],
            type=config["type"],
            config=config,
        )


@dataclass
class ServerConfig:
    host: str = "0.0.0.0"
    port: int = 8005
    reload: bool = False
    allow_origins: list[str] = field(default_factory=lambda: ["*"])

    def update_from_dict(self, config: dict):
        if "host" in config:
            self.host = config["host"]
        if "port" in config:
            self.port = config["port"]
        if "reload" in config:
            self.reload = config["reload"]
        if "allow_origins" in config:
            self.allow_origins = config["allow_origins"]


@dataclass
class Config:
    server: ServerConfig = field(default_factory=ServerConfig)
    storage: dict[str, StorageConfig] = field(default_factory=dict)

    def update_from_dict(self, update: dict):
        if "server" in update:
            self.server.update_from_dict(update["server"])
        if "storage" in update:
            for config in update["storage"]:
                self.storage[config["name"]] = StorageConfig.from_dict(config)


config = Config()


def load_config(path: str) -> dict:
    """
    Load the config from the given path.
    """
    with open(path, "r", encoding="utf-8") as f:
        update = yaml.safe_load(f)
    config.update_from_dict(update)
