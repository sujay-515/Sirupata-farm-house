# core/forms.py
from django import forms
from .models import ContactSubmission, Review

class ReviewForm(forms.ModelForm):
    class Meta:
        model = Review
        fields = ['user_name', 'user_email', 'rating', 'review_title', 'review_text']
        widgets = {
            'user_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your name',
                'required': True
            }),
            'user_email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your email (optional)'
            }),
            'rating': forms.Select(attrs={
                'class': 'form-control',
                'required': True
            }, choices=[(i, '⭐' * i) for i in range(1, 6)]),
            'review_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Summarize your experience'
            }),
            'review_text': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Write your review here...',
                'rows': 4,
                'required': True
            }),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactSubmission
        fields = ["name", "email", "subject", "message"]
        widgets = {
            "name": forms.TextInput(attrs={
                "placeholder": "Your Name",
                "required": True,
            }),
            "email": forms.EmailInput(attrs={
                "placeholder": "Your Email",
                "required": True,
            }),
            "subject": forms.TextInput(attrs={
                "placeholder": "Subject",
                "required": True,
            }),
            "message": forms.Textarea(attrs={
                "placeholder": "Write Message",
                "required": True,
                "rows": 5,
            }),
        }
