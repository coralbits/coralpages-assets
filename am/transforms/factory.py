from am.transforms.types import Transform
from am.transforms.resize import ResizeTransform


class Factory:
    def __init__(self):
        self.transforms = {}

    def register_transform(self, name: str, transform: Transform):
        self.transforms[name] = transform

    def create_transform(self, name: str, config: dict) -> Transform:
        return self.transforms[name](name, config)


factory = Factory()
factory.register_transform("resize", ResizeTransform)
