from django import forms

from .models import Comment, Post, Tag


class PostForm(forms.ModelForm):
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        required=False,
        widget=forms.SelectMultiple(attrs={"class": "form-control"}),
        help_text="Hold down the Ctrl (Windows) or Command (Mac) button to select multiple options.",
    )

    class Meta:
        model = Post
        fields = "__all__"
        exclude = ["created_at", "updated_at", "user"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 6}),
            "image": forms.FileInput(
                attrs={"class": "form-control post_image", "accept": "image/*"}
            ),
        }
        help_texts = {}


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ["comment"]
        widgets = {
            "comment": forms.Textarea(attrs={"class": "form-control", "rows": "3"})
        }
