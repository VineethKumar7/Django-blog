from django import forms
from .models import Post
from pagedown.widgets import PagedownWidget
class PostForm(forms.ModelForm):
    # The PagedownWidget ischanged to PagedownWidget(show_preview = False)
    # Then we no longer view the image at edit view.  
    content = forms.CharField(widget=PagedownWidget(show_preview = False))
    publish = forms.DateField(widget = forms.SelectDateWidget)
    class Meta:
        model = Post
        fields = [
            "title",
            "image",
            "content",
            "draft",
            "publish",
        ]
