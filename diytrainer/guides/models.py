import datetime
from markdown import markdown
from model_utils import Choices
from typogrify.filters import typogrify
from sorl.thumbnail import ImageField

from django.utils.encoding import python_2_unicode_compatible
from django.db import models
from django.core.urlresolvers import reverse
from django.utils.translation import ugettext_lazy as _


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
class Guide(models.Model):
    """ A guide for a given splash page """
    VERSION_CHOICES = Choices((1, 'low', _('1')),
                             (2, 'medium', _('2')),
                             (3, 'high', _('3')))
    name = models.CharField(max_length=100,
                            help_text='Max 100 characters.')
    version = models.PositiveSmallIntegerField(
        choices=VERSION_CHOICES, help_text='Version of splash page')
    headline = models.CharField(max_length=250,
                                help_text='Max 250 characters.')
    description_image = ImageField(blank=True,
                                   upload_to='images/guides/description'
                                   )
    rendering = ImageField(upload_to='images/guides/renderings')

    class Meta:
        verbose_name_plural = 'Guides'
        ordering = ('version',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('email_signup', kwargs={'guide_version': self.version})


class GuideRelatedModel(models.Model):
    class Meta:
        abstract = True

    guide = models.ForeignKey(Guide)


@python_2_unicode_compatible
class Descriptor(GuideRelatedModel):
    """ A descriptor for a guide. """
    RANK_CHOICES = Choices((1, 'low', _('1')),
                           (2, 'medium', _('2')),
                           (3, 'high', _('3')))
    rank = models.PositiveSmallIntegerField(
        choices=RANK_CHOICES, help_text='An integer from 1 to 3')
    title = models.CharField(max_length=100, help_text='Max 100 characters')
    body = models.TextField(help_text='No HTML allowed')
    image = ImageField(blank=True, upload_to='images/guides/descriptors')

    class Meta:
        verbose_name_plural = 'Descriptors'
        ordering = ('rank',)

    def __str__(self):
        return self.title


@python_2_unicode_compatible
class Feedback(GuideRelatedModel):
    """ Feedback submitted for a given guide """
    submission_date = models.DateTimeField(default=datetime.datetime.now,
                                           editable=False)
    project_recommendation = models.TextField(blank=True)
    skill_ranking = models.PositiveSmallIntegerField(null=True, blank=True)

    class Meta:
        verbose_name_plural = 'Feedback'
        ordering = ('submission_date',)

    def __str__(self):
        return 'Feedback for %s submitted %s' % (self.guide.name,
                                                 self.submission_date.strftime('%A, %B %w %Y, %I:%M %p'))


@python_2_unicode_compatible
class EmailSignUp(GuideRelatedModel):
    """ Emails submitted for a given guide """
    email = models.EmailField(blank=True)
    submission_date = models.DateTimeField(default=datetime.datetime.now)

    class Meta:
        verbose_name_plural = 'Email sign ups'
        ordering = ('pk',)

    def __str__(self):
        return self.email
