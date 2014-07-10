import datetime
from markdown import markdown
from typogrify.filters import typogrify
from model_utils import Choices
from sorl.thumbnail import ImageField

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _
from django.utils.html import strip_tags


def markup(text):
    """
    Mark up plain text into fancy HTML.

    """
    return typogrify(
        markdown(
            text,
            lazy_ol=False,
            output_format='html5',
            extensions=[
                'abbr',
                'codehilite',
                'fenced_code',
                'sane_lists',
                'smart_strong']))


@python_2_unicode_compatible
class Project(models.Model):
    """ A project for the granularity test. """
    name = models.CharField(max_length=250, help_text='Max 250 characters')
    slug = models.SlugField(help_text='Will populate from the name field')
    lead_art = ImageField(upload_to='images/projects/project', blank=True)

    class Meta:
        verbose_name_plural = 'Projects'
        ordering = ('pk',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse(
            'detaillevel_detail',
            kwargs={'slug': self.slug, 'level': 1}
            )


class ProjectRelatedModel(models.Model):
    class Meta:
        abstract = True

    project = models.ForeignKey(Project)


@python_2_unicode_compatible
class DetailLevel(ProjectRelatedModel):
    """ A detail level for a given project. """
    LEVEL_CHOICES = Choices((1, 'low', _('1')),
                            (2, 'medium', _('2')),
                            (3, 'high', _('3')))
    DESCRIPTOR_CHOICES = Choices(
                                      ('nuts and bolts',
                                       _('Nuts and Bolts')),
                                      ('more bells and whistles',
                                       _('More Bells and Whistles')),
                                      ('everything and the kitchen sink',
                                       _('Everything and the Kitchen Sink')))
    level = models.IntegerField(choices=LEVEL_CHOICES)
    descriptor = models.CharField(choices=DESCRIPTOR_CHOICES, max_length=50)
    introduction = models.TextField()
    project_overview = models.TextField(
        help_text='Use Markdown for formatting')
    project_overview_html = models.TextField(editable=False, blank=True)
    time_skill_and_complexity = models.TextField(
        blank=True, help_text='Use Markdown for formatting')
    time_skill_and_complexity_html = models.TextField(
        editable=False, blank=True)
    terminology = models.TextField(blank=True,
                                   help_text='Use Markdown for formatting')
    terminology_html = models.TextField(editable=False, blank=True)
    tools_and_materials = models.TextField(
        blank=True, help_text='Use Markdown for formatting')
    tools_and_materials_html = models.TextField(editable=False, blank=True)

    class Meta:
        verbose_name_plural = 'Detail levels'
        ordering = ('level',)

    def save(self, *args, **kwargs):
        """ Convert Markdown to HTML on save """
        self.time_skill_and_complexity_html = markup(
            self.time_skill_and_complexity)
        self.terminology_html = markup(self.terminology)
        self.tools_and_materials_html = markup(self.tools_and_materials)
        self.project_overview_html = markup(self.project_overview)
        super(DetailLevel, self).save(*args, **kwargs)

    def __str__(self):
        # Return the string for level instead of int
        return '%s' % (self.level)

    # For paging-type functionality to get the next level for a project
    def get_next(self):
        next = DetailLevel.objects.filter(level__gt=self.level)
        if next:
            return next[0]
        return False

    # For paging-type functionality to get the previous level for a project
    def get_prev(self):
        prev = DetailLevel.objects.filter(level__lt=self.level)
        if prev:
            return prev[0]
        return False

    # Return steps for the current detaillevel
    def get_steps_for_detaillevel(self):
        return Step.objects.filter(detail_level__level=self.level)

    # get modules for current detaillevel
    def get_modules_for_detaillevel(self):
        return Module.objects.filter(detail_level__level=self.level)

    def get_absolute_url(self):
        return reverse(
            'detaillevel_detail',
            kwargs={'level': self.level, 'slug': self.project.slug}
            )


class DetailLevelRelatedModel(models.Model):
    class Meta:
        abstract = True

    detail_level = models.ForeignKey(DetailLevel, null=True, blank=True)


@python_2_unicode_compatible
class Step(DetailLevelRelatedModel):
    rank = models.PositiveSmallIntegerField(
        help_text='Used for ordering steps')
    title = models.CharField(max_length=100, help_text='Max 100 characters')
    body = models.TextField(help_text='Markdown only')
    body_html = models.TextField(editable=False, blank=True)
    quick_tip = models.TextField(blank=True, help_text='No HTML allowed')
    image = ImageField(upload_to='images/projects/steps', blank=True)

    class Meta:
        ordering = ('rank',)

    def save(self, *args, **kwargs):
        """ Convert Markdown to HTML on save """
        self.body_html = markup(self.body)
        super(Step, self).save(*args, **kwargs)

    def sanitized_title(self):
        return strip_tags(self.title)

    def __str__(self):
        return strip_tags(self.title)


@python_2_unicode_compatible
class Module(models.Model):
    title = models.CharField(max_length=100, help_text='Max 100 characters')
    rank = models.PositiveSmallIntegerField(
        help_text='Used for ordering modules')
    steps = models.ManyToManyField(Step, limit_choices_to={'detail_level__level': 3}, null=True, blank=True)
    detail_level = models.ForeignKey(DetailLevel, limit_choices_to={'level': 3}, null=True, blank=True)

    def get_steps_for_module(self):
        return Step.objects.filter(module__id=self.id)

    class Meta:
        ordering = ('rank',)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Feedback(DetailLevelRelatedModel, ProjectRelatedModel):
    """ Feedback for a given project. """
    PROJECT_PROGRESS_CHOICES = Choices(
                                      ('planning and preparing',
                                       _('Planning and preparing')),
                                      ('getting started',
                                       _('Getting started')),
                                      ('in the thick of it',
                                       _('In the thick of it')),
                                      ('figuring out a hiccup',
                                       _('Figuring out a hiccup')),
                                      ('finishing touches',
                                       _('Finishing touches')),
                                      ('not currently working on this project',
                                       _('Not currently working on this project')))
    PROJECT_CONFIDENCE_CHOICES = Choices(
                                        ('not confident i can complete it. i rarely if ever do these types of projects myself.',
                                         _('Not confident I can complete it. I rarely if ever do these types of projects myself.')),
                                        ('curious about learning how to do this project. i\'d like to do it myself if i can.',
                                         _('Curious about learning how to do this project. I\'d like to do it myself if I can.')),
                                        ('confident i can complete this project on my own.',
                                         _('Confident I can complete this project on my own.')),
                                        ('a home services professional or craftsman. i make a living by working on/repairing homes.',
                                         _('A home services professional or craftsman. I make a living by working on/repairing homes.')))
    project_progress = models.CharField(
        choices=PROJECT_PROGRESS_CHOICES, max_length=50, blank=True)
    project_confidence = models.CharField(
        choices=PROJECT_CONFIDENCE_CHOICES, max_length=100, blank=True)
    project_recommendation = models.TextField(blank=True)
    submission_date = models.DateTimeField(default=datetime.datetime.now)
    was_satisifed = models.BooleanField(
        default=False,
        help_text='Returns true if the user exits the process early.')

    class Meta:
        verbose_name_plural = 'Feedback'
        ordering = ('submission_date',)

    def __str__(self):
        return 'Feedback for %s submitted %s' % (self.project.name,
                                                 self.submission_date.strftime('%A, %B %w %Y, %I:%M %p'))
