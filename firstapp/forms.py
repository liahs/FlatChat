from django import forms
from firstapp.models import add_property

class add_property_form(forms.ModelForm):
    class Meta:
        model = add_property
        exclude = ["seller"]
        # fields = "__all__"