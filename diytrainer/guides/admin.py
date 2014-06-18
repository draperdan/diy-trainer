from django.contrib import admin

from .models import GuideFeedback


class GuideFeedbackAdmin(admin.ModelAdmin):
    pass

admin.site.register(GuideFeedback, GuideFeedbackAdmin)
