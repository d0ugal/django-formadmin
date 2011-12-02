from django import forms


class EmailForm(forms.Form):

    email = forms.EmailField()


class UploadForm(forms.Form):

    file = forms.FileField()
