from django.db import models

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _
from django.utils import timezone as tz

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
        ('-', 'Unlimited'),
        ('1m', '1m'),
        ('5m', '5m'),
        ('15m', '15m'),
        ('30m', '30m'),
        ('1h', '1h'),
        ('3h', '3h'),
        ('5h', '5h'),
        ('10h', '10h'),
        ('1d', '1d'),
        ('3d', '3d'),
        ('1w', '1w'),
    )
    
    """\_____________[RELATIONS]_____________/"""
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='signals')
    
    """\_____________[MAIN]_____________/"""
    title      = models.CharField(max_length=100)
    summary    = models.CharField(max_length=150)
    slug_title = models.SlugField(unique=True)
    
    is_open = models.BooleanField(default=True)
    goal_datetime = models.DateTimeField()
    
    token = models.CharField(max_length=30)
    target_market = models.CharField(max_length=3, choices=TARGET_MARKETS)
    investment_period = models.CharField(max_length=1, choices=INVESTMENT_PERIOD_CHOICES, null=True, blank=True)
    direction = models.CharField(max_length=1, choices=DIRECTION_CHOICES, null=True, blank=True)
    max_range = models.PositiveSmallIntegerField(
            default=None,
            null=True,
            blank=True,
            validators=[
                MinValueValidator(1),
                MaxValueValidator(100)
            ]
        ) # 1% to 100%

    min_range = models.PositiveSmallIntegerField(
            default=None,
            null=True,
            blank=True,
            validators=[
                MinValueValidator(0),
                MaxValueValidator(100)
            ]
        ) # 0% to 100%

    
    fundamental_analysis  = RichTextField()
    technical_analysis    = RichTextField()
    price_action_analysis = RichTextField()
    
    pa_time_frame = models.CharField(max_length=3, default='Unlimited', choices=TIME_FRAMES)
    
    hints = RichTextField(null=True, blank=True)
    like = models.IntegerField(default=0)
    
    def save(self):
        super().save()
        
        if tz.now() >= self.goal_datetime:
            raise ValidationError("the goal datetime cann't be past!")
        
        if self.max_range and self.max_range:
            if self.max_range <= self.min_range:
                raise ValidationError("the max range cann't be less than or equal with the min range!")
        else:
            if self.max_range or self.min_range:
                raise ValidationError("both max & min range required!")
    
    def expire_signal(self):
        if tz.now() >= self.goal_datetime:
            self.is_open = False
    
    def __str__(self):
        return self.title
    

class Comment(LogicalBaseModel, TimeStampBaseModel, StatusMixin):
    """\_____________[RELATIONS]_____________/"""
    signal = models.ForeignKey(Signal, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    
    """\_____________[MAIN]_____________/"""
    body = RichTextField(max_length=1000)
    
    probability = models.PositiveSmallIntegerField(
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
    
