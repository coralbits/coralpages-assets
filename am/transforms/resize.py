import logging
from PIL import Image

from .types import Input, Output, Transform

logger = logging.getLogger(__name__)


class ResizeTransform(Transform):
    """
    ResizeTransform is a transform that resizes an image.
    """

    def __init__(self, name: str, config: dict):
        super().__init__(name, config)
        self.width = int(config["width"])
        self.height = int(config["height"])
        self.fit = config.get("fit", "cover")
        self.quality = int(config.get("quality", 80))
        self.format = config.get("format", "webp")

    def config_schema(self):
        return {
            "width": {
                "type": "integer",
                "required": True,
                "description": "Width of the image",
            },
            "height": {
                "type": "integer",
                "required": True,
                "description": "Height of the image",
            },
            "fit": {
                "type": "select",
                "options": ["fill", "cover", "contain"],
                "required": False,
                "description": "Crop the image to the given width and height",
                "default": "cover",
            },
            "quality": {
                "type": "integer",
                "required": False,
                "description": "Quality of the image, 0-100",
                "default": 80,
            },
            "format": {
                "type": "select",
                "options": ["webp", "png", "jpg", "jpeg"],
                "required": False,
                "default": "webp",
                "description": "Format of the image",
            },
        }

    def for_mime_types(self):
        return ["image/*"]

    def apply(self, input: Input, output: Output):
        image = Image.open(input)
        match self.fit:
            case "cover":
                image = self.cover(image)
            case "contain":
                image = self.contain(image)
            case "fill":
                image = image.resize((self.width, self.height))
            case _:
                logger.warning("Unknown fit=%s. Using cover", self.fit)
                image = self.cover(image)

        image.save(output, quality=self.quality, format=self.format)

    def cover(self, image: Image.Image) -> Image.Image:
        """
        Keeps the aspect ratio, cutting from the sides or from top and down if longer
        than the width or height.
        """
        logger.info(
            "Transforming image cover %sx%s to %sx%s",
            image.width,
            image.height,
            self.width,
            self.height,
        )
        new_aspect_ratio = self.width / self.height
        current_aspect_ratio = image.width / image.height

        is_wider = current_aspect_ratio > new_aspect_ratio
        if is_wider:
            projected_width = image.height * new_aspect_ratio
            top = 0
            left = (image.width - projected_width) / 2
            crop_width = image.width - left - left
            crop_height = image.height
        else:
            projected_height = image.width / new_aspect_ratio
            top = (
                image.height - projected_height
            ) / 3  # slightly up, as normally its more interesting
            removed_height = image.height - projected_height
            left = 0
            crop_width = image.width
            crop_height = image.height - removed_height

        image = image.crop((left, top, left + crop_width, top + crop_height))
        image = image.resize((self.width, self.height))
        return image

    def contain(self, image: Image.Image) -> Image.Image:
        """
        Keeps the older aspect ratio, making the new image width and height at most
        the given width and height.

        If the image is wider ratio wise, it will be shorter than requested
        and if it is taller ratio wise, it will be wider than requested.
        """
        logger.info(
            "Transforming image contain %sx%s to %sx%s",
            image.width,
            image.height,
            self.width,
            self.height,
        )

        new_aspect_ratio = self.width / self.height
        current_aspect_ratio = image.width / image.height
        new_width = self.width
        new_height = self.height

        is_wider = current_aspect_ratio > new_aspect_ratio
        if is_wider:
            # logger.info("Image is wider, scaling height")
            new_height = self.width / current_aspect_ratio
        else:
            # logger.info("Image is taller, scaling width")
            new_width = self.height * current_aspect_ratio

        # logger.info("New width: %s, new height: %s", new_width, new_height)

        image = image.resize(
            (int(new_width), int(new_height)),
            resample=Image.Resampling.LANCZOS,
        )
        return image

    # def crop_resize(
    #     self, image: Image.Image, crop: list[int], resize: list[int]
    # ) -> Image.Image:
    #     """
    #     Crops the image and then resizes it to the given width and height.
    #     """
    #     image = image.crop(crop)
    #     image = image.resize(resize, resample=Image.Resampling.LANCZOS)
    #     return image
