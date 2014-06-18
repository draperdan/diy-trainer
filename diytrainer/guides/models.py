import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Guide(models.Model):
    """ A guide for a given splash page """
    name = models.CharField(max_length=100, help_text='Limited to 100 characters.')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Guides'
        ordering = ('id',)

    def __str__(self):
        return self.name


@python_2_unicode_compatible
class Feedback(models.Model):
    """ Feedback submitted for a given guide """
    guide = models.ForeignKey(Guide)
    submission_date = models.DateTimeField(default=datetime.datetime.now)
    email = models.EmailField()
    project_recommendation = models.TextField()
    skill_ranking = models.PositiveSmallIntegerField()

    class Meta:
        verbose_name_plural = 'Feedback'
        ordering = ('submission_date',)

    def __str__(self):
        return self.id
