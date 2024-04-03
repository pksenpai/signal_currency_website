from django.db import models

from .managers import LogicalManager

# from django.core.exceptions import ValidationError
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
    
