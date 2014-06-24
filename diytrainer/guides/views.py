from django.views.generic import CreateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from .models import Guide, Feedback, EmailSignUp
from .forms import FeedbackForm, EmailSignUpForm


class FormActionMixin(object):
    def dispatch(self, *args, **kwargs):
        self.guide = get_object_or_404(Guide, version=kwargs['guide_version'])
        return super(FormActionMixin, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.guide = self.guide
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

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
