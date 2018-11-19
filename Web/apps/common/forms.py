from django import forms
from Web.apps.common.models import Genre

class GenreForm(forms.ModelForm):

    def clean_level(self):
        level = self.cleaned_data['level']
        if level > 2:
            raise forms.ValidationError("分级过多，最高分级层数为3层")
        return level

    class Meta:
        model = Genre
        fields = (
            'title',
            'parent',
            'level'
        )
