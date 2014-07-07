import floppyforms.__future__ as forms
from django.utils.translation import ugettext_lazy as _

from .models import Feedback, EmailSignUp


class Slider(forms.RangeInput):
    min = 0
    max = 10
    step = 1
    template_name = 'slider.html'

    class Media:
        js = (
            #'ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js',
            'ajax.googleapis.com/ajax/libs/jqueryui/1.10.4/jquery-ui.min.js',
        )
        css = {
            'all': (
                'ajax.googleapis.com/ajax/libs/jqueryui/1.10.4/themes/smoothness/jquery-ui.css',
            )
        }


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('project_recommendation', 'skill_ranking')
        labels = {
            'project_recommendation': _('We\'re diligently building '
                                        'our DIY project database. Please '
                                        'tell us what projects you\'d '
                                        'like to see covered by DIY Trainer!'),
            'skill_ranking': _('On a scale of 1-10, when it comes to the '
                               'idea of starting a home improvement project '
                               'unlike anything I\'ve tried before, I am...')
        }
        widgets = {'skill_ranking': Slider}


class EmailSignUpForm(forms.ModelForm):
    class Meta:
        model = EmailSignUp
        fields = ('email',)
        labels = {
            'email': _('Sign up to be notified when DIY Trainer launches.')
        }
