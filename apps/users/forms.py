from django import forms
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.contrib.auth import get_user_model; User = get_user_model()

    
class UserRegisterForm(forms.ModelForm): # C
    password1 = forms.CharField(max_length=128, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=128, widget=forms.PasswordInput)
    
    class Meta:
        model = User
        exclude = (
            'password', 'email', 'date_joined', 'is_admin', 'is_active'
        )
        
        widgets = {
            'country': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2
    
    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user
    

class UserLoginForm(forms.Form): # R
    username = forms.CharField(max_length=150, validators=[UnicodeUsernameValidator])
    password = forms.CharField(max_length=128)


class UserUpdateForm(forms.ModelForm): # U
    # password = ReadOnlyPasswordHashField(help_text="<a href=\"{% url 'core:home' %}\">change password?</a>")
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = User
        fields = '__all__'
        
class UserDeleteFrom: ... # D

