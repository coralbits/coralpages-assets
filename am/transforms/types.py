from typing import Generator
from typing import BinaryIO

type Input = Generator[BinaryIO, None, None]
type Output = Generator[BinaryIO, None, None]


class Transform:
    """
    Transform is the base class for all transforms.
    """

    def __init__(self, name: str, config: dict):
        self.name = name
        self.config = config

    def for_mime_types(self):
        """
        Return the mime types that this transform can apply to.

        May use "text/*" to match all text mime types.
        """
        return []

    def apply(self, input: Input) -> Output:
        """
        Apply the transform to the file.
        """
        raise NotImplementedError("Subclasses must implement this method")
