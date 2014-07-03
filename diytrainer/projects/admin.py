from django.contrib import admin

from sorl.thumbnail.admin import AdminImageMixin

from .models import Project, Feedback, DetailLevel, Step, Module


class StepInline(AdminImageMixin, admin.StackedInline):
    model = Step


class StepAdmin(admin.ModelAdmin):
    list_display = ('sanitized_title', 'detail_level', 'rank', 'module')
    readonly_fields = ('module',)

    def module(self, obj):
        if obj.detail_level.level == 3:
            module = Module.objects.filter(
                steps__id=obj.id).values_list('title', flat=True)[0]
            return module
        else:
            return 'N/A'
    module.short_description = 'Module'

    #def project(self, obj):
    #    project = Project.objects.filter(
    #        detaillevel__level=obj.detail_level.level).values_list(
    #        'name', flat=True)#[0]
    #    return project
    #project.short_description = 'Project'


class ModuleAdmin(admin.ModelAdmin):
    fields = ('detail_level', 'project', 'title', 'rank', 'steps')
    list_display = ('title', 'rank', 'project', 'detail_level')
    filter_horizontal = ('steps',)
    readonly_fields = ('project',)

    def project(self, obj):
        project = Project.objects.filter(
            detaillevel__level=obj.detail_level.level).values_list(
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
