from django.db import models
from django import forms
from .models import Comment

class CommentForm(forms.ModelForm):

    text = forms.CharField(label="Comment")

    class Meta:
        model = Comment
        fields = ['text']