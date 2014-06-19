from django.contrib import admin

from .models import Guide, Feedback, EmailSignUp


class GuideAdmin(admin.ModelAdmin):
    pass


class FeedbackAdmin(admin.ModelAdmin):
    pass


class EmailSignUpAdmin(admin.ModelAdmin):
    pass

admin.site.register(Guide, GuideAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(EmailSignUp, EmailSignUpAdmin)
