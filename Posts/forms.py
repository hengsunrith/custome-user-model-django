from django import forms

from .models import Post


class PostForm(forms.ModelForm):

  title = forms.CharField(label='Title:', widget=forms.TextInput(attrs={'class': 'form-control'}))
  text = forms.CharField(widget=forms.Textarea(attrs={'class': 'form-control'}))


  class Meta:
    model = Post
    fields = ('title', 'text', 'image')