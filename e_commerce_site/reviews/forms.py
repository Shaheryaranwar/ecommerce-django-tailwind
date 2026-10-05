from django import forms

from .models import Review


class ReviewForm(forms.ModelForm):
    RATING_CHOICES = [(i, str(i)) for i in range(5, 0, -1)]

    rating = forms.ChoiceField(
        choices=RATING_CHOICES, widget=forms.RadioSelect(), label="Your rating"
    )

    class Meta:
        model = Review
        fields = ("rating", "title", "comment")
        widgets = {
            "title": forms.TextInput(attrs={"placeholder": "Summarise your experience (optional)"}),
            "comment": forms.Textarea(
                attrs={"rows": 4, "placeholder": "How is the quality, finish and comfort?"}
            ),
        }
