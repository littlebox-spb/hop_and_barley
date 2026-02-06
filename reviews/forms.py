from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.RadioSelect(
            choices=[(i, "★" * i) for i in range(1, 6)]
        )
    )

    class Meta:
        model = Review
        fields = ["rating", "text"]
        widgets = {
            "text": forms.Textarea(attrs={
                "rows": 4,
                "placeholder": "Write your review here..."
            })
        }
