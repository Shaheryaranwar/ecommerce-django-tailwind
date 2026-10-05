import os

from django import forms

from .models import Project

ALLOWED_IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".webp"}
ALLOWED_DOC_EXTENSIONS = {".pdf", ".doc", ".docx"}
MAX_IMAGE_SIZE = 5 * 1024 * 1024  # 5MB
MAX_DOC_SIZE = 10 * 1024 * 1024  # 10MB


class MultipleFileInput(forms.ClearableFileInput):
    allow_multiple_selected = True


class MultipleFileField(forms.FileField):
    widget = MultipleFileInput

    def to_python(self, data):
        if data in self.empty_values:
            return []
        if not isinstance(data, (list, tuple)):
            data = [data]
        return [forms.FileField.to_python(self, item) for item in data]


def _validate_file(file, allowed_extensions, max_size, label):
    if file.size > max_size:
        raise forms.ValidationError(
            f"{label} “{file.name}” is too large (max {max_size // (1024 * 1024)}MB)."
        )
    ext = os.path.splitext(file.name)[1].lower()
    if ext not in allowed_extensions:
        allowed = ", ".join(sorted(allowed_extensions))
        raise forms.ValidationError(
            f"{label} “{file.name}” has an unsupported format. Allowed: {allowed}."
        )
    return file


class ProjectForm(forms.ModelForm):
    images = MultipleFileField(
        required=False,
        help_text="Up to 5 photos (JPG, PNG or WebP, max 5MB each).",
    )
    document = forms.FileField(
        required=False,
        help_text="Optional proof document (PDF or Word, max 10MB).",
    )

    class Meta:
        model = Project
        fields = ("title", "category", "description")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "e.g. Hand-carved walnut console"}),
            "category": forms.Select(),
            "description": forms.Textarea(
                attrs={
                    "rows": 6,
                    "placeholder": "What did you learn or build? Tell the story — materials, process, what it taught you.",
                }
            ),
        }

    def clean_images(self):
        files = self.cleaned_data.get("images") or []
        if len(files) > 5:
            raise forms.ValidationError("You can upload up to 5 photos per project.")
        return [
            _validate_file(f, ALLOWED_IMAGE_EXTENSIONS, MAX_IMAGE_SIZE, "Photo")
            for f in files
        ]

    def clean_document(self):
        file = self.cleaned_data.get("document")
        if file:
            _validate_file(file, ALLOWED_DOC_EXTENSIONS, MAX_DOC_SIZE, "Document")
        return file
