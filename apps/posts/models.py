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
        ('سهام ایران', 'سهام ایران'),
        ('ارز دیجیتال', 'ارز دیجیتال'),
    )
    
    INVESTMENT_PERIOD_CHOICES = (
        ('بلند مدت', 'بلند مدت'),
        ('میان مدت', 'میان مدت'),
        ('کوتاه مدت', 'کوتاه مدت'),
    )
    
    DIRECTION_CHOICES = (
        ('خرید', 'خرید'),
        ('فروش', 'فروش'),
    )
    
    TIME_FRAMES = (
        ('۱ دقیقه', '۱ دقیقه'),
        ('۵ دقیقه', '۵ دقیقه'),
        ('۱۵ دقیقه', '۱۵ دقیقه'),
        ('۳۰ دقیقه', '۳۰ دقیقه'),
        ('۱ ساعت', '۱ ساعت'),
        ('۴ ساعت', '۴ ساعت'),
        ('روز', 'روز'),
        ('هفته', 'هفته'),
        ('ماه', 'ماه'),
        ('سال', 'سال'),
    )
    
    """\_____________[RELATIONS]_____________/"""
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='signals')
    
    """\_____________[MAIN]_____________/"""
    title      = models.CharField(max_length=50)
    summary    = models.CharField(max_length=100)
    slug_title = models.SlugField(max_length=50, unique=True, allow_unicode=True)
    
    is_open = models.BooleanField(default=True)
    goal_datetime = models.DateTimeField()
    
    token = models.CharField(max_length=30)
    target_market = models.CharField(max_length=20, choices=TARGET_MARKETS)
    investment_period = models.CharField(max_length=9, choices=INVESTMENT_PERIOD_CHOICES, null=True, blank=True)
    direction = models.CharField(max_length=4, choices=DIRECTION_CHOICES, null=True, blank=True)

    entry_point = models.FloatField(validators=[MinValueValidator(0)])
    profit_limit = models.FloatField(validators=[MinValueValidator(0)]) # take_profit
    loss_limit = models.FloatField(validators=[MinValueValidator(0)]) # stop_loss
    
    # max_range = models.PositiveSmallIntegerField(
    #         default=None,
    #         null=True,
    #         blank=True,
    #         validators=[
    #             MinValueValidator(1),
    #             MaxValueValidator(100)
    #         ]
    #     ) # 1% to 100%

    # min_range = models.PositiveSmallIntegerField(
    #         default=None,
    #         null=True,
    #         blank=True,
    #         validators=[
    #             MinValueValidator(0),
    #             MaxValueValidator(100)
    #         ]
    #     ) # 0% to 100%

    
    fundamental_analysis  = RichTextField()
    technical_analysis    = RichTextField()
    price_action_analysis = RichTextField()
    
    pa_time_frame = models.CharField(max_length=10, default='۱ ساعت', choices=TIME_FRAMES)
    
    hints = RichTextField(null=True, blank=True)
    like = models.IntegerField(default=0)
    
    def clean(self):
        if tz.now() >= self.goal_datetime:
            raise ValidationError("تاریخ انقضا تحلیل نمیتواند گذشته باشد!")
        
        if self.profit_limit and self.loss_limit:
            if self.profit_limit <= self.loss_limit:
                raise ValidationError("حد سود نمیتواند از حد ضرر کمتر باشد!")
        else:
            if self.profit_limit or self.loss_limit:
                raise ValidationError("حد سود و حد ضرر نمیتواند خالی باشد!")
    
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
    
