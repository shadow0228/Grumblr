from django import forms
from grumblr.models import *
from django.contrib.auth.models import User

class RegistrationForm(forms.Form):
    username = forms.CharField(max_length = 20,
        widget=forms.TextInput(attrs={"class":"form-control","placeholder":"User Name"}))
    firstname = forms.CharField(max_length = 20,
        widget=forms.TextInput(attrs={"class":"form-control","placeholder":"First Name","style":"width:50%;float:left"}))
    lastname = forms.CharField(max_length = 20,
        widget=forms.TextInput(attrs={"class":"form-control","placeholder":"Last Name","style":"width:50%;float:left"}))
    email = forms.CharField(max_length = 200,
        widget=forms.EmailInput(attrs={"class":"form-control","placeholder":"Email"}))
    password1 = forms.CharField(max_length = 200, 
        label='Password', 
        widget = forms.PasswordInput(attrs={"class":"form-control","placeholder":"Password"}))
    password2 = forms.CharField(max_length = 200, 
        label='Confirm password',  
        widget = forms.PasswordInput(attrs={"class":"form-control","placeholder":"Confirm Password"}))

    # Customizes form validation for properties that apply to more
    # than one field.  Overrides the forms.Form.clean function.
    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(RegistrationForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data


    # Customizes form validation for the username field.
    def clean_username(self):
        # Confirms that the username is not already present in the
        # User model database.
        username = self.cleaned_data['username']
        if User.objects.filter(username = username).exists():
            raise forms.ValidationError("Username is already taken.")

        # Generally return the cleaned data we got from the cleaned_data
        # dictionary
        return username

class ImageUploadForm(forms.Form):
    image = forms.FileField()

class ChangePasswordForm(forms.Form):

    password1 = forms.CharField(max_length = 200, 
        label='Password', 
        widget = forms.PasswordInput(attrs={"class":"form-control","placeholder":"Password"}))
    password2 = forms.CharField(max_length = 200, 
        label='Confirm password',  
        widget = forms.PasswordInput(attrs={"class":"form-control","placeholder":"Confirm Password"}))

    def clean(self):
        # Calls our parent (forms.Form) .clean function, gets a dictionary
        # of cleaned data as a result
        cleaned_data = super(ChangePasswordForm, self).clean()

        # Confirms that the two password fields match
        password1 = cleaned_data.get('password1')
        password2 = cleaned_data.get('password2')
        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords did not match.")

        # Generally return the cleaned data we got from our parent.
        return cleaned_data



    """docstring for EntryForm"""
    

