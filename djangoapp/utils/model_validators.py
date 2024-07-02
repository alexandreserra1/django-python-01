from django.core.exceptions import ValidationError

def validate_png(image):
    if not image.name.endswith('.png'):
        raise ValidationError('Only PNG files are allowed.')
    