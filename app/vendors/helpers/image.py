from PIL import Image
from typing import Tuple
from django.conf import settings
from app.vendors.exceptions import ResizeImageError


def get_new_image_dimensions(original_dimensions: Tuple[int, int], new_width: int) -> Tuple[int, int]:
    """
    Get new image dimensions.
    -------------------------
    Parameters:
        original_dimensions (tuple[int, int]): original dimensions of image
        new_width (int): new width for image
    Returns:
        new_width, new_height (tuple[int, int]): new size for image
    """
    original_width, original_height = original_dimensions

    if original_width < new_width:
        return original_dimensions

    aspect_ratio = original_height / original_width
    new_height = round(new_width * aspect_ratio)

    return new_width, new_height


def resize_image(img_path: str, width: int, raise_exc: bool = False) -> Image.Image | None:
    """
    Resize image by path to width.
    -------------------------------
    Parameters:
        img_path (str): image path
        width (int): new image width
    Returns:
        (Image.Image | None): new image or None if old width == new width
    Raise:
        ResizeImageError: if there is any error in image resize, or image extension not in settings.RESIZABLE_IMAGES
    """
    if img_path.split('.')[-1] not in settings.RESIZABLE_IMAGES:
        if raise_exc is True:
            raise ResizeImageError("Not resizable image")
        else:
            return None
    
    if img_path:
        with Image.open(img_path) as image:
            new_size = get_new_image_dimensions(image.size, width)
            if new_size == image.size:
                return None
            try:
                return image.resize(new_size, Image.Resampling.LANCZOS)
            except Exception as exc:
                if raise_exc is True:
                    raise ResizeImageError() from exc
                else:
                    return None