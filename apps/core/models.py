from django.db import models

from .managers import LogicalManager
from apps.user.models import Profile
from apps.signal.models import Signal

from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.utils.translation import gettext_lazy as _


"""\__________________[[Abstract Models]]__________________/"""

class TimeStampBaseModel(models.Model):
    created_at = models.DateTimeField(
        auto_now_add = True,
        editable     = False,
        verbose_name = _("Created at"),
    )

    updated_at = models.DateTimeField(
        auto_now     = True,
        editable     = False,
        verbose_name = _("Update at"),
    )

    class Meta:
        abstract = True


class LogicalBaseModel(models.Model):
    is_active = models.BooleanField(
        default      = False,
        verbose_name = _("Active"),
    )
    
    is_deleted = models.BooleanField(
        default      = False,
        verbose_name = _("Deleted"),
    )

    objects = LogicalManager()

    class Meta:
        abstract = True

    def delete(self, using=None, keep_parents=False):
        """
        - override delete method for one obj
        - is_deleted object is hide from users
        """
        self.is_deleted = True
        self.save()

    def hard_delete(self): # danger
        """ !!! delete that one obj from database forever !!! """
        super().delete()

    def undelete(self):
        """ unhide is_deleted object """
        self.is_deleted = False
        self.save()


class StatusMixin:
    @property
    def status(self) -> bool:
        return self.is_active and not self.is_deleted


class ProfileImageBaseModel(LogicalBaseModel, StatusMixin):
    """ low size images for User & Seller profiles """
    src = models.ImageField(upload_to='images/profile/', default='images/profile/default.png')
    alt = models.CharField(max_length=255)
        
    class Meta:
        abstract = True
    
    
"""\__________________[[MAIN Models]]__________________/"""

class Comment(LogicalBaseModel, TimeStampBaseModel, StatusMixin):
    """\_____________[RELATIONS]_____________/"""
    signal = models.ForeignKey(Signal, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='comments')
    
    """\_____________[MAIN]_____________/"""
    body = models.TextField(max_length=1000)
    
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
    reply = models.ForeignKey('self', on_delete=models.CASCADE)
    
    """\_____________[MAIN]_____________/"""
    body = models.CharField(max_length=150)


class Report(TimeStampBaseModel):
    """\_____________[RELATIONS]_____________/"""
    reporter = models.ForeignKey(Profile, on_delete=models.DO_NOTHING, related_name='reports')
    signal = models.ForeignKey(Signal, null=True, on_delete=models.DO_NOTHING, related_name='reports')
    comment = models.ForeignKey(Comment, null=True, on_delete=models.DO_NOTHING, related_name='reports')
    reply = models.ForeignKey(Reply, null=True, on_delete=models.DO_NOTHING, related_name='reports')
    
    """\_____________[MAIN]_____________/"""
    reason = models.CharField(max_length=100)
    
