from django import forms
from .models import Ads, Reply
from django.core.exceptions import ValidationError


class AdsForm(forms.ModelForm):
    description = forms.CharField(min_length=20)

    class Meta:
        model = Ads
        fields = ['category', 'title', 'text', 'image', 'video']

    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) < 20:
            raise forms.ValidationError("Описание должно содержать не менее 20 символов.")
        return description

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['category'].empty_label = "Выберите категорию"
        self.fields['title'].label = 'Заголовок'
        self.fields['text'].label = 'Текст объявления'
        self.fields['image'].label = 'Фото'
        self.fields['video'].label = 'Видео'



class ReplyForm(forms.ModelForm):
    class Meta:
        model = Reply
        fields = ['content']


class SendForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(SendForm, self).__init__(*args, **kwargs)

    content = forms.CharField(required=True, max_length=400, label='Текст')
    