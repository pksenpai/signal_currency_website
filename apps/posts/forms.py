from django import forms

from django.core.exceptions import ValidationError

from string import punctuation

from .models import Signal
from apps.users.models import Profile


class CreateSignalForm(forms.ModelForm):

    class Meta:
        model = Signal
        exclude = ('author', 'slug_title', 'like')
        
        widgets = {
            'target_market': forms.Select(attrs={'required': True, 'class': 'form-control'}),
            'investment_period': forms.Select(attrs={'required': True, 'class': 'form-control'}),
            'direction': forms.Select(attrs={'required': True, 'class': 'form-control'}),
            'pa_time_frame': forms.Select(attrs={'required': True, 'class': 'form-control'}),
            
            'max_range': forms.NumberInput(attrs={'type': 'number'}),
            'min_range': forms.NumberInput(attrs={'type': 'number'}),
            
            'goal_datetime':forms.TextInput(attrs={'required': True, 'type':'datetime-local'}),
        }
    
    def save(self, commit=True, **kwargs):
        # Save current user as signal author
        # Set is_active True at the first or not!
        signal = super().save(commit=False)
        user = kwargs.get('user', None)
        
        if not user:
            raise ValidationError("nice try!, but you are not authenticated!")
        
        """ author is who creating this signal """
        user_profile = Profile.objects.get(user=user)
        signal.author = user_profile
        
        """ remove the start and end spaces """
        signal.title = signal.title.strip()
        signal.summary = signal.summary.strip()
        
        """ set the summary for url """
        signal.slug_title = '_'.join(
            "".join(
                filter(
                    lambda char: not char in punctuation,
                       signal.title + ' ' + signal.summary
                    )
                ).split()
            )
        
        """ active or unactive signal at the first """
        signal.is_active = True
        
        if commit:
            signal.save()
        
        return signal
    
