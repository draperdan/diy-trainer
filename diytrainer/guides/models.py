import datetime

from django.db import models
from django.core.urlresolvers import reverse
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class Guide(models.Model):
    """ A guide for a given splash page """
    name = models.CharField(max_length=100,
                            help_text='Limited to 100 characters.')
    description = models.TextField(blank=True)

    class Meta:
        verbose_name_plural = 'Guides'
        ordering = ('pk',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('guide_detail', kwargs={'pk': self.pk})


@python_2_unicode_compatible
class Feedback(models.Model):
    """ Feedback submitted for a given guide """
    guide = models.ForeignKey(Guide)
    submission_date = models.DateTimeField(default=datetime.datetime.now)
    email = models.EmailField(blank=True)
    project_recommendation = models.TextField(blank=True)
    skill_ranking = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Feedback'
        ordering = ('submission_date',)

    def __str__(self):
        return self.pk
