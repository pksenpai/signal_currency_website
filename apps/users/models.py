from django.db import models
from apps.core.models import LogicalBaseModel, TimeStampBaseModel
from django.contrib.auth.models import AbstractUser

from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _

class Account(models.Model):
    """\_______________[MAIN]_______________/"""
    account_number = models.CharField(max_length=30)
    
    USER_TYPE_CHOICES = (
        ('G', 'Golden'),
        ('S', 'Silver'),
        ('N', 'Normal'),
    )
    user_type = models.CharField(max_length=1, choices=USER_TYPE_CHOICES)
    
    class Meta:
        abstract = True
    
    
class CustomUser(AbstractUser, Account, LogicalBaseModel, TimeStampBaseModel):
    """\_______________[MAIN]_______________/"""
    CountryChoices = (('IR', 'Iran +98'),)
    country = models.CharField(max_length=2, choices=CountryChoices)
    
    phone_number = models.CharField(
        max_length   = 50,
        unique       = True,
        verbose_name = "Phone Number",
        validators   = [
            RegexValidator(
                regex=r'(?:([+]\d{1,4})[-.\s]?)?(?:[(](\d{1,3})[)][-.\s]?)?(\d{1,4})[-.\s]?(\d{1,4})[-.\s]?(\d{1,9})',
                message="Invalid phone number format!",
            ),
        ], 
    )
    
    email = models.EmailField(
        unique       = True,
        blank        = True,
        verbose_name = _("Email Address")
    )
    
    is_active = models.BooleanField(
        _("active"),
        default=False,
    )

    def __str__(self):
        return self.username


class Profile(LogicalBaseModel):
    """\_____________[RELATIONS]_____________/"""
    follows = models.ManyToManyField(
        to           = 'self',
        blank        = True,
        symmetrical  = False,
        related_name = "followed_by",
        verbose_name = _('Follows'),
    )
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)

    """\_______________[MAIN]_______________/"""
    nick_name  = models.CharField(max_length=50, unique=True)
    first_name = models.CharField(max_length=50, blank=True)
    last_name  = models.CharField(max_length=50, blank=True)
    
    score = models.SmallIntegerField(
        default    = None,
        null       = True,
        validators = [
            MinValueValidator(-100),
            MaxValueValidator(100)
        ]
    ) # wrost score(-100%) to best score(100%)
    
    bio = models.TextField(max_length=500, null=True, blank=True)
    
    def __str__(self):
        return (self.first_name + ' ' + self.last_name).strip() or self.nick_name

    # add a method that check last and first name exists or not if not dont access input!