from django import forms

from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.contrib.auth import get_user_model; User = get_user_model()


class UserCreationFrom(forms.ModelForm):
    password1 = forms.CharField(max_length=128)
    password2 = forms.CharField(max_length=128)
    
    class Meta:
        model = User
        exclude = (
            'password', 'is_staff', 'is_active', 'date_joined', 'email'
        )
        
        widgets = {
            'country': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def clean_password2(self):
        cd = self.cleaned_data
        
        if not cd['password1'] or not cd['password2']:
            raise ValidationError('please enter the password!')
            
        if cd['password1'] != cd['password2']:
            raise ValidationError('passwords not match!')
        
        return cd['password2']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
        
        return user
    

class UserLoginForm(forms.Form):
    username = forms.CharField(max_length=150, validators=[UnicodeUsernameValidator])
    password = forms.CharField(max_length=128)


class UserChangeForm(forms.ModelForm):
    # password = ReadOnlyPasswordHashField(help_text="<a href=\"{% url 'core:home' %}\">change password?</a>")
    password = ReadOnlyPasswordHashField()
    
    class Meta:
        model = User
        fields = '__all__'
        
