from django.conf.urls import patterns
from django.conf.urls import url
from django.views.generic import TemplateView

from . import views

urlpatterns = patterns('',
    url(
        regex=r'^(?P<project_slug>[-\w]+)/(?P<level>\d+)/$',
        view=views.DetailLevelView.as_view(),
        name='detaillevel_detail'
    ),
    url(
        regex=r'^(?P<project_slug>[-\w]+)/feedback/$',
        view=views.FeedbackSatisfiedCreateView.as_view(),
        name='project_satisfied_feedback'
    ),
    url(
        regex=r'^(?P<project_slug>[-\w]+)/feedback/$',
        view=views.FeedbackUnsatisfiedCreateView.as_view(),
        name='project_unsatisfied_feedback'
    ),
    url(r'^(?P<project_slug>[-\w]+)/feedback/thanks/$',
        views.SatisfiedFeedbackSubmittedTemplateView.as_view(),
        name='feedback_submitted'),
    url(r'^(?P<project_slug>[-\w]+)/feedback/sorry/$',
        views.UnsatisfiedFeedbackSubmittedTemplateView.as_view(),
        name='feedback_submitted'),
)
