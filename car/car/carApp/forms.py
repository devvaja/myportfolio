from django import forms

class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=80, widget=forms.TextInput(attrs={
        'placeholder': 'Full Name here',
        'class': 'wpcf7-form-control wpcf7-text wpcf7-validates-as-required',
    }))
    email = forms.EmailField(max_length=80, widget=forms.EmailInput(attrs={
        'placeholder': 'Email Address',
        'class': 'wpcf7-form-control wpcf7-email wpcf7-validates-as-required wpcf7-text wpcf7-validates-as-email',
    }))
    message = forms.CharField(max_length=400, widget=forms.Textarea(attrs={
        'placeholder': 'Write Message.',
        'class': 'wpcf7-form-control wpcf7-textarea',
        'rows': 10,
        'cols': 40,
    }))
