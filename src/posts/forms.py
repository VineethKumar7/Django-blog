from django import forms

from .models import Post

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        # is the list of fields that we have to include inside the post.
        fields = [
            "title",
            "image",
            "content",
        ]
