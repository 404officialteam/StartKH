from django import forms
from .models import Project, ProjectScreenshot

class MultipleFileInput(forms.FileInput):
    allow_multiple_selected = True

class MultipleFileField(forms.FileField):
    def __init__(self, *args, **kwargs):
        kwargs.setdefault("widget", MultipleFileInput(attrs={'class': 'form-control'}))
        super().__init__(*args, **kwargs)

    def clean(self, data, initial=None):
        single_file_clean = super().clean
        if isinstance(data, (list, tuple)):
            result = [single_file_clean(d, initial) for d in data]
        else:
            result = single_file_clean(data, initial)
        return result

class ProjectForm(forms.ModelForm):
    # Field to support multiple screenshots in the same form upload
    screenshots = MultipleFileField(
        required=False,
        help_text="Upload one or more screenshots of your project"
    )

    class Meta:
        model = Project
        fields = ['title', 'category', 'logo', 'cover_image', 'tagline', 'description', 'website', 'github', 'video_demo']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'e.g. StartKH'}),
            'category': forms.Select(attrs={'class': 'form-select'}),
            'logo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'cover_image': forms.ClearableFileInput(attrs={'class': 'form-control'}),
            'tagline': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Khmer-first startup & project discovery platform'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 6, 'placeholder': 'Explain what your project does, who it is for, and what technology you used.'}),
            'website': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://startkh.com'}),
            'github': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'https://github.com/founder/startkh'}),
            'video_demo': forms.URLInput(attrs={'class': 'form-control', 'placeholder': 'e.g. YouTube video link'}),
        }
