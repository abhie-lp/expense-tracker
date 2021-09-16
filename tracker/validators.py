"""Validators for tracker app"""

from django.core.exceptions import ValidationError
from django.db.models.fields.files import FieldFile

ATTACHMENT_EXTENSIONS = ("csv", "jpeg", "jpg", "pdf", "png", "xls", "xlsx")
MAX_ATTACHMENT_SIZE = 5242880   # 5 * 1024 * 1024
MAX_ATTACHMENT_VERBOSE = "5 MB"


def validate_attachment(file: FieldFile):
    """Validate attachment for size and extension"""
    file_extension: str = file.name.rsplit(".", 1)[1].lower()
    if file_extension not in ATTACHMENT_EXTENSIONS:
        raise ValidationError(f"Allowed extensions are {', '.join(ATTACHMENT_EXTENSIONS)}.")
    if file.size > MAX_ATTACHMENT_SIZE:
        raise ValidationError(f"Max size for a file is {MAX_ATTACHMENT_VERBOSE}.")
