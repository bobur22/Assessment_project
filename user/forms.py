from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()
class LoginForm(forms.Form):
    email = forms.EmailField(required=True, widget=forms.EmailInput(attrs={
        'id': 'input_email',
        'name': "email",
        'placeholder': 'youremail@gmail.com',
        "class": "form-control py-3 ps-4 font_f_n color_g z"
    }))

    password = forms.CharField(required=True, widget=forms.PasswordInput(attrs={
        'id': "password",
        'name': "password",
        'placeholder': 'Password',
        "class": "form-control py-3 ps-4 pe-5 font_f_n color_g",
    }))

    def __init__(self, *args, **kwargs):
        super(LoginForm, self).__init__(*args, **kwargs)
        self.fields['password'].label = ""
