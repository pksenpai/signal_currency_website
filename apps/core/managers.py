from django.db import models


class LogicalQuerySet(models.QuerySet):
    def delete(self):
        """
        - override delete method for querysets(multiple objs)
        - is_deleted objects is hide from users
        """
        return super().update(is_deleted=True)

    def hard_delete(self): # danger!!!
        """!!! delete all of that objs from database forever !!!"""
        return super().delete()


class LogicalManager(models.Manager):
    
    def get_queryset(self):
        """ only show objects that is unhide by default! """
        return LogicalQuerySet(self.model).filter(is_deleted=False, is_active=True)

    def archive(self):
        """ show all objects by this method | hide & unhide! no diff! """
        return LogicalQuerySet(self.model)

    def deleted(self):
        """ only show objects that is hide by this method! """
        return LogicalQuerySet(self.model).filter(is_deleted=True)

