from django.forms import ModelForm, TextInput, Select, FileInput, Textarea, NumberInput

from .models import Listing

class ListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ["title", "category", "image", "description", "price"]
        widgets = {
            'title': TextInput(attrs={
                'class': "form-control m-2",
                'placeholder': "Enter Title",
            }),
            'category': Select(attrs={
                'class': "form-control",
            }),
            'image': FileInput(attrs={
            }),
            'description': Textarea(attrs={
                'class': "form-control m-2",
                'placeholder': "Enter Description",
                'rows': "2",
            }),
            'price': NumberInput(attrs={
                'class': "form-control",
                'placeholder': "Enter Price",
                'step': "0.01",
            })
        }
