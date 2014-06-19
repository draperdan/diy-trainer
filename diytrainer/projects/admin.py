from django.contrib import admin

from .models import Project, Feedback, DetailLevel


class DetailLevelInline(admin.StackedInline):
    model = DetailLevel


class ProjectAdmin(admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}
    inlines = [
        DetailLevelInline
    ]


class FeedbackAdmin(admin.ModelAdmin):
    pass


admin.site.register(Project, ProjectAdmin)
admin.site.register(Feedback, FeedbackAdmin)
