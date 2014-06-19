from django.views.generic import CreateView, DetailView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from .models import Project, Feedback
from .forms import FeedbackForm


class FeedbackActionMixin(object):
    model = Feedback
    form_class = FeedbackForm


class SatisfiedFeedbackCreateView(FeedbackActionMixin, CreateView):
    success_url = 'thanks/'

    def dispatch(self, *args, **kwargs):
        self.project = get_object_or_404(Project, slug=kwargs['project_slug'])
        return super(SatisfiedFeedbackCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        #Get associated project and save
        self.object = form.save(commit=False)
        self.object.project = self.project
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        context_data = super(SatisfiedFeedbackCreateView, self).get_context_data(*args, **kwargs)
        context_data.update({'project': self.project})
        context_data.append(self.extra_context)
        return context_data


class NeedMoreInfoFeedbackCreateView(FeedbackActionMixin, CreateView):
    success_url = 'sorry/'

    def dispatch(self, *args, **kwargs):
        self.project = get_object_or_404(Project, slug=kwargs['project_slug'])
        return super(NeedMoreInfoFeedbackCreateView, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        #Get associated project and save
        self.object = form.save(commit=False)
        self.object.project = self.project
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        context_data = super(NeedMoreInfoFeedbackCreateView, self).get_context_data(*args, **kwargs)
        context_data.update({'project': self.project})
        context_data.append(self.extra_context)
        return context_data


class DetailLevelView(DetailView):
    model = DetailView

    def get_context_data(self, *args, **kwargs):
        context = super(DetailLevelView, self).get_context_data(*args, **kwargs)
        context.update({'project': self.project})
        return context
