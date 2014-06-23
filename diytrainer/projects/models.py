import datetime
from markdown import markdown
from typogrify.filters import typogrify
from model_utils import Choices
from sorl.thumbnail import ImageField

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.core.urlresolvers import reverse


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
    name = models.CharField(max_length=250)
    slug = models.SlugField()
    description = models.TextField()
    description_html = models.TextField(editable=False, blank=True)
    # NOTE: Change lead_art to null=False in production
    lead_art = ImageField(upload_to='images/projects/project', null=True)

    class Meta:
        verbose_name_plural = 'Projects'
        ordering = ('pk',)

    def save(self, *args, **kwargs):
        self.description_html = markup(self.description)
        super(Project, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class ProjectRelatedModel(models.Model):
    class Meta:
        abstract = True

    project = models.ForeignKey(Project)


@python_2_unicode_compatible
class DetailLevel(ProjectRelatedModel):
    """ A detail level for a given project. """
    level = models.PositiveSmallIntegerField()
    time_skill_and_complexity = models.TextField()
    time_skill_and_complexity_html = models.TextField(editable=False, blank=True)
    terminology = models.TextField()
    terminology_html = models.TextField(editable=False, blank=True)
    tools_and_materials = models.TextField()
    tools_and_materials_html = models.TextField(editable=False, blank=True)
    instructions = models.TextField()
    instructions_html = models.TextField(editable=False, blank=True)

    class Meta:
        verbose_name_plural = 'Detail level'
        ordering = ('level',)

    def save(self, *args, **kwargs):
        self.time_skill_and_complexity_html = markup(self.time_skill_and_complexity)
        self.terminology_html = markup(self.terminology)
        self.tools_and_materials_html = markup(self.tools_and_materials)
        self.instructions_html = markup(self.instructions)
        super(DetailLevel, self).save(*args, **kwargs)

    def __str__(self):
        return self.level

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

    def get_absolute_url(self):
        return reverse('detaillevel_detail', kwargs={'level': self.level})


@python_2_unicode_compatible
class Feedback(ProjectRelatedModel):
    """ Feedback for a given project. """
    PROJECT_PROGRESS_CHOICES = Choices(
                                      ('planning and preparing', ('Planning and preparing')),
                                      ('getting started', ('Getting started')),
                                      ('getting started', ('Getting started')),
                                      ('in the thick of it', ('In the thick of it')),
                                      ('figuring out a hiccup', ('Figuring out a hiccup')),
                                      ('finishing touches', ('Finishing touches')),
                                      ('not currently working on this project', ('Not currently working on this project')))
    PROJECT_CONFIDENCE_CHOICES = Choices(
                                      ('not confident i can complete it. i rarely if ever do these types of projects myself.', ('Not confident I can complete it. I rarely if ever do these types of projects myself.')),
                                      ('curious about learning how to do this project. i\'d like to do it myself if i can.', ('Curious about learning how to do this project. I\'d like to do it myself if I can.')),
                                      ('confident i can complete this project on my own.', ('Confident I can complete this project on my own.')),
                                      ('a home services professional or craftsman. i make a living by working on/repairing homes.', ('A home services professional or craftsman. I make a living by working on/repairing homes.')))
    project_progress = models.CharField(choices=PROJECT_PROGRESS_CHOICES, max_length=50, blank=True)
    project_confidence = models.CharField(choices=PROJECT_CONFIDENCE_CHOICES, max_length=100, blank=True)
    project_recommendation = models.TextField(blank=True)
    submission_date = models.DateTimeField(default=datetime.datetime.now,
                                           editable=False)

    class Meta:
        verbose_name_plural = 'Feedback'
        ordering = ('submission_date',)

    def __str__(self):
        return 'Feedback for %s submitted %s' % (self.project.name,
                                                 self.submission_date.date().strftime('%A, %B %w %Y'))
