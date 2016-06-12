"""
forms
"""

from django import forms

class ExerciseForm(forms.Form):
    name = forms.CharField(label='name', max_length=100)
    bodyweight = forms.BooleanField(label='bodyweight', required=False)

class ContactForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField(widget=forms.Textarea)
    sender = forms.EmailField()
    cc_myself = forms.BooleanField(required=False)
