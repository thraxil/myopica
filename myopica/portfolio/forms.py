from .models import Image
from django.forms import ModelForm


class AddImageForm(ModelForm):
    class Meta:
        model = Image
        exclude = ('ahash', 'extension')
