from django.contrib import admin

from sorl.thumbnail.admin import AdminImageMixin

from .models import Project, Feedback, DetailLevel, Step, Module


class StepInline(AdminImageMixin, admin.StackedInline):
    model = Step


class ModuleInline(admin.StackedInline):
    model = Module


class ProjectAdmin(AdminImageMixin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class DetailLevelAdmin(admin.ModelAdmin):
    list_display = ('level', 'project')
    inlines = [
        ModuleInline,
        StepInline
    ]


class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('submission_date', 'project', 'detail_level', 'was_satisifed')
    list_filter = ('was_satisifed', 'submission_date')


admin.site.register(DetailLevel, DetailLevelAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Feedback, FeedbackAdmin)
