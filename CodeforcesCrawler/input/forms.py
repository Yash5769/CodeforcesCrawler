from django import forms

class Handle(forms.Form):
    Handle = forms.CharField(max_length=200, label='Handle',widget=forms.TextInput(attrs = {'class':'col-sm-2 col-form-label'}))
    # Username = forms.CharField(max_length = 200,label = 'Username')