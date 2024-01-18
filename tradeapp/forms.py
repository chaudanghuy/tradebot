from django import forms

class CryptoSearchForm(forms.Form):
  search_query = forms.CharField(label='Search', max_length=100)