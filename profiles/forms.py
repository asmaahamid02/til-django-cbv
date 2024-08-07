from typing import Any, Mapping
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import PasswordChangeForm

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'email']

    image = forms.ImageField(label='Profile Picture', required=False)

    def __init__(self, *args:Any, **kwargs:Any) -> None:
        super(ProfileUpdateForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full p-4 text-sm bg-gray-50 focus:outline-none border border-gray-200 rounded text-gray-600',
                'placeholder': field.label

            })  

    def save(self, commit: bool = True) -> Any:
        user = super(ProfileUpdateForm, self).save(commit=False)

        if 'image' in self.files:
            user.profile.image = self.files['image']

        if commit:
            user.save()
            user.profile.save()
        return user
    
class CustomPasswordChangeForm(PasswordChangeForm):
    def __init__(self, *args: Any, **kwargs: Any) -> None:
        super(CustomPasswordChangeForm, self).__init__(*args, **kwargs)
        for fieldname, field in self.fields.items():
            field.widget.attrs.update({
                'class': 'w-full p-4 text-sm bg-gray-50 focus:outline-none border border-gray-200 rounded text-gray-600',
                'placeholder': field.label
            })

