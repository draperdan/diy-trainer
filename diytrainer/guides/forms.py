import floppyforms.__future__ as forms

from .models import Feedback, EmailSignUp


class Slider(forms.RangeInput):
    min = 0
    max = 10
    step = 1
    template_name = 'slider.html'

    class Media:
        js = (
            'ajax.googleapis.com/ajax/libs/jquery/1.11.1/jquery.min.js',
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
        widgets = {'skill_ranking': Slider}


class EmailSignUpForm(forms.ModelForm):
    class Meta:
        model = EmailSignUp
        fields = ('email',)
