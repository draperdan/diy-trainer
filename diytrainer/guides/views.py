from django.views.generic import CreateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from .models import Guide, Feedback, EmailSignUp
from .forms import FeedbackForm, EmailSignUpForm


class EmailSignUpCreateView(CreateView):
    model = EmailSignUp
    form_class = EmailSignUpForm
    success_url = 'feedback/'

    def dispatch(self, *args, **kwargs):
        self.guide = get_object_or_404(Guide, version=kwargs['guide_version'])
        return super(EmailSignUpCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        #Get associated guide and save
        self.object = form.save(commit=False)
        self.object.guide = self.guide
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        context_data = super(EmailSignUpCreateView, self).get_context_data(*args, **kwargs)
        context_data.update({'guide': self.guide})
        return context_data


class FeedbackCreateView(CreateView):
    model = Feedback
    form_class = FeedbackForm
    success_url = 'thanks/'

    def dispatch(self, *args, **kwargs):
        self.guide = get_object_or_404(Guide, version=kwargs['guide_version'])
        return super(FeedbackCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        #Get associated guide and save
        self.object = form.save(commit=False)
        self.object.guide = self.guide
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        context_data = super(FeedbackCreateView, self).get_context_data(*args, **kwargs)
        context_data.update({'guide': self.guide})
        return context_data