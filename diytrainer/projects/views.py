import pytz

from django.views.generic import CreateView, DetailView, TemplateView
from django.shortcuts import get_object_or_404
from django.core.mail import EmailMessage

from braces.views import SelectRelatedMixin

from .models import Project, Feedback, DetailLevel
from .forms import SuccessfulFeedbackForm, UnsuccessfulFeedbackForm


class FeedbackSubmittedActionMixin(object):
    template_name = "projects/feedback_submitted.html"


class FeedbackActionMixin(object):
    model = Feedback

    def dispatch(self, *args, **kwargs):
        self.project = get_object_or_404(Project, slug=kwargs['project_slug'])
        self.detail_level = get_object_or_404(DetailLevel, project=self.project, level=kwargs['level'])
        return super(FeedbackActionMixin, self).dispatch(*args, **kwargs)

    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.project = self.project
        instance.detail_level = self.detail_level

        project = self.project
        detail_level = self.detail_level
        project_progress = form.cleaned_data.get('project_progress')
        project_confidence = form.cleaned_data.get('project_confidence')
        project_recommendation = form.cleaned_data.get('project_recommendation')

        est = pytz.timezone('US/Eastern')
        submission_date = instance.submission_date.astimezone(est).strftime('%A, %B %d %Y, %I:%M %p')

        email = EmailMessage()
        email.body = 'Project progress: ' + project_progress + '\n' + 'Project confidence: ' + project_confidence + '\n' + "Project recommendation: " + project_recommendation + '\n' + 'Submission date: ' + str(submission_date)
        email.subject = 'Feedback has been submitted for %s (detail level %s)' % (project, str(detail_level))
        email.from_email = 'admin@diy-trainer.com'
        email.to = ['pbeeson@thevariable.com']
        #email.to = ['notifications@diy-trainer.com']
        #email.bcc = ['pbeeson@thevariable.com']
        email.send()

        return super(FeedbackActionMixin, self).form_valid(form)

    def get_context_data(self, *args, **kwargs):
        context_data = super(FeedbackActionMixin,
                             self).get_context_data(*args, **kwargs)
        context_data.update({'project': self.project})
        context_data.update({'level': self.detail_level})
        return context_data


class FeedbackSatisfiedCreateView(FeedbackActionMixin, CreateView):
    success_url = 'thanks/'
    form_class = SuccessfulFeedbackForm


class FeedbackUnsatisfiedCreateView(FeedbackActionMixin, CreateView):
    success_url = 'sorry/'
    form_class = UnsuccessfulFeedbackForm


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


class DetailLevelView(SelectRelatedMixin, DetailView):
    slug_field = 'level'
    slug_url_kwarg = 'level'
    model = DetailLevel
    select_related = [u"project", u"step", u"module"]

    def get_queryset(self):
        self.project = get_object_or_404(Project, slug__iexact=self.kwargs['slug'])
        return DetailLevel.objects.filter(project=self.project)
