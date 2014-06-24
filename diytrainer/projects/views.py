from django.views.generic import CreateView, DetailView, TemplateView
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from .models import Project, Feedback, DetailLevel
from .forms import FeedbackForm


class FeedbackSubmittedActionMixin(object):
    template_name = "projects/feedback_submitted.html"


class FeedbackActionMixin(object):
    model = Feedback
    form_class = FeedbackForm

    def dispatch(self, *args, **kwargs):
        self.project = get_object_or_404(Project, slug=kwargs['project_slug'])
        return super(FeedbackActionMixin, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.project = self.project
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())

    def get_context_data(self, *args, **kwargs):
        context_data = super(FeedbackActionMixin,
                             self).get_context_data(*args, **kwargs)
        context_data.update({'project': self.project})
        return context_data


class FeedbackSatisfiedCreateView(FeedbackActionMixin, CreateView):
    success_url = 'thanks/'


class FeedbackUnsatisfiedCreateView(FeedbackActionMixin, CreateView):
    success_url = 'sorry/'


class SatisfiedFeedbackSubmittedTemplateView(FeedbackSubmittedActionMixin,
                                             TemplateView):

    def get_context_data(self, **kwargs):
        context = super(SatisfiedFeedbackSubmittedTemplateView,
                        self).get_context_data(**kwargs)
        context['show_extra_content'] = False
        return context


class UnsatisfiedFeedbackSubmittedTemplateView(FeedbackSubmittedActionMixin,
                                               TemplateView):

    def get_context_data(self, **kwargs):
        context = super(UnsatisfiedFeedbackSubmittedTemplateView,
                        self).get_context_data(**kwargs)
        context['show_extra_content'] = True
        return context


class DetailLevelView(DetailView):
    slug_field = 'level'
    slug_url_kwarg = 'level'
    queryset = DetailLevel.objects.select_related('project').all()
