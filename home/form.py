from django import forms

class SearchForm(forms.Form):
    query = forms.CharField(max_length=500)
    catid = forms.IntegerField()