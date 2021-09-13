from django import forms
from django.contrib.auth import authenticate
from django.contrib.auth.forms import UserCreationForm, UsernameField
from .models import User


class UserRegistrationForm(UserCreationForm):

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['username'].widget.attrs.update({'placeholder': 'Enter Username'})
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter Email'})
      #  self.fields['contact_number'].widget.attrs.update({'placeholder': 'Enter contact number'})
      #  self.fields['first_name'].widget.attrs.update({'placeholder': 'Enter your name'})
      #  self.fields['dob'].widget.attrs.update({'placeholder': 'Enter date of birth'})
        self.fields['password1'].widget.attrs.update({'placeholder': 'Enter password'})
        self.fields['password2'].widget.attrs.update({'placeholder': 'Repeat your password'})

    class Meta:
        model = User
        fields = ("username",
                  "email",
                  "gender",
                  "contact_number",
                  "first_name",
                  "dob",
                  "password1",
                  "password2")


    def clean_username(self):
        username = self.cleaned_data['username']
        print(username)
        if ' ' in username:
            raise forms.ValidationError("Username can't contain spaces")
        return username

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.username = self.cleaned_data['username']
        user.email = self.cleaned_data['email']
        user.contact_number = self.cleaned_data['contact_number']
        if commit:
            user.save()
        return user


class UserLoginForm(forms.Form):
    email = forms.EmailField(label="Email")
    password = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput,
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user = None
        self.fields['email'].widget.attrs.update({'placeholder': 'Enter Email'})
        self.fields['password'].widget.attrs.update({'placeholder': 'Enter Password'})

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get("email")
        password = self.cleaned_data.get("password")

        if email and password:
            self.user = authenticate(email=email, password=password)

            if self.user is None:
                raise forms.ValidationError("User Does Not Exist")
            if not self.user.check_password(password):
                raise forms.ValidationError("Incorrect Password")
            if not self.user.is_active:
                raise forms.ValidationError("User is not Active")

        # return self.cleaned_data
        return super(UserLoginForm, self).clean(*args, **kwargs)

    def get_user(self):
        return self.user
