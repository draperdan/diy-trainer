from django.contrib import admin

from .models import Guide, Feedback


class GuideAdmin(admin.ModelAdmin):
    pass


class FeedbackAdmin(admin.ModelAdmin):
    pass

admin.site.register(Guide, GuideAdmin)
admin.site.register(Feedback, FeedbackAdmin)
