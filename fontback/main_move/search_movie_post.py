from django import forms
class SearchForm(forms.Form):
    search = forms.CharField(label='search_sth', max_length=100)