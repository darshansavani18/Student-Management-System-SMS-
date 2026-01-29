from django import forms
from .models import Student, Teacher
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password

class StudentForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())


    class Meta:
        model = Student
        fields = [
            'roll_number',
            'classroom',
            'gender',
            'date_of_birth',
            'address',
            'profile_image'
        ] 

class TeacherForm(forms.ModelForm):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = Teacher
        fields = [
            'full_name',
            'email',
            'subject',
            'phone',
            'profile_image'
        ]
class ChangePasswordForm(forms.Form):

    old_password = forms.CharField(
        label="Old Password",
        widget=forms.PasswordInput(attrs={'placeholder':'Enter Your Old Password'})
    )

    new_password = forms.CharField(
        label="New Password",
        widget=forms.PasswordInput(attrs={'placeholder':'Enter Your New Password'})
    )

    confirm_password = forms.CharField(
        label="Confirm Password",
        widget=forms.PasswordInput(attrs={'placeholder':'Enter Confirm Password'})
    )

    def clean(self):
        cleaned_data = super().clean()
        new = cleaned_data.get("new_password")
        confirm = cleaned_data.get("confirm_password")

        if new and confirm and new != confirm:
            raise forms.ValidationError("New password and confirm password do not match")
        return cleaned_data 