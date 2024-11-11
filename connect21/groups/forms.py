from django import forms

from .models import ChatGroup


class CreateGroupForm(forms.ModelForm):
    class Meta:
        model = ChatGroup
        fields = ['name', 'interest', 'description']

    def clean_name(self):
        name = self.cleaned_data['name']
        if len(name) < 5:
            raise forms.ValidationError('Имя группы не может быть короче 5 символов.')
        return name
