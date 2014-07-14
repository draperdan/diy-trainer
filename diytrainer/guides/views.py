import pytz
import datetime

from django.views.generic import CreateView
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage
from django.utils.timezone import utc

from .models import Guide, Feedback, EmailSignUp
from .forms import FeedbackForm, EmailSignUpForm

now = datetime.datetime.utcnow().replace(tzinfo=utc)
est = pytz.timezone('US/Eastern')


class FormActionMixin(object):
    def dispatch(self, *args, **kwargs):
        self.guide = get_object_or_404(Guide, version=kwargs['guide_version'])
        return super(FormActionMixin, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.guide = self.guide

        if self.form_class == FeedbackForm:
            # Gather up data for email send
            guide = self.object.guide
            version = guide.version
            project_recommendation = form.cleaned_data.get('project_recommendation')
            skill_ranking = form.cleaned_data.get('skill_ranking')
            submission_date = now.astimezone(est).strftime('%A, %B %d %Y, %I:%M %p')

            email = EmailMessage()
            email.body = 'Splash-page version: ' + str(version) + '\n' + 'Project recommendation: ' + project_recommendation + '\n' + 'Skill ranking: ' + str(skill_ranking) + '\n' + 'Submission date: ' + str(submission_date)
            email.subject = 'Feedback has been submitted for %s (splash page %s)' % (guide, version)
            email.from_email = 'admin@diy-trainer.com'
            email.to = ['pbeeson@thevariable.com']
            #email.to = ['notifications@diy-trainer.com']
            #email.bcc = ['pbeeson@thevariable.com']
            email.send()
        elif self.form_class == EmailSignUpForm:
            # Gather up data for email send
            submitted_email = form.cleaned_data.get('email')
            guide = self.object.guide
            version = guide.version
            submission_date = now.astimezone(est).strftime('%A, %B %d %Y, %I:%M %p')

            email = EmailMessage()
            email.body = 'Splash-page version: ' + str(version) + '\n' + 'Email address: ' + submitted_email + '\n' + 'Submission date: ' + str(submission_date)
            email.subject = 'Email address has been submitted for %s (splash page %s)' % (guide, version)
            email.from_email = 'admin@diy-trainer.com'
            email.to = ['pbeeson@thevariable.com']
            #email.to = ['notifications@diy-trainer.com']
            #email.bcc = ['pbeeson@thevariable.com']
            email.send()
        return super(FormActionMixin, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context_data = super(FormActionMixin, self).get_context_data(*args,
                                                                     **kwargs)
        context_data.update({'guide': self.guide})
        return context_data


class EmailSignUpCreateView(FormActionMixin, CreateView):
    model = EmailSignUp
    form_class = EmailSignUpForm
    # Send the to the feedback form to capture more info
    success_url = 'feedback/'


class FeedbackCreateView(FormActionMixin, CreateView):
    model = Feedback
    form_class = FeedbackForm
    # Send them to the thanks page
    success_url = 'thanks/'
