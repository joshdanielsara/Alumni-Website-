# fields.py
from django.forms import FileField
from .widgets import MultipleFileInput

class MultipleFileField(FileField):
    widget = MultipleFileInput

    def to_python(self, data):
        if not data:
            return []
        if not isinstance(data, list):
            data = [data]
        return data
