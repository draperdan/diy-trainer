import floppyforms.__future__ as forms

from .models import Feedback


class FeedbackForm(forms.ModelForm):
    class Meta:
        model = Feedback
        fields = ('project_progress',
                  'project_confidence',
                  'project_recommendation',
                  'submission_date')
