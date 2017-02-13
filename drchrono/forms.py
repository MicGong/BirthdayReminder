from django import forms

# class SearchForm(forms.Form):
#     """Django form of search"""
#     first_name = forms.CharField(max_length=255, required=False)
#     last_name = forms.CharField(max_length=255, required=False)
#     gender = forms.ChoiceField(choices=(('M','Male'),('F','Female')), required=False)
#     date_of_birth = forms.DateField(input_formats='%m/%d/%Y', required=False)

#     def clean(self):
#         cleaned_data = super(SearchForm, self).clean()
#         return cleaned_data

class EmailForm(forms.Form):
    """Email Django form"""
    title = forms.CharField(max_length=300, required=False)
    body = forms.CharField(required=False)

    def clean(self):
        cleaned_data = super(EmailForm, self).clean()
        return cleaned_data