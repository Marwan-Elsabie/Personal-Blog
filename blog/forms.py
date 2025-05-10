from django import forms
from .models import Post, Comment , Profile

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'image']

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['text']

class ProfileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['bio', 'location', 'birth_date', 'profile_pic', 'website']
        widgets = {
            'birth_date': forms.DateInput(attrs={'type': 'date'}),
            'bio': forms.Textarea(attrs={'rows': 4}),
        }
