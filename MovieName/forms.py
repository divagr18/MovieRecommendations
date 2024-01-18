# MovieDjango/MovieName/forms.py

from django import forms

class UserInputForm(forms.Form):
    user_id = forms.IntegerField()
