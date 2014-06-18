import datetime

from django.db import models
from django.utils.encoding import python_2_unicode_compatible


@python_2_unicode_compatible
class GuideFeedback(models.Model):
    VERSION_ONE = 1
    VERSION_TWO = 2
    VERSION_THREE = 3
    VERSION_CHOICES = (
        (VERSION_ONE, 'Version one'),
        (VERSION_TWO, 'Version two'),
        (VERSION_THREE, 'Version three')
    )
    """ Feedback for a guide on a given splash page """
    VERSION_TYPE = models.IntegerField(choices=VERSION_CHOICES)
    submission_date = models.DateTimeField(default=datetime.datetime.now)
    email = models.EmailField(blank=True)
    project_recommendation = models.TextField(blank=True)
    skill_ranking = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Feedback'
        ordering = ('submission_date',)

    def __str__(self):
        return self.pk
