"""Forms for reviews."""

from typing import TYPE_CHECKING

from django import forms

from .models import Review

if TYPE_CHECKING:
    ReviewModel = forms.ModelForm[Review]
else:
    ReviewModel = forms.ModelForm


class ReviewForm(ReviewModel):
    """Review form."""

    rating = forms.IntegerField(
        min_value=1,
        max_value=5,
        widget=forms.RadioSelect(choices=[(i, "★" * i) for i in range(1, 6)]),
    )

    class Meta:
        """Meta class for the form."""

        model = Review
        fields = ["rating", "text"]
        widgets = {
            "text": forms.Textarea(
                attrs={"rows": 4, "placeholder": "Write your review here..."}
            )
        }
