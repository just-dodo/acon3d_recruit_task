from django.db import models
from datetime import datetime, timedelta

class TimeModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(null=True, default=None)


    def __str__(self):
        try:
            return self.name
        except AttributeError:
            try:
                return self.title
            except AttributeError:  
                return super().__str__()
    class Meta:
        abstract = True

    def check_as_delete(self):
        self.deleted_at = datetime.now()
        self.save(update_fields=["deleted_at"])
    
    @staticmethod
    def check_queryset_as_delete(queryset):
        queryset.update(deleted_at = datetime.now())