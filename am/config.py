import yaml


def load_config(path: str) -> dict:
    """
    Load the config from the given path.
    """
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)


config = load_config("config.yaml")
