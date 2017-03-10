from django import forms
from .models import Article, BlogComment


class BlogCommentForm(forms.ModelForm):
    class Meta:
        model = BlogComment
        fields = ['user_name', 'body']
        widgets = {
            'user_name': forms.TextInput(attrs={
                'class': 'validate',
                'placeholder': '请输入昵称',
                'aria-describedby': 'sizing-addon1'
            }),
            'body': forms.Textarea(attrs={
                'placeholder': '让我来说两句',
                'class': 'validate materialize-textarea',
                'rows': 2
            }),
        }


