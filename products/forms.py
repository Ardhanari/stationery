from django import forms
from django.contrib.auth.models import User
from .models import ProductReview

class ProductReviewForm(forms.ModelForm):

    class Meta:
        model = ProductReview
        fields = ('title', 'review_text')