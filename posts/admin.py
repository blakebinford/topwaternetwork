from django.contrib import admin
from .models import FishingReport, Comment

# Register your models here.


class FishingReportAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('title',)}

admin.site.register(FishingReport, FishingReportAdmin)

admin.site.register(Comment)
