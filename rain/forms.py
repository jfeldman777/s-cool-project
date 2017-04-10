from django import forms

class BookSearch(forms.Form):
    in_title = forms.CharField(label='seek in title',
        max_length=100,
        required=False)
    kw_after = forms.CharField(label='seek in after-kw',
            max_length=100,
            required=False)
    pass
