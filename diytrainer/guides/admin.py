from django.contrib import admin

from sorl.thumbnail.admin import AdminImageMixin

from .models import Guide, Feedback, EmailSignUp


class GuideAdmin(AdminImageMixin, admin.ModelAdmin):
    pass


class FeedbackAdmin(admin.ModelAdmin):
    pass


class EmailSignUpAdmin(admin.ModelAdmin):
    pass

admin.site.register(Guide, GuideAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(EmailSignUp, EmailSignUpAdmin)
