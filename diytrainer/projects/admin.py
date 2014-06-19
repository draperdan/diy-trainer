from django.contrib import admin

from .models import Project, Feedback, DetailLevel


class ProjectAdmin(admin.ModelAdmin):
    pass


class FeedbackAdmin(admin.ModelAdmin):
    pass


class DetailLevelAdmin(admin.ModelAdmin):
    pass

admin.site.register(Project, ProjectAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(DetailLevel, DetailLevelAdmin)
