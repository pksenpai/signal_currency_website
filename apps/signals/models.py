from django.db import models
from apps.core.models import LogicalBaseModel, TimeStampBaseModel, StatusMixin
from apps.user.models import Profile


class Signal(LogicalBaseModel, TimeStampBaseModel, StatusMixin):
    
    """\_____________[RELATIONS]_____________/"""
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='signals')
    
    """\_____________[MAIN]_____________/"""
    title = models.CharField(max_length=30)
    MARKETS_CHOICES = (
        ('EIR', 'Iran Exchanges'),
        ('CRP', 'Crypto'),
    )
    target_market = models.CharField(max_length=3, choices=MARKETS_CHOICES)
    token = models.CharField(max_length=30)
    
    INVESTMENT_PERIOD_CHOICES = (
        ('L', 'Long time'),
        ('M', 'Mid time'),
        ('S', 'Short time'),
    )
    investment_period = models.CharField(max_length=1, choices=INVESTMENT_PERIOD_CHOICES, null=True, blank=True)
    
    DIRECTION_CHOICES = (
        ('U', 'Up'),
        ('D', 'Down'),
    )
    direction = models.CharField(max_length=1, choices=DIRECTION_CHOICES, null=True, blank=True)
    
    fundamental_analysis = models.TextField()
    technical_analysis = models.TextField()
    price_action_analysis = models.TextField()
    pa_time_frame = models.PositiveSmallIntegerField()
    
    hints = models.TextField()
    like = models.IntegerField()
    
