# validators.py
from django.core.exceptions import ValidationError

def validate_file_size(value):
    limit = 2 * 1024 * 1024  # 2 MB limit (in bytes)
    if value.size > limit:
        raise ValidationError('File size should not exceed 2 MB')
