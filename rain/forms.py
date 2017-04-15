from django import forms

class BookSearch(forms.Form):
    in_title = forms.CharField(label='искать в названии',
        max_length=100,
        required=False)
    kw_after = forms.CharField(label='искать ключевые слова',
            max_length=100,
            required=False)
    pass
