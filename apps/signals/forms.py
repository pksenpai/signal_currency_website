from django import forms

from ckeditor.widgets import CKEditorWidget

from .models import Signal


class CreateSignalForm(forms.ModelForm):
    fundamental_analysis = forms.CharField(widget=CKEditorWidget())
    
    class Meta:
        model = Signal
        exclude = ('author', 'like')
        
        TIME_FRAMES = (
            (0, 'Unlimited'),
            (1, '1m'),
            (5, '5m'),
            (15, '15m'),
            (30, '30m'),
            (60, '1h'),
            (90, '3h'),
            (300, '5h'),
            (600, '10h'),
            (1440, '1d'),
            (4320, '3d'),
            (10080, '1w'),
        )
                
        widgets = {
            'investment_period': forms.Select(attrs={'class': 'form-control'}),
            'direction': forms.Select(attrs={'class': 'form-control'}),
            'pa_time_frame': forms.Select(choices=TIME_FRAMES,attrs={'class': 'form-control'}),
        }
         
