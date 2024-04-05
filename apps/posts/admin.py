from django.contrib import admin
from .models import Signal, Comment, Reply, Report


admin.site.register(Signal)
admin.site.register(Comment)
admin.site.register(Reply)
admin.site.register(Report)
