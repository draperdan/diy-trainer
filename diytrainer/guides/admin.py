from django.contrib import admin

from sorl.thumbnail.admin import AdminImageMixin

from .models import Guide, Feedback, EmailSignUp, Descriptor


class DescriptorInline(AdminImageMixin, admin.StackedInline):
    model = Descriptor


class GuideAdmin(AdminImageMixin, admin.ModelAdmin):
    inlines = [
        DescriptorInline
    ]


class FeedbackAdmin(admin.ModelAdmin):
    pass


class EmailSignUpAdmin(admin.ModelAdmin):
    pass

admin.site.register(Guide, GuideAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(EmailSignUp, EmailSignUpAdmin)
