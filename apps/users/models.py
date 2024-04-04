from django.db import models
from django.contrib.auth.models import AbstractBaseUser, AbstractUser

from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.utils.translation import gettext_lazy as _
from django.utils import timezone

from apps.core.models import LogicalBaseModel, TimeStampBaseModel, StatusMixin
from .managers import UserManager
# from PIL import Image


class ProfileImageBaseModel(LogicalBaseModel, StatusMixin):
    image = models.ImageField(upload_to='images/profile/', default='images/profile/default.png')
    alt   = models.CharField(max_length=255, default="default_img", blank=True)

    # def resize_image(self):
    #     MAX_SIZE = (50, 50)
    #     image = Image.open(self.src)
    #     image.thumbnail(MAX_SIZE)
    #     # save the resized image to the file system
    #     # this is not the model save method!
    #     image.save(self.src.path)
    
    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)
    #     self.resize_image()
        
    class Meta:
        abstract = True


class AccountBaseModel(models.Model):
    """\_______________[MAIN]_______________/"""
    account_number = models.CharField(max_length=30)
    
    USER_TYPE_CHOICES = (
        ('G', 'Golden'),
        ('S', 'Silver'),
        ('N', 'Normal'),
    )
    user_type = models.CharField(max_length=1, default='N', choices=USER_TYPE_CHOICES)
    
    class Meta:
        abstract = True


class Profile(ProfileImageBaseModel):
    """\_____________[RELATIONS]_____________/"""
    follows = models.ManyToManyField(
        to           = 'self',
        blank        = True,
        symmetrical  = False,
        related_name = "followed_by",
        verbose_name = _('Follows'),
    )
    user = models.OneToOneField('CustomUser', on_delete=models.CASCADE)

    """\_______________[MAIN]_______________/"""
    nick_name  = models.CharField(max_length=50, unique=True)
    
    first_name = models.CharField(max_length=50, blank=True)
    last_name  = models.CharField(max_length=50, blank=True)
    
    score = models.SmallIntegerField(
        default    = None,
        null       = True,
        blank      = True,
        validators = [
            MinValueValidator(-100),
            MaxValueValidator(100)
        ]
    ) # wrost score(-100%) to best score(100%)
    
    bio = models.TextField(max_length=500, null=True, blank=True)
    
    def get_full_name(self):
        """
        Return the first_name plus the last_name, with a space in between.
        """
        full_name = "%s %s" % (self.first_name, self.last_name)
        return full_name.strip()

    def get_short_name(self):
        """Return the short name for the user."""
        return self.first_name
    
    def __str__(self):
        return (self.first_name + ' ' + self.last_name).strip() or self.nick_name

    # add a method that check last and first name exists or not if not dont access input!


class CustomUser(AbstractBaseUser, AccountBaseModel, LogicalBaseModel, TimeStampBaseModel, StatusMixin):
    """\_______________[MAIN]_______________/"""

    username = models.CharField(
        _("username"),
        max_length=150,
        unique=True,
        help_text=_(
            "Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only."
        ),
        validators=[UnicodeUsernameValidator()],
        error_messages={
            "unique": _("A user with that username already exists."),
        },
    )
    
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
    
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
    )
    is_active = models.BooleanField(
        _("active"),
        default=True,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
    )
    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    email = models.EmailField(
        blank        = True,
        null         = True,
        verbose_name = _("Email Address")
    )
    
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ('phone_number',)
    
    def save(self, *args, **kwargs):
        super().save()
        Profile.objects.create(user=self, nick_name=self.username, is_active=True)

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)

    def __str__(self):
        return self.username
    
