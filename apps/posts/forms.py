from django import forms

from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

from .models import Signal
from apps.users.models import Profile

import string
import random


class CreateSignalForm(forms.ModelForm):

    class Meta:
        model = Signal
        exclude = ('author', 'slug_title', 'like')
        
        widgets = {
            'target_market': forms.Select(attrs={'required': True, 'class': 'form-control'}),
            'investment_period': forms.Select(attrs={'required': True, 'class': 'form-control'}),
            'direction': forms.Select(attrs={'required': True, 'class': 'form-control'}),
            'pa_time_frame': forms.Select(attrs={'required': True, 'class': 'form-control'}),
            
            'entry_point': forms.NumberInput(attrs={
                'type': 'number', 'step': "0.01", 
                'style': 'margin: auto; border-radius: 25px; height: 40px; padding-right: 20px; width: 300px;'
            }),

            'profit_limit': forms.NumberInput(attrs={
                'type': 'number', 'step': "0.01", 
                'style': 'margin: auto; border-radius: 25px; height: 40px; padding-right: 20px; width: 300px;'
            }),

            'loss_limit': forms.NumberInput(attrs={
                'type': 'number', 'step': "0.01",
                'style': 'margin: auto; margin-left: 25px; border-radius: 25px; height: 40px; padding-right: 20px; width: 300px;'
            }),
            
            'goal_datetime':forms.TextInput(attrs={
                'required': True, 'type':'datetime-local', 
                'style': 'border-radius: 25px; height: 40px; padding-left: 20px; width: 300px;'
            }),
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
        
        """ Create Unique Slug from title """
        signal.slug_title = '_'.join( # slugify!
            "".join(
                filter(
                    lambda char: not char in string.punctuation,
                    signal.title.strip()
                    )
                ).split()
            )
        
        while Signal.objects.filter(slug_title=signal.slug_title).exists(): # unique test!
            signal.slug_title += str(random.randint(0, 10))
                
        """ active or unactive signal at the first """
        signal.is_active = True
        
        if commit:
            signal.save()
        
        return signal
    
