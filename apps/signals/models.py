from django.db import models
from apps.core.models import LogicalBaseModel, TimeStampBaseModel, StatusMixin
from apps.users.models import Profile

from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _

from ckeditor_uploader.fields import RichTextUploadingField


class Signal(LogicalBaseModel, TimeStampBaseModel, StatusMixin):
    """\_____________[CHOICES]_____________/"""
    MARKETS_CHOICES = (
        ('EIR', 'Iran Exchanges'),
        ('CRP', 'Crypto'),
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
    
    """\_____________[RELATIONS]_____________/"""
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='signals')
    
    """\_____________[MAIN]_____________/"""
    title   = models.CharField(max_length=100)
    summary = models.CharField(max_length=150)
    
    target_market = models.CharField(max_length=3, choices=MARKETS_CHOICES)
    token = models.CharField(max_length=30)
    investment_period = models.CharField(max_length=1, choices=INVESTMENT_PERIOD_CHOICES, null=True, blank=True)
    direction = models.CharField(max_length=1, choices=DIRECTION_CHOICES, null=True, blank=True)
    
    fundamental_analysis  = RichTextUploadingField()
    technical_analysis    = RichTextUploadingField()
    price_action_analysis = RichTextUploadingField()
    pa_time_frame = models.PositiveSmallIntegerField()
    
    hints = RichTextUploadingField(null=True, blank=True)
    like = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        self.author = kwargs['user']
        super(Signal, self).save(*args, **kwargs)


class Comment(LogicalBaseModel, TimeStampBaseModel, StatusMixin):
    """\_____________[RELATIONS]_____________/"""
    signal = models.ForeignKey(Signal, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    
    """\_____________[MAIN]_____________/"""
    body = RichTextUploadingField(max_length=1000)
    
    probability = models.SmallIntegerField(
            default=None,
            null=True,
            validators=[
                MinValueValidator(0),
                MaxValueValidator(100)
            ]
        ) # 0% to 100%
    
    like = models.IntegerField(default=0) # can be negative(-)


class Reply(LogicalBaseModel, TimeStampBaseModel, StatusMixin):
    """\_____________[RELATIONS]_____________/"""
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE, related_name='replies')
    reply = models.ForeignKey('self', on_delete=models.CASCADE, related_name='replies')
    
    """\_____________[MAIN]_____________/"""
    body = models.CharField(max_length=150)


class Report(TimeStampBaseModel):
    """\_____________[RELATIONS]_____________/"""
    reporter = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='reporter')
    profile  = models.ForeignKey(Profile, null=True, on_delete=models.DO_NOTHING, related_name='profile_reps')
    signal   = models.ForeignKey(Signal, null=True, on_delete=models.DO_NOTHING, related_name='reports')
    comment  = models.ForeignKey(Comment, null=True, on_delete=models.DO_NOTHING, related_name='reports')
    reply    = models.ForeignKey(Reply, null=True, on_delete=models.DO_NOTHING, related_name='reports')

    """\_____________[MAIN]_____________/"""
    reason = models.CharField(max_length=100)
    
