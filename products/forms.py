from django import forms
from django.contrib.auth.models import User
from .models import ProductReview

class ProductReviewForm(forms.ModelForm):

    author = forms.CharField()

    class Meta:
        model = ProductReview
        fields = ('title', 'review_text')