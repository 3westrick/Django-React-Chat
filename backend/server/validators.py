from PIL import Image
from django.core.exceptions import ValidationError

valid_extensions = ['jpg', 'jpeg', 'svg', 'gif', 'png']


def validate_icon_image_size(image):
    if image:
        with Image.open(image) as img:
            if img.width > 70 or img.height > 70:
                raise ValidationError(
                    f"The maximum allowed dimensions for for icon is 70x70 - size of image you uploaded\
                    {img.width}x{img.height}"
                )


def validate_banner_image_size(image):
    if image:
        with Image.open(image) as img:
            ratio = img.width / img.height
            if ratio > 16 / 12:
                raise ValidationError(
                    f"The preferred dimensions for banner is 1600/900 - make your image wider"
                )
            if ratio < 16 / 6:
                raise ValidationError(
                    f"The preferred dimensions for banner is 1600/900 - make your image less wider"
                )


def validate_image_file_extension(value):
    ext = value.path.split('.')[-1]
    if ext not in valid_extensions:
        raise ValidationError(
            f"Unsupported file extension. Valid extensions : {valid_extensions}"
        )
