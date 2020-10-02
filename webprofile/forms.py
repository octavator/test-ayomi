from django.forms import ModelForm, Form
from webprofile.models import User

class LoginForm(Form):
    email = ''
    password = ''
    def clean(self):
        cleaned_data = super(LoginForm, self).clean()
        return cleaned_data
    class Meta:
        fields = ['email', 'password']

class EditForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'favorite_food']

class RegistrationForm(ModelForm):
    class Meta:
        model = User
        fields = ['email', 'password', 'favorite_food']

