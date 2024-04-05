from django import forms

from django.core.exceptions import ValidationError

from .models import Signal
from apps.users.models import Profile


class CreateSignalForm(forms.ModelForm):
    
    class Meta:
        model = Signal
        exclude = ('author', 'like')
        
        widgets = {
            'target_market': forms.Select(attrs={'class': 'form-control'}),
            'investment_period': forms.Select(attrs={'class': 'form-control'}),
            'direction': forms.Select(attrs={'class': 'form-control'}),
            'pa_time_frame': forms.Select(attrs={'class': 'form-control'}),
        }
    
    def save(self, commit=True, **kwargs):
        # Save current user as signal author
        # Set is_active True at the first or not!
        signal = super().save(commit=False)
        user = kwargs.get('user', None)
        
        if not user:
            raise ValidationError("nice try!, but you are not authenticated!")
        
        user_profile = Profile.objects.get(user=user)
        
        signal.author = user_profile
        signal.is_active = True
        
        if commit:
            signal.save()
        
        return signal            
    
