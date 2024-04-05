from django.db import models

from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

from apps.core.models import LogicalBaseModel, TimeStampBaseModel, StatusMixin
from apps.users.models import Profile

from ckeditor.fields import RichTextField


class Signal(LogicalBaseModel, TimeStampBaseModel, StatusMixin):
    """\_____________[CHOICES]_____________/"""
    TARGET_MARKETS = (
        ('EIR', 'Iran Exchanges'),
        ('CRP', 'Crypto Currency'),
    )
    
    INVESTMENT_PERIOD_CHOICES = (
        ('L', 'Long time'),
        ('M', 'Mid time'),
        ('S', 'Short time'),
    )
    
    DIRECTION_CHOICES = (
        ('U', 'Up'),
        ('D', 'Down'),
    )
    
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
    
    """\_____________[RELATIONS]_____________/"""
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='signals')
    
    """\_____________[MAIN]_____________/"""
    title   = models.CharField(max_length=100)
    summary = models.CharField(max_length=150)
    
    target_market = models.CharField(max_length=3, choices=TARGET_MARKETS)
    token = models.CharField(max_length=30)
    investment_period = models.CharField(max_length=1, choices=INVESTMENT_PERIOD_CHOICES, null=True, blank=True)
    direction = models.CharField(max_length=1, choices=DIRECTION_CHOICES, null=True, blank=True)
    
    fundamental_analysis  = RichTextField()
    technical_analysis    = RichTextField()
    price_action_analysis = RichTextField()
    
    pa_time_frame = models.PositiveSmallIntegerField(default=0, choices=TIME_FRAMES)
    
    hints = RichTextField(null=True, blank=True)
    like = models.IntegerField(default=0)

    def __str__(self):
        return self.title
    

class Comment(LogicalBaseModel, TimeStampBaseModel, StatusMixin):
    """\_____________[RELATIONS]_____________/"""
    signal = models.ForeignKey(Signal, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    
    """\_____________[MAIN]_____________/"""
    body = RichTextField(max_length=1000)
    
    probability = models.SmallIntegerField(
            default=None,
            null=True,
            validators=[
                MinValueValidator(0),
                MaxValueValidator(100)
            ]
        ) # 0% to 100%
    
    like = models.IntegerField(default=0) # can be negative(-)
    
    def __str__(self):
        return str(self.signal)
    

class Reply(LogicalBaseModel, TimeStampBaseModel, StatusMixin):
    """\_____________[RELATIONS]_____________/"""
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies')
    
    """\_____________[MAIN]_____________/"""
    body = models.CharField(max_length=150)
    
    def __str__(self):
        return str(self.comment) or str(self.reply)


class Report(TimeStampBaseModel):
    """\_____________[RELATIONS]_____________/"""
    reporter = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='reporter')
    profile  = models.ForeignKey(Profile, null=True, on_delete=models.DO_NOTHING, related_name='profile_reps')
    signal   = models.ForeignKey(Signal, null=True, on_delete=models.DO_NOTHING, related_name='reports')
    comment  = models.ForeignKey(Comment, null=True, on_delete=models.DO_NOTHING, related_name='reports')
    reply    = models.ForeignKey(Reply, null=True, on_delete=models.DO_NOTHING, related_name='reports')

    """\_____________[MAIN]_____________/"""
    reason = models.CharField(max_length=100)
    
    def __str__(self):
        return self.reason
    
