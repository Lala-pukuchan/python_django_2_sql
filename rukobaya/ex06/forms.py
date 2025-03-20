from django import forms

class UpdateForm(forms.Form):
    film_title = forms.ChoiceField(label="Select a film to update")
    opening_crawl = forms.CharField(
        label="Opening Crawl",
        required=False,
        widget=forms.TextInput(attrs={'placeholder': 'Enter new opening crawl'})
    )
