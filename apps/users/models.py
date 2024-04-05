from django.db import models
from django.contrib.auth.models import AbstractBaseUser

from django.core.validators import RegexValidator
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.validators import UnicodeUsernameValidator

from django.utils.translation import gettext_lazy as _
from django.utils import timezone

# from PIL import Image
from apps.core.models import LogicalBaseModel, TimeStampBaseModel, StatusMixin
from .regexes import PHONE_NUMBER_REGEX
from .managers import CustomUserManager


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


class CustomUser(AbstractBaseUser,
                 AccountBaseModel,
                 LogicalBaseModel,
                 TimeStampBaseModel,
                 StatusMixin):
    
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

    email = models.EmailField(
        verbose_name=_("email address"),
        max_length=150,
        blank=True,
    )
    
    CountryChoices = (('+98|IR', 'IR'),)
    country = models.CharField(max_length=6, choices=CountryChoices)
    
    phone_number = models.CharField(
        max_length   = 50,
        unique       = True,
        verbose_name = "Phone Number",
        validators   = [
            RegexValidator(
                regex=fr"{PHONE_NUMBER_REGEX}",
                message="Invalid phone number format!",
            ),
        ],
    )

    date_joined = models.DateTimeField(_("date joined"), default=timezone.now)

    is_admin = models.BooleanField(default=False)
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "this user is not active!"
        ),
    )

    objects = CustomUserManager()

    USERNAME_FIELD = "username"
    REQUIRED_FIELDS = ["phone_number", "country"]

    def __str__(self):
        return self.username

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    
    
#     is_staff = models.BooleanField(
#         _("staff status"),
#         default=False,
#         help_text=_("Designates whether the user can log into this admin site."),
#     )
#     def email_user(self, subject, message, from_email=None, **kwargs):
#         """Send an email to this user."""
#         send_mail(subject, message, from_email, [self.email], **kwargs)
    
