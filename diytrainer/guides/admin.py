from django.contrib import admin

from sorl.thumbnail.admin import AdminImageMixin

from .models import Guide, Feedback, EmailSignUp, Descriptor


class DescriptorInline(AdminImageMixin, admin.StackedInline):
    model = Descriptor


class GuideAdmin(AdminImageMixin, admin.ModelAdmin):
    list_display = ('name', 'version')
    inlines = [
        DescriptorInline
    ]


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('guide', 'submission_date', 'skill_ranking')
    list_filter = ('submission_date',)
    readonly_fields = (
        'guide', 'submission_date', 'skill_ranking', 'project_recommendation')


class EmailSignUpAdmin(admin.ModelAdmin):
    list_display = ('email', 'guide', 'submission_date')
    list_filter = ('submission_date',)
    readonly_fields = ('email', 'guide', 'submission_date')

admin.site.register(Guide, GuideAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(EmailSignUp, EmailSignUpAdmin)
