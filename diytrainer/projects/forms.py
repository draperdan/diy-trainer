import floppyforms.__future__ as forms
from django.utils.translation import ugettext_lazy as _

from .models import Feedback


class FeedbackFormMixin(object):

    class Meta:
        model = Feedback
        fields = ('project_progress',
                  'project_confidence',
                  'project_recommendation',
                  'was_satisifed')
        labels = {
            'project_progress': _('How far along are you in the process of '
                                  'completing this project?'),
            'project_confidence': _('When it comes to this project, I am:'),
            'project_recommendation': _('What other projects would you like '
                                        'us to create guides for, and what '
                                        'info or media would you expect '
                                        'to be included?')
        }
        widgets = {
            'project_progress': forms.RadioSelect,
            'project_confidence': forms.RadioSelect,
            'was_satisifed': forms.HiddenInput
        }


class SuccessfulFeedbackForm(FeedbackFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(SuccessfulFeedbackForm, self).__init__(*args, **kwargs)
        self.fields['was_satisifed'].initial = True


class UnsuccessfulFeedbackForm(FeedbackFormMixin, forms.ModelForm):

    def __init__(self, *args, **kwargs):
        super(UnsuccessfulFeedbackForm, self).__init__(*args, **kwargs)
        self.fields['was_satisifed'].initial = False
