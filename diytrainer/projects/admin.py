from django.contrib import admin

from sorl.thumbnail.admin import AdminImageMixin

from .models import Project, Feedback, DetailLevel, Step, Module


class StepInline(AdminImageMixin, admin.StackedInline):
    model = Step


class StepAdmin(admin.ModelAdmin):
    list_display = ('sanitized_title', 'detail_level', 'rank', 'module', 'project')
    readonly_fields = ('module', 'project')
    search_fields = ('title',)

    def module(self, obj):
        if obj.detail_level.level == 3:
            module = Module.objects.filter(
                steps__id=obj.id).values_list('title', flat=True)[0]
            return module
        else:
            return 'N/A'
    module.short_description = 'Module'

    def project(self, obj):
        project = Project.objects.filter(
            detaillevel__project_id=obj.detail_level.project.id).values_list(
            'name', flat=True)[0]
        return project
    project.short_description = 'Project'


class ModuleAdmin(admin.ModelAdmin):
    fields = ('detail_level', 'title', 'rank', 'steps', 'project')
    list_display = ('title', 'rank', 'project')
    filter_horizontal = ('steps',)
    readonly_fields = ('project',)
    search_fields = ('title',)

    def project(self, obj):
        project = Project.objects.filter(
            detaillevel__project_id=obj.detail_level.project.id).values_list(
            'name', flat=True)[0]
        return project
    project.short_description = 'Project'


class ModuleInline(admin.StackedInline):
    model = Module
    filter_horizontal = ('steps',)
    extra = 1


class ProjectAdmin(AdminImageMixin, admin.ModelAdmin):
    prepopulated_fields = {'slug': ('name',)}


class DetailLevelAdmin(admin.ModelAdmin):
    save_on_top = True
    list_display = ('level', 'project',)
    inlines = [
        StepInline
    ]


class FeedbackAdmin(admin.ModelAdmin):
    list_display = (
        'submission_date', 'project', 'detail_level', 'was_satisifed')
    list_filter = ('was_satisifed', 'submission_date')
    readonly_fields = (
        'project',
        'detail_level',
        'project_progress',
        'project_confidence',
        'project_recommendation',
        'submission_date',
        'was_satisifed')


admin.site.register(DetailLevel, DetailLevelAdmin)
admin.site.register(Project, ProjectAdmin)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(Module, ModuleAdmin)
admin.site.register(Step, StepAdmin)
