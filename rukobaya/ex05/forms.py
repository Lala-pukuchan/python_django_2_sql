from django import forms

class RemoveForm(forms.Form):
    film_title = forms.ChoiceField(label="Film to remove")
