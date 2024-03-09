from django.core.exceptions import ValidationError

def validate_image_dimensions(image):
    width = image.width
    height = image.height

    # Check if image dimensions are at least 320x320 pixels
    if width < 320 or height < 320:
        raise ValidationError('Image dimensions should be at least 320x320 pixels.')

def validate_image_size(image):
    # Check if image size is less than 5MB
    if image.size > 5 * 1024 * 1024:
        raise ValidationError('Image size should be less than 5MB.')

def validate_trip_image_size(image):
    # Check if image size is less than 5MB
    if image.size > 5 * 1024 * 1024:
        raise ValidationError('Image size should be less than 5MB.')
